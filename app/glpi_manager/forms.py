from pydantic import BaseModel


class Organization(BaseModel):
    name: str
    glpi_id: int
    station_number: str | None = None
    phone_number: str | None = None

class Ticket(BaseModel):
    name: str
    content: str
    organization: Organization
    user_number: int | None = None
    from_telegram: bool
