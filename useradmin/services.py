"""Client per la API interna di gestione utenti esposta da ogni app
(accounts/api/internal/users/, vedi deploy/README.md di MKRemote e
FBOFiberReport). Chiamate solo via loopback (AppLink.internal_base_url),
mai tramite l'URL pubblico dell'app.
"""

import ssl

import requests
from requests.adapters import HTTPAdapter

TIMEOUT = 5


class RemoteAppError(Exception):
    """L'app di destinazione non ha risposto correttamente (giù, token
    sbagliato, errore di validazione)."""


class _PinnedCertAdapter(HTTPAdapter):
    """Ogni app satellite ha un proprio certificato per la sua
    internal_base_url (self-signed per l'IP del VPS, senza campo SAN, o
    Let's Encrypt per un hostname diverso da 127.0.0.1): la verifica
    hostname standard fallirebbe comunque. Verifichiamo invece l'identità
    del certificato stesso (pinning, AppLink.internal_ca_cert): la
    connessione riesce solo con la chiave privata di QUEL certificato
    esatto — stessa protezione da MITM di una verifica normale, senza
    controllo hostname (qui comunque poco significativo: si connette
    sempre a 127.0.0.1)."""

    def __init__(self, ca_cert_path, **kwargs):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=ca_cert_path)
        self._ssl_context = context
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self._ssl_context
        # urllib3 fa una propria verifica dell'hostname (via `assert_hostname`),
        # indipendente da `ssl_context.check_hostname`: va disattivata anche
        # questa, altrimenti richiede comunque un SAN che il certificato non ha.
        kwargs['assert_hostname'] = False
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = self._ssl_context
        kwargs['assert_hostname'] = False
        return super().proxy_manager_for(*args, **kwargs)


def _session(app_link):
    session = requests.Session()
    if app_link.internal_ca_cert:
        session.mount('https://', _PinnedCertAdapter(app_link.internal_ca_cert))
    return session


def _base_url(app_link):
    return app_link.internal_base_url.rstrip('/') + '/api/internal/users/'


def _headers(app_link):
    return {'Authorization': f'Token {app_link.api_token}', 'Content-Type': 'application/json'}


def list_users(app_link):
    try:
        resp = _session(app_link).get(_base_url(app_link), headers=_headers(app_link), timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise RemoteAppError(str(exc)) from exc
    if resp.status_code != 200:
        raise RemoteAppError(f'HTTP {resp.status_code}: {resp.text[:200]}')
    return resp.json().get('users', [])


def create_user(app_link, username, password, email=''):
    try:
        resp = _session(app_link).post(
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
        resp = _session(app_link).patch(
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
        resp = _session(app_link).delete(
            f'{_base_url(app_link)}{user_id}/', headers=_headers(app_link), timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise RemoteAppError(str(exc)) from exc
    if resp.status_code != 204:
        raise RemoteAppError(f'HTTP {resp.status_code}: {resp.text[:200]}')
