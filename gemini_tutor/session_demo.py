
import asyncio
from google.adk.sessions import InMemorySessionService

async def main():
    session_service = InMemorySessionService()

    # 1. Create a session with initial state
    session = await session_service.create_session(
        app_name="my_app",
        user_id="uma",
        state={"name": "Uma"},
    )

    print("Created session:", session.id)

    # 2. Retrieve the same session
    retrieved_session = await session_service.get_session(
        app_name="my_app",
        user_id="uma",
        session_id=session.id,
    )

    # 3. Read the stored state
    print("Retrieved state:", retrieved_session.state)
    print("Retrieved name:", retrieved_session.state["name"])


if __name__ == "__main__":
    asyncio.run(main())
