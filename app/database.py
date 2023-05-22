from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import Session

from app.glpi_manager.models import Ticket, Organization


def connect_db():
    engine = create_engine(f"postgresql://postgres:postgres@db:5532/postgres", echo=True, pool_size=10,
                           max_overflow=20)
    session = Session(engine)
    return session


def get_all_tickets():
    return connect_db().scalars(select(Ticket).order_by(desc(Ticket.created_at))).all()


def get_all_org():
    session = connect_db()
    query = select(Organization).order_by(Organization.name)
    organizations = session.scalars(query).all()
    session.close()
    return organizations


def create_org(organization: Organization):
    session = connect_db()
    session.add(organization)
    session.commit()
    session.close()



def get_org_by_glpi_id(glpi_id):
    return connect_db().scalars(select(Organization).where(Organization.glpi_id == glpi_id))
