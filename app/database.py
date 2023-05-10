from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import Session

from app.glpi_manager.models import Organization, Ticket

from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')


def connect_db():
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True, pool_size=10,
                           max_overflow=20)
    session = Session(engine)
    return session


async def get_all_tickets():
    return connect_db().scalars(select(Ticket).order_by(desc(Ticket.created_at))).all()
