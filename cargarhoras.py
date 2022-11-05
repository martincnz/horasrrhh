from datetime import date
import constants as const
import requests as req
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', type=str, required=True)
    parser.add_argument('--passwd', type=str, required=True)
    return parser.parse_args()


def login(credentials):
    login_data = {
        "nombreUsuario": credentials.email,
        "password": credentials.passwd
    }
    login_token = req.post(url=const.login_url,
                           json=login_data).json()['token']
    print('Login Ok')
    return {'Authorization': 'Bearer ' + login_token}


def get_dev_id(auth):
    return req.get(url=const.get_dev_id_url, headers=auth).json()['developerId']


def load_hours(auth, dev_id):
    payload = [{
        "developerId": dev_id,
        "moduloId": const.dev_module_id,
        "cantHoras": 8,
        "descripcion": "",
        "tipoTareaId": const.dev_task_id,
        "ticketId": None,
        "fechaReporte": date.today().isoformat(),
        "developerModuloId": None}]

    return req.post(url=const.load_hours_url, headers=auth, json=payload)


if __name__ == '__main__':
    credentials = parse_args()
    auth_token = login(credentials)

    dev_id = get_dev_id(auth_token)
    success = load_hours(auth_token, dev_id).text

    print(success)
