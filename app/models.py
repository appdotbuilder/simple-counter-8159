from sqlmodel import SQLModel, Field
from typing import Optional


class Counter(SQLModel, table=True):
    """Model to store counter state in the database."""

    __tablename__ = "counters"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    count: int = Field(default=0)
    name: str = Field(default="default", max_length=100, unique=True)


class CounterCreate(SQLModel, table=False):
    """Schema for creating a new counter."""

    name: str = Field(default="default", max_length=100)
    count: int = Field(default=0)


class CounterUpdate(SQLModel, table=False):
    """Schema for updating counter values."""

    count: Optional[int] = Field(default=None)
