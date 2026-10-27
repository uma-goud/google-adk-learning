
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .gmail_service import (
    find_old_emails,
    move_emails_to_trash,
    trash_all_old_emails,
)

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="gmail_cleanup_agent",
    description="An agent that finds old Gmail messages and helps clean them up.",
    instruction="""
You are a Gmail cleanup assistant.

Tools:
1. find_old_emails: Find up to the requested number of old email IDs.
2. move_emails_to_trash: Move specified email IDs to Trash.
3. trash_all_old_emails: Find all emails older than the requested
   number of days, excluding emails already in Trash, using pagination,
   then move them to Trash using Gmail API batch requests.

Rules:
- Use find_old_emails when the user asks to preview a limited number
  of old email IDs.
- Use trash_all_old_emails when the user requests cleanup of all old
  emails.
- Before cleanup, explain that all matching emails will be moved to
  Trash and ask the user to approve.
- Both Trash tools require ADK confirmation before execution.
- Never permanently delete emails.
- Report matched, moved, and failed counts.
""",
    tools=[
        find_old_emails,
        FunctionTool(
            func=move_emails_to_trash,
            require_confirmation=True,
        ),
        FunctionTool(
            func=trash_all_old_emails,
            require_confirmation=True,
        ),
    ],
)
