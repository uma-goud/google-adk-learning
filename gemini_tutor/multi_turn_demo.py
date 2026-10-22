
import asyncio
from dotenv import load_dotenv

load_dotenv("gemini_tutor/.env")

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part


async def main():
    app_name = "multi_turn_demo"
    user_id = "uma"

    # 1. Create session storage
    session_service = InMemorySessionService()

    # 2. Create the agent
    agent = Agent(
        model="gemini-3.5-flash-lite",
        name="memory_agent",
        instruction="Answer the user's questions using the conversation history.",
    )

    # 3. Create the Runner
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
    )

    # 4. Create one session
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
    )

    # 5. First message
    print("Turn 1:")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=Content(
            role="user",
            parts=[Part(text="My name is Uma.")],
        ),
    ):
        if event.is_final_response() and event.content:
            print(event.content.parts[0].text)

    # 6. Second message in the SAME session
    print("\nTurn 2:")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=Content(
            role="user",
            parts=[Part(text="What is my name?")],
        ),
    ):
        if event.is_final_response() and event.content:
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
