from gmail_cleanup.gmail_service import find_old_emails

emails = find_old_emails(days=30)

print(f"\nFound {len(emails)} emails older than 30 days:\n")

for email in emails:
    print(f"ID:      {email['id']}")
    print(f"From:    {email['sender']}")
    print(f"Subject: {email['subject']}")
    print(f"Date:    {email['date']}")
    print("-" * 50) 