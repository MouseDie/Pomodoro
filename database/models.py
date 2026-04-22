from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from typing import Optional



Base = declarative_base()


class Tasks(Base):
    __tablename__ = "Tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]
    

class Categories(Base):
    __tablename__ = "Categories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Optional[str]]
    name: Mapped[str]