
from gmail_cleanup.gmail_service import (
    find_old_emails,
    move_emails_to_trash,
)

emails = find_old_emails(days=30)

print(f"\nFound {len(emails)} emails older than 30 days:\n")

for index, email in enumerate(emails, start=1):
    print(f"{index}. From: {email['sender']}")
    print(f"   Subject: {email['subject']}")
    print(f"   Date: {email['date']}")
    print()

if not emails:
    print("No matching emails found.")
    raise SystemExit

confirmation = input(
    f"Move these {len(emails)} emails to Trash? Type YES to confirm: "
)

if confirmation == "YES":
    email_ids = [email["id"] for email in emails]
    results = move_emails_to_trash(email_ids)
    print(f"\nMoved {len(results)} emails to Trash.")
else:
    print("Cancelled. No emails were moved.")
