# Deploy sul VPS

Pattern identico a quello già in uso per MKRemote (repo separato, utente di
sistema dedicato, venv proprio, sottodominio proprio). Riusare questa
cartella come modello per ogni nuova app della famiglia FBO.

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

cp .env.example .env   # poi valorizzare DJANGO_SECRET_KEY, DJANGO_ALLOWED_HOSTS=portal.tuodominio.it
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
