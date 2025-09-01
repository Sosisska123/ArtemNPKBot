# ArtemNPKBot

This is a Telegram bot built with aiogram and SQLAlchemy.

## Database Decorator

The `with_db` decorator in `utils/decorators.py` provides database access to handler functions. It automatically creates a database session and passes a `Database` instance to the decorated function.

### Usage

```python
from utils.decorators import with_db

@router.message(Command("example"))
@with_db(your_session_maker)
async def example_handler(message: Message, db=None):
    # Now you can use the db parameter to access the database
    # For example:
    # user = await db.get_user(message.from_user.id)
    pass
```

The decorator handles the async session lifecycle automatically, so you don't need to worry about opening or closing sessions.

## Schedule Functionality

The bot now supports schedule management with the following features:

### Database Structure

Schedules are stored in the `schedules` table with the following fields:
- `id`: Primary key
- `group`: Group identifier (string)
- `url`: URL to the schedule (string)
- `date`: Date of the schedule (date)
- `schedule_type`: Type of schedule ("regular" or "modified")

### Logic

1. **Regular vs Modified Schedules**: 
   - Regular schedules are the default schedules for a group
   - Modified schedules are temporary overrides for specific dates (like tomorrow)

2. **Schedule Retrieval**:
   - When requesting a schedule for a specific date, the system first looks for a modified schedule
   - If no modified schedule is found, it falls back to the regular schedule
   - This ensures that modified schedules (like for tomorrow) take precedence

### Commands

- `/schedule` - Get today's schedule for the user's group
- `/tomorrow` - Get tomorrow's schedule for the user's group (with modified schedule priority)
- `/set_tomorrow` - Set a modified schedule for tomorrow (admin function)

### Implementation

The schedule functionality is implemented across several files:
- `models/schedule.py` - Database model for schedules
- `db/database.py` - Database methods for schedule management
- `handlers/schedules.py` - Bot command handlers for schedule operations
- `utils/schedule_parser.py` - Utilities for parsing schedule data