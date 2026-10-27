
from gmail_cleanup.gmail_service import get_gmail_service

service = get_gmail_service()

page_token = None
total = 0
page = 0

while True:
    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            q="older_than:30d -in:trash",
            maxResults=100,
            pageToken=page_token,
        )
        .execute()
    )

    messages = response.get("messages", [])
    total += len(messages)
    page += 1

    print(f"Page {page}: {len(messages)} IDs; total={total}")

    page_token = response.get("nextPageToken")

    if not page_token:
        break

print(f"Total matching emails: {total}")
