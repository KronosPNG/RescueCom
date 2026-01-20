# Project Charter - Progetto RescueCom

**Versione:** 1.0  
**Data:** 8 Ottobre 2025  
**Redatto da:** Luigi Turco  

---

## 1.0 Panoramica del Progetto

### 1.1 Nome del Progetto
**RescueCom** - Sistema di Comunicazione di Emergenza Resiliente

### 1.2 Sponsor del Progetto
Dipartimento della Protezione Civile

### 1.3 Project Manager
Luigi Turco

### 1.4 Data di Inizio e Fine Prevista
- **Inizio:** Ottobre 2025
- **Fine:** Gennaio 2026
- **Durata:** 3,5 mesi

---

## 2.0 Scopo del Progetto

### 2.1 Background
RescueCom nasce come iniziativa per sviluppare un sistema di comunicazione di emergenza resiliente in scenari di disastro o mancanza di connettività Internet. In tali contesti, le infrastrutture di rete tradizionali risultano spesso inaccessibili, rendendo impossibile il coordinamento tempestivo dei soccorsi e la richiesta di aiuto da parte delle vittime.

Il progetto mira a fornire un sistema di comunicazione decentralizzato basato su Bluetooth e Wi-Fi Direct, in grado di permettere lo scambio di messaggi di emergenza anche in assenza di rete Internet. Una volta ristabilita la connettività, il sistema sincronizza automaticamente i dati con un server cloud centrale, rendendo accessibili i messaggi ai centri di soccorso e alle autorità competenti.

### 2.2 Obiettivi del Progetto

#### Obiettivi di Business
1. Migliorare la resilienza delle comunicazioni di emergenza
2. Ridurre la dipendenza da infrastrutture centralizzate durante situazioni critiche
3. Ridurre i tempi di risposta dei soccorsi in situazioni dove le reti tradizionali falliscono
4. Dimostrare un modello di comunicazione resiliente e decentralizzato replicabile

#### Obiettivi Tecnici
1. Consentire la trasmissione di messaggi di emergenza tra utenti e soccorritori anche in assenza di Internet
2. Creare una rete peer-to-peer dinamica che si auto-organizza e si adatta al contesto operativo
3. Fornire un'architettura scalabile e interoperabile con infrastrutture cloud esistenti
4. Implementare un proof of concept funzionante sulla piattaforma Windows

### 2.3 Dichiarazione dello Scopo (Scope Statement)
Il progetto RescueCom colma le lacune critiche di comunicazione durante situazioni di emergenza in cui le infrastrutture Internet tradizionali risultano non disponibili. Il sistema consente comunicazioni di emergenza attraverso Bluetooth e Wi-Fi Direct, con sincronizzazione automatica al cloud quando la connettività viene ripristinata.

---

## 3.0 Caratteristiche e Requisiti Principali

### 3.1 Capacità di Comunicazione Offline
- Trasmissione di messaggi tra dispositivi Rescuee (persone in difficoltà) e Rescuer (soccorritori)
- Utilizzo di Bluetooth e Wi-Fi Direct quando la connettività Internet non è disponibile
- Memorizzazione locale dei messaggi con sincronizzazione cloud automatica

### 3.2 Funzionalità di Relay
- Tutti i dispositivi funzionano come nodi relay
- Inoltro messaggi di emergenza per estendere la portata della rete
- Prevenzione della duplicazione dei messaggi
- Instradamento efficiente

### 3.3 Tipologie di Messaggi di Emergenza
- Supporto richieste di aiuto da parte degli utenti
- Messaggi con timestamp, ID mittente e livello di priorità
- Determinazione posizione tramite prossimità ai dispositivi Rescuer

### 3.4 Persistenza Dati Locale
- Database locale su ogni dispositivo
- Memorizzazione messaggi inviati e ricevuti
- Disponibilità dati durante periodi offline

### 3.5 Sincronizzazione Cloud
- Sincronizzazione automatica quando disponibile connettività Internet
- Gestione risoluzione conflitti per messaggi duplicati o modificati
- Algoritmi basati su data e ID dispositivo

### 3.6 API REST
- API REST completa per comunicazione dispositivi
- Supporto connessioni HTTPS sicure
- Funzionalità di invio, recupero e aggiornamento stato messaggi

### 3.7 Interfacce Utente
**Interfaccia Rescuee:**
- Desktop semplice e intuitivo
- Template messaggi predefiniti
- Attivazione rapida SOS

**Interfaccia Rescuer:**
- Gestione coda messaggi
- Strumenti di prioritizzazione
- Capacità di risposta alle emergenze

### 3.8 Sicurezza e Autenticazione
- Dispositivi Rescuee: accesso immediato senza autenticazione (emergenze)
- Dispositivi Rescuer: validazione e autorizzazione dal sistema

### 3.9 Scoperta Dispositivi e Gestione Rete
- Scoperta automatica dispositivi nelle vicinanze
- Scansione Bluetooth/Wi-Fi Direct a intervalli regolari
- Topologia di rete dinamica e adattiva

### 3.10 Supporto Piattaforma
- Proof of concept per piattaforma Windows
- Architettura progettata per futuri porting (Linux, macOS, mobile)

---

## 4.0 Deliverable del Progetto

### 4.1 Deliverable Relativi alla Gestione del Progetto
- Business Case
- Project Charter
- Team Contract
- Scope Statement
- Work Breakdown Structure (WBS)
- Cronoprogramma del progetto
- Risk Management Plan
- Presentazione finale del progetto
- Relazione finale del progetto

### 4.2 Deliverable Relativi al Prodotto
- Modulo Rescuee (applicazione desktop)
- Modulo Rescuer (applicazione desktop)
- Server Cloud centrale
- Database locale (SQLite)
- API REST per sincronizzazione
- Sistema di relay multi-hop
- Documentazione tecnica completa
- Manuale utente
- Test suite e report di testing
- Codice sorgente documentato

---

## 5.0 Criteri di Successo

### 5.1 Criteri Tecnici
- Implementazione del proof-of-concept funzionante
- Infrastruttura CI/CD funzionante
- Test suite ben strutturata con copertura adeguata
- Comunicazione offline funzionante tramite Bluetooth/Wi-Fi Direct
- Sincronizzazione cloud operativa
- Sistema di relay multi-hop verificato

### 5.2 Criteri di Qualità
- Rispetto delle specifiche funzionali e non funzionali
- Codice documentato e seguente best practices
- Test superati con successo
- Interfacce utente intuitive e accessibili
- Sistema stabile e privo di bug critici

### 5.3 Criteri di Progetto
- Rispetto della timeline di 3 mesi
- Consegna di tutti i deliverable entro Gennaio 2026
- Budget non superato (€250.000 massimo)
- Soddisfazione dello sponsor
- Documentazione completa e professionale

---

## 6.0 Vincoli del Progetto

### 6.1 Vincoli Temporali
- Timeline fissa di 3 mesi dall'avvio alla consegna finale
- Scadenza finale: Gennaio 2026
- Milestone intermedie da rispettare

### 6.2 Vincoli Tecnologici
- Sviluppo limitato alla piattaforma Windows per il proof of concept
- Utilizzo di computer desktop/laptop come dispositivi
- Tecnologie limitate a Bluetooth e Wi-Fi Direct
- Nessuna dipendenza da GPS o localizzazione precisa

### 6.3 Vincoli di Risorse
- Team limitato (massimo 5 persone)
- Budget massimo di €250.000
- Risorse hardware disponibili per test limitato

### 6.4 Vincoli Normativi e di Sicurezza
- Conformità alle normative sulla privacy
- Sicurezza dei dati di emergenza
- Autorizzazioni necessarie per dispositivi Rescuer

---

## 7.0 Assunzioni del Progetto

1. Lo Sponsor fornirà feedback e validazione sui requisiti
2. Gli utenti concederanno i permessi necessari ai dispositivi (Bluetooth, Wi-Fi Direct)
3. I dispositivi utilizzati per i test saranno computer Windows con capacità Bluetooth e Wi-Fi
4. Il server cloud sarà simulato in ambiente di sviluppo locale o su infrastruttura cloud gratuita/educativa
5. I membri del team possiedono conoscenze di base nello sviluppo software e nel networking
6. Saranno disponibili computer per simulare scenari multi-dispositivo durante i test
7. Il sistema deve operare efficacemente senza connessione Internet
8. La sincronizzazione cloud avverrà solo quando la connessione Internet sarà disponibile
9. Tutti i dati scambiati devono essere accessibili solo a utenti autorizzati
10. Il sistema dovrà dimostrare la fattibilità tecnica e funzionale in ambienti simulati

---

## 8.0 Rischi Principali del Progetto

### 8.1 Rischi Tecnici (Alto Impatto)
| Rischio | Probabilità | Impatto | Rank | Mitigazione |
|---------|-------------|---------|------|-------------|
| Sottostima effort integrazione componenti | 60% | 70% | 0.420 | Analisi tempi con prototipi; pianificazione sprint |
| Stime dei test insufficienti | 50% | 80% | 0.400 | Test plan e traceability matrix dall'inizio |
| Bug critici in funzionalità core | 40% | 90% | 0.360 | Test end-to-end; test manuale su feature core |

### 8.2 Rischi Organizzativi
| Rischio | Probabilità | Impatto | Rank | Mitigazione |
|---------|-------------|---------|------|-------------|
| Requisiti ambigui/incompleti | 55% | 70% | 0.385 | Meeting settimanali; discussioni aperte |
| Scarsa comunicazione interna | 60% | 65% | 0.390 | Canale dedicato; meeting settimanali |
| Scope creep | 50% | 70% | 0.350 | Definizione baseline; posticipare non critici |

### 8.3 Rischi di Risorse Umane
| Rischio | Probabilità | Impatto | Rank | Mitigazione |
|---------|-------------|---------|------|-------------|
| Competenze tecniche insufficienti | 50% | 75% | 0.375 | Condivisione conoscenze; comunicazione aperta |
| Calo di motivazione del team | 60% | 60% | 0.360 | Task chiari; riconoscimenti; obiettivi visibili |

---

## 9.0 Budget e Risorse

### 9.1 Budget Stimato
**Budget Massimo:** €250.000

#### Investimento Iniziale (Anno 0)
- Costi setup e sviluppo: €165.000

#### Costi Operativi Annuali (Anni 1-3)
- Manutenzione e supporto: €30.000/anno

### 9.2 Analisi Finanziaria (3 anni)
- **Tasso di sconto:** 8%
- **NPV (3 anni):** €118.480,67
- **Valore attuale benefici:** €360.793,58
- **Valore attuale costi:** €242.312,91

### 9.3 Risorse Umane
- **Team Size:** Massimo 5 persone
- **Project Manager:** 1
- **Sviluppatori:** 2-3
- **Testing/QA:** 1
- **Documentazione:** Condivisa nel team

### 9.4 Risorse Tecnologiche
- Computer Windows con Bluetooth e Wi-Fi Direct
- Server per ambiente di sviluppo
- Tools di sviluppo e testing
- Piattaforme di collaborazione (GitHub, Trello, Discord)

---

## 10.0 Organizzazione del Progetto

### 10.1 Struttura del Team
- **Project Manager:** Luigi Turco
  - Coordinamento generale
  - Pianificazione e monitoraggio
  - Gestione rischi e stakeholder
  - Reporting

- **Development Team:**
  - Sviluppo moduli Rescuee/Rescuer
  - Implementazione server cloud
  - Sviluppo API REST
  - Implementazione funzionalità di relay

- **Quality Assurance:**
  - Test planning
  - Test execution
  - Bug tracking e reporting

- **Documentation:**
  - Documentazione tecnica
  - Manuali utente
  - Report di progetto

### 10.2 Stakeholder Principali
1. **Sponsor:** Dipartimento della Protezione Civile
   - Approvazione budget e scope
   - Validazione requisiti
   - Accettazione finale

2. **Project Manager:** Luigi Turco
   - Responsabilità esecuzione progetto
   - Comunicazione con sponsor
   - Gestione team

3. **Team di Sviluppo:**
   - Implementazione tecnica
   - Testing e quality assurance
   - Documentazione

4. **Utenti Finali:**
   - Rescuee (persone in difficoltà)
   - Rescuer (personale di soccorso)
   - Autorità di protezione civile

---

## 11.0 Approccio e Metodologia

### 11.1 Metodologia di Progetto
- **Approccio:** Iterativo e incrementale
- **Framework:** Elementi di metodologia Agile adattati al contesto accademico
- **Sprint Duration:** 2 settimane
- **Cerimonie:**
  - Meeting settimanali del team
  - Review intermedie
  - Retrospettive a fine fase

### 11.2 Fasi del Progetto

#### Fase 1: Analisi e Progettazione (Mese 1)
- Raccolta e analisi requisiti dettagliati
- Progettazione architetturale del sistema
- Definizione interfacce e protocolli
- Setup ambiente di sviluppo

#### Fase 2: Implementazione (Mese 2)
- Sviluppo moduli Rescuee e Rescuer
- Implementazione server cloud
- Sviluppo funzionalità di comunicazione offline
- Implementazione sistema di relay
- Integrazione componenti

#### Fase 3: Testing e Finalizzazione (Mese 3)
- Test funzionali e di integrazione
- Test in scenari simulati multi-dispositivo
- Debugging e ottimizzazioni
- Documentazione finale
- Preparazione presentazione

### 11.3 Strumenti di Gestione
- **Project Management:** Trello/Notion
- **Version Control:** GitHub
- **Communication:** Discord, Email
- **Documentation:** Markdown, Google Docs
- **Testing:** Framework appropriati per Windows

---

## 12.0 Comunicazione e Reporting

### 12.1 Piano di Comunicazione

#### Meeting Settimanali
- **Frequenza:** Settimanale
- **Durata:** 1-2 ore
- **Partecipanti:** Tutto il team
- **Agenda:**
  - Progress update
  - Identificazione blockers
  - Pianificazione attività successive
- **Output:** Verbale condiviso entro 24 ore

#### Meeting con Sponsor
- **Frequenza:** Mensile o su richiesta
- **Formato:** Presentazione progress e milestone
- **Partecipanti:** PM e rappresentanti sponsor

#### Comunicazione Giornaliera
- **Strumento:** Discord
- **Scopo:** Quick updates, domande tecniche, coordinamento

### 12.2 Reporting
- **Status Report:** Settimanale (interno team)
- **Progress Report:** Mensile (per sponsor)
- **Risk Report:** Su necessità o eventi trigger
- **Final Report:** A fine progetto

### 12.3 Documentazione
- Tutti i documenti condivisi su piattaforma comune
- Versioning dei documenti importanti
- Backup regolari
- Templates standardizzati per deliverable

---

## 13.0 Gestione delle Modifiche

### 13.1 Processo di Change Management
1. **Identificazione:** Chiunque può proporre una modifica
2. **Valutazione:** PM valuta impatto su scope, tempi, costi
3. **Approvazione:** 
   - Modifiche minori: PM
   - Modifiche maggiori: Sponsor
4. **Implementazione:** Dopo approvazione formale
5. **Documentazione:** Aggiornamento documenti di progetto

### 13.2 Criteri per Modifiche Maggiori
- Impatto su budget > 10%
- Modifica timeline > 1 settimana
- Cambiamento requisiti core
- Aggiunta/rimozione deliverable principali

---

## 14.0 Qualità e Accettazione

### 14.1 Standard di Qualità
- Codice conforme a coding standards definiti
- Documentazione completa e chiara
- Test coverage adeguata (target: >70% per componenti critici)
- Review del codice (peer review)
- Testing su scenari definiti

### 14.2 Criteri di Accettazione Finale
1. Tutti i requisiti funzionali implementati e testati
2. Documentazione completa consegnata
3. Demo funzionante del sistema
4. Bug critici risolti
5. Approvazione formale dello sponsor
6. Codice sorgente e materiali consegnati

### 14.3 Processo di Accettazione
1. **Internal Testing:** Team verifica completezza
2. **Demo Preparation:** Preparazione scenario dimostrativo
3. **Sponsor Review:** Presentazione e demo per sponsor
4. **Feedback Integration:** Correzioni se necessarie
5. **Final Sign-off:** Approvazione formale

---

## 15.0 Autorizzazioni e Approvazioni

### 15.1 Approvazione del Charter
Questo Project Charter è stato rivisto e approvato dalle seguenti parti:

| Ruolo | Nome | Firma | Data |
|-------|------|-------|------|
| Sponsor | Dipartimento Protezione Civile | _________________ | ________ |
| Project Manager | Luigi Turco | _________________ | 08/12/2025 |

### 15.2 Autorità del Project Manager
Il Project Manager ha l'autorità per:
- Allocare risorse all'interno del budget approvato
- Prendere decisioni tecniche di routine
- Approvare modifiche minori allo scope
- Gestire il team e assegnare compiti
- Escalare problemi critici allo sponsor

### 15.3 Escalation
Questioni che richiedono escalation allo sponsor:
- Superamento budget > 10%
- Ritardi > 1 settimana sulla timeline
- Modifiche significative ai requisiti core
- Problemi di risorse non risolvibili internamente
- Rischi con impatto critico

---

## 16.0 Allegati e Riferimenti

### 16.1 Documenti Correlati
- Business Case (v1.0)
- Statement of Work (v1.1)
- Scope Statement (dettagliato)
- Work Breakdown Structure
- Risk Management Plan (v1.0)
- Team Contract (v1.1)
- Cronoprogramma dettagliato

### 16.2 Riferimenti Tecnici
- Specifiche Bluetooth
- Specifiche Wi-Fi Direct
- Documentazione piattaforma Windows
- Standards di sicurezza per sistemi di emergenza

---

## Registro delle Modifiche

| Versione | Data | Autore | Descrizione Modifiche |
|----------|------|--------|-----------------------|
| 1.0 | 08/12/2025 | Luigi Turco | Versione iniziale del Project Charter |

---

**Fine del Documento**
