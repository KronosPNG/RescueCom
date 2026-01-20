# Contratto di Team - Progetto RescueCom
Versione 2.0

## Ruoli e Responsabilità

### Project Manager
- **Luigi Turco** - Responsabile della pianificazione, coordinamento generale, gestione delle scadenze e punto di escalation per decisioni critiche.

### Development Leaders
- **Francesco** - Backend Lead - Responsabile dell'architettura backend, coordinamento sviluppo lato server, code review backend.
- **Mirko** - Frontend Lead - Responsabile dell'architettura frontend, coordinamento sviluppo lato client, code review frontend.

### Team Members
- Tutti i membri del team contribuiscono attivamente allo sviluppo, testing e documentazione secondo le competenze e gli assignment definiti durante i meeting settimanali.

## Codice di Condotta

Come team, ci impegniamo a:

- Lavorare in modo proattivo per individuare e affrontare tempestivamente eventuali problemi tecnici o organizzativi.
- Mantenere informati tutti i membri del team sui progressi, sulle sfide tecniche e sulle decisioni relative allo sviluppo di RescueCom.
- Concentrarci su ciò che è meglio per il successo complessivo del progetto e per il raggiungimento dei suoi obiettivi.
- Mantenere un comportamento professionale e rispettoso nei confronti di tutti i membri del team in ogni interazione.

## Partecipazione

Ci impegniamo a:

- Essere onesti, rispettosi e trasparenti durante tutte le attività e discussioni di progetto.
- Promuovere la diversità di opinioni e incoraggiare la collaborazione tra tutti i membri.
- Garantire pari opportunità di partecipazione a tutte le fasi del progetto: sviluppo, progettazione, test e documentazione.
- Essere aperti a nuovi approcci e tecnologie che possano migliorare il sistema RescueCom.
- Svolgere una discussione alla volta, assicurandoci che ogni voce venga ascoltata.
- Informare il project manager con **almeno 24 ore di anticipo** in caso di assenza a una riunione o di difficoltà nel rispettare una scadenza assegnata.
- Comprendere che assenze ripetute e non giustificate possono comportare la decadenza del diritto decisionale come specificato nella sezione Processo Decisionale.

## Comunicazione

Ci impegniamo a:

- Utilizzare strumenti quali e-mail, Discord, e piattaforme GitHub e Trello.
- Organizzare riunioni settimanali per aggiornare i progressi, individuare eventuali ostacoli e pianificare le attività successive.
- Redigere e condividere brevi resoconti o registri di progetto per mantenere informati tutti i membri, anche chi non ha potuto partecipare a una riunione.
- Mantenere le discussioni focalizzate e pertinenti.

## Processo Decisionale

Ci impegniamo a:

- Prendere le decisioni importanti durante i meeting settimanali del team.
- Raggiungere una **risoluzione unanime** per tutte le decisioni significative che impattano l'architettura, le tecnologie o la direzione del progetto.
- In caso di disaccordo, dedicare tempo alla discussione costruttiva per comprendere tutte le prospettive.
- Se l'unanimità non viene raggiunta dopo adeguata discussione, il Project Manager ha l'autorità finale per prendere la decisione nel migliore interesse del progetto.
- I membri che non partecipano ai meeting perdono il diritto di voto sulle decisioni prese in quella sessione.
- **Decadenza del diritto decisionale**: La mancata partecipazione continua e non giustificata ai meeting (più di 2 assenze consecutive o 3 non consecutive in un mese) comporta la decadenza temporanea del diritto di voto nelle decisioni di team fino al ripristino della partecipazione regolare.

## Risoluzione dei Problemi

Ci impegniamo a:

- Incoraggiare la partecipazione attiva di tutti i membri nell'individuazione e risoluzione dei problemi tecnici e gestionali.
- Utilizzare un approccio costruttivo, concentrandoci sulla soluzione dei problemi anziché sull'attribuzione delle responsabilità.
- Sfruttare le idee di ciascun membro per costruire soluzioni condivise e migliorative per RescueCom.

### Processo di Escalation

1. **Livello Team**: I problemi tecnici o organizzativi vengono affrontati prima all'interno del micro-team pertinente (Frontend o Backend) con il supporto del rispettivo Development Leader.
2. **Livello Leadership**: Se il problema non trova risoluzione a livello di micro-team entro un tempo ragionevole (2-3 giorni lavorativi), viene escalato al Project Manager.
3. **Livello Project Manager**: Luigi Turco prende decisioni definitive su questioni critiche che impattano il progetto nel suo complesso o che richiedono arbitrato tra i team.

## Linee Guida per le Riunioni

Ci impegniamo a:

- Organizzare riunioni settimanali del team, con una frequenza inizialmente maggiore se necessario.
- Prevedere la partecipazione a distanza tramite videoconferenza per i membri impossibilitati a essere presenti fisicamente.
- Mantenere le riunioni strutturate, seguendo un ordine del giorno preparato dal project manager.
- Redigere e condividere i verbali delle riunioni entro 24 ore, includendo le decisioni prese, i compiti assegnati e le scadenze concordate.
- Organizzare riunioni aggiuntive, se necessario, per affrontare fasi critiche, test o attività di integrazione.

## Gestione del Codice

Ci impegniamo a:

### Repository e Branching Strategy

- Utilizzare **GitHub** come piattaforma principale per il version control del progetto RescueCom.
- Mantenere tre branch principali:
  - **main**: Branch di produzione, contiene solo codice stabile e testato.
  - **frontend**: Macro-branch per l'integrazione delle feature frontend.
  - **backend**: Macro-branch per l'integrazione delle feature backend.
- Creare un **feature branch** dedicato per ogni nuova funzionalità o fix, nominato in modo descrittivo (es. `feature/login-authentication`, `fix/api-timeout`).
- Effettuare il merge dei feature branch sul rispettivo macro-branch (frontend o backend) prima dell'integrazione finale in main.

### Code Review e Qualità del Codice

- **Nessun push diretto su main** è consentito senza approvazione.
- Ogni merge su main richiede:
  - **Code review approvata** dal Project Manager (Luigi Turco), OPPURE
  - **Approvazione di almeno 3 peer** del team.
- I Development Leaders (Francesco per backend, Mirko per frontend) sono responsabili delle code review sui rispettivi macro-branch.
- Seguire gli standard di coding concordati e documentati nel repository.
- Assicurarsi che ogni feature includa test appropriati prima del merge.

### Definition of Done

Una task è considerata completata quando:
- Il codice è stato scritto e testato localmente.
- I test unitari/integrazione sono stati implementati e passano con successo.
- La code review è stata completata e approvata.
- Il codice è stato mergiato sul branch appropriato.
- La documentazione pertinente è stata aggiornata.

## Metriche di Successo del Progetto

Il progetto RescueCom sarà considerato un successo se, entro la fine di Gennaio 2026:

- Esiste un **proof-of-concept funzionante** che dimostra le funzionalità core del sistema.
- Tutte le **funzionalità core identificate** sono implementate e operative.
- È presente una **suite di test completa** che copre le funzionalità principali con test automatizzati.
- Tutti i **deliverables documentali** richiesti sono completati, revisionati e consegnati:

## Scadenze e Consegna
Ci impegnamo a:
- Rispettare le scadenze concordate per le varie fasi del progetto, comunicando tempestivamente eventuali difficoltà.
- Lavorare al progetto RescueCom a partire da Ottobre 2025
- Terminare il lavoro, consegnare deliverables entro la fine di Gennaio 2026

## Modifiche al Contratto

Il presente contratto può essere modificato secondo le seguenti modalità:

- Le proposte di modifica devono essere presentate durante un meeting settimanale o comunicate al Project Manager con almeno 48 ore di anticipo.
- Le modifiche al contratto richiedono l'**approvazione unanime** di tutti i membri attivi del team.
- Il Project Manager è responsabile dell'aggiornamento del documento e della distribuzione della nuova versione.
- Ogni modifica comporta l'incremento del numero di versione del contratto.
- Tutti i membri devono confermare l'accettazione della nuova versione entro 72 ore dalla pubblicazione.
- Le modifiche entrano in vigore solo dopo la conferma da parte di tutti i membri.

## Conferma e Impegno

Firmando il presente contratto, tutti i membri del team RescueCom dichiarano di accettare le presenti linee guida e di impegnarsi a collaborare in modo costruttivo per il successo del progetto.
