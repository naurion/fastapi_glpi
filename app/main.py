from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from sqlalchemy import select

from app.database import connect_db, get_all_tickets
from app.glpi_manager.models import Ticket, Organization

from app.utils.telegram_bot_manager import send_message
from app.utils.glpi import add_ticket

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')

templates = Jinja2Templates(directory='app/static/templates')


@app.get('/index')
async def index(request: Request, tickets = Depends(get_all_tickets)):
    return templates.TemplateResponse('index.html', context={'request': request, 'tickets': tickets})


@app.get('/create_ticket', response_class=HTMLResponse)
async def create_ticket(request: Request):
    session = connect_db()

    query = select(Organization)
    organizations = session.scalars(query).all()

    return templates.TemplateResponse('new_ticket.html', context={'request': request, 'organizations': organizations})


@app.post('/create_ticket')
async def create_ticket(request: Request, org: str = Form(),
                        name: str = Form(),
                        content: str = Form(),
                        user_number: int = Form(),
                        from_telegram: bool = Form(default=False),
                        tickets=Depends(get_all_tickets)
                        ):
    session = connect_db()
    query = select(Organization).where(Organization.name == org)
    organization = session.scalars(query).one_or_none()

    ticket = Ticket(name=name, content=content, user_number=user_number, from_telegram=from_telegram,
                    organization=organization)
    session.add(ticket)
    # add_ticket(ticket)
    session.commit()
    send_message(ticket)

    return templates.TemplateResponse('new_ticket.html', context={'request': request, 'tickets': tickets})
    session.close()


@app.get('/create_organization')
async def create_organization(request: Request):
    return templates.TemplateResponse('new_organization.html', context={'request': request})


@app.post('/create_organization')
async def create_organization(request: Request, name: str = Form(),
                              glpi_id: int = Form(),
                              station_number: int | None = Form(default=None),
                              phone_number: int | None = Form(default=None),
                              ):
    org = Organization(name=name, glpi_id=glpi_id, station_number=station_number, phone_number=phone_number)

    session = connect_db()
    session.add(org)
    session.commit()
    session.close()

    return templates.TemplateResponse('new_organization.html', context={'request': request, 'name': name})
