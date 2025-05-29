from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class DBModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
