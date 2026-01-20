# RescueCom Business Case

## 1.0 Background

RescueCom nasce come iniziativa per sviluppare un sistema di comunicazione di emergenza resiliente in scenari di disastro o mancanza di connettività Internet.  
In tali contesti, le infrastrutture di rete tradizionali risultano spesso inaccessibili, rendendo impossibile il coordinamento tempestivo dei soccorsi e la richiesta di aiuto da parte delle vittime.  
<br/>Il progetto mira a fornire un sistema di comunicazione decentralizzato basato su Bluetooth e Wi-Fi Direct, in grado di permettere lo scambio di messaggi di emergenza anche in assenza di rete Internet.  
Una volta ristabilita la connettività, il sistema sincronizza automaticamente i dati con un server cloud centrale, rendendo accessibili i messaggi ai centri di soccorso e alle autorità competenti.  
<br/>RescueCom funge da proof of concept per dimostrare la fattibilità tecnica e l'impatto potenziale di un'infrastruttura di comunicazione offline in scenari di emergenza reale.  

## 2.0 Business Objective

L'obiettivo principale del progetto RescueCom è quello di migliorare la resilienza delle comunicazioni di emergenza e ridurre la dipendenza da infrastrutture centralizzate durante situazioni critiche.  
Il progetto si propone di:  
\- Consentire la trasmissione di messaggi di emergenza tra utenti e soccorritori anche in assenza di Internet.  
\- Creare una rete peer-to-peer dinamica che si auto-organizza e si adatta al contesto operativo.  
\- Ridurre i tempi di risposta dei soccorsi in situazioni dove le reti tradizionali falliscono.  
\- Fornire un'architettura scalabile e interoperabile con infrastrutture cloud esistenti.  
\- Dimostrare un modello di comunicazione resiliente e decentralizzato replicabile.  

## 3.0 Opportunity Statement

Durante catastrofi naturali, blackout di rete o eventi che compromettono le infrastrutture digitali, la comunicazione tra cittadini e soccorritori diventa critica ma spesso impossibile.  
Le attuali applicazioni di emergenza si basano quasi esclusivamente sulla connettività Internet, rendendole inutilizzabili nei momenti di maggiore necessità.  
<br/>C'è quindi un'opportunità effettiva per sviluppare un sistema di comunicazione offline, che utilizzi tecnologie già integrate nei dispositivi moderni (Bluetooth e Wi-Fi Direct), per garantire continuità nelle comunicazioni.  
RescueCom intende colmare questo gap tecnologico, fornendo una piattaforma sicura, autonoma e sincronizzata con un cloud centrale per l'aggregazione dei dati di emergenza.  

## 4.0 Assunzioni Critiche e Vincoli

Il progetto RescueCom si fonda sulle seguenti assunzioni e vincoli:  
\- Il sistema deve operare efficacemente senza connessione Internet, utilizzando solo Bluetooth e Wi-Fi Direct.  
\- Il proof of concept sarà limitato alla piattaforma Windows, con possibilità future di estensione ad altri sistemi operativi.  
\- La sincronizzazione cloud avverrà solo quando la connessione Internet sarà disponibile.  
\- Tutti i dati scambiati devono essere accessibili solo a utenti autorizzati.  
\- Il sistema dovrà dimostrare la fattibilità tecnica e funzionale in ambienti simulati, non necessariamente in condizioni reali di disastro.  

## 5.0 Analisi di Opzioni e Raccomandazioni

Opzioni considerate per la realizzazione del progetto:  
1\. Non procedere. Continuare con sistemi tradizionali di comunicazione d'emergenza che richiedono connettività Internet.  
\- Svantaggio: nessuna innovazione o miglioramento della resilienza comunicativa.  
<br/>2\. Adottare software di terze parti. Utilizzare soluzioni commerciali esistenti per la comunicazione offline.  
\- Svantaggio: costi elevati, mancanza di controllo sull'architettura e scarsa adattabilità accademica.  
<br/>3\. Progettare e sviluppare RescueCom internamente. Creare una soluzione su misura che sfrutti Bluetooth, Wi-Fi Direct e un cloud centralizzato per sincronizzazione dati.  
\- Vantaggi: totale controllo tecnico, validazione accademica, prova di fattibilità per applicazioni future.  
<br/>Raccomandazione:  
Basandosi sulle discussioni con gli stakeholder l'opzione 3 rappresenta la scelta migliore per il progetto RescueCom.  

## 6.0 Requisiti Preliminari del Progetto

I requisiti preliminari includono:  
1\. Capacità di inviare e ricevere messaggi di emergenza tramite Bluetooth e Wi-Fi Direct.  
2\. Funzione di relay per inoltrare messaggi di altri utenti nella rete offline.  
3\. Database locale per memorizzare i messaggi durante l'assenza di connessione.  
4\. Sincronizzazione automatica con un server cloud centrale al ritorno della connettività.  
5\. Interfaccia utente intuitiva sia per i Rescuee (utenti in difficoltà) sia per i Rescuer (personale di soccorso).  
6\. Dashboard di monitoraggio per le autorità di soccorso.  
7\. Supporto all'integrazione con API RESTful per espandibilità futura.  

## 7.0 Stima del Cronoprogramma

Il progetto sarà completato entro tre mesi, suddivisi in:  
\- Mese 1: Analisi requisiti e progettazione architetturale  
\- Mese 2: Implementazione del sistema e sviluppo interfacce  
\- Mese 3: Testing, validazione e presentazione finale  

## 8.0 Potenziali Rischi

I rischi principali identificati includono:  
\- Difficoltà nella simulazione realistica di scenari di emergenza offline.  
\- Limiti tecnici nella gestione di Bluetooth e Wi-Fi Direct su diversi dispositivi.  
\- Complessità nella risoluzione dei conflitti di sincronizzazione dati.  
\- Rischio di basso engagement del team o ritardi accademici nella consegna.  
\- Possibili problemi di sicurezza o vulnerabilità di rete durante la fase di test.  

## 9.0 Analisi Finanziaria

**Premesse e Assunzioni**

Tasso di sconto utilizzato: 8%

Questa versione adotta una stima ponderata dei costi e benefici, mantenendosi al di sotto del limite massimo di progetto di €250.000. Le cifre sono conservative per coprire personale, integrazione, infrastruttura e contingenze.

**Sintesi dei costi e benefici (3 anni)**

| Anno | Costi operativi (€) | Investimento iniziale (€) | Benefici (€) | Flusso netto (€) | Flusso scontato (€) |
| --- | --- | --- | --- | --- | --- |
| 0   | 0,00 | 165.000,00 | 0,00 | \-165.000,00 | \-165.000,00 |
| 1   | 30.000,00 | 0,00 | 140.000,00 | 110.000,00 | 101.851,85 |
| 2   | 30.000,00 | 0,00 | 140.000,00 | 110.000,00 | 94.307,27 |
| 3   | 30.000,00 | 0,00 | 140.000,00 | 110.000,00 | 87.321,55 |

**Risultati finanziari**

Valore attuale netto (NPV) a 3 anni: €118.480,67

Valore attuale dei benefici (PV benefici): €360.793,58

Valore attuale dei costi (PV costi = investimento + PV manutenz,): €242.312,91

Discounted ROI (3 anni): 48.9%

Payback (non scontato): anno 2 (cumulativo positivo dopo anno 2).

**Dettaglio costi iniziali (€165.000)**

Project Manager (interno/mentoring) - 200 ore equivalenti @ €60/ora (costo imputato): €12.000,00

PM coordinating & external consultancy (audit sicurezza e protocol design): €18.000,00

Senior Team Member (3 mesi. loaded cost): €18.000,00

3 Junior Team Members (totale per 3 mesi. loaded): €30.000,00

Integrazione & QA (contractor e test interoperability): €15.000,00

Software. API e servizi cloud iniziali (hosting. TLS. DB): €12.000,00

Hardware e dispositivi di test (noleggio/acquisto): €8.000,00

Licenze e tool di sviluppo: €4.000,00

Overhead universitario e spese amministrative: €6.000,00

Contingenza & imprevisti (circa 5% dell'investimento): €8.250,00

Documentazione. formazione e presentazione finale: €3.730,00

Totale dettagliato dei costi iniziali: €134.980,00

**Considerazioni e giustificazioni (sintesi)**

Questa stima è stata ponderata per rimanere ben al di sotto del tetto massimo di €250.000, pur garantendo sufficiente copertura per le attività critiche: analisi e design prototipo, sviluppo PoC, test di integrazione e costi infrastrutturali iniziali. I valori assegnati a PM, senior e junior riflettono costi 'loaded' comprensivi di oneri e tempo reale dedicato al progetto.