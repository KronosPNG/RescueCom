# Organization Breakdown Structure (OBS) - Progetto RescueCom

**Versione:** 1.0  
**Data:** 20 Novembre 2025  
**Redatto da:** Luigi Turco

---

## 1.0 Introduzione

Questo documento definisce la struttura organizzativa del team RescueCom, identificando ruoli, responsabilità e relazioni gerarchiche tra i membri del progetto. L'Organization Breakdown Structure (OBS) fornisce una rappresentazione chiara della struttura del team per facilitare la comunicazione, il coordinamento e la gestione delle attività.

---

## 2.0 Struttura Organizzativa

```
                        Project Manager
                        Luigi Turco
                             |
             +---------------+---------------+
             |                               |
       Front-End Team                  Back-End Team
       (4 membri)                      (3 membri)
             |                               |
      Front-End Lead                  Development Lead
      Mirko Strianese                 Francesco Moccaldi
             |                               |
     +-------+-------+                  +-----+-----+
     |       |       |                  |           |
  Matteo Francesca Marco              Vito      Vittorio
Cavaliere  Latino  Donatiello        Altieri     Landi

```

---

## 3.0 Dettaglio Ruoli e Responsabilità

### 3.1 Project Manager
**Nome:** Luigi Turco

**Responsabilità:**
- Coordinamento generale del progetto
- Pianificazione e monitoraggio delle attività
- Gestione dei rischi e degli stakeholder
- Reporting verso lo sponsor
- Allocazione delle risorse
- Gestione delle modifiche al progetto
- Facilitazione della comunicazione tra team
- Risoluzione dei conflitti
- Approvazione dei deliverable principali

**Competenze Chiave:**
- Project management
- Coordinamento team
- Gestione stakeholder
- Risk management

---

### 3.2 Front-End Team

#### 3.2.1 Mirko Strianese
**Ruolo:** Front-End Lead

**Responsabilità Tecniche:**
- Integrazione UI con backend
- Gestione comunicazione client-server
- Implementazione logica di presentazione
- Ottimizzazione performance UI
- Sviluppo componenti desktop Windows

**Responsabilità di Leadership:**
- Coordinamento tecnico del front-end team
- Code review e quality assurance del codice front-end
- Supporto tecnico ai membri del team front-end
- Definizione standard di sviluppo UI/UX
- Integrazione tra componenti front-end e backend
- Comunicazione tecnica con PM e back-end team

**Competenze Chiave:**
- Client-server integration
- API consumption
- Performance optimization
- Leadership tecnica
- Code review

---

#### 3.2.2 Matteo Cavaliere
**Ruolo:** Front-End Developer

**Responsabilità:**
- Sviluppo interfaccia utente Rescuee
- Implementazione UI/UX design
- Sviluppo componenti desktop Windows
- Testing interfaccia utente
- Documentazione tecnica front-end

**Competenze Chiave:**
- Sviluppo desktop applications
- UI/UX design
- Windows platform development
- User interaction design

---

#### 3.2.3 Francesca Pia Latino
**Ruolo:** Front-End Developer

**Responsabilità:**
- Sviluppo interfaccia utente Rescuer
- Implementazione dashboard di monitoraggio
- Sviluppo funzionalità di gestione messaggi
- Testing e validazione UI
- Supporto documentazione utente

**Competenze Chiave:**
- Sviluppo desktop applications
- Dashboard design
- Windows platform development
- Testing UI/UX

---

### 3.3 Back-End Team

#### 3.3.1 Francesco Moccaldi
**Ruolo:** Development Lead / Back-End Developer

**Responsabilità Tecniche:**
- Sviluppo server cloud centrale
- Implementazione API REST
- Architettura backend
- Gestione database centrale
- Ottimizzazione performance server

**Responsabilità di Leadership:**
- Coordinamento tecnico del back-end team
- Code review e quality assurance del codice backend
- Supporto tecnico ai membri del team
- Definizione standard di sviluppo
- Integrazione tra componenti backend
- Comunicazione tecnica con PM e front-end team

**Competenze Chiave:**
- Architettura software
- API REST development
- Database design
- Leadership tecnica
- Server-side programming

---

#### 3.3.2 Vito Altieri
**Ruolo:** Back-End Developer

**Responsabilità:**
- Sviluppo modulo di comunicazione Bluetooth
- Implementazione discovery dispositivi
- Gestione connessioni peer-to-peer
- Testing comunicazione offline
- Documentazione protocolli di comunicazione

**Competenze Chiave:**
- Bluetooth programming
- Network protocols
- Peer-to-peer communication
- Windows networking APIs

---

#### 3.3.3 Vittorio Landi
**Ruolo:** Back-End Developer

**Responsabilità:**
- Sviluppo modulo Wi-Fi Direct
- Implementazione sistema di relay multi-hop
- Gestione routing messaggi
- Testing rete mesh
- Ottimizzazione algoritmi di routing

**Competenze Chiave:**
- Wi-Fi Direct programming
- Network routing algorithms
- Mesh networking
- Performance optimization

---

#### 3.2.4 Marco Donatiello
**Ruolo:** Front-End Developer

**Responsabilità:**
- Sviluppo componenti UI comuni
- Implementazione validazione input utente
- Testing interfaccia utente
- Supporto integrazione front-end
- Documentazione componenti riutilizzabili

**Competenze Chiave:**
- Sviluppo desktop applications
- Component development
- Input validation
- Windows platform development

---

## 4.0 Matrice di Responsabilità (RACI)

### Legenda:
- **R** = Responsible (Esecutore)
- **A** = Accountable (Responsabile finale)
- **C** = Consulted (Consultato)
- **I** = Informed (Informato)

| Attività | PM | Dev Lead | Front-End | Back-End |
|----------|----|----|-----------|----------|
| **Gestione Progetto** |
| Pianificazione generale | A | C | I | I |
| Risk management | A | C | I | I |
| Reporting sponsor | A | I | I | I |
| Gestione team | A | C | - | - |
| **Analisi e Design** |
| Raccolta requisiti | A | C | C | C |
| Architettura sistema | C | A | C | R |
| Design UI/UX | C | I | A/R | C |
| Design database | C | A | I | R |
| Design API | C | A | C | R |
| **Sviluppo** |
| Interfacce Rescuee/Rescuer | I | C | A/R | I |
| Server cloud | I | A | I | R |
| API REST | I | A | C | R |
| Comunicazione Bluetooth | I | A | I | R |
| Comunicazione Wi-Fi Direct | I | A | I | R |
| Sistema relay | I | A | I | R |
| Database locale | I | A | I | R |
| Sincronizzazione cloud | I | A | C | R |
| **Testing** |
| Test planning | A | C | C | C |
| Unit testing | I | C | R | R |
| Integration testing | C | A | R | R |
| System testing | A | C | R | R |
| **Documentazione** |
| Documentazione tecnica | C | A | R | R |
| Manuali utente | A | C | R | I |
| Report di progetto | A | C | I | I |
| **Quality Assurance** |
| Code review | C | A | R | R |
| Quality standards | A | C | C | C |
| Bug fixing | I | C | R | R |

---

## 5.0 Canali di Comunicazione

### 5.1 Comunicazione Interna Team

#### Meeting Settimanali
- **Frequenza:** Ogni settimana
- **Partecipanti:** Tutto il team (7 persone)
- **Facilitatore:** Luigi Turco (PM)
- **Durata:** 1-2 ore
- **Scopo:** 
  - Progress update
  - Identificazione blockers
  - Coordinamento attività
  - Decisioni tecniche

#### Stand-up Tecnici (Opzionali)
- **Frequenza:** 2-3 volte/settimana
- **Partecipanti:** Dev Lead + sviluppatori
- **Durata:** 15-30 minuti
- **Scopo:**
  - Quick sync tecnico
  - Risoluzione blockers immediati
  - Coordinamento integrazioni

#### Comunicazione Asincrona
- **Strumento:** Discord
- **Canali:**
  - #risorse - condivisione documenti
  - #comunicazione-e-notifiche - annunci importanti
  - #mmeeting-summaries - riassunti meeting
  - #report - report e aggiornamenti
  - #chat - comunicazione quotidiana
  - #front-end - discussioni front-end
  - #back-end - discussioni back-end

### 5.2 Comunicazione con Stakeholder
- **PM → Sponsor:** Email formale, meeting mensili
- **Dev Lead → PM:** Report settimanale, escalation su richiesta
- **Team → PM:** Attraverso meeting e canali Discord

---

## 6.0 Escalation Path

### Livello 1: Risoluzione a Livello Team
- Problemi tecnici di routine
- Bug di bassa/media priorità
- Questioni di coordinamento quotidiano
- **Responsabile:** Dev Lead Back-End (Francesco Moccaldi) / Front-End Lead (Mirko Strianese)

### Livello 2: Escalation al Project Manager
- Problemi che impattano timeline
- Conflitti tra team membri
- Rischi emergenti
- Decisioni che richiedono riallocazione risorse
- **Responsabile:** Project Manager (Luigi Turco)

### Livello 3: Escalation allo Sponsor
- Modifiche significative allo scope
- Superamento budget
- Ritardi critici sulla timeline
- Problemi di risorse non risolvibili internamente
- **Responsabile:** Project Manager → Sponsor

---

## 7.0 Collaborazione e Best Practices

### 7.1 Collaborazione Cross-Team
- **Front-End ↔ Back-End:**
  - Definizione API contracts
  - Testing integrazione
  - Coordinamento release
  - Responsabile coordinamento: Francesco Moccaldi (Dev Lead) e Mirko Strianese (Front-End Lead)

### 7.2 Code Review Process
- **Reviewer Assegnati:**
  - Front-End code: Mirko Strianese (Front-End Lead) + peer review
  - Back-End code: Francesco Moccaldi (Dev Lead) + peer review
  - Integrazione: Francesco Moccaldi + Mirko Strianese + team members

### 7.3 Version Control
- **Repository:** GitHub
- **Branch Strategy:**
  - `main` - produzione
  - `develop` - integrazione
  - `feature/*` - sviluppo feature
  - `bugfix/*` - correzioni bug
- **Pull Request:** Obbligatorie, richiesta approvazione rispettivi Lead (Francesco Moccaldi per BE, Mirko Strianese per FE)

---

## 8.0 Allocazione Tempo e Impegno

### 8.1 Effort Stimato per Ruolo

| Ruolo | Ore/Settimana | Durata | Effort Totale |
|-------|---------------|--------|---------------|
| Project Manager | 15-20 | 12 settimane | 180-240h |
| Dev Lead | 20-25 | 12 settimane | 240-300h |
| Front-End Developer (x3) | 15-20 | 12 settimane | 540-720h |
| Back-End Developer (x2) | 15-20 | 12 settimane | 360-480h |
| **Totale Team** | - | - | **1320-1740h** |

### 8.2 Distribuzione per Fase

#### Fase 1: Analisi e Design (Mese 1)
- PM: 60-80h
- Dev Lead: 80-100h
- Front-End: 120-180h
- Back-End: 120-180h

#### Fase 2: Implementazione (Mese 2)
- PM: 60-80h
- Dev Lead: 80-100h
- Front-End: 240-300h
- Back-End: 240-300h

#### Fase 3: Testing e Finalizzazione (Mese 3)
- PM: 60-80h
- Dev Lead: 80-100h
- Front-End: 180-240h
- Back-End: 180-240h
