
import asyncio
import traceback
from dotenv import load_dotenv

load_dotenv("gemini_tutor/.env")

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.genai.types import Content, Part


def save_city(city: str, tool_context: ToolContext) -> dict:
    """Save the user's city in the current session."""
    tool_context.state["city"] = city
    return {"message": f"Saved city: {city}"}


async def main():
    app_name = "state_demo"
    user_id = "uma"

    session_service = InMemorySessionService()

    agent = Agent(
        model="gemini-3.5-flash-lite",
        name="city_agent",
        instruction="When the user tells you their city, use save_city.",
        tools=[save_city],
    )

    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
    )

    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=Content(
                role="user",
                parts=[Part(text="My city is Boston. Save it.")],
            ),
        ):
            if event.is_final_response() and event.content:
                print("Agent:", event.content)

    except Exception:
        traceback.print_exc()
        return

    updated_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session.id,
    )

    print("Updated state:", updated_session.state)


if __name__ == "__main__":
    asyncio.run(main())
