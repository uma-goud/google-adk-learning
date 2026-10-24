
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


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

        results.append(
            {
                "id": details["id"],
                "sender": headers.get("from", "(unknown sender)"),
                "subject": headers.get("subject", "(no subject)"),
                "date": headers.get("date", "(unknown date)"),
            }
        )

    return results


def find_old_emails(days: int = 30) -> list[dict]:
    """Find Gmail messages older than the specified number of days."""
    if not 1 <= days <= 3650:
        raise ValueError("days must be between 1 and 3650")

    service = get_gmail_service()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            q=f"older_than:{days}d",
            maxResults=50,
        )
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

        results.append(
            {
                "id": details["id"],
                "sender": headers.get("from", "(unknown sender)"),
                "subject": headers.get("subject", "(no subject)"),
                "date": headers.get("date", "(unknown date)"),
            }
        )

    return results


def move_emails_to_trash(email_ids: list[str]) -> list[dict]:
    """Move selected Gmail messages to Trash."""
    if not email_ids:
        return []

    service = get_gmail_service()
    results = []

    for email_id in email_ids:
        response = (
            service.users()
            .messages()
            .trash(userId="me", id=email_id)
            .execute()
        )

        results.append({
            "id": response["id"],
            "status": "moved_to_trash",
        })

    return results

