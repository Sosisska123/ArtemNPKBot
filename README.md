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