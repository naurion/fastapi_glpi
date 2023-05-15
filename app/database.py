from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import Session

from app.glpi_manager.models import Ticket


def connect_db():
    engine = create_engine(f"postgresql://postgres:postgres@db:5532/postgres", echo=True, pool_size=10,
                           max_overflow=20)
    session = Session(engine)
    return session


async def get_all_tickets():
    return connect_db().scalars(select(Ticket).order_by(desc(Ticket.created_at))).all()
