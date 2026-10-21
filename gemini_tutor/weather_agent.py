def get_weather(city: str) -> dict:
    """Get sample weather information for a city.

    Args:
        city: The name of the city.
    """
    weather_data = {
        "hyderabad": {
            "temperature": 25,
            "condition": "Mostly cloudy",
        },
        "bengaluru": {
            "temperature": 23,
            "condition": "Light rain",
        },
    }

    result = weather_data.get(city.lower())

    if result is None:
        return {"error": f"No weather data available for {city}"}

    return result