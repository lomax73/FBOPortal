"""Client per la API interna di gestione utenti esposta da ogni app
(accounts/api/internal/users/, vedi deploy/README.md di MKRemote e
FBOFiberReport). Chiamate solo via loopback (AppLink.internal_base_url),
mai tramite l'URL pubblico dell'app.
"""

from portal.internal_api import TIMEOUT, session_for


class RemoteAppError(Exception):
    """L'app di destinazione non ha risposto correttamente (giù, token
    sbagliato, errore di validazione)."""


def _base_url(app_link):
    return app_link.internal_base_url.rstrip('/') + '/api/internal/users/'


def _headers(app_link):
    return {'Authorization': f'Token {app_link.api_token}', 'Content-Type': 'application/json'}


def list_users(app_link):
    try:
        resp = session_for(app_link).get(_base_url(app_link), headers=_headers(app_link), timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise RemoteAppError(str(exc)) from exc
    if resp.status_code != 200:
        raise RemoteAppError(f'HTTP {resp.status_code}: {resp.text[:200]}')
    return resp.json().get('users', [])


def create_user(app_link, username, password, email=''):
    try:
        resp = session_for(app_link).post(
            _base_url(app_link), headers=_headers(app_link), timeout=TIMEOUT,
            json={'username': username, 'password': password, 'email': email},
        )
    except requests.RequestException as exc:
        raise RemoteAppError(str(exc)) from exc
    if resp.status_code != 201:
        raise RemoteAppError(f'HTTP {resp.status_code}: {resp.text[:200]}')
    return resp.json()


def update_user(app_link, user_id, **fields):
    try:
        resp = session_for(app_link).patch(
            f'{_base_url(app_link)}{user_id}/', headers=_headers(app_link), timeout=TIMEOUT,
            json=fields,
        )
    except requests.RequestException as exc:
        raise RemoteAppError(str(exc)) from exc
    if resp.status_code != 200:
        raise RemoteAppError(f'HTTP {resp.status_code}: {resp.text[:200]}')
    return resp.json()


def delete_user(app_link, user_id):
    try:
        resp = session_for(app_link).delete(
            f'{_base_url(app_link)}{user_id}/', headers=_headers(app_link), timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise RemoteAppError(str(exc)) from exc
    if resp.status_code != 204:
        raise RemoteAppError(f'HTTP {resp.status_code}: {resp.text[:200]}')
