
def move_sample_emails_to_trash(email_ids: list[str]) -> dict:
    """Move approved sample emails to a simulated Trash.

    Args:
        email_ids: IDs of sample emails approved for cleanup.
    """
    allowed_ids = {"email_001", "email_002", "email_003", "email_004"}

    invalid_ids = [email_id for email_id in email_ids if email_id not in allowed_ids]
    if invalid_ids:
        return {
            "status": "rejected",
            "message": "Unknown email IDs were supplied.",
            "invalid_ids": invalid_ids,
        }

    return {
        "status": "simulated_success",
        "moved_ids": email_ids,
        "message": (
            "Simulation only: these sample emails would be moved to Trash. "
            "No real Gmail messages were changed."
        ),
    }
