
import asyncio
from dotenv import load_dotenv

load_dotenv("gemini_tutor/.env")

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from weather_agent import get_weather


async def main():
    app_name = "response_demo"
    user_id = "uma"

    session_service = InMemorySessionService()

    agent = Agent(
        model="gemini-3.5-flash-lite",
        name="weather_event_agent",
        instruction="When asked about weather, call get_weather and use its result.",
        tools=[get_weather],
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

    message = Content(
        role="user",
        parts=[Part(text="What's the weather in Hyderabad?")],
    )

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=message,
    ):
        print("\n--- EVENT ---")
        print("Author:", event.author)
        print("Event ID:", event.id)
        print("Final response:", event.is_final_response())

        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.function_call:
                    print("Tool call:", part.function_call)
                elif part.function_response:
                    print("Tool result:", part.function_response)
                elif part.text:
                    print("Text:", part.text)


if __name__ == "__main__":
    asyncio.run(main())
    