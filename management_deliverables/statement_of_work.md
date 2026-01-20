# Statement of Work - Progetto RescueCom  

| Riferimento |     |
| --- | --- |
| Versione | 1.1 |
| Data | 07/10/2025 |
| Destinatario | Dipartimento della Protezione Civile |
| Presentato da | Turco Luigi |

Statement of Work (SOW) del Progetto  
RescueCom

## Introduzione

In situazioni di emergenza (terremoti, alluvioni, blackout), la comunicazione basata su Internet può risultare inaccessibile. RescueCom nasce per garantire comunicazioni di soccorso resilienti anche in assenza di connettività, utilizzando canali Bluetooth e Wi-Fi Direct per trasmettere e inoltrare messaggi tra dispositivi vicini.

Quando la rete torna disponibile, i dati vengono sincronizzati automaticamente con un server cloud, che aggiorna lo stato dei messaggi e coordina le operazioni di soccorso.

## Obiettivi di Business

### **Obiettivo generale**

Progettare e sviluppare un sistema software open source che permetta la **trasmissione e sincronizzazione di messaggi di emergenza** tra utenti (rescuee e rescuer) in modo affidabile, anche in modalità offline.

### **Obiettivi specifici**

- Consentire la **creazione e memorizzazione locale di messaggi di emergenza**.
- Permettere la **trasmissione diretta** di messaggi via Bluetooth o Wi-Fi Direct.
- Implementare un meccanismo di **relay multi-hop** (inoltro tra nodi).
- Integrare la **sincronizzazione con un server cloud** quando Internet è disponibile.
- Fornire un'interfaccia utente semplice e accessibile su laptop con Bluetooth/Wi-Fi.
- Mantenere il codice open source e documentato per uso didattico.

## Ambito del Prodotto / Product Scope

### **Includerà**

- Analisi dei requisiti funzionali e non funzionali
- Progettazione architetturale del sistema
- Implementazione dei tre moduli principali:
  - **Rescuee** (utente che invia richieste di aiuto)
  - **Rescuer** (utente che riceve e gestisce le richieste)
  - **Cloud Server** (database e sincronizzazione)
- Sviluppo delle funzionalità di:
  - Comunicazione Bluetooth e Wi-Fi Direct
  - Storage locale (SQLite)
  - Sincronizzazione via REST API
  - Gestione dei conflitti tramite timestamp
- Test funzionali, di integrazione e di sincronizzazione
- Documentazione tecnica e guida utente

### **Non includerà (Out of Scope)**

- Applicazioni mobile native (iOS/Android)
- Supporto per protocolli di comunicazione satellitare
- Gestione di chiamate vocali o video
- Integrazione con sistemi legacy della Protezione Civile
- Supporto multilingua (solo italiano nella versione 1.0)
- Hosting e manutenzione del server cloud in produzione

### **Possibili estensioni future**

- Implementazione di algoritmi AI o di machine learning per prioritizzazione messaggi
- Crittografia end-to-end avanzata
- Applicazioni web o mobile avanzate
- Geolocalizzazione automatica tramite GPS

## Deliverable

### **Documentazione Manageriale**

1. **Project Charter** - Autorizzazione formale del progetto
2. **Business Case** - Giustificazione economica e strategica
3. **Project Scope Statement** - Definizione dettagliata dello scope
4. **Work Breakdown Structure (WBS)** - Decomposizione gerarchica del lavoro
5. **Organization Breakdown Structure (OBS)** - Struttura organizzativa
6. **Project Budget** - Piano finanziario dettagliato
7. **Financial Analysis** - Analisi costi-benefici
8. **Risk Management Plan** - Identificazione e mitigazione rischi
9. **Team Contract** - Accordi e regole del team

### **Documentazione Tecnica di Sviluppo**

10. **Requirements Analysis Document (RAD)** - Analisi dettagliata dei requisiti funzionali e non funzionali
11. **System Design Document (SDD)** - Architettura software, design pattern, diagrammi UML
12. **Object Design Document (ODD)** - Design dettagliato delle classi e oggetti
13. **Test Plan** - Strategia e pianificazione dei test
14. **Test Execution Report** - Risultati dei test eseguiti

### **Prodotti Software**

15. **Frontend Web (Rescuee/Rescuer)** - Interfaccia web in HTML/CSS/JavaScript per utenti e soccorritori
16. **Cloud Server (Backend Python)** - Backend in Python con database e API REST
17. **Database Schema** - Struttura del database relazionale
18. **API Documentation** - Documentazione delle REST API

### **Codice e Repository**

19. **Codice sorgente completo** su repository Git pubblico
20. **README.md** con istruzioni di installazione e configurazione
21. **Script di deployment** del prodotto
22. **Unit test e integration test** con coverage minimo 70%

### **Documentazione Utente**

23. **Manuale Utente Rescuee** - Guida operativa per utenti in emergenza
24. **Manuale Utente Rescuer** - Guida operativa per soccorritori
25. **Guida Amministratore** - Configurazione e manutenzione del sistema

## Criteri di Accettazione

Ogni deliverable sarà accettato secondo i seguenti criteri:

### **Documentazione**
- Formato conforme agli standard IEEE/PMI
- Revisione e approvazione da parte del committente
- Completezza rispetto al template fornito

### **Software**
- Superamento di tutti i test funzionali critici
- Code coverage minimo del 70%
- Assenza di bug critici o bloccanti
- Conformità ai requisiti funzionali del RAD
- Performance: latenza < 2 secondi per invio messaggio locale
- Compatibilità: Windows 10/11, Ubuntu 20.04+

### **Codice**
- Rispetto degli standard di codifica:
  - Python: PEP 8 Style Guide
  - JavaScript: Airbnb JavaScript Style Guide o Standard JS
  - HTML/CSS: Best practices W3C
- Documentazione inline completa (docstrings Python, JSDoc per JavaScript)
- Licenza open source applicata (MIT License)
- Build e deployment automatizzati funzionanti

## Timeline e Milestone

| Milestone | Data Target | Deliverable Associati |
|-----------|-------------|----------------------|
| **M1: Kickoff e Planning** | Ottobre 2025 | Project Charter, Business Case, WBS, OBS |
| **M2: Requirements Complete** | Novembre 2025 | RAD, Scope Statement, Risk Management Plan |
| **M3: Design Complete** | Metà Novembre 2025 | SDD, ODD, Database Schema |
| **M4: Development 50%** | Fine Novembre 2025 | Moduli Rescuee/Rescuer (funzionalità base) |
| **M5: Development Complete** | Metà Dicembre 2025 | Tutti i moduli software, Cloud Server |
| **M6: Testing Complete** | Fine Dicembre 2025 | Test Plan, Test Execution Report |
| **M7: Project Closure** | Gennaio 2026 | Documentazione utente, deployment, consegna finale |

**Data di Inizio:** Ottobre 2025  
**Data di Fine:** Gennaio 2026  
**Durata Totale:** 3,5 mesi

## Ruoli e Responsabilità

| Ruolo | Responsabilità | Persona |
|-------|----------------|---------|
| **Project Manager** | Pianificazione, coordinamento, reporting | Turco Luigi |
| **Lead Developer** | Architettura software, code review | TBD |
| **Backend Developer** | Sviluppo Cloud Server e API | TBD |
| **Frontend Developer** | Sviluppo interfacce Rescuee/Rescuer | TBD |
| **QA Engineer** | Test planning ed esecuzione | TBD |
| **Technical Writer** | Documentazione tecnica e utente | TBD |
| **Stakeholder/Cliente** | Approvazioni e feedback | Dipartimento Protezione Civile |

## Assunzioni e Vincoli

### **Assunzioni**

- I dispositivi laptop hanno Bluetooth 4.0+ e Wi-Fi Direct
- Il team ha accesso a un server cloud per testing (es. AWS Free Tier)
- Gli utenti hanno conoscenze informatiche di base
- È disponibile connettività Internet per la sincronizzazione (quando possibile)
- Il progetto è a scopo didattico/dimostrativo

### **Vincoli**

- **Budget:** Limitato (progetto accademico/open source)
- **Tempo:** 3,5 mesi (Ottobre 2025 - Gennaio 2026)
- **Tecnologia:** Python per backend, HTML/CSS/JavaScript per frontend, database relazionale
- **Piattaforma:** Applicazione web accessibile da browser moderni
- **Risorse umane:** Team limitato (dimensione da definire)
- **Licenza:** Deve essere open source (MIT License)

## Requisiti Tecnici Minimi

### **Hardware (Client)**
- Laptop/desktop con Bluetooth 4.0 o superiore
- Wi-Fi Direct supportato
- Minimo 4GB RAM
- 100MB spazio disco disponibile per cache locale

### **Software (Client)**
- Browser moderno: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- JavaScript abilitato
- Supporto per Web Bluetooth API e WebRTC

### **Server Cloud (Backend)**
- Linux server (Ubuntu 20.04 LTS o superiore)
- Python 3.9 o superiore
- Minimo 2GB RAM, 10GB spazio disco
- Database PostgreSQL 12+ o MySQL 8+
- Web server: Nginx o Apache
- HTTPS/SSL certificato per produzione
- Connessione Internet stabile

## Gestione delle Modifiche

Qualsiasi modifica allo scope, timeline o deliverable richiede:

1. **Richiesta formale** tramite Change Request Form
2. **Impact analysis** su tempo, costi e qualità
3. **Approvazione** dal Project Manager e stakeholder
4. **Aggiornamento** della documentazione di progetto

## Metriche di Successo

Il progetto sarà considerato un successo se:

- ✅ Tutti i deliverable documentali sono completati e approvati
- ✅ Il software supera tutti i test di accettazione
- ✅ La comunicazione offline funziona con latenza < 5 secondi (trasmissione diretta)
- ✅ La sincronizzazione cloud funziona correttamente senza perdita dati
- ✅ Il codice è pubblicato su repository pubblico con licenza open source
- ✅ La documentazione è completa e comprensibile
- ✅ Il progetto è consegnato entro Gennaio 2026

## Termini e Condizioni

- **Proprietà intellettuale:** Il codice sarà rilasciato sotto licenza MIT License
- **Confidenzialità:** Non applicabile (progetto open source)
- **Garanzia:** Software fornito "as-is" senza garanzie (standard open source)
- **Supporto post-consegna:** Non previsto (progetto accademico)
