
from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool

from .email_tools import find_old_emails
from .cleanup_tool import move_sample_emails_to_trash

root_agent = Agent(
    model="gemini-3.5-flash",
    name="gmail_cleanup_agent",
    description="Finds old sample emails and requests approval before simulated cleanup.",
    instruction="""
    You are a careful Gmail Cleanup Assistant.

    Use find_old_emails to search the sample email dataset.
    Show the user the email IDs, subjects, senders, and dates.
    Ask the user which email IDs they want to clean up.

    Before calling move_sample_emails_to_trash, explain which IDs will
    be processed and request explicit approval.
    Never claim that sample data is real Gmail data.
    Never claim that real emails were deleted or moved.
    """,
    tools=[
        find_old_emails,
        FunctionTool(
            func=move_sample_emails_to_trash,
            require_confirmation=True,
        ),
    ],
)
