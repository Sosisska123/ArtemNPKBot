from enum import Enum
from models.user import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column


class ScheduleType(Enum):
    REGULAR = "regular"  # base schedule
    MODIFIED = "modified"  # for schedules that are changed for a specific day
    RING = "ring"  # ring schedule
    DEFAULT_RING = "default_ring"  # ring schedule whenever


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group: Mapped[str] = mapped_column(String(10))
    url: Mapped[str] = mapped_column(Text, unique=True)
    date: Mapped[str] = mapped_column()
    schedule_type: Mapped[str] = mapped_column(
        String(20), default=ScheduleType.REGULAR.value
    )
    file_type: Mapped[str] = mapped_column(String(10))
