
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .gmail_service import find_old_emails, move_emails_to_trash


root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="gmail_cleanup_agent",
    description="An agent that finds old Gmail messages and helps clean them up.",
    instruction="""
    You are a Gmail cleanup assistant.

    You can use these tools:
    1. find_old_emails: Find Gmail messages older than a specified
       number of days.
    2. move_emails_to_trash: Move selected Gmail message IDs to Trash.

    Rules:
    - When the user asks to find old emails, call find_old_emails
      with the requested number of days.
    - Show the user the matching emails, including sender, subject,
      date, and message ID.
    - Do not move any emails to Trash unless the user explicitly
      asks you to proceed.
    - The Trash tool requires ADK confirmation before execution.
    - Never permanently delete emails.
    - Clearly report the outcome of each operation.
    """,
    tools=[
        find_old_emails,
        FunctionTool(
            func=move_emails_to_trash,
            require_confirmation=True,
        ),
    ],
)
