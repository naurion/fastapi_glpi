import requests
from dotenv import load_dotenv
import os


load_dotenv()

URL = os.getenv('URL')
USER_TOKEN = os.getenv('USER_TOKEN')
APP_TOKEN = os.getenv('APP_TOKEN')


def get_session_token():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'user_token {USER_TOKEN}',
        'App-Token': APP_TOKEN
    }
    r = requests.get(f'{URL}initSession', headers=headers)

    session_token = r.json().get('session_token')

    return session_token


def close_session(session_token):
    headers = {
        'Content-Type': 'application/json',
        'Session-Token': session_token,
        'App-Token': APP_TOKEN
    }
    r = requests.get(f'{URL}killSession', headers=headers)


def add_ticket(name, content, user_number, from_telegram, organization):
    session_token = get_session_token()
    headers = {
        'Session-Token': session_token,
        'App-Token': APP_TOKEN
    }

    entities_id = organization.glpi_id

    if from_telegram:
        name = f'{organization.name}, из Телеграм: {name}'
    else:
        name = f'{organization.name}, {organization.station_number}{user_number}: {name}'

    item = {'input': {
        'name': name,
        'content': content,
        '_users_id_assign': 104,  # user id
        '_users_id_requester': 104,  # user id
        # '_groups_id_assign': 1,
        'status': '5',
        'entities_id': entities_id,
        '_disablenotif': '1'
    }}

    response = requests.post(f'{URL}Ticket', headers=headers, json=item)

    close_session(session_token)

    return response


if __name__ == '__main__':
    # organization = Organization(name='Integrasky', glpi_id=0, station_number='911')
    #
    # ticket = Ticket(name='Test', content='Test', user_number='765', from_telegram=False,
    #                 organization=organization)
    # response = add_ticket(ticket)
    # print(response.text)
    pass