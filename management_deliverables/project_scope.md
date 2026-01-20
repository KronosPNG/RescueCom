# Scope Statement - Progetto RescueCom

## Titolo del Progetto: RescueCom

Data: 24 ottobre 2025

Redatto da: Luigi Turco

## Sintesi e Giustificazione del Progetto

Il progetto RescueCom nasce per colmare le lacune critiche di comunicazione durante situazioni di emergenza in cui le infrastrutture Internet tradizionali risultano non disponibili. Il sistema consente comunicazioni di emergenza attraverso Bluetooth e Wi-Fi Direct, con sincronizzazione automatica al cloud quando la connettività viene ripristinata.  
<br/>Questo progetto supporta le organizzazioni di protezione civile e soccorso nel mantenere la continuità operativa durante disastri, catastrofi naturali o guasti infrastrutturali. La rete di relay decentralizzata garantisce che i messaggi di emergenza raggiungano il personale di soccorso anche quando i canali di comunicazione diretta sono compromessi.  
<br/>Si tratta di un proof of concept con l'obiettivo di dimostrare la fattibilità tecnica del sistema e validare l'architettura proposta. I benefici attesi includono la dimostrazione di un modello di comunicazione resiliente e decentralizzato applicabile in contesti di emergenza reale.

## Caratteristiche e Requisiti del Prodotto

### 1\. Capacità di Comunicazione Offline

Il sistema deve consentire la trasmissione di messaggi tra dispositivi Rescuee (persone in difficoltà) e Rescuer (soccorritori) utilizzando Bluetooth e Wi-Fi Direct quando la connettività Internet non è disponibile. I messaggi verranno memorizzati localmente sui dispositivi e sincronizzati automaticamente con il server cloud una volta ripristinata la connettività.

### 2\. Funzionalità di Relay

Tutti i dispositivi (sia Rescuee che Rescuer) devono essere in grado di funzionare come nodi relay, inoltrando messaggi di emergenza da altri utenti per estendere la portata della rete di comunicazione. Il protocollo di relay deve prevenire la duplicazione dei messaggi e garantire un instradamento efficiente.

### 3\. Tipologie di Messaggi di Emergenza

Il sistema deve supportare richieste di aiuto da parte degli utenti. I messaggi devono includere timestamp, ID mittente e livello di priorità. La posizione dell'utente in difficoltà viene determinata tramite prossimità ai dispositivi Rescuer che ricevono il messaggio, non attraverso coordinate GPS.

### 4\. Persistenza Dati Locale

Ogni dispositivo deve mantenere un database locale dei messaggi inviati e ricevuti per garantire la disponibilità dei dati durante i periodi offline. Il database locale deve essere capace di memorizzare messaggi con i relativi metadati.

### 5\. Sincronizzazione Cloud

Quando la connettività Internet diventa disponibile, i dispositivi devono sincronizzarsi automaticamente con il server cloud centrale. Il processo di sincronizzazione deve gestire la risoluzione dei conflitti per messaggi duplicati o modificati utilizzando algoritmi basati su data e ID dispositivo.

### 6\. API REST

Il server cloud deve fornire un'API REST completa per la comunicazione dei dispositivi, l'invio di messaggi, il recupero e gli aggiornamenti di stato. L'API deve supportare connessioni HTTPS sicure.

### 7\. Requisiti dell'Interfaccia Utente

\- Interfaccia Rescuee: Interfaccia desktop semplice e intuitiva per l'invio di richieste di emergenza con template di messaggi predefiniti e attivazione rapida dell'SOS.  
\- Interfaccia Rescuer: Interfaccia desktop per la gestione della coda messaggi, strumenti di prioritizzazione e capacità di risposta alle emergenze.

### 8\. Sicurezza e Autenticazione

I dispositivi Rescuee non richiedono autenticazione per facilitare l'accesso immediato in situazioni di emergenza. I dispositivi Rescuer devono essere validati e autorizzati dal sistema.

### 9\. Scoperta Dispositivi e Gestione Rete

Il sistema deve scoprire automaticamente i dispositivi nelle vicinanze tramite scansione Bluetooth/Wi-Fi Direct a intervalli regolari. La topologia di rete deve adattarsi dinamicamente mentre i dispositivi si muovono, si connettono o si disconnettono.

### 10\. Supporto Piattaforma

Il sistema sarà sviluppato come proof of concept per la piattaforma Windows, con l'architettura progettata per consentire futuri porting su altre piattaforme (Linux, macOS, mobile).

## Riepilogo dei Deliverable del Progetto

### Deliverable Relativi alla Gestione del Progetto

Business case, Project Charter, Team Contract, Scope Statement, Work Breakdown Structure (WBS), cronoprogramma del progetto, presentazione finale del progetto, relazione finale del progetto e qualsiasi altro documento necessario per gestire il progetto.

### Deliverable Relativi al Prodotto

Elenco dettagliato dei deliverable tecnici e documentali, inclusi documenti di analisi, progettazione, implementazione, testing e documentazione finale.

## Criteri di Successo del Progetto

Implementazione del proof-of-concept, infrastruttura CI/CD funzionante, test suite ben strutturata.

## Vincoli e Assunzioni del Progetto

### Vincoli

- Timeline di 3 mesi dall'avvio del progetto alla consegna finale.
- Sviluppo limitato alla piattaforma Windows per il proof of concept.
- Utilizzo di computer desktop/laptop come dispositivi.
- Limitato alle tecnologie Bluetooth e Wi-Fi Direct.

### Assunzioni

- Lo Sponsor fornirà feedback e validazione sui requisiti.
- Gli utenti concederanno i permessi necessari ai dispositivi (Bluetooth, Wi-Fi Direct, ecc.).
- I dispositivi utilizzati per i test saranno computer Windows con capacità Bluetooth e Wi-Fi.
- Il server cloud sarà simulato in ambiente di sviluppo locale o su infrastruttura cloud gratuita/educativa.
- I membri del team possiedono conoscenze di base nello sviluppo software e nel networking.
- Saranno disponibili computer per simulare scenari multi-dispositivo durante i test.