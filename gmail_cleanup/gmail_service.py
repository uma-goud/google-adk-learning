
from pathlib import Path
import random
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Allows reading and modifying Gmail messages, including moving them to Trash.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"


def get_gmail_service():
    """Authenticate the user and return a Gmail API service."""
    credentials = None

    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(
            str(TOKEN_FILE), SCOPES
        )

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials or not credentials.valid:
        if not CREDENTIALS_FILE.exists():
            raise FileNotFoundError(
                f"OAuth credentials file not found: {CREDENTIALS_FILE}"
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE), SCOPES
        )
        credentials = flow.run_local_server(port=0)

    TOKEN_FILE.write_text(credentials.to_json(), encoding="utf-8")

    return build("gmail", "v1", credentials=credentials)


def list_recent_emails(max_results: int = 10) -> list[dict]:
    """List recent Gmail messages without modifying them."""
    if not 1 <= max_results <= 50:
        raise ValueError("max_results must be between 1 and 50")

    service = get_gmail_service()

    response = (
        service.users()
        .messages()
        .list(userId="me", maxResults=max_results)
        .execute()
    )

    results = []

    for message in response.get("messages", []):
        details = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"],
            )
            .execute()
        )

        headers = {
            header["name"].lower(): header["value"]
            for header in details.get("payload", {}).get("headers", [])
        }

        results.append({
            "id": details["id"],
            "sender": headers.get("from", "(unknown sender)"),
            "subject": headers.get("subject", "(no subject)"),
            "date": headers.get("date", "(unknown date)"),
        })

    return results


def find_old_emails(days: int = 30, max_emails: int = 100) -> list[str]:
    """Return IDs of old Gmail messages, excluding messages in Trash."""
    if not 1 <= days <= 3650:
        raise ValueError("days must be between 1 and 3650")

    if not 1 <= max_emails <= 1000:
        raise ValueError("max_emails must be between 1 and 1000")

    service = get_gmail_service()
    email_ids = []
    page_token = None

    while len(email_ids) < max_emails:
        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=f"older_than:{days}d -in:trash",
                maxResults=min(100, max_emails - len(email_ids)),
                pageToken=page_token,
            )
            .execute()
        )

        email_ids.extend(
            message["id"] for message in response.get("messages", [])
        )

        page_token = response.get("nextPageToken")

        if not page_token:
            break

    return email_ids


def move_emails_to_trash(email_ids: list[str]) -> list[dict]:
    """Move emails to Trash with retry and exponential backoff."""
    if not email_ids:
        return []

    service = get_gmail_service()
    results = []
    max_retries = 5

    for email_id in email_ids:
        for attempt in range(max_retries + 1):
            try:
                service.users().messages().trash(
                    userId="me",
                    id=email_id,
                ).execute()

                results.append({
                    "id": email_id,
                    "status": "moved_to_trash",
                })
                break

            except HttpError as exc:
                status = exc.resp.status

                # Retry rate-limit and temporary server errors.
                if status != 429 and status not in (500, 502, 503, 504):
                    results.append({
                        "id": email_id,
                        "status": "failed",
                        "error": str(exc),
                    })
                    break

                # Stop after the maximum number of retries.
                if attempt == max_retries:
                    results.append({
                        "id": email_id,
                        "status": "failed",
                        "error": str(exc),
                    })
                    break

                # Wait 2, 4, 8, 16, then 32 seconds, plus random jitter.
                wait_seconds = min(2 ** (attempt + 1), 32)
                wait_seconds += random.uniform(0, 1)

                print(
                    f"Gmail error {status} for email {email_id}. "
                    f"Retrying in {wait_seconds:.1f} seconds..."
                )
                time.sleep(wait_seconds)

            except Exception as exc:
                results.append({
                    "id": email_id,
                    "status": "failed",
                    "error": str(exc),
                })
                break

    return results


def trash_all_old_emails(days: int = 30) -> dict:
    """Find all matching old emails and move them to Trash."""
    if not 1 <= days <= 3650:
        raise ValueError("days must be between 1 and 3650")

    service = get_gmail_service()
    email_ids = []
    page_token = None

    # Collect all matching IDs before moving any emails.
    while True:
        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=f"older_than:{days}d -in:trash",
                maxResults=100,
                pageToken=page_token,
            )
            .execute()
        )

        email_ids.extend(
            message["id"] for message in response.get("messages", [])
        )

        page_token = response.get("nextPageToken")

        if not page_token:
            break

    # Move emails using the retry-enabled function.
    results = move_emails_to_trash(email_ids)

    moved = sum(
        1 for result in results
        if result.get("status") == "moved_to_trash"
    )

    failed_results = [
        result for result in results
        if result.get("status") != "moved_to_trash"
    ]

    return {
        "days": days,
        "matched": len(email_ids),
        "moved_to_trash": moved,
        "failed": len(failed_results),
        "failure_details": failed_results[:10],
    }
