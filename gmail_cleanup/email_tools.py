from datetime import date, timedelta


SAMPLE_EMAILS = [
    {
        "id": "email_001",
        "sender": "offers@shop.example",
        "subject": "Festive sale offers",
        "date": "2026-01-10",
    },
    {
        "id": "email_002",
        "sender": "newsletter@news.example",
        "subject": "Your weekly newsletter",
        "date": "2026-03-15",
    },
    {
        "id": "email_003",
        "sender": "manager@company.example",
        "subject": "Project review notes",
        "date": "2026-09-20",
    },
    {
        "id": "email_004",
        "sender": "receipts@shop.example",
        "subject": "Your purchase receipt",
        "date": "2025-12-05",
    },
]


def find_old_emails(months: int = 3) -> dict:
    """Find sample emails older than a specified number of months.

    Args:
        months: Number of months old an email must be to appear in the results.
    """
    if months < 1 or months > 120:
        return {"error": "months must be between 1 and 120"}

    cutoff_date = date.today() - timedelta(days=months * 30)
    matches = []

    for email in SAMPLE_EMAILS:
        email_date = date.fromisoformat(email["date"])

        if email_date < cutoff_date:
            matches.append(email)

    return {
        "cutoff_date": cutoff_date.isoformat(),
        "count": len(matches),
        "emails": matches,
        "message": "Sample data only. No real Gmail messages were accessed or changed.",
    }
