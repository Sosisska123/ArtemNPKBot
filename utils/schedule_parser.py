def parse_schedule(url: str) -> dict:
    """
    Parse schedule from URL.
    This is a placeholder implementation.
    In a real application, you would implement actual parsing logic here.
    """
    # Placeholder implementation
    # You would implement actual parsing based on your schedule format
    return {
        "url": url,
        "lessons": [
            {"time": "08:00", "subject": "Математика", "room": "201"},
            {"time": "09:00", "subject": "Физика", "room": "305"},
            # Add more lessons as needed
        ]
    }

def format_schedule(schedule_data: dict) -> str:
    """
    Format parsed schedule data into a readable string.
    """
    if not schedule_data or "lessons" not in schedule_data:
        return "Расписание недоступно"
    
    formatted = "Расписание:\n"
    for lesson in schedule_data["lessons"]:
        formatted += f"{lesson['time']} - {lesson['subject']} (каб. {lesson['room']})\n"
    
    return formatted