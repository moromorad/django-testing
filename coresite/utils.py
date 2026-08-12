
from google import genai
from schemas import TaskCreateList, TaskCreate
from datetime import datetime, timezone
import zoneinfo

def get_weather_category(weather_code: int) -> str:
    """
    Maps an Open-Meteo (WMO) weather code to its official string description.
    
    Args:
        weather_code (int): The numeric weather code.
        
    Returns:
        str: A string describing the weather condition.
    """
    wmo_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle: Light intensity",
        53: "Drizzle: Moderate intensity",
        55: "Drizzle: Dense intensity",
        56: "Freezing Drizzle: Light intensity",
        57: "Freezing Drizzle: Dense intensity",
        61: "Rain: Slight intensity",
        63: "Rain: Moderate intensity",
        65: "Rain: Heavy intensity",
        66: "Freezing Rain: Light intensity",
        67: "Freezing Rain: Heavy intensity",
        71: "Snow fall: Slight intensity",
        73: "Snow fall: Moderate intensity",
        75: "Snow fall: Heavy intensity",
        77: "Snow grains",
        80: "Rain showers: Slight",
        81: "Rain showers: Moderate",
        82: "Rain showers: Violent",
        85: "Snow showers: Slight",
        86: "Snow showers: Heavy",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    
    # Return the description, or a default message if the code isn't recognized
    return wmo_codes.get(weather_code, "Unknown weather code")



def text_to_tasks(text: str, user_timezone: str = "UTC") -> list[TaskCreate]:
    tz = zoneinfo.ZoneInfo(user_timezone)
    current_time_str = datetime.now(tz).strftime("%A, %Y-%m-%d %H:%M:%S %z")
    instructions = (
        f"You are a productivity helper designed to generate task(s) from user input.\n"
        f"The user is in the timezone: {user_timezone}.\n"
        f"CURRENT DATE & TIME: {current_time_str}\n"
        f"Use the current date and time above (which includes the timezone offset) to resolve relative dates like 'tomorrow', 'next Monday', or 'in 3 hours'. "
        f"Make sure to include the timezone offset (like +03:00) in your output. Only enter due date up to minutes, leave seconds at 00. If no due date is implied, leave due_date as null."
    )
    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=f"{instructions}\n\nUser Input: {text}",
        response_format= {
            "type": "text",
            "mime_type": "application/json",
            "schema": TaskCreateList.model_json_schema(),
        },
    )

    result = TaskCreateList.model_validate_json(interaction.output_text)
    return result.tasks