# Portale FBO

Pagina di lancio per le applicazioni indipendenti della famiglia FBO
(MKRemote, e future utility per la gestione degli apparati clienti). Elenca
le app disponibili come card cliccabili; ogni app è un progetto Django
separato, deployato e autenticato in modo indipendente.

## Sviluppo locale

```
python3 -m venv venv
venv/bin/pip install -r requirements.txt
cp .env.example .env
venv/bin/python manage.py migrate
venv/bin/python manage.py createsuperuser
venv/bin/python manage.py runserver
```

Le app mostrate in home sono gestite dal modello `AppLink` (app `catalog`),
editabile da `/admin/`.

## Deploy

Vedi `deploy/README.md`.
