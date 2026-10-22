
from gmail_cleanup.gmail_service import list_recent_emails

emails = list_recent_emails(max_results=10)

print(f"\nFound {len(emails)} Gmail messages:\n")

for email in emails:
    print(f"ID:      {email['id']}")
    print(f"From:    {email['sender']}")
    print(f"Subject: {email['subject']}")
    print(f"Date:    {email['date']}")
    print("-" * 50)
