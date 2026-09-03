"""Client HTTP condiviso verso le API interne (loopback) delle app satellite.

Un solo posto per il pinning del certificato TLS (AppLink.internal_ca_cert) e
la creazione della sessione con token: lo usano useradmin/services.py
(gestione utenti) e catalog/gateway.py (widget stato host). Chiamate solo via
loopback (AppLink.internal_base_url), mai tramite l'URL pubblico dell'app.
"""

import ssl

import requests
from requests.adapters import HTTPAdapter

TIMEOUT = 5


class PinnedCertAdapter(HTTPAdapter):
    """Ogni app satellite ha un proprio certificato per la sua internal_base_url
    (self-signed per l'IP del VPS, senza campo SAN, o Let's Encrypt per un
    hostname diverso da 127.0.0.1): la verifica hostname standard fallirebbe
    comunque. Verifichiamo invece l'identità del certificato stesso (pinning,
    AppLink.internal_ca_cert): la connessione riesce solo con la chiave privata
    di QUEL certificato esatto — stessa protezione da MITM di una verifica
    normale, senza controllo hostname (qui comunque poco significativo: si
    connette sempre a 127.0.0.1)."""

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


def session_for(app_link):
    session = requests.Session()
    if app_link.internal_ca_cert:
        session.mount('https://', PinnedCertAdapter(app_link.internal_ca_cert))
    return session
