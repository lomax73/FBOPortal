# Report sessioni redflag

Report generati dalla skill `redflag`: segnalazioni FBOFlag esaminate e verifica rapida del codice, per questo progetto.

## 2026-08-08 — sessione redflag

### Segnalazioni FBOFlag
- [Conclusa] "negli utenti mi dice MKRemote non raggiungibile: HTTP 404: {\"detail\":\"Not Found\"}" (pagina `/utenti/`).

  **Causa**: `AppLink.internal_base_url` di MKRemote era `https://127.0.0.1:443`. La porta 443 della VPS è condivisa da più vhost nginx (Squadfy, Portal, FBOFlag, MKRemote), distinti tramite `server_name`/header `Host`. La richiesta di `useradmin/services.py` verso `127.0.0.1` manda `Host: 127.0.0.1`, che non corrisponde a nessun `server_name` configurato: nginx la instrada sul vhost di default (non MKRemote), che risponde 404. Le altre app collegate (Collaudi Fibra, FBOPreventivi, FBONetVault, FBORackReport) non avevano questo problema perché usano ciascuna una **porta dedicata** non condivisa (8444-8447).

  **Fix** (solo configurazione VPS + dato nel DB, nessuna modifica al codice di questo repo):
  - Aggiunto un `server{}` block dedicato in `/etc/nginx/sites-available/mkremote` su `listen 127.0.0.1:8449 ssl;` (bind solo su loopback, oltre alla regola `allow 127.0.0.1; deny all;` già presente), esclusivamente per `/api/internal/`.
  - Aggiornato `AppLink.internal_base_url` di MKRemote a `https://127.0.0.1:8449` (sia in produzione sia nel DB locale).
  - Colta l'occasione per completare anche la migrazione dell'URL pubblico: `AppLink.url` di MKRemote era ancora il placeholder `https://mkremote.tuodominio.it/`, aggiornato a `https://mkremote.fbosolution.it/` dopo aver seguito la stessa procedura di migrazione a sottodominio già usata per Squadfy/Portal (DNS su Aruba, certbot `certonly --webroot`, vhost SNI dedicato su 443, `DJANGO_ALLOWED_HOSTS` esteso nel `.env` di MKRemote).

  Verificato end-to-end chiamando `useradmin.services.list_users()` direttamente sulla VPS: risposta corretta con l'utente `admin` di MKRemote.

### Per chi riprende questo progetto
Se un'altra app collegata alla gestione utenti smette di rispondere con un errore simile ("non raggiungibile: HTTP 404" o 403 inatteso), controlla per prima cosa se la sua `internal_base_url` (admin di Django, modello `AppLink`) usa una porta condivisa con altri vhost invece di una porta dedicata — è la causa più probabile su questa VPS, dato lo schema di deploy con più app dietro lo stesso nginx.

## 2026-08-14 — sessione redflag

### Segnalazioni FBOFlag
- [Conclusa] "pagina impostazioni x variare la descrizione delle schede" (testata e confermata dall'utente) — la descrizione di ogni card (`AppLink.description`) era modificabile solo da `/admin/`; aggiunta pagina dedicata `/descrizioni-app/` (`catalog/views.py:app_description_list`, template `catalog/app_description_list.html`), linkata dalla topbar in `templates/base.html` accanto a "Stato app", stesso pattern (form unico, salva tutte le righe in un colpo).

### Verifica rapida del codice
Saltata in questa sessione su richiesta dell'utente — da fare alla prossima sessione redflag su questo progetto, prima di chiudere altre note.

### Per chi riprende questo progetto
La verifica rapida del codice per `catalog`/FBOPortal non è ancora stata fatta in questa sessione: alla prossima ripresa vale la pena farla prima di passare a nuove note. Nessun'altra nota FBOFlag aperta o approvata per `portal` al momento di chiudere questa sessione.
