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

## 2026-08-18 — sessione redflag

### Segnalazioni FBOFlag
- [In test, in attesa di conferma] (id 86) "DEBUG=True di default, impatto esteso: DEBUG=True esporrebbe MASTER_ENCRYPTION_KEY, con cui si decifrano i token di ogni app satellite" — verificato che in produzione `DJANGO_DEBUG=false` è già impostato correttamente (non era un rischio attivo). Aggiunto promemoria esplicito in `deploy/README.md`. Commit+push (`1f55b78`), nessun deploy applicativo necessario (solo doc).
- [In test, in attesa di conferma] (id 87) "`useradmin/services.py`, `verify=False` verso ogni app satellite (direzione opposta: qui il Portale chiama le satelliti)" — più complesso dei casi analoghi già risolti in RackReport/Preventivi/FiberReport perché coinvolge 7 app diverse, ognuna col proprio certificato. Aggiunto `AppLink.internal_ca_cert` (pinning configurabile per app dall'admin) e `_PinnedCertAdapter` in `useradmin/services.py`. 5 app hanno certificati self-signed leggibili da chiunque; 2 (mailer, fboaigate) hanno certificati Let's Encrypt reali ma vivono in `/etc/letsencrypt` (700 root:root, non leggibile dagli utenti applicativi) — per queste il certificato pubblico (mai la chiave privata) è ora copiato in `/etc/ssl/pinned-certs/` da un hook di rinnovo certbot dedicato (`/etc/letsencrypt/renewal-hooks/deploy/copy-pinned-certs.sh`, verificato eseguendolo a mano). Popolate tutte e 7 le righe `AppLink` in produzione, testato `list_users` per ognuna con verifica TLS reale, verificato anche in negativo (un certificato diverso viene rifiutato). Deployato (commit `ccb275f`).
- [In test, in attesa di conferma] (id 88) "`cliente_import_confirm()`, token da POST usato senza validazione nel path — potenziale path traversal" — validato con `uuid.UUID(hex=token)` prima di costruire il path. Deployato (commit `97703e7`).
- [Scartata] (id 108) "Nessun test automatico per catalog/useradmin/clienti" — l'utente ha scelto di scartarla quando proposta (implementazione ora / rimando a sessione dedicata / scarto).

### Verifica rapida del codice
Nessun bug nuovo trovato oltre alle note stesse, tutte confermate nel codice prima di procedere. La verifica rapida generale su `catalog`, rimasta in sospeso dalla sessione del 2026-08-14, resta ancora da fare in una sessione futura.

### Per chi riprende questo progetto
Tutte e 3 le note implementate restano `testing` su FBOFlag finché l'utente non conferma di persona: in particolare provare la gestione utenti da remoto (admin → una card → utenti) per una qualsiasi app satellite (id 87), e l'import clienti da Excel (id 88). Il pattern `verify=False` verso il Portale (lato satelliti, id 91/94/78 di altre sessioni) resta da correggere in mailer e netvault. `/etc/ssl/pinned-certs/` è una posizione condivisa: se in futuro si aggiungono altre app satellite con certificato Let's Encrypt reale (non self-signed), va aggiunta anche lì una riga nell'hook di rinnovo `copy-pinned-certs.sh`.
