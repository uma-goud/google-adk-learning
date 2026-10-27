
from gmail_cleanup.gmail_service import find_old_emails

email_ids = find_old_emails(days=30, max_emails=100)

print(f"Found {len(email_ids)} old email IDs.")
for email_id in email_ids:
    print(email_id)
