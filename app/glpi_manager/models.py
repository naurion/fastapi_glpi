from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Status(Enum):
    NEW = '1'
    ASSIGNET = '2'
    PLANNED = '3'
    PENDING = '4'
    SOLVED = '5'
    CLOSED = '6'


class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(24), unique=True)
    glpi_id: Mapped[int] = mapped_column(Integer, unique=True)
    station_number: Mapped[str | None]
    phone_number: Mapped[str | None]

    tickets: Mapped[List['Ticket']] = relationship(back_populates='organization', cascade='all, delete-orphan')

    def __repr__(self):
        return f'[id: {self.id}, name: {self.name}]'


class Ticket(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column((String(128)))
    content: Mapped[str] = mapped_column(String, default='+')
    status: Mapped[str] = mapped_column(String, default=Status.SOLVED.value)
    created_at: Mapped[str] = mapped_column(String, default=datetime.utcnow())
    user_number: Mapped[str | None]
    from_telegram: Mapped[bool] = mapped_column(Boolean, default=False)

    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    organization: Mapped['Organization'] = relationship(back_populates="tickets")
