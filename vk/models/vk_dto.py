from models.user import Base
import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Schedule(Base):
    __tablename__ = "vk_group_dto"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    domain: Mapped[str] = mapped_column(String(10))
    group_name_shortcut: Mapped[str] = mapped_column(String(5))
    start_post_offset: Mapped[int] = mapped_column()
    return_file_type: Mapped[str] = mapped_column(String(10))

    post_date: Mapped[datetime.date | str]
    post_title: Mapped[str] = mapped_column(String(100))
