# ArtemNPKBot

This is a Telegram bot built with aiogram and SQLAlchemy. Bot was created for forwarding new schedules from vk to Telegram.

## Schedule Functionality

The bot now supports schedule management with the following features:

### Logic

1. **Regular vs Modified Schedules**:

   - Regular schedules are the default schedules for a group
   - Modified schedules are temporary overrides for specific dates (like tomorrow)

2. **Schedule Retrieval**:

   - When requesting a schedule for a specific date, the system first looks for a modified schedule
   - If no modified schedule is found, it falls back to the regular schedule
   - This ensures that modified schedules (like for tomorrow) take precedence

3. **Schedule Confirmation**:
   - Before publishing the schedule, it is sent to the administrators for moderation.
   - If the moderator does not respond within 5 minutes, the schedule is published automatically.

## Implementing automatic verification

- At 9 a.m. every day, an APScheduler Job is created for each verified group
- Every 5 minutes an HTTP request is made to the verified groups.

> Each first request is not considered a new schedule. This means that if the verification starts at 9 a.m., the last post on the page becomes a tag to distinguish it from the new one

### Commands

- `/today` - Get today's schedule for the user's group
- `/schedule` - Get tomorrow's schedule for the user's group

or you can use the buttons below

### Implementation

The schedule functionality is implemented across several files:

- `models/schedule.py` - Database model for schedules
- `db/database.py` - Database methods for schedule management
- `handlers/schedules.py` - User command handlers for schedule operations
- `handlers/admin.py` - Admin command handlers for schedule operations (add, remove)
- `utils/mailing_handler.py` - Mailig many schedules to users
- `services/schedule.py` - Schedule operations management. Caching, quick access from anywhere

## Roadmap

- [ ] Enabling notifications
- [ ] Automatic schedule publication
- [ ] Store bot variables (for example, groups to be checked) in a database as a table.
- [ ] Homeworks
- [ ] RSS
- [ ] Workin services/schedule.py

### AIs Used

[Qwen Code CLI](https://github.com/QwenLM/qwen-code) - Writing Tests, Problem Solving, Assistance

[Gemini Code Assist](https://marketplace.visualstudio.com/items?itemName=Google.geminicodeassist) - Code completion
