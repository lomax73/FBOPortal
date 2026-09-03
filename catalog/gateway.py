"""Client per la API interna di FBOAIGate (stato host), usato dal widget
"Server & VPS" della home del Portale. Stesse regole di useradmin/services.py:
chiamate solo via loopback (AppLink.internal_base_url), token statico, pinning
del certificato TLS (AppLink.internal_ca_cert).
"""

import requests

from portal.internal_api import TIMEOUT, session_for

from .models import AppLink

GATEWAY_SLUG = 'fboaigate'


class GatewayError(Exception):
    """FBOAIGate non è raggiungibile o non è configurato per l'integrazione."""


def get_app_link():
    try:
        return AppLink.objects.get(slug=GATEWAY_SLUG)
    except AppLink.DoesNotExist:
        return None


def is_configured(app_link):
    return bool(app_link and app_link.internal_base_url and app_link.api_token)


def _base_url(app_link):
    return app_link.internal_base_url.rstrip('/') + '/api/internal/'


def _headers(app_link):
    return {'Authorization': f'Token {app_link.api_token}'}


def list_targets(app_link=None):
    app_link = app_link or get_app_link()
    if not is_configured(app_link):
        raise GatewayError(
            'FBOAIGate non configurato per l\'integrazione '
            '(internal_base_url/api_token mancanti sulla card).'
        )
    try:
        resp = session_for(app_link).get(
            _base_url(app_link) + 'targets/',
            headers=_headers(app_link),
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise GatewayError(str(exc)) from exc
    if resp.status_code != 200:
        raise GatewayError(f'HTTP {resp.status_code}: {resp.text[:200]}')
    return resp.json().get('targets', [])


def target_resources(pk, app_link=None):
    app_link = app_link or get_app_link()
    if not is_configured(app_link):
        raise GatewayError(
            'FBOAIGate non configurato per l\'integrazione '
            '(internal_base_url/api_token mancanti sulla card).'
        )
    try:
        resp = session_for(app_link).get(
            f'{_base_url(app_link)}targets/{pk}/resources/',
            headers=_headers(app_link),
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise GatewayError(str(exc)) from exc
    if resp.status_code != 200:
        raise GatewayError(f'HTTP {resp.status_code}: {resp.text[:200]}')
    return resp.json()
