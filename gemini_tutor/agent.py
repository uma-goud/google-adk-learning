from google.adk.agents.llm_agent import Agent
from .weather_agent import get_weather

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="root_agent",
    description="An assistant that answers weather questions.",
    instruction="When asked about weather, call get_weather and use its result.",
    tools=[get_weather],
)