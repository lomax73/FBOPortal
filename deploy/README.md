# Deploy sul VPS

Pattern identico a quello già in uso per MKRemote (repo separato, utente di
sistema dedicato, venv proprio, sottodominio proprio). Riusare questa
cartella come modello per ogni nuova app della famiglia FBO.

## Stato attuale in produzione (provvisorio)

**Non esiste ancora un dominio reale**: anche MKRemote è servito sull'IP nudo
(`94.177.161.127`) con un certificato self-signed, non c'è DNS configurato.
Il Portale è stato quindi deployato provvisoriamente sulla stessa IP, porta
diversa: **`https://94.177.161.127:8443/`**, cert self-signed dedicato in
`/etc/ssl/portal/`, config Nginx realmente in uso in
`deploy/nginx-portal-ip-provisional.conf` (porta aperta anche su UFW).
`deploy/nginx-portal.conf` resta il template "finale" a sottodominio, da
usare appena sarà disponibile un dominio vero (vedi passi sotto).

## Provisioning iniziale (una tantum)

```
# da root sul VPS
adduser --system --group --home /opt/portal portal
mkdir -p /opt/portal/app
chown portal:portal /opt/portal/app

sudo -u portal git clone <url-repo> /opt/portal/app
cd /opt/portal/app
sudo -u portal python3 -m venv venv
sudo -u portal venv/bin/pip install -r requirements.txt

cp .env.example .env   # poi valorizzare DJANGO_SECRET_KEY, DJANGO_ALLOWED_HOSTS=portal.tuodominio.it, INTERNAL_API_TOKEN
sudo -u portal venv/bin/python manage.py migrate
sudo -u portal venv/bin/python manage.py collectstatic --noinput
sudo -u portal venv/bin/python manage.py createsuperuser

cp deploy/portal-web.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now portal-web.service

cp deploy/nginx-portal.conf /etc/nginx/sites-available/portal
ln -s /etc/nginx/sites-available/portal /etc/nginx/sites-enabled/portal
nginx -t && systemctl reload nginx
# + certificato TLS (es. certbot --nginx -d portal.tuodominio.it)
```

## API interna anagrafica clienti (per le app satellite)

Da qui in poi il Portale **riceve** anche chiamate interne, non solo le fa
(caso finora unico: gestione utenti multi-app). `clienti/api/internal/`
espone in sola lettura l'anagrafica clienti condivisa (`GET .../clienti/`,
`GET .../clienti/<uuid>/`), protetta da header
`Authorization: Token <INTERNAL_API_TOKEN>` e da un blocco Nginx dedicato
che consente solo `127.0.0.1` (già incluso in `nginx-portal-ip-
provisional.conf`/`nginx-portal.conf`, prima del blocco generico
`location /`). Ogni app satellite che deve risolvere un client_id (es.
FBOPreventivi) configura nel proprio `.env`:
- `PORTAL_INTERNAL_BASE_URL` (es. `https://127.0.0.1:8443`)
- `PORTAL_API_TOKEN` (stesso valore di `INTERNAL_API_TOKEN` qui sopra)

## Report rack/patch panel (app `rackreport`)

Il PDF è generato con WeasyPrint, che richiede librerie di sistema (non
pacchetti Python), stessa nota già in `FBOFiberReport/deploy/README.md`:

```
apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libcairo2
```

Gli allegati caricati sui rack (report degli strumenti di verifica) sono
la prima cosa che il Portale salva in `media/`: va creata la cartella al
provisioning (o al primo deploy di questa funzionalità se il Portale è
già in produzione):

```
mkdir -p /opt/portal/app/media && chown portal:portal /opt/portal/app/media
```

Il blocco Nginx `location /media/` è già incluso in
`nginx-portal-ip-provisional.conf`/`nginx-portal.conf`.

## Deploy di un aggiornamento

```
ssh mkremote-vps
cd /opt/portal/app
sudo -u portal git pull origin main
sudo -u portal venv/bin/pip install -r requirements.txt
sudo -u portal venv/bin/python manage.py migrate
sudo -u portal venv/bin/python manage.py collectstatic --noinput
systemctl restart portal-web.service
```
