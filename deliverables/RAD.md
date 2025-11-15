# RAD

1. **Introduction**

**1.1. Purpose of the system**

**1.2. Scope of the system**

**1.3. Objectives and success criteria of the project**

**1.4. Definition, acronyms, and abbreviations**

**1.5. References**

**1.6. Overview**

**2. Current system**

1. **Proposed system**

**3.1. Overview**

**3.2. Functional requirements**

**3.3. Nonfunctional requirements**

**3.4. System models**

**3.4.1. Scenarios**

**3.4.2. Use case model**

**3.4.3. Object model    (during analysis)**

**3.4.4. Dynamic model (during analysis)**

**3.4.5. User interface – navigational path and screen mock-up**

1. **Glossary**

Introduzione

Il progetto **RescueCom** nasce con l’obiettivo di sviluppare un sistema di comunicazione d’emergenza capace di funzionare anche in assenza di connettività Internet.

1.1 Scopo del sistema

***Problema che risolve***: colmare le lacune critiche di comunicazione durante situazioni di emergenza (disastri naturali, blackout infrastrutturali) in cui l’accesso a Internet non è disponibile.

***Funzione principale***: permettere l’invio, il relay e la ricezione di messaggi di emergenza fra dispositivi presenti nell’area interessata utilizzando Bluetooth e Wi-Fi Direct; memorizzare i messaggi localmente e sincronizzarli automaticamente con un server cloud quando la connettività è ripristinata.

Utenti target:

***Rescuee*** — persone in difficoltà che inviano richieste di aiuto.

***Rescuer*** — personale di soccorso che riceve, prioritizza e risponde alle richieste.

1.2 Ambito del sistema

Lo scopo del sistema RescueCom è fornire una soluzione di comunicazione d’emergenza affidabile e resiliente, capace di garantire lo scambio di messaggi anche in assenza di connettività Internet. Il sistema consente agli utenti in difficoltà (Rescuee) di inviare richieste di aiuto che vengono trasmesse e inoltrate tra i dispositivi vicini tramite Bluetooth e Wi-Fi Direct, fino a raggiungere un soccorritore (Rescuer). Ogni dispositivo può agire come nodo relay, estendendo la copertura della rete e contribuendo alla diffusione del messaggio all’interno dell’area interessata. I messaggi vengono salvati localmente e sincronizzati automaticamente con un server cloud quando la connessione torna disponibile, assicurando la tracciabilità e la conservazione dei dati. Il sistema è progettato per essere semplice, immediato e accessibile, riducendo i tempi di comunicazione nelle situazioni critiche e aumentando la probabilità che le richieste di soccorso vengano ricevute e gestite tempestivamente.

1.3 Obiettivi e criteri di successo

L’obiettivo principale del progetto **RescueCom** è dimostrare la fattibilità tecnica di un sistema di comunicazione d’emergenza capace di operare anche in assenza di connettività Internet, garantendo la trasmissione e la ricezione di messaggi critici tra persone in difficoltà e soccorritori. In particolare, il progetto mira a sviluppare un *Proof of Concept* che implementi una rete decentralizzata basata su Bluetooth e Wi-Fi Direct, in cui ogni dispositivo possa funzionare come nodo relay, permettendo l’inoltro dei messaggi e l’estensione della copertura comunicativa. Un ulteriore obiettivo è l’integrazione di un meccanismo di persistenza locale e sincronizzazione cloud, che consenta di salvare i messaggi sul dispositivo e aggiornarli automaticamente sul server quando la connessione torna disponibile, garantendo coerenza e integrità dei dati. Il sistema deve inoltre offrire interfacce utente intuitive e funzional**i** sia per gli utenti in difficoltà (*Rescuee*) sia per i soccorritori (*Rescuer*), in modo da assicurare rapidità di utilizzo e accesso immediato alle funzioni essenziali in contesti di emergenza. Il successo del progetto sarà misurato attraverso criteri specifici, tra cui la capacità del sistema di stabilire una comunicazione affidabile in rete locale, la corretta propagazione dei messaggi tramite relay, la sincronizzazione senza perdite con il server cloud e la validazione del *Proof of Concept* attraverso test pratici. Il raggiungimento di questi obiettivi dimostrerà l’efficacia del sistema come strumento di supporto alle comunicazioni di emergenza in scenari privi di infrastrutture di rete.

1.4 Definizioni , acronimi e abbreviazioni

**FURPS+** =

Rappresenta:

- Funzionalità
- Usabilità
- Affidabilità
- Prestazioni
- Sopportabilità

Il “+” sta per pseudo-requisiti o vincoli del sistema:

- Implementazione
- Interfaccia
- Operazioni
- Packaging
- Legali

1.5 Riferimenti

Bruegge, Bernd, and Allen H. Dutoit. "Object–oriented software engineering. using uml, patterns, and java." Learning 5.6 (2009): 7

Slide e materiale aggiuntivo sulla piattaforma e-learning del corso.

1.6 Panoramica del documento

Il  documento è organizzato in diverse sezioni, ognuna delle quali affronta un aspetto specifico dell’analisi e della progettazione del sistema RescueCom, con l’obiettivo di fornire una visione completa, chiara e strutturata del progetto.

- ***Introduzione***: presenta lo scopo generale del sistema, l’ambito di applicazione, gli obiettivi e i criteri di successo, oltre a una panoramica delle definizioni, degli acronimi e delle abbreviazioni utilizzate.
- ***Sistema Corrente***: analizza il funzionamento attuale del sistema, evidenziandone le problematiche, i limiti e gli aspetti rilevanti.
- ***Sistema Proposto***: descrive in dettaglio il nuovo sistema partire dalla definizione degli attori del sistema per poi focalizzarsi sui Requisiti Funzionali, che identificano le funzionalità che il sistema deve offrire. Questi sono suddivisi per categoria in base agli attori coinvolti e seguono la convenzione di denominazione:

RF_[attore]_[numero] nomeDelRequisitoFunzionale. A seguire sono elencati i Requisiti Non Funzionali, anch’essi organizzati secondo la convenzione: NFR_[attore]_[numero] nomeDelRequisitoNonFunzionale. I requisiti non funzionali fanno riferimento al modello FURPS+. La sezione prosegue con il Modello ad Oggetti, che include le diverse entità di tipo *Boundary*, *Control* ed *Entity*, accompagnate dai rispettivi Diagrammi delle Classi e Diagrammi degli Oggetti. Seguono i Modelli Dinamici, costituiti da Diagrammi di Sequenza e Diagrammi delle Attività, utili per rappresentare il comportamento del sistema nel tempo. Infine, viene presentata l’Interfaccia Utente, comprendente mock-up, prototipo interattivo (impiegato nella validazione dei requisiti) e Navigational Path che illustra i percorsi di navigazione all’interno del sistema.

***Glossario***: conclude il documento fornendo un elenco di termini, sigle e abbreviazioni utilizzate, con relative definizioni, per assicurare chiarezza e uniformità terminologica.

1. Sistema Corrente

2.1 Panoramica

Attualmente, non esiste alcuna piattaforma o applicazione in grado di garantire una comunicazione d’emergenza efficace in condizioni di totale assenza di connettività Internet. Le soluzioni oggi disponibili si basano quasi esclusivamente su reti mobili o connessioni dati, rendendo impossibile l’invio o la ricezione di messaggi in scenari critici come disastri naturali, blackout o aree prive di copertura di rete.

Alcune applicazioni di messaggistica offline esistenti, come quelle che sfruttano connessioni Bluetooth o Wi-Fi Direct, offrono funzionalità limitate e non sono pensate per contesti di emergenza. Queste soluzioni, infatti, non prevedono un meccanismo affidabile di inoltro dei messaggi (*relay*), non garantiscono la persistenza locale dei dati né una sincronizzazione automatica con un server remoto una volta ripristinata la connettività.

La proposta di RescueCom nasce quindi per superare tali limitazioni, introducendo un sistema più completo, resiliente e specializzato per la gestione delle comunicazioni in emergenza. Attraverso una rete decentralizzata di dispositivi, RescueCom consente lo scambio di messaggi anche in assenza di infrastrutture di rete, assicurando affidabilità, continuità delle comunicazioni e una gestione efficiente delle richieste di soccorso.

3.0 Sistema Proposto

**Obiettivo**

comunicazione e gestione di richieste di aiuto fra due componenti umane:

**rescuee (persona che deve essere soccorsa)**

**rescuer (persona che soccorre)**.  // TODO: definire meglio

Consentire la comunicazione in scenari di emergenza anche in assenza di connessione.

1. **Comunicazione**

**2.1 tecnologie utilizzate**

- bluetooth
- wifi-direct

**2.2 modalità di comunicazione**

- p2p per scambio diretto di messaggi fra utenti nelle vicinanze
- comunicazione a corto raggio

**Posizione e GPS**

determinare la distanza: utile per la gestione delle richieste di aiuto.

Durante l’utilizzo si ottiene la posizione mediante gps, ma se non disponibile si ottiene mediante input dell'utente (se possibilitato) -

1. **Richieste di aiuto**

**3.1 Rescuee**

- possono inserire le richieste degli altri rescuee nel db, ma non vi possono accedere.
- Il rescuee deve comunicare il proprio problema mediante un’apposita interfaccia.

**3.2 Rescuer**

- devono avere un’interfaccia CRUD (delete non permesso).
- Le richieste sono ordinate in base alla gravità (determinata anche dalla presenza di eventuali disabilità del rescuee)
- ha un’interfaccia per risolvere le richieste di aiuto

**Altre funzionalità:**

- se una persona non può digitare si può usare un sistema di **speech to text**
- ci deve essere la possibilità di premere anche solo un tasto per poter chiedere aiuto
1. **Ruoli e gestione credenziali**
- **rescuee → rescuer**

il cambio di ruolo non è consentito, poiché le credenziali di base identificano il ruolo dell’utente. La componente rescuer è accessibile solo da chi è soccorritore

- **rescuer → rescuee**

il rescuer può comportarsi da rescuee se ha bisogno di aiuto. In questo caso il rescuer potrebbe avere maggiore priorità rispetto agli altri rescue.

1. **Sincronizzazione Cloud**

Il cloud si occupa della sincronizzazione in base allo stato più coerente

in base alle versioni più recenti

- **zone disgiunte:** le informazioni delle due zone si combinano
- **altre zone:** si controlla l’ordine di arrivo delle informazioni e la versione più recente viene utilizzata
1. **Modalità di comunicazione**
- **Offline**: si usano wi-fi direct e bluetooth
- **Online**: comunicazione mediante server

—--

1. **Funzionamento**

Abbiamo detto quindi che le due componenti sono il **rescuee** e il **rescuer**.

- **messaggio → rescuer:** il sistema deve salvarlo in un database locale.
- **messaggio → rescuee:** il rescuee funge da ripetitore e il sistema deve salvarlo in un database locale

**7.1 Processo di richiesta**

1. **invio richiesta**

**richiesta senza connessione**

la richiesta viene mandata mediante bluetooth o wifi-direct, i vari dispositivi nelle vicinanze fungono da ripetitori per garantire la ricezione del messaggio da parte del rescuer

**richiesta con connessione**

la comunicazione deve avvenire inviando la richiesta di soccorso al server

1. **recupero posizione**

Quando viene mandata la richiesta di soccorso, il sistema tenta di ricavare la posizione mediante GPS, se disponibile. Nel caso in cui non fosse disponibile si chiede al rescuee di inserire la sua posizione

dati richiesti:

- coordinate
- via, zona, descrizione luogo
- foto della zona

// TODO: chiarire in che modo gestire eventuali rescuee che non conoscono la zona

1. **gestione richieste**

Quando il rescuer accede al sistema, il sistema deve mostrargli una lista di tutte le richieste di aiuto (quelle prioritarie mostrate evidenziate in alto (non funzionale?))

Il server (cloud) centrale deve mantenere uno **storico** di tutte le richieste di aiuto all’interno di un database.

Quando il rescuee invia una richiesta di soccorso, riceve un **messaggio di conferma** se recapitabile.

Quando due o più rescuer accettano la stessa richiesta di aiuto, il sistema assegna la richiesta di aiuto al primo rescuer il quale messaggio di conferma viene ricevuto

Quando il rescuer accede al sistema, quest’ultimo deve permettergli di accettare una richiesta di aiuto tra quelle presenti nella lista.

Quando il rescuee ritiene che la sua situazione di emergenza sia cambiata, il sistema deve permettergli di aggiornare la vecchia richiesta di aiuto dopo che sono passati N minuti

Finché la richiesta di aiuto non riceve una conferma di ricezione, il sistema deve continuare a mandare il messaggio di aiuto ogni N secondi

Quando un rescuer accetta una richiesta di soccorso, il sistema deve inviare un messaggio in broadcast in cui specifica che tale richiesta di soccorso è stata accettata

**7.2 Primo accesso rescuee**

Il sistema deve fargli compilare un form in cui deve inserire:

- nome
- cognome
- data di nascita
- gruppo sanguigno
- eventuali allergie a medicinali
- eventuali disabilità o malattie gravi

**7.3 Accessi successivi rescuee**

Quando il rescuee vuole inviare una richiesta di aiuto, il sistema deve fargli compilare un form in cui inserire dettagli riguardo l’emergenza.

NON TOCCARE (PLS):

comunicazione bluetooth e wifi-direct -

comunicazione a corto raggio -

p2p per lo scambio di messaggi -

due componenti umane: rescuee (persona da soccorrere) e rescuer (soccorritore) // TODO: definire meglio

determinare la distanza -

ottenere la posizione mediante gps o input dell'utente (se possibilitato) -

le persone devono comunicare il loro problema -

i rescuee devono avere un db per mandare le richieste degli altri rescuee ma non devono poter accedere -

i rescuer devono avere una interfaccia CRUD (tranne delete) con tutte le richieste di aiuto oridinate in base alla gravità (determinata anche in base alla presenza di disabilità nel rescuee)

- se una persona non può digitare si può usare un sistema di speech to text

- ci deve essere la possibilità di premere anche solo un tasto per poter chiedere aiuto

un rescuee può diventare rescuer?

- le credenziali di base ci identificano (quindi se sono rescuee non posso diventare rescuer)

- la componente rescuer è indirizzata a chi è effettivamente un rescuer

il rescuer ha l'interfaccia per risolvere le domande di aiuto -

il rescuer può comportarsi da rescuee se ha bisogno di aiuto e potrebbe avere maggiore priorità -

il cloud si occupa della sincronizzazione in base allo stato più coerente

in base alle versioni più recenti

ad esempio se si hanno due zone, est e ovest, tra loro disgiunte, le informazioni delle due zone si "sommano"

per gestire altre zone, invece, controlliamo l'ordine d'arrivo (usiamo la versione più recente)

per comunicare si usano wifi-direct e bluetooth in assenza di internet, altrimenti si comunica mediante il server

non necessariamente crossplatform

—--

Il sistema deve avere due tipi di utente: rescuee (la persona da soccorrere) e il rescuer (il soccorritore)

Quando il messaggio viene ricevuto dal rescueer, il sistema deve salvarlo in un database locale

Quando il messaggio viene ricevuto da un rescuee che funge da ripetitore, il sistema deve salvarlo in un database locale

in assenza di connessione, il sistema deve garantire una comunicazione a corto raggio mediante bluetooth o wifi-direct

Quando il rescuee deve mandare una richiesta di soccorso e non c’è connessione ad internet, il sistema deve mandarla mediante bluetooth o wifi-direct

in assenza di connessione, i vari dispositivi nelle vicinanze devono fungere da ripetitori per garantire la ricezione del messaggio da parte del rescuer

Quando il rescuee deve mandare una richiesta di soccorso e c’è connessione ad internet, la comunicazione deve avvenire inviando la richiesta di soccorso al server (cloud)

Quando il rescuee manda una richiesta di soccorso, il sistema deve tentare di ricavare la posizione mediante il gps se quest’ultimo è abilitato e disponibile

Quando il rescuee manda una richiesta di soccorso e il gps non è attivo o disponibile, il sistema deve chiedere al rescuee di inserire la sua posizione (coordinate, via, zona, descrizione del luogo, foto della zona ecc.) // TODO: chiarire in che modo gestire eventuali rescuee che non conoscono la zona

Quando il rescuer accede al sistema, il sistema deve mostrargli una lista di tutte le richieste di aiuto (quelle prioritarie mostrate evidenziate in alto (non funzionale?))

Il server (cloud) centrale deve mantenere uno storico di tutte le richieste di aiuto all’interno di un database

Quando il rescuee invia una richiesta di soccorso, può ricevere un messaggio di conferma se recapitabile

Quando due o più rescuer accettano la stessa richiesta di aiuto, il sistema assegna la richiesta di aiuto al primo rescuer il quale messaggio di conferma viene ricevuto dal rescuee

Quando il rescuer accede al sistema, quest’ultimo deve permettergli di accettare una richiesta di aiuto tra quelle presenti nella lista

Quando il rescuee ritiene che la sua situazione di emergenza sia cambiata, il sistema deve permettergli di aggiornare la vecchia richiesta di aiuto dopo che sono passati N minuti

Finché la richiesta di aiuto non riceve una conferma di ricezione, il sistema deve continuare a mandare il messaggio di aiuto ogni N secondi in broadcast

Al primo accesso al sistema da parte del rescuee, il sistema deve fargli compilare un form in cui deve inserire: nome, cognome, data di nascita, gruppo sanguigno, eventuali allergie a medicinali, eventuali disabilità o malattie gravi e deve salvarlo in locale

Quando il rescuee vuole inviare una richiesta di aiuto, il sistema deve fargli compilare un form in cui inserire dettagli riguardo l’emergenza

Quando un rescuer accetta una richiesta di soccorso, il sistema deve inviare un messaggio in broadcast in cui specifica che tale richiesta di soccorso è stata accettata

I rescuee devono avere un database locale per inoltrare le richieste degli altri rescuee in modalità broadcast, ma il sistema non deve permettergli l’accesso in lettura e modifica delle altre richieste di soccorso

Se il rescuer si ritrova in una situazione di emergenza, il sistema deve garantirgli la possibilità di inviare una richiesta di aiuto

Quando ritorna la connessione, il sistema manderà i messaggi dei rescuer e rescuee al cloud

Quando ritorna la connessione, il cloud si occupa di gestire le priorità delle emergenze e comunicarle ai rescuer

non funzionale: il sistema deve dare priorità alla comunicazione bluetooth/wifi-direct

non funzionale: se non si riceve un “ACK bluetooth”, il sistema deve tentare di comunicare mediante il cloud

non funzionale: il sistema deve garantire prestazioni elevate

non funzionale: il sistema deve gestire correttamente i conflitti tra messaggi

non funzionale: il sistema deve garantire sicurezza (crittografia dei dati)

non funzionale: la chiave tra un rescuee ed un rescuer viene propagata dai vari hop (solo i rescuer l’accettano)

non funzionale: in presenza di connessione e al primo accesso, il rescuee e rescuer e il cloud scambiano dei certificati per la crittografia

Dopo il primo accesso, il sistema non deve permettere i rescuee di diventare rescuer

non funzionale: quando il sistema deve ottenere la posizione mediante gps deve provare ad usare anche il wifi per aumentare la precisione

Se il rescuer manda una richiesta di soccorso, il sistema deve impedirgli di accettare richieste di soccorso

Il sistema deve permettere la modifica dei dati inseriti nel form iniziale

Il sistema deve permettere ad un rescuee/rescuer di poter segnalare che non ha più bisogno di aiuto

X.X  Requisiti non funzionali

X.X.X Funzionalità :

| **Codice** | **Nome** | **Descrizione** | **Priorità** |
| --- | --- | --- | --- |
| **RNF_F.1** | Funzionalità
richieste | La prima release del prodotto includerà i requisiti funzionali essenziali(o prioritari) richiesti dal committente | ALTA |
| **RNF_F.2** | Priorità comunicazione | Il sistema deve dare priorità alla comunicazione Bluetooth o Wi-Fi Direct rispetto ad altri canali di trasmissione | ALTA |

X.X.X Affidabilità :

| **Codice** | **Nome** | **Descrizione** | **Autore** | **Sorgente (perché è stato individuato🧠)** | **Priorità** |
| --- | --- | --- | --- | --- | --- |
| **RNF_A.1** | Coerenza dei dati | Durante la sincronizzazione tra i nodi e il cloud, il sistema deve garantire la coerenza dei dati, privilegiando la versione più recente per evitare conflitti o duplicati |  |  | ALTA |
| **RNF_A.2** | Sicurezza credenziali e ruoli | Durante l’autenticazione e la gestione degli accessi, il sistema deve garantire che le credenziali identifichino univocamente il ruolo dell’utente e impediscano modifiche non autorizzate |  |  | ALTA |
| **RNF_A.3** | Reperibilità | In qualsiasi momento, il sistema deve essere operativo 24 ore su 24 e 7 giorni su 7, senza interruzioni di servizio |  |  | ALTA |

X.X.X Usabilità :

| **Codice** | **Nome** | **Descrizione** | **Priorità** |
| --- | --- | --- | --- |
| **RNF_U.1** | Interfaccia Univoca | Su qualsiasi dispositivo, l’interfaccia del sistema deve mantenere un aspetto e un comportamento coerente per garantire un’esperienza d’uso uniforme | MEDIA |
| **RNF_U.2** | Accessibilità visiva | Durante l’utilizzo dell’interfaccia, il sistema deve garantire un contrasto cromatico adeguato per utenti con difficoltà visive | BASSO |
| **RNF_U.3** | User-friendly | Il sistema deve essere progettato in modo che sia facilmente utilizzabile da chiunque, senza richiedere particolari competenze tecniche specifiche. | ALTA |
| **RNF_U.4** | Feedback all’utente | Dopo ogni azione eseguita dall’utente, il sistema deve fornire un feedback immediato e chiaro che indichi lo stato dell’operazione e gli eventuali problemi. | ALTA |

X.X.X Prestazioni :

| **Codice** | **Descrizione** | **Priorità** |
| --- | --- | --- |
| **RNF_P.1** | Durante l’elaborazione e l’invio dei messaggi, il sistema deve garantire una latenza minima per assicurare comunicazioni tempestive | MEDIA |
| **RNF_P.2** | All’aumentare del numero di nodi (rescuer), il sistema deve mantenere prestazioni costanti senza degradare la velocità di risposta | ALTA |
| **RNF_P.3** | Il sistema deve garantire prestazioni elevate in termini di tempi di trasmissione, elaborazione e risposta. | MEDIO |

X.X.X Sostenibilità :

| **Codice** | **Descrizione** | **Priorità** |
| --- | --- | --- |
| **RNF_S.1** | Durante lo sviluppo del software, il sistema deve essere progettato in modo da garantire almeno il 70% di codice riusabile tra i moduli | ALTA |

Pseudo-Requisiti

X.X.X Implementazione :

| **Codice** | **Nome** | **Descrizione** | **Priorità** |
| --- | --- | --- | --- |
| **PR_IM.2** | Database locale | Il sistema deve poter utilizzare un database locale installato sulla stessa macchina, senza necessità di connessione a un server esterno | ALTA |
| **PR_IM.3** | Front-end | Il front-end della piattaforma deve essere sviluppato utilizzando i linguaggi HTML, CSS e JavaScript, | ALTA |

X.X.X Interfaccia

| **Codice** | **Nome** | **Descrizione** | **Priorità** |
| --- | --- | --- | --- |
| **PR_I.1** | Integrazione cloud | Il sistema deve poter comunicare con il server cloud tramite API REST | ALTA |

X.X.X Operazione :

| **Codice** | **Nome** | **Descrizione** | **Priorità** |
| --- | --- | --- | --- |
| **PR_OP.1** | Compatibilità con Windows | Il sistema deve poter essere eseguito in locale su macchine dotate di sistema operativo Windows 10 o superiore | ALTA |
| **PR_OP.2** | Esecuzione locale | Il sistema deve poter essere eseguito in locale su una singola macchina senza la necessità di connessione a Internet o di un server remoto | ALTA |

X.X.X Packaging :

| **Codice** | **Nome** | **Descrizione** | **Priorità** |
| --- | --- | --- | --- |
| **PR_P.1** | Distribuzione | Il sistema deve poter essere consegnato come pacchetto installabile unico | ALTA |

X.X.X Legali :

| **Codice** | **Nome** | **Descrizione** | **Priorità** |
| --- | --- | --- | --- |
| **PR_L.1** | Consenso all’uso dei dati | Il sistema deve richiedere all’utente il consenso all’utilizzo dei suoi dati personali prima di memorizzarli | ALTA |

3.4 Modello del sistema

3.4.1 Scenari Utente :

**3.4.1.1 Registrazione al sistema RescueCom**

| **Identificativo**
 
**SCR_1** | **SC_Rescue_01**
 
**Autore : Marco Donatiello** |  |
| --- | --- | --- |
| **Attori** | Mario Rossi:Utente |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Mario apre per la prima volta il portale RescueCom sul proprio dispositivo |
|  | Il Sistema rileva che non esiste un profilo locale associato e propone un pop-up di scelta del tipo di ruolo (Rescuee o Rescuer ) , consiglia di compilare il form di registrazione iniziale per raccogliere le informazioni iniziali di Mario | 

 |
|  |  | Mario conferma il ruolo di Rescuee del sistema e compila il form inserendo i propri dati anagrafici e sanitari: nome, cognome, data di nascita, gruppo sanguigno, allergie a medicinali, disabilità o patologie rilevanti. |
|  | Il Sistema esegue la validazione dei campi (formato, campi obbligatori, dati coerenti). |  |
|  |  | Mario conferma l’inserimento dei dati,cliccando sul bottone “conferma dati”. |
|  | Il Sistema salva le informazioni in un database locale |  |
|  | Il Sistema mostra un messaggio di conferma della registrazione e abilita le funzionalità principali del Rescuee salvando le informazioni come header per il messaggio di soccorso |  |

**3.4.1.2 Richiesta di soccorso in assenza della connessione internet**

| **Identificativo**
 
**SRC_2** | **SC_Rescue_01**
 
**Autore : Marco Donatiello** |  |
| --- | --- | --- |
| **Attori** | Antonio Cassano:Utente |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Antonio apre il portale RescueCom con  l’intento di richiedere soccorso |
|  | Il Sistema verifica la presenza di dati relativi all’utente e propone all’utente di compilare il form di soccorso ,nascondendo i campi non necessari se precedentemente compilati | 

 |
|  |  | Antonio inserisce tutti i dati richiesti dal sistema (dati personali e dati di emergenza) e conferma l’invio della richiesta di soccorso. |
|  | Il Sistema valida i campi del form e cerca di stabilire una connessione con il sistema cloud gestito dai  Rescuer |  |
|  | Il Sistema rileva che non è presente una connessione ad internet , salva la richiesta localmente sul dispositivo. |  |
|  | Il Sistema mostra un messaggio di conferma all’utente: “La richiesta è stata salvata correttamente e, in assenza di connessione Internet, sarà trasmessa ai rescuer vicini tramite rete P2P locale. In caso di ripristino della connessione, verrà inviata automaticamente al server centrale. |  |
|  | Il Sistema propone a Mario una serie di buone norma da seguire in caso di emergenza |  |
|  |  |  |

**3.4.1.3 Richiesta di soccorso in presenza della connessione internet**

| **Identificativo**
**SCR_3** | **SC_Rescue_01**
 
Autore : Marco Donatiello |  |  |
| --- | --- | --- | --- |
| **Attori** | Steve Jobs :Utente 
 |  | Mark Zuckerberg : Rescuer |
| **Flusso di eventi** | **Sistema**
 | **Attore** | **Attore** 
**Secondario** |
|  |  | Steve vuole inviare una richiesta di soccorso ed apre il sistema RescueCom |  |
|  | Il Sistema verifica la presenza di dati relativi all’utente e propone a Steve di compilare il form di soccorso ,nascondendo i campi non necessari se precedentemente compilati | 

 |  |
|  |  | Steve inserisce tutti i dati richiesti dal sistema e conferma l’invio della richiesta di soccorso. |  |
|  | Il Sistema valida i campi del form e cerca di stabilire una connessione con il sistema cloud gestito dai  Rescuer |  |  |
|  | Il Sistema rileva la presente una connessione ad internet e trasferisce il messaggio al pannello di controllo dei Rescuer |  |  |
|  |  |  | Mark riceve la richiesta di soccorso , analizza l’emergenza e  contatta le autorità preposte alla risoluzione del problema |
|  | Il Sistema, in base alla priorità calcolata automaticamente tramite euristiche, notifica a Steve il tempo stimato di arrivo dei soccorsi. |  |  |
|  | Il Sistema propone a Steve una serie di buone norma da seguire in caso di emergenza |  |  |

**3.4.1.4 Il rescuee/rescuer modifica una sua richiesta di soccorso**

autore: Latino Francesca Pia

| **Identificativo** | **SC_Rescue_04**
 |  |
| --- | --- | --- |
| **Attori** | Mario Rossi:Utente |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Mario apre il portale RescueCom sul proprio dispositivo |
|  | Il Sistema mostra l’elenco delle richieste di soccorso effettuate dall’utente | 

 |
|  |  | L’utente seleziona la richiesta che desidera modificare dal proprio elenco |
|  | il sistema verifica i permessi, e mostra il form per modificare la richiesta |  |
|  |  | L’utente aggiorna le informazioni |
|  | Il sistema valida i nuovi dati |  |
|  | Il Sistema salva le informazioni in un database locale |  |
|  | Il Sistema invia la modifica al cloud server in caso di connessione, altrimenti la modifica viene propagata ai dispositivi vicini. |  |
|  | Il sistema invia una conferma di aggiornamento all’utente |  |

**3.4.1.5 Un rescuer accetta una richiesta di soccorso**

autore: Latino Francesca Pia

| **Identificativo** | **SC_Rescue_05**
 |  |
| --- | --- | --- |
| **Attori** | Mario Rossi:Utente
 |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Mario Rossi apre l’app e accede alle richieste di aiuto |
|  | il sistema carica le richieste di aiuto e le mostra |  |
|  |  | il rescuer seleziona una richiesta da accettare |
|  | il sistema aggiorna localmente lo stato della richiesta |  |
|  | invia un messaggio ai dispositivi vicini per indicare che la richiesta è già stata accettata |  |
|  | lo stato della richiesta viene aggiornato nel database centrale |  |

**3.4.1.6 Due o più rescuer accettano contemporaneamente una richiesta di soccorso**

Autore: Altieri Vito

| **Identificativo** | **SC_Rescue_06**
 |  |
| --- | --- | --- |
| **Attori** | Guido Mista:Utente
Leone Abbacchio:Utente
 
 |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Guido e Leone ricevono la richiesta di un Rescuee, accettandola entrambi. |
|  | Il sistema mostra al Rescuee un singolo acknowledgement di accettazione richiesta (tramite un'euristica basata su vicinanza, timestamp, etc.), assumiamo sia quella di Guido. |  |
|  | Il sistema risponde a Guido dicendo che il Rescuee ha accettato la sua richiesta, e a Leone che un altro Rescuer ha già accettato la richiesta. |  |

**3.4.1.7 Un rescuee riceve una richiesta inoltrata da un altro rescuee**

Autore: Francesco Moccaldi

| **Identificativo** | **SC_Rescue_07**
 |  |
| --- | --- | --- |
| **Attori** | Alice: Utente
Bob: Utente |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Alice riceve una richiesta di soccorso di un altro utente |
|  | Il sistema inoltra la richiesta di soccorso ad altri utenti |  |
|  |  | Bob riceve la richiesta di soccorso ma se è un rescuee non può leggerla o modificarla |
|  | Il sistema salva la richiesta inoltrata da Alice sul database locale |  |
|  | Il sistema inoltra la richiesta di soccorso inoltrata da Alice ad altri utenti |  |

**3.4.1.8 Il rescue/rescuer segnala di non aver più bisogno di aiuto**

Autore: Francesco Moccaldi

| **Identificativo** | **SC_Rescue_08**
 |  |
| --- | --- | --- |
| **Attori** | Alice: Utente |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Alice dopo aver mandato una richiesta di soccorso, constata che non ha più bisogno di aiuto e lo segnala |
|  | Il sistema segnala  (mediante internet se c’è connessione, altrimenti mediante p2p) agli altri utenti che Alice non ha più bisogno di aiuto |  |
|  | Se Alice è una Rescuer, il sistema ripristina la possibilità di accettare richieste di soccorso |  |

**3.4.1.9 Utenti si collegano al cloud per la sincronizzazione quando torna la connessione**

autore: Latino Francesca Pia

| **Identificativo** | **SC_Rescue_05**
 |  |
| --- | --- | --- |
| **Attori** | Mario Rossi:Utente
 |  |
| **Flusso di eventi** | **Sistema**
 | **Cloud** |
|  | il sistema monitora periodicamente lo stato della rete |  |
|  | quando rileva il ritorno della connessione ad internet recupera tutti i dati non sincronizzati dal database locale |  |
|  | il sistema invia i dati locali al cloud |  |
|  |  | avviene la sincronizzazione |

**3.4.1.10 Inoltrare le richieste di soccorso ai rescuer in assenza di internet (hop P2P)**

Autore: Vittorio Landi

| **Identificativo** | **SC_Rescue_10**
 |  |
| --- | --- | --- |
| **Attori** | Gino Sorbillo:Utente |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Gino tenta di inviare una richiesta di soccorso ma non dispone di connessione internet |
|  | Il sistema rileva l’assenza di rete e attiva la modalità *Offline* (Bluetooth/Wi-Fi Direct) | 

 |
|  |  | Gino conferma l’invio della richiesta |
|  | ll sistema crea un pacchetto dati contenente: ID utente, posizione, priorità, timestamp e messaggio di emergenza |  |
|  | I dispositivi nelle vicinanze ricevono la richiesta |  |
|  | Il sistema verifica la distanza GPS e propaga il messaggio in broadcast a tutti i nodi vicini |  |
|  | Ogni Rescuee intermedio riceve la richiesta e la ritrasmette |  |
|  |  | Un Rescuer riceve la richiesta di soccorso di Gino |
|  | Il sistema salva la richiesta nel database locale e inoltra il messaggio fino a raggiungere un rescuer disponibile |  |

**3.4.1.11 Il cloud inoltra le richieste di soccorso ai rescuer in presenza di internet (hop P2P)**

Autore: Vittorio Landi

| **Identificativo** | **SC_Rescue_11**
 |  |
| --- | --- | --- |
| **Attori** | Enrico Porzio:Utente |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Enrico tenta di inviare una richiesta di soccorso connesso a internet |
|  | ll sistema rileva la connessione e instrada la richiesta al server cloud |  |
|  | Il Cloud riceve la richiesta, la salva nel database con un id univoco e ne valuta la priorità analizzando i metadati |  |
|  |  | Un dispositivo riceve la richiesta di soccorso di Enrico |
|  | Il sistema aggiorna lo stato della richiesta su “inoltrata” e attende conferme |  |
|  |  | Uno o più dispositivi accettano la richiesta di Enrico |
|  | Il sistema invia conferma al cloud e al rescuee con i dettagli del primo rescuer assegnato |  |

**3.4.1.12 Il rescuer segnala che una richiesta di soccorso è stata risolta**

Autore: Vittorio Landi

| **Identificativo** | **SC_Rescue_12**
 |  |
| --- | --- | --- |
| **Attori** | Vincenzo Capuano:Utente |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Vincenzo apre il portale RescueCom e seleziona una richiesta attiva |
|  | Il sistema mostra i dettagli della richiesta (ID,utente, posizione, stato) | 

 |
|  |  | Vincenzo segnala che la richiesta è stata risolta |
|  | il sistema chiede conferma e aggiorna lo stato della richiesta a “risolta” e salva la richiesta nel database locale |  |
|  | In presenza di connessione, il sistema  sincronizza immediatamente con il cloud |  |
|  | Il Cloud riceve la segnalazione e aggiorna la dashboard globale e invia la notifica di “risoluzione” al rescuee di Vincenzo |  |
|  |  | I’utente riceve la notifica di risoluzione |
|  | Il sistema archivia la richiesta nel log storico e la rimuove dall’elenco attivo di Vincenzo |  |

**3.4.1.13 Il rescuee riceve una conferma che la sua richiesta di soccorso è stata accettata**

Autore: Matteo Cavaliere

| **Identificativo** | **SC_Rescue_13**|  |
| --- | --- | --- |
| **Attori** | Pasquale:Utente |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Pasquale ha precedentemente inviato una richiesta di soccorso tramite l'app RescueCom dopo un incidente in montagna. |
|  | Il Sistema riceve dal cloud (o tramite rete mesh bluetooth/wifi-direct) un messaggio di conferma indicante che un rescuer ha accettato la richiesta di soccorso. | |
|  | Il Sistema interrompe l'invio in broadcast della richiesta di aiuto. |  |
|  | Il Sistema mostra a Pasquale una notifica push sullo schermo del dispositivo con il messaggio: "La tua richiesta è stata accettata! Un soccorritore sta arrivando." |  |
|  |  | Pasquale tocca la notifica per aprire l'applicazione. |
|  | Il Sistema visualizza nella schermata principale un banner verde con l'icona di conferma e il testo: "Soccorso in arrivo - Richiesta accettata alle 14:32". |  |
|  | Il Sistema mostra a Pasquale i dettagli del rescuer (nome, tempo stimato di arrivo, eventuale messaggio). |  |
|  |  | Pasquale si sente rassicurato vedendo la conferma e attende i soccorsi. |

**3.4.1.14 Il cloud gestisce i conflitti nelle richieste**

Autore: Altieri Vito

| **Identificativo** | **SC_Rescue_06**
 |  |
| --- | --- | --- |
| **Attori** | Dario Brando:Utente
 
 |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Dario invia più richieste di soccorso, alcune delle quali intese come modifiche di altre (ma senza aver usato la funzionalità di modifica) o duplicati di richieste fatte in precedenza. |
|  | Il sistema (Cloud) sceglie: in caso di duplicati di mantenere la versione nuova, in caso di modifica (determinata da un'euristica basata su similarità della richiesta e vicinanza temporale) di mantenere la versione nuova. |  |

**3.4.1.15 Il rescuer riceve una richiesta di soccorso**

Autore: Matteo Cavaliere

| **Identificativo** | **SC_Rescue_15**
 |  |
| --- | --- | --- |
| **Attori** | Peppe:Utente |  |
| **Flusso di eventi** | **Sistema**
 | **Attore** |
|  |  | Peppe ha l'applicazione RescueCom aperta mentre si trova in servizio nella sua zona. |
|  | Il Sistema riceve tramite la rete mesh bluetooth/wifi-direct (o dal cloud se connesso) una nuova richiesta di soccorso inviata da un rescuee nelle vicinanze. | 

 |
|  | Il Sistema salva la richiesta nel database locale di Peppe. |  |
|  | Il Sistema mostra una notifica push sullo schermo: "Nuova richiesta di soccorso a 2.3 km - Priorità ALTA". |  |
|  |  | Peppe tocca la notifica per visualizzare i dettagli. |
|  | Il Sistema apre la schermata "Dettagli Emergenza" mostrando: Nome del rescuee, Tipo di emergenza, Posizione, Descrizione, Dati medici, Timestamp, Priorità |  |
|  | Il Sistema aggiorna automaticamente la lista delle emergenze nella schermata principale, posizionando questa richiesta in cima con evidenziazione rossa. |  |
|  |  | Peppe legge attentamente i dettagli dell'emergenza. |
|  |  | Peppe utilizza il pulsante "Visualizza su mappa" nell'interfaccia. |
|  | Il Sistema apre una mappa che mostra la posizione segnalata dal rescuee. |  |
|  |  | Peppe valuta la distanza e la gravità della situazione. |
|  |  | Peppe tocca il pulsante verde "Accetta richiesta" nella parte inferiore dello schermo. |
|  | Il Sistema invia un messaggio di conferma verso il rescuee (tramite rete mesh o cloud). |  |
|  | Il Sistema mostra a Peppe una schermata con informazioni sull'emergenza. |  |

**3.4.1.16 Il sistema mantiene un log degli errori**

Autore: Mirko Strianese

| **Identificativo**
 
**Attori** | **SC_SYSTEM_01** |  |
| --- | --- | --- |
|  | Mario Rossi: Rescuer |  |
| **Flusso di eventi** | **Sistema** | **Attore** |
|  |  | Il Sistema (Componente UI) riceve l'input e invoca il (Componente Network) per comunicare l'accettazione al server Cloud. |
|  | Il dispositivo di Mario perde improvvisamente la connessione. Il tentativo di chiamata API al server fallisce |  |
|  | Il sistema intercetta l'eccezione |  |
|  | Il Sistema viene invocato per registrare l'anomalia. |  |
|  | Il Sistema formatta un messaggio di log dettagliato. |  |
|  | Il Sistema scrive il messaggio nel file di log locale (errors.log) |  |
|  | Il Sistema (Componente UI) mostra un messaggio di errore chiaro a Mario. |  |
|  | L'errore è stato registrato con successo nel log, senza causare un crash dell'applicazione, e l'utente è stato informato. |  |

**3.4.1.17 Il sistema mantiene un log degli eventi**

Autore: Mirko Strianese

| **Identificativo**
 
**Attori** | **SC_SYSTEM_01** |  |
| --- | --- | --- |
|  | Mario Rossi: Rescuee
Giulia verdi: Rescuer |  |
| **Flusso di eventi** | **Sistema** | **Attore** |
|  |  | Mario invia una richiesta di soccorso |
|  | Il Sistema riceve l'input e la inoltra |  |
|  | Il sistema riceve l’evento di invio e lo registra immediatamente |  |
|  | Il sistema riceve il report e lo mostra sull’interfaccia di Giulia (es. nuova richiesta) |  |
|  |  | Giulia visualizza i dettagli dell’emergenza e l’accetta |
|  | Il sistema riceve l’evento di accettazione e lo registra |  |
|  | Il sistema invia una notifica a Mario della richiesta accettata |  |
|  | Il sistema recupera i timestamp associati alla richiesta |  |
|  | Il sistema aggiorna lo stato del report in “Accettato” specificando anche in quanto tempo |  |

3.4.2 Modello dei Casi d’Uso

**3.4.2.1 Lato Utente : Richiesta di soccorso in assenza della connessione internet**

| **Identificativo** | UC_Rescue_01 | **Data** | 11/11/2025 |
| --- | --- | --- | --- |
|  |  | **Versione** | 1.0.0 |
|  |  | **Autore** | Donatiello Marco |
| **Nome** | Richiesta di soccorso in assenza della connessione internet
 | **Attore Principale** | **Attore Secondario** |
|  |  | **Rescuee**
 
Il Rescuee è l’utente finale del sistema RescueCom che può trovarsi in una situazione di emergenza e ha bisogno di richiedere assistenza immediata. | Na |
| **Descrizione** |  | Il caso d’uso **“Richiesta di soccorso in assenza di connessione Internet”** descrive come un Rescuee possa inviare una richiesta di aiuto anche quando il dispositivo non è connesso a Internet. Il sistema RescueCom rileva l’assenza di connessione e guida l’utente nell’inserimento dei dati necessari per la richiesta di soccorso, garantendo che le informazioni vengano salvate localmente in modo sicuro. Il Rescuee fornisce le proprie informazioni personali e mediche, necessarie per l’intervento dei soccorritori (Rescuer), confermando l’invio della richiesta. Il sistema gestisce automaticamente la memorizzazione temporanea dei dati, notifica all’utente lo stato della richiesta e provvede a inviarla al sistema cloud dei Rescuer non appena la connessione a Internet viene ristabilita.
 |  |
| **Entry Condition** |  | Questo caso d'uso inizia quando il rescuee si trova in una situazione di emergenza e ha bisogno di aiuto immediato. Il rescuee apre il sistema RescueCom e seleziona l’opzione per inviare una richiesta di soccorso.
 |  |
| **Exit condition**
                       **On success** |  | Questo caso d’uso termina quando la richiesta di soccorso è salvata correttamente nel database locale. Il Sistema notifica all’utente l’avvenuto salvataggio e, in assenza di connessione Internet, tenta la trasmissione tramite rete P2P locale verso altri dispositivi (Rescuee o Rescuer) nelle vicinanze. La richiesta verrà inviata automaticamente al cloud centrale non appena raggiunge un nodo connesso o al ripristino della connessione Internet |  |
| **Exit condition** 
                       **On failure** |  | Questo caso d'uso termina quando la richiesta non è salvata a causa di un errore interno (database, dispositivo, ecc.).
L’utente riceve un messaggio di errore e può ripetere l’invio della richiesta
 |  |
| **Rilevanza/User Priority** |  | **Alta** – La funzionalità è critica per la sicurezza dell’utente in situazioni di emergenza. |  |
| **Frequenza stimata** |  | **Alta** – Si verifica ogni volta che l’utente tenta di inviare una richiesta di soccorso senza connessione Internet |  |
| **Extension point** | NA | **Generalization of** | NA |
| **Flusso degli eventi** |  |  |  |
| **1** | Rescuee | Il Rescuee apre il sistema RescueCom e seleziona l’opzione per inviare una richiesta di soccorso. |  |
| **2** | Sistema | Il sistema rileva l’assenza di connessione Internet e informa l’utente che la richiesta sarà salvata localmente e inviata automaticamente al ripristino della connessione. 
 |  |
| **3** | Rescuee | Il Rescuee inserisce i dati necessari per la richiesta di soccorso, come dati personali ,  informazioni mediche , descrizione dell’emergenza. |  |
| **4** | Sistema | Il Sistema convalida i dati inseriti (campi completi, formati corretti) |  |
| **5** | Rescuee | Il Rescuee conferma l’inserimento dei dati cliccando su “Invia soccorso”. |  |
| **6** | Sistema | Il Sistema salva i dati localmente nel database cifrato e mostra un messaggio di conferma della registrazione |  |
| **7** | Sistema | Il Sistema tenta di inoltrare la richiesta di soccorso ai dispositivi RescueCom vicini, cercando di raggiungere almeno uno con connessione Internet, in modo da trasmettere infine il messaggio al sistema dei Rescuer. |  |
| 1. **Flusso Alternativo : (Speech-to-Text) - Operazioni 3-5** |  |  |  |
| **Condizione :** |  | Il Rescuee ha difficoltà a digitare o preferisce usare la voce per compilare il form di registrazione. |  |
| **1.1** | Rescuee | Il Rescuee seleziona l’opzione “Inserimento vocale” nella schermata di registrazione |  |
| **1.2** | Sistema | Il sistema attiva il microfono e guida l’utente nella pronuncia dei dati richiesti |  |
| **1.3** | Rescuee | Il Rescuee conferma l’inserimento dei dati cliccando su “Registrati” |  |
| **0.                       Flusso di errore : Fallimento del salvataggio dati (deriva da passo 6)** |  |  |  |
| **2.e1** | Sistema | Il sistema comunica al Rescuee che si è verificato un errore interno |  |
| **2.e2** | Sistema | La registrazione termina con un errore e senza essere salvata |  |
| **Note** | NA | **Special Requirements** | La connessione Internet non è disponibile. |

**3.4.2.4 Lato Utente :    Il rescuee/rescuer modifica una sua richiesta di soccorso**

| **Identificativo** | UC_Rescue_04 | **Data** | 10/11/2025 |
| --- | --- | --- | --- |
|  |  | **Versione** | 1.0.0 |
|  |  | **Autore** | Latino Francesca Pia |
| **Nome** | modifica della richiesta di soccorso da parte del rescuee/rescuer | **Attore Principale** | **Attore Secondario** |
|  |  | **Rescuee/Rescuer**
 
Interessato a modificare una richiesta di soccorso precedentemente inviata | Na |
| **Descrizione** |  | Il Rescuee/rescuer, dopo aver aperto il sistema, vuole modificare una richiesta di soccorso precedentemente inviata. |  |
| **Entry Condition** |  | Il Rescuee/rescuer accede al sistema. 
Il Rescuee/rescuer ha già inviato una richiesta di soccorso.
Sono trascorsi N minuti dall’ultimo invio o aggiornamento. |  |
| **Exit condition**
                       **On success** |  | I dati del Rescuee/rescuer vengono aggiornati correttamente |  |
| **Exit condition** 
                       **On failure** |  | La modifica non avviene a causa di errori nel formato dati inserito o problemi di connessione al database locale . L’utente è invitato a correggere gli errori o riprovare più tardi. |  |
| **Rilevanza/User Priority** |  | **Alta** |  |
| **Frequenza stimata** |  | Bassa |  |
| **Extension point** | N/A | **Generalization of** | gestione richieste soccorso |
| **Flusso degli eventi** |  |  |  |
| **1** | Rescuee/rescuer | Il Rescuee/rescuer apre il sistema  del RescueCom. |  |
| **2** | Sistema | il sistema mostra l’elenco delle richieste di soccorso precedentemente inviate dall’utente |  |
| **3** | Rescuee/rescuer | L’utente selezione la richiesta che desidera modificare dal proprio elenco |  |
| **4** | Sistema | il sistema verifica i permessi e mostra il form per modificare la richiesta |  |
| **5** | Rescuee/rescuer | L’utente aggiorna la propria richiesta con i nuovi dati |  |
| **6** | Sistema | Il Sistema valida i dati e li salva localmente nel database. Di seguito un messaggio di conferma viene inviato all’utente |  |
| 1. **Flusso Alternativo: NA (operazione di delete non permessa)** |  |  |  |
| **0.                       Flusso di errore : Il sistema non riesce a salvare l’aggiornamento dei dati** |  |  |  |
| **2.e1** | Sistema | Il sistema comunica al Rescuee che si è verificato un errore interno |  |
| **2.e2** | Sistema | La modifica termina con un errore e senza essere salvata |  |
| **Note** | NA | **Special Requirements** | NA |

**3.4.2.5 Lato Utente : Un rescuer accetta una richiesta di soccorso**

| **Identificativo** | UC_Rescue_05 | **Data** | 11/11/2025 |
| --- | --- | --- | --- |
|  |  | **Versione** | 1.0.0 |
|  |  | **Autore** | Latino Francesca Pia |
| **Nome** | un rescuer accetta una nuova richiesta di soccorso | **Attore Principale** | **Attore Secondario** |
|  |  | **Rescuer**
 
Accetta la richiesta di soccorso ricevuta | Na |
| **Descrizione** |  | Il rescuer, dopo aver aperto il sistema, accetta la richiesta di soccorso dall’elenco delle richieste |  |
| **Entry Condition** |  | Il rescuer accede al sistema. 
il rescuer è autenticato e autorizzato per visualizzare le richieste di soccorso.
 |  |
| **Exit condition**
                       **On success** |  | lo stato della richiesta è “accettata”. Il rescuee riceve la notifica che la sua richiesta è stata presa in carico. |  |
| **Exit condition** 
                       **On failure** |  | se la richiesta è stata già presa in carico da un altro rescuer, , il rescuer riceve un messaggio di errore. |  |
| **Rilevanza/User Priority** |  | **Alta** |  |
| **Frequenza stimata** |  | Alta |  |
| **Extension point** | NA | **Generalization of** | gestione richieste soccorso |
| **Flusso degli eventi** |  |  |  |
| **1** | Rescuer | Il rescuer accede al sistema |  |
| **2** | Sistema | Recupera e mostra le richieste di soccorso disponibili |  |
| **3** | Rescuer | seleziona una richiesta di soccorso e l’accetta |  |
| **4** | Sistema | cambia lo stato della richiesta in “accettata”. Invia una notifica al rescuer per notificare che la sua richiesta è stata presa in carico |  |
| **0.                       Flusso Alternativo: NA** |  |  |  |
|  |  |  |  |
| **0.                       Flusso di errore : Errore nell’accettazione della richiesta di soccorso** |  |  |  |
| **2.e1** | Sistema | Il sistema comunica al Rescuer che si è verificato un errore interno |  |
| **Note** | NA | **Special Requirements** | NA |

**3.4.2.6 Lato Utente:** **Due o più rescuer accettano contemporaneamente una richiesta di soccorso**

|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  | **Autore** | Altieri Vito |
| **Nome** | 
Gestione race condition su accettazione contemporanea di una richiesta di soccorso da parte di più di un Rescuer. | **Attore Principale** | **Attore Secondario** |
|  |  |  |  |
|  |  |  |  |
|  |  | •  |  |
|  |  |  |  |
|  |  | •  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
| **Note** | N/A | **Special Requirements** | N/A |

**v**

**3.4.2.9 Lato Utente:** **Utenti si collegano al cloud per la sincronizzazione quando torna la connessione**

autore: Latino Francesca Pia

| **Identificativo** | UC_Rescue_09 | **Data** | 11/11/2025 |
| --- | --- | --- | --- |
|  |  | **Versione** | 1.0.0 |
|  |  | **Autore** | Latino Francesca Pia |
| **Nome** | gli utenti si collegano al cloud per la sincronizzazione quando ritorna la connessione | **Attore Principale** | **Attore Secondario** |
|  |  | **Rescuer/rescuee** | Na |
| **Descrizione** |  | al ritorno della connessione ad internet i differenti utenti si collegano al cloud per la sincronizzione |  |
| **Entry Condition** |  | il dispositivo dell’utente è stato offline
esistono dati non sincronizzati nel database locale
la connessione ad internet torna disponibile |  |
| **Exit condition**
                       **On success** |  | tutti i dati locali sono sincronizzati con il cloud.
gli stati delle richieste di soccorso risultano coerenti tra dispositivi e cloud |  |
| **Exit condition** 
                       **On failure** |  | alcuni dati restano in attesa di sincronizzazione
verrà tentata una nuova sincronizzazione al prossimo controllo di rete |  |
| **Rilevanza/User Priority** |  | **Alta** |  |
| **Frequenza stimata** |  | media |  |
| **Extension point** | Gestione conflitti di sincronizzazione | **Generalization of** | Sincronizzazione dati con il cloud |
| **Flusso degli eventi** |  |  |  |
| **1** | Sistema locale | Monitora periodicamente lo stato della rete |  |
| **2** | Sistema locale | Rileva che la connessione è nuovamente disponibile |  |
| **3** | Sistema locale | Identifica i dati non sincronizzati nel database locale |  |
| **4** | Sistema locale -> cloud | Invia i dati non sincronizzati al clou |  |
| **5** | cloud | confronta le versioni dei dati e gestisce i conflitti |  |
| **6** | cloud -> sistema locale | invia conferma di sincronizzazione completata e aggiorna lo stato dei dati |  |
| **7** | sistema locale | aggiorna il database locale e notifica l’utente che la sincronizzazione è avvenuta con successo |  |
| **0.                       Flusso Alternativo:NA** |  |  |  |
|  |  |  |  |
| **0.                       Flusso di errore : Errore nella sincronizzazione del cloud** |  |  |  |
| **2.e1** | Sistema | Il sistema salva un log dell’errore e riprova la sincronizzazione dopo N minuti |  |
| **Note** | la sincronizzazione avviene in background senza richiedere l’intervento dell’utente.
l’utente viene notificato in caso di errori/conflitti | **Special Requirements** | le comunicazioni tra cloud e client devono avvenire tramite connessione sicura |

**3.4.2.10 Lato Utente : Il rescuee invia una richiesta di soccorso in un contesto privo di connessione internet.**

| **Identificativo** | UC_Rescue_10 | **Data** | 12/11/2025 |
| --- | --- | --- | --- |
|  |  | **Versione** | 1.0.0 |
|  |  | **Autore** | Landi Vittorio |
| **Nome** | 
Inoltro richiesta di soccorso ai rescuer in assenza di connessione internet (hop P2P) | **Attore Principale** | **Attore Secondario** |
|  |  | **Rescuee/Rescuer**
 
Interessato a inviare una richiesta di soccorso | Rescuer, Rescuee intermedio (ripetitore) |
| **Descrizione** |  | Il Rescuee, dopo aver aperto il sistema, invia una richiesta di soccorso in un contesto privo di connessione internet.
Il sistema, riconosciuta l’assenza di rete, attiva la modalità *Offline* e utilizza la comunicazione **Bluetooth/Wi-Fi Direct** per inoltrare la richiesta in modalità *peer-to-peer (P2P)*.
I dispositivi Rescuee o Rescuer nelle vicinanze fungono da ripetitori (*hop*) fino al raggiungimento di un rescuer disponibile. |  |
| **Entry Condition** |  | • Il Rescuee/rescuer accede al sistema. 
• Non è disponibile connessione a internet
• Il modulo Bluetooth/Wi-Fi Direct è attivo sul dispositivo. |  |
| **Exit condition**
                       **On success** |  | La richiesta viene inoltrata con successo a uno o più dispositivi vicini e raggiunge almeno un rescuer. |  |
| **Exit condition** 
                       **On failure** |  | La richiesta non viene inoltrata a causa di assenza di nodi nelle vicinanze o errori di trasmissione. Il sistema salva i dati localmente e tenta un nuovo invio automatico al ripristino della connessione oppure al rilevamento di un utente nelle vicinanze |  |
| **Rilevanza/User Priority** |  | **Alta** |  |
| **Frequenza stimata** |  | media |  |
| **Extension point** | N/A | **Generalization of** | gestione richieste soccorso |
| **Flusso degli eventi** |  |  |  |
| **1** | Rescuee | Il Rescuee apre RescueCom. |  |
| **2** | Sistema | Verifica la disponibilità di connessione internet e rileva che non è presente. |  |
| **3** | Sistema | Attiva automaticamente la modalità *Offline* (Bluetooth/Wi-Fi Direct). |  |
| **4** | Rescuee | Compila il form di soccorso e conferma l’invio della richiesta. |  |
| **5** | Sistema | Valida i campi inseriti e crea un pacchetto dati cifrato contenente ID utente, posizione, messaggio e livello di priorità. |  |
| **6** | Sistema | Invia la richiesta in broadcast ai dispositivi nel raggio d’azione tramite Bluetooth/Wi-Fi Direct. |  |
| **7** | Rescuee/Rescuer intermedio | Riceve la richiesta, la salva nel database locale e la ritrasmette (hop) ai dispositivi vicini. |  |
| **8** | Rescuer | Riceve la richiesta, la salva nel proprio database locale e invia un messaggio di conferma in caso di accettazione della richiesta |  |
| **9** | Sistema | Mostra al Rescuee il messaggio “Richiesta inoltrata correttamente tramite rete P2P”. |  |
| **0.                       Flusso Alternativo: Nessun dispositivo nelle vicinanze** |  |  |  |
| **1.a1** | Sistema | Mostra messaggio “Nessun dispositivo trovato. La richiesta verrà inviata automaticamente al ripristino della connessione.” |  |
| **1.a2** | Sistema | Salva la richiesta nel database locale in attesa di rete. |  |
| **0.                       Flusso di errore : Il sistema non riesce a salvare l’aggiornamento dei dati** |  |  |  |
| **2.e1** | Sistema | Il modulo Bluetooth/Wi-Fi Direct non è abilitato. |  |
| **2.e2** | Sistema | Mostra messaggio “Impossibile attivare la comunicazione locale. Abilitare Bluetooth o Wi-Fi Direct e riprovare.” |  |
| **2.e3** | Sistema | Logga l’errore nel registro locale per successive analisi. |  |
| **Note** | • Ogni hop intermedio (Rescuee o Rescuer) registra nel log locale l’avvenuto inoltro.
• Il sistema mantiene traccia della catena di propagazione fino al rescuer finale per consentire auditing e tracciabilità. | **Special Requirements** | NA |

| **Identificativo** | UC_SYS_01 | **Data** | 14/11/2025 |
| --- | --- | --- | --- |
|  |  | **Versione** | 1.0.0 |
|  |  | **Autore** | Strianese Mirko |
| **Nome** | 
Consultare il log degli errori ed eventi | **Attore Principale** | **Attore Secondario** |
|  |  | **Amministratore di sistema**
 
Verificare l'attività del sistema, diagnosticare errori tecnici
 | **Sistema**
 
fornire un accesso sicuro e performante ai dati di log archiviati in modo persistente. |
| **Descrizione** |  | L'Amministratore accede a un'interfaccia di sistema riservata per consultare i log degli eventi e i log degli errori. Questo è necessario per attività di auditing, per diagnosticare problemi tecnici o per verificare i tempi di risposta. |  |
| **Entry Condition** |  | • L'Amministratore è autenticato nel pannello di amministrazione del sistema e può visualizzare i Log |  |
| **Exit condition**
                       **On success** |  | Questo caso d’uso termina quando:
1. Il Sistema ha recuperato i record di log richiesti dal Repository dei Log.
2. I log (filtrati o completi) sono stati mostrati in modo leggibile all'Amministratore.
3. L'evento di consultazione log è stato a sua volta registrato nel log. |  |
| **Exit condition** 
                       **On failure** |  | Questo caso d'uso termina quando:
• Nessun dato di log viene mostrato all'Amministratore. ad un altro Rescuer.
• l Sistema mostra un messaggio di errore chiaro all'Amministratore |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |