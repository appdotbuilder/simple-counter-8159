from sqlmodel import select
from typing import Optional
from app.database import get_session
from app.models import Counter, CounterCreate, CounterUpdate


def get_counter(name: str = "default") -> Optional[Counter]:
    """Get counter by name, return None if not found."""
    with get_session() as session:
        statement = select(Counter).where(Counter.name == name)
        return session.exec(statement).first()


def create_counter(counter_data: CounterCreate) -> Counter:
    """Create a new counter."""
    with get_session() as session:
        counter = Counter(name=counter_data.name, count=counter_data.count)
        session.add(counter)
        session.commit()
        session.refresh(counter)
        return counter


def get_or_create_counter(name: str = "default") -> Counter:
    """Get existing counter or create new one if it doesn't exist."""
    counter = get_counter(name)
    if counter is None:
        counter_data = CounterCreate(name=name, count=0)
        counter = create_counter(counter_data)
    return counter


def increment_counter(name: str = "default") -> Counter:
    """Increment counter by 1 and return updated counter."""
    with get_session() as session:
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is None:
            # Create new counter if it doesn't exist
            counter = Counter(name=name, count=1)
            session.add(counter)
        else:
            counter.count += 1
            session.add(counter)

        session.commit()
        session.refresh(counter)
        return counter


def update_counter(name: str, counter_data: CounterUpdate) -> Optional[Counter]:
    """Update counter with new values."""
    with get_session() as session:
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is None:
            return None

        if counter_data.count is not None:
            counter.count = counter_data.count

        session.add(counter)
        session.commit()
        session.refresh(counter)
        return counter


def reset_counter(name: str = "default") -> Optional[Counter]:
    """Reset counter to 0."""
    counter_data = CounterUpdate(count=0)
    return update_counter(name, counter_data)


def get_counter_value(name: str = "default") -> int:
    """Get current counter value, returns 0 if counter doesn't exist."""
    counter = get_counter(name)
    return counter.count if counter else 0
