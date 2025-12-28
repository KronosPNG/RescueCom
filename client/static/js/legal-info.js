class RescueGDPR extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
    }

    static get observedAttributes() {
        return ['lang'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'lang' && oldValue !== newValue) {
            this.render();
        }
    }

    getStyles() {
        return `
            :host {
                display: block;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                color: #1d1d1f;
                background-color: #ffffff;
                line-height: 1.47059;
                font-weight: 400;
                letter-spacing: -0.022em;
                --link-color: #0066cc;
                --border-color: #d2d2d7;
                --max-width: 980px;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            a {
                color: var(--link-color);
                text-decoration: none;
                cursor: pointer;
            }
            a:hover {
                text-decoration: underline;
            }

            h1 {
                font-size: 48px;
                line-height: 1.08349;
                font-weight: 700;
                letter-spacing: -0.003em;
                margin-bottom: 20px;
            }

            h2 {
                font-size: 24px;
                line-height: 1.16667;
                font-weight: 600;
                letter-spacing: .009em;
            }

            h3 {
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 15px;
            }

            p {
                margin-bottom: 0.8em;
            }

            ul {
                list-style-position: outside;
                margin-left: 1.5em;
                margin-bottom: 1em;
            }

            .section-content {
                margin-left: auto;
                margin-right: auto;
                width: 100%;
                max-width: var(--max-width);
                padding-left: 22px;
                padding-right: 22px;
            }

            .section-hero {
                padding-top: 60px;
                padding-bottom: 40px;
                text-align: center;
            }

            .typography-intro {
                font-size: 21px;
                line-height: 1.381;
                font-weight: 400;
                letter-spacing: .011em;
                max-width: 800px;
                margin: 0 auto 20px auto;
            }

            .hero-icon {
                margin: 30px auto;
                display: block;
            }

            .section-transparency-accordion {
                padding: 40px 0;
            }

            .accordion-wrapper {
                list-style: none;
                margin: 0;
                border-top: 1px solid var(--border-color);
            }

            .accordion-item {
                border-bottom: 1px solid var(--border-color);
            }

            .header-wrapper {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 24px 0;
                cursor: pointer;
                width: 100%;
                background: none;
                border: none;
                text-align: left;
            }

            .header-wrapper:hover .accordion-headline {
                color: var(--link-color);
            }

            .accordion-headline {
                color: #1d1d1f;
                transition: color 0.3s ease;
            }

            .icon-plus {
                position: relative;
                width: 18px;
                height: 18px;
                flex-shrink: 0;
                margin-left: 15px;
            }

            .icon-plus::before, .icon-plus::after {
                content: '';
                position: absolute;
                background-color: #1d1d1f;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                transition: transform 0.3s ease;
            }

            .icon-plus::before {
                width: 14px;
                height: 1px;
            }

            .icon-plus::after {
                width: 1px;
                height: 14px;
            }

            .accordion-item.active .icon-plus::after {
                transform: translate(-50%, -50%) rotate(90deg);
            }

            .accordion-panel {
                max-height: 0;
                overflow: hidden;
                opacity: 0;
                transition: max-height 0.4s cubic-bezier(0.65, 0, 0.35, 1), opacity 0.4s ease;
            }

            .accordion-item.active .accordion-panel {
                max-height: 2000px;
                opacity: 1;
                padding-bottom: 30px;
            }

            .accordion-content {
                font-size: 17px;
                color: #1d1d1f;
            }

            @media (max-width: 734px) {
                h1 { font-size: 40px; }
                .section-content { padding-left: 16px; padding-right: 16px; }
            }
        `;
    }

    getContent(lang) {
        const logoPath = this.getAttribute('logo-path') || 'logoDGPR.png';
        const translations = {
            'it': `
                <div class="language-switcher-container" style="display: flex; justify-content: center; margin-bottom: 20px;">
                    <div class="language-switcher" style="background-color: #f0f0f0; padding: 15px 25px; border-radius: 15px; display: flex; flex-direction: column; align-items: center; gap: 5px;">
                        <span style="font-size: 0.9rem; color: #666; font-weight: 500;">Seleziona la tua lingua preferita</span>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 24px;">🌍</span>
                            <div style="width: 1px; height: 24px; background-color: #ccc; margin: 0 5px;"></div>
                            <a class="lang-link" data-lang="it" style="font-size: 24px;">IT</a>
                            <a class="lang-link" data-lang="en" style="font-size: 24px;">EN</a>
                            <a class="lang-link" data-lang="es" style="font-size: 24px;">ES</a>
                            <a class="lang-link" data-lang="fr" style="font-size: 24px;">FR</a>
                            <a class="lang-link" data-lang="de" style="font-size: 24px;">DE</a>
                        </div>
                    </div>
                </div>

                <h1>Regolamento Generale sulla Protezione dei Dati di RescueCom</h1>
                <h3 style="font-weight: 500; color: #000000; margin-top: 0;">Informativa sul Regolamento (UE) 2016/679 (GDPR)</h3>
                <p style="font-size: 0.9em; color: #666; margin-top: -10px; margin-bottom: 20px;">Ultimo aggiornamento: 28 Dicembre 2025</p>

                <p class="typography-intro">RescueCom è una piattaforma di comunicazione d'emergenza (Proof of Concept), sviluppata in ambito accademico per facilitare le operazioni di soccorso in scenari privi di connettività internet.</p>
                <p class="typography-intro">Questa informativa descrive in dettaglio le modalità di trattamento dei tuoi dati personali e particolari (sanitari), le misure di sicurezza crittografica adottate e i tuoi diritti. La nostra priorità è garantire la massima riservatezza: adottiamo un approccio <strong>Privacy by Design</strong> e <strong>Privacy by Default</strong>, minimizzando la raccolta dei dati al solo necessario per salvare vite umane.</p>
                
                <img alt="Privacy Icon" src="${logoPath}" width="60" class="hero-icon">

                <p class="typography-intro">Il sistema utilizza una rete decentralizzata (Mesh) in cui la sicurezza è garantita matematicamente tramite crittografia End-to-End. Nessun intermediario può accedere al contenuto delle tue comunicazioni.</p>

                <div style="margin-top: 30px;">
                    <a href="static/pdf/gdpr(IT).pdf" target="_blank">Scarica l'informativa legale completa (PDF firmato digitalmente)</a>
                </div>
            `,
            'en': `
                 <div class="language-switcher-container" style="display: flex; justify-content: center; margin-bottom: 20px;">
                    <div class="language-switcher" style="background-color: #f0f0f0; padding: 15px 25px; border-radius: 15px; display: flex; flex-direction: column; align-items: center; gap: 5px;">
                        <span style="font-size: 0.9rem; color: #666; font-weight: 500;">Select your preferred language</span>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 24px;">🌍</span>
                            <div style="width: 1px; height: 24px; background-color: #ccc; margin: 0 5px;"></div>
                            <a class="lang-link" data-lang="it" style="font-size: 24px;">IT</a>
                            <a class="lang-link" data-lang="en" style="font-size: 24px;">EN</a>
                            <a class="lang-link" data-lang="es" style="font-size: 24px;">ES</a>
                            <a class="lang-link" data-lang="fr" style="font-size: 24px;">FR</a>
                            <a class="lang-link" data-lang="de" style="font-size: 24px;">DE</a>
                        </div>
                    </div>
                </div>

                <h1>Extended Personal Data Processing Notice</h1>
                <h3 style="font-weight: 500; color: #000000; margin-top: 0;">Notice pursuant to Regulation (EU) 2016/679 (GDPR)</h3>
                <p style="font-size: 0.9em; color: #666; margin-top: -10px; margin-bottom: 20px;">Last updated: December 28, 2025</p>

                <p class="typography-intro">RescueCom is an emergency communication platform (Proof of Concept), developed academically to facilitate rescue operations in scenarios lacking internet connectivity.</p>
                <p class="typography-intro">This notice describes in detail how we process your personal and special (health) data, the cryptographic security measures adopted, and your rights. Our priority is ensuring maximum confidentiality: we adopt a <strong>Privacy by Design</strong> and <strong>Privacy by Default</strong> approach, minimizing data collection to only what is necessary to save human lives.</p>

                <img alt="Privacy Icon" src="${logoPath}" width="60" class="hero-icon">

                <p class="typography-intro">The system uses a decentralized (Mesh) network where security is mathematically guaranteed via End-to-End encryption. No intermediary can access the content of your communications.</p>

                <div style="margin-top: 30px;">
                    <a href="static/pdf/gdpr(EN).pdf" target="_blank">Download full legal notice (Digitally Signed PDF)</a>
                </div>
            `,
            'es': `
                <div class="language-switcher-container" style="display: flex; justify-content: center; margin-bottom: 20px;">
                    <div class="language-switcher" style="background-color: #f0f0f0; padding: 15px 25px; border-radius: 15px; display: flex; flex-direction: column; align-items: center; gap: 5px;">
                        <span style="font-size: 0.9rem; color: #666; font-weight: 500;">Selecciona tu idioma preferido</span>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 24px;">🌍</span>
                            <div style="width: 1px; height: 24px; background-color: #ccc; margin: 0 5px;"></div>
                            <a class="lang-link" data-lang="it" style="font-size: 24px;">IT</a>
                            <a class="lang-link" data-lang="en" style="font-size: 24px;">EN</a>
                            <a class="lang-link" data-lang="es" style="font-size: 24px;">ES</a>
                            <a class="lang-link" data-lang="fr" style="font-size: 24px;">FR</a>
                            <a class="lang-link" data-lang="de" style="font-size: 24px;">DE</a>
                        </div>
                    </div>
                </div>

                <h1>Aviso Extendido de Tratamiento de Datos Personales</h1>
                <h3 style="font-weight: 500; color: #000000; margin-top: 0;">Aviso de conformidad con el Reglamento (UE) 2016/679 (GDPR)</h3>
                <p style="font-size: 0.9em; color: #666; margin-top: -10px; margin-bottom: 20px;">Última actualización: 28 de diciembre de 2025</p>

                <p class="typography-intro">RescueCom es una plataforma de comunicación de emergencia (Prueba de Concepto), desarrollada en el ámbito académico para facilitar las operaciones de rescate en escenarios sin conectividad a internet.</p>
                 <p class="typography-intro">Este aviso describe en detalle cómo tratamos sus datos personales y especiales (de salud), las medidas de seguridad criptográfica adoptadas y sus derechos. Nuestra prioridad es garantizar la máxima confidencialidad: adoptamos un enfoque de <strong>Privacy by Design</strong> e <strong>Privacy by Default</strong>, minimizando la recopilación de datos a lo estrictamente necesario para salvar vidas humanas.</p>

                <img alt="Icono de Privacidad" src="${logoPath}" width="60" class="hero-icon">

                <p class="typography-intro">El sistema utiliza una red descentralizada (Mesh) donde la seguridad está garantizada matemáticamente mediante cifrado de extremo a extremo. Ningún intermediario puede acceder al contenido de sus comunicaciones.</p>

                <div style="margin-top: 30px;">
                    <a href="static/pdf/gdpr(ES).pdf" target="_blank">Descargar aviso legal completo (PDF firmado digitalmente)</a>
                </div>
            `,
            'fr': `
                <div class="language-switcher-container" style="display: flex; justify-content: center; margin-bottom: 20px;">
                    <div class="language-switcher" style="background-color: #f0f0f0; padding: 15px 25px; border-radius: 15px; display: flex; flex-direction: column; align-items: center; gap: 5px;">
                        <span style="font-size: 0.9rem; color: #666; font-weight: 500;">Sélectionnez votre langue préférée</span>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 24px;">🌍</span>
                            <div style="width: 1px; height: 24px; background-color: #ccc; margin: 0 5px;"></div>
                            <a class="lang-link" data-lang="it" style="font-size: 24px;">IT</a>
                            <a class="lang-link" data-lang="en" style="font-size: 24px;">EN</a>
                            <a class="lang-link" data-lang="es" style="font-size: 24px;">ES</a>
                            <a class="lang-link" data-lang="fr" style="font-size: 24px;">FR</a>
                            <a class="lang-link" data-lang="de" style="font-size: 24px;">DE</a>
                        </div>
                    </div>
                </div>

                <h1>Avis Étendu sur le Traitement des Données Personnelles</h1>
                <h3 style="font-weight: 500; color: #000000; margin-top: 0;">Avis conforme au Règlement (UE) 2016/679 (RGPD)</h3>
                <p style="font-size: 0.9em; color: #666; margin-top: -10px; margin-bottom: 20px;">Dernière mise à jour : 28 décembre 2025</p>

                <p class="typography-intro">RescueCom est une plateforme de communication d'urgence (Preuve de Concept), développée dans un cadre académique pour faciliter les opérations de secours dans des scénarios dépourvus de connectivité internet.</p>
                <p class="typography-intro">Cet avis décrit en détail comment nous traitons vos données personnelles et particulières (santé), les mesures de sécurité cryptographiques adoptées et vos droits. Notre priorité est de garantir une confidentialité maximale : nous adoptons une approche de <strong>Privacy by Design</strong> et <strong>Privacy by Default</strong>, minimisant la collecte de données au strict nécessaire pour sauver des vies humaines.</p>

                <img alt="Icône de confidentialité" src="${logoPath}" width="60" class="hero-icon">

                <p class="typography-intro">Le système utilise un réseau décentralisé (Mesh) où la sécurité est mathématiquement garantie par un chiffrement de bout en bout. Aucun intermédiaire ne peut accéder au contenu de vos communications.</p>

                <div style="margin-top: 30px;">
                    <a href="static/pdf/gdpr(FR).pdf" target="_blank">Télécharger l'avis juridique complet (PDF signé numériquement)</a>
                </div>
            `,
            'de': `
                 <div class="language-switcher-container" style="display: flex; justify-content: center; margin-bottom: 20px;">
                    <div class="language-switcher" style="background-color: #f0f0f0; padding: 15px 25px; border-radius: 15px; display: flex; flex-direction: column; align-items: center; gap: 5px;">
                        <span style="font-size: 0.9rem; color: #666; font-weight: 500;">Wählen Sie Ihre bevorzugte Sprache</span>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 24px;">🌍</span>
                            <div style="width: 1px; height: 24px; background-color: #ccc; margin: 0 5px;"></div>
                            <a class="lang-link" data-lang="it" style="font-size: 24px;">IT</a>
                            <a class="lang-link" data-lang="en" style="font-size: 24px;">EN</a>
                            <a class="lang-link" data-lang="es" style="font-size: 24px;">ES</a>
                            <a class="lang-link" data-lang="fr" style="font-size: 24px;">FR</a>
                            <a class="lang-link" data-lang="de" style="font-size: 24px;">DE</a>
                        </div>
                    </div>
                </div>

                <h1>Erweiterte Datenschutzerklärung</h1>
                <h3 style="font-weight: 500; color: #000000; margin-top: 0;">Hinweis gemäß Verordnung (EU) 2016/679 (DSGVO)</h3>
                <p style="font-size: 0.9em; color: #666; margin-top: -10px; margin-bottom: 20px;">Zuletzt aktualisiert: 28. Dezember 2025</p>

                <p class="typography-intro">RescueCom ist eine Notfallkommunikationsplattform (Proof of Concept), die im akademischen Bereich entwickelt wurde, um Rettungseinsätze in Szenarien ohne Internetverbindung zu erleichtern.</p>
                <p class="typography-intro">Diese Erklärung beschreibt im Detail, wie wir Ihre personenbezogenen und besonderen (Gesundheits-)Daten verarbeiten, die angewandten kryptografischen Sicherheitsmaßnahmen und Ihre Rechte. Unsere Priorität ist die Gewährleistung maximaler Vertraulichkeit: Wir verfolgen einen Ansatz von <strong>Privacy by Design</strong> und <strong>Privacy by Default</strong>, wobei die Datenerhebung auf das zur Lebensrettung Notwendige beschränkt wird.</p>

                <img alt="Datenschutz-Symbol" src="${logoPath}" width="60" class="hero-icon">

                <p class="typography-intro">Das System verwendet ein dezentrales Netzwerk (Mesh) in dem Sicherheit mathematisch durch End-to-End-Verschlüsselung garantiert wird. Kein Vermittler kann auf den Inhalt Ihrer Kommunikation zugreifen.</p>

                <div style="margin-top: 30px;">
                    <a href="static/pdf/gdpr(DE).pdf" target="_blank">Vollständigen rechtlichen Hinweis herunterladen (Digital signiertes PDF)</a>
                </div>
            `
        };

        // Mappa del contenuto della fisarmonica
        // Semplificato per brevità in questa costruzione manuale del componente, ma dovrei usare il contenuto completo se possibile.
        // In realtà, data la lunghezza, incollerò il contenuto completo nel metodo render o in una struttura dati separata.
        // Usare l'HTML completo dai file è meglio.
        const accordionContent = {
            'it': [
                { title: "1. Categorie di Dati Trattati e Finalità", content: "<p>In conformità al principio di minimizzazione dei dati...</p>" },
                // In realtà, data la lunghezza, incollerò il contenuto completo nel metodo render o in una struttura dati separata.
                // Usare l'HTML completo dai file è meglio.
            ],
        };

        return translations[lang] || translations['en'];
    }

    getAccordions(lang) {
        const data = {
            'it': [
                { title: "1. Categorie di Dati Trattati e Finalità", content: `<p>In conformità al principio di minimizzazione dei dati, raccogliamo esclusivamente le informazioni indispensabili per la gestione efficace delle emergenze:</p><ul><li><strong>Dati Identificativi Comuni:</strong> Nome, cognome, data di nascita e un identificativo utente univoco . Questi dati servono per identificare in modo certo la persona che richiede soccorso.</li><li><strong>Categorie Particolari di Dati (Dati Sanitari):</strong> Il trattamento include dati sensibili critici per il triage medico, quali: gruppo sanguigno, allergie farmacologiche note, disabilità specifiche (motorie, sensoriali o cognitive) e patologie croniche rilevanti (es. diabete, cardiopatie).</li><li><strong>Dati di Geolocalizzazione:</strong> Coordinate GPS precise (latitudine/longitudine) acquisite in tempo reale o inserite manualmente, utilizzate esclusivamente per localizzare il dispositivo in scenario di crisi.</li><li><strong>Dati di Telemetria Tecnica:</strong> Metadati relativi allo stato della batteria e della connettività, necessari per valutare l'affidabilità del nodo nella rete mesh.</li></ul>` },
                { title: "2. Base Giuridica del Trattamento", content: `<p>Il trattamento dei tuoi dati personali è legittimato dalle seguenti basi giuridiche:</p><ul><li><strong>Consenso Esplicito:</strong> In ottemperanza allo pseudo-requisito tecnico di sistema PR_L.1, la memorizzazione dei dati sanitari avviene solo previo consenso libero, specifico ed informato, manifestato tramite un'azione positiva inequivocabile (opt-in) nell'app.</li><li><strong>Salvaguardia degli Interessi Vitali:</strong> Nelle situazioni di emergenza in cui l'interessato si trovi nell'incapacità fisica o giuridica di prestare il consenso, il trattamento è necessario per proteggere la vita dell'interessato o di terzi.</li></ul>` },
                { title: "3. Architettura del Sistema e Modalità di Trattamento", content: `<p>Il trattamento avviene mediante un'infrastruttura ibrida resiliente, progettata per operare anche in scenari catastrofici:</p><ul><li><strong>Archiviazione Locale (Edge):</strong> I dati risiedono primariamente sul dispositivo dell'utente in un database SQLite cifrato (SQLCipher). Questo garantisce che l'utente mantenga il possesso fisico dei propri dati.</li><li><strong>Rete Mesh Peer-to-Peer (P2P):</strong> In assenza di internet, i dati viaggiano attraverso una rete di dispositivi interconnessi via Bluetooth LE o Wi-Fi Direct. Ogni dispositivo funge da ripetitore, ma senza accesso ai dati (vedere punto 4).</li><li><strong>Sincronizzazione Cloud Sicura:</strong> Quando la connettività viene ripristinata, i dati critici vengono sincronizzati con il server centrale tramite API REST protette, garantendo la coerenza delle cartelle cliniche d'emergenza.</li></ul>` },
                { title: "4. Misure di Sicurezza Tecniche", content: `<p>Per mitigare i rischi di accesso non autorizzato, perdita o alterazione, implementiamo misure di sicurezza allo stato dell'arte:</p><ul><li><strong>Crittografia AES-GCM-256:</strong> Tutti i dati sensibili, sia a riposo che in transito nella rete mesh, sono cifrati con Advanced Encryption Standard (AES) in modalità Galois/Counter Mode (GCM) a 256 bit, garantizando confidenzialità e integrità autenticata.</li><li><strong>Protocollo Blind Relay (RF_16):</strong> I dispositivi che inoltrano i messaggi per conto di altri utenti agiscono come "blind relays" (nodi ciechi). Essi trasportano pacchetti cifrati senza possedere la chiave di decifrazione, rendendo tecnicamente impossibile l'accesso al contenuto dei messaggi di soccorso da parte di terzi intermediari.</li><li><strong>Gestione delle Chiavi:</strong> Utilizzo di curve ellittiche (ECDH e ECDSA) per la negoziazione sicura delle chiavi di sessione e per la firma digitale dei messaggi, prevenendo attacchi Man-in-the-Middle.</li></ul>` },
                { title: "5. Segregazione dei Ruoli e Controllo Accessi", content: `<p>Il sistema impone una rigorosa separazione dei ruoli, definita a livello di codice e immutabile:</p><ul><li><strong>Utente "Rescuee" (Richiedente):</strong> Può accedere, modificare e cancellare esclusivamente i propri dati. Non ha privilegi per consultare dati di altri utenti.</li><li><strong>Utente "Rescuer" (Soccorritore Qualificato):</strong> Ottiene l'accesso temporaneo ai dati sanitari e di posizione del Rescuee solo nel contesto attivo di una missione di soccorso. L'accesso è loggato e monitorato.</li><li><strong>Amministratore di Sistema:</strong> Gestisce l'infrastruttura tecnica ma non possiede le chiavi private per decifrare i dati sanitari degli utenti, garantendo la confidenzialità anche rispetto al gestore del servizio.</li></ul>` },
                { title: "6. Retention Policy e Diritti dell'Interessato", content: `<p><strong>Periodo di Conservazione:</strong> I dati operativi vengono conservati per la durata dell'emergenza. Al termine, vengono archiviati per finalità medico-legali per il periodo prescritto dalla legge (es. 10 anni per la responsabilità medica) o anonimizzati irreversibilmente per scopi statistici e di ricerca.</p><p><strong>Esercizio dei Diritti:</strong> Puoi esercitare in ogni momento il diritto di accesso, rettifica, cancellazione ("diritto all'oblio"), limitazione, portabilità e opposizione. Puoi revocare il consenso tramite le impostazioni dell'app, comportando la cancellazione dei dati locali e remoti. Per reclami, puoi rivolgerti al Garante Privacy nazionale.</p>` },
                { title: "7. Informazioni Legali ", content: `<p><strong>Titolare del Trattamento:</strong> Università degli Studi di Salerno / Dipartimento di Informatica.<br><strong>Contatto:</strong> RescueCom@gmail.com</p><p><strong>DPO (Responsabile della Protezione dei Dati):</strong> Non è stato nominato un DPO in quanto il sistema è un proof of concept a fini accademici.</p><p><strong>Trasferimento Extra-UE:</strong> I dati personali non sono trasferiti al di fuori dell’Unione Europea.</p><p><strong>Autorità di Controllo:</strong> L’interessato ha il diritto di proporre reclamo al Garante per la Protezione dei Dati Personali.</p><p><strong>Natura Obbligatoria del Conferimento:</strong> Il conferimento dei dati essenziali è necessario per l’erogazione del servizio di emergenza. Il mancato conferimento comporta l’impossibilità di utilizzare il sistema.</p>` }
            ],
            'en': [
                { title: "1. Categories of Processed Data and Purposes", content: `<p>In accordance with the data minimization principle, we collect exclusively the information indispensable for effective emergency management:</p><ul><li><strong>Common Identification Data:</strong> First name, last name, date of birth, and a unique user identifier (UUID). These data are used to unmistakably identify the person requesting rescue.</li><li><strong>Special Categories of Data (Health Data):</strong> Processing includes sensitive data critical for medical triage, such as: blood type, known drug allergies, specific disabilities (motor, sensory, or cognitive), and relevant chronic conditions (e.g., diabetes, heart disease).</li><li><strong>Geolocation Data:</strong> Precise GPS coordinates (latitude/longitude) acquired in real-time or manually entered, used exclusively to locate the device in crisis scenarios.</li><li><strong>Technical Telemetry Data:</strong> Metadata regarding battery status and connectivity, necessary to assess node reliability in the mesh network.</li></ul>` },
                { title: "2. Legal Basis for Processing", content: `<p>The processing of your personal data is legitimized by the following legal bases:</p><ul><li><strong>Explicit Consent:</strong> In compliance with the technical system pseudo-requirement PR_L.1, the storage of health data occurs only following free, specific, and informed consent, manifested through an unambiguous positive action (opt-in) in the app.</li><li><strong>Protection of Vital Interests:</strong> In emergency situations where the data subject is physically or legally incapable of giving consent, processing is necessary to protect the life of the data subject or another natural person.</li></ul>` },
                { title: "3. System Architecture and Processing Methods", content: `<p>Processing takes place via a resilient hybrid infrastructure, designed to operate even in catastrophic scenarios:</p><ul><li><strong>Local Storage (Edge):</strong> Data resides primarily on the user's device in an encrypted SQLite database (SQLCipher). This ensures the user maintains physical possession of their data.</li><li><strong>Peer-to-Peer (P2P) Mesh Network:</strong> In the absence of internet, data travels through a network of devices interconnected via Bluetooth LE or Wi-Fi Direct. Each device acts as a relay, but without access to data (see point 4).</li><li><strong>Secure Cloud Synchronization:</strong> When connectivity is restored, critical data is synchronized with the central server via secure REST APIs, ensuring emergency health record consistency.</li></ul>` },
                { title: "4. Technical Security Measures", content: `<p>To mitigate risks of unauthorized access, loss, or alteration, we implement state-of-the-art security measures:</p><ul><li><strong>AES-GCM-256 Encryption:</strong> All sensitive data, both at rest and in transit within the mesh network, are encrypted with Advanced Encryption Standard (AES) in Galois/Counter Mode (GCM) at 256 bits, guaranteeing confidentiality and authenticated integrity.</li><li><strong>Blind Relay Protocol (RF_16):</strong> Devices forwarding messages on behalf of other users act as "blind relays." They transport encrypted packets without possessing the decryption key, making it technically impossible for third-party intermediaries to access the content of rescue messages.</li><li><strong>Key Management:</strong> Use of elliptic curves (ECDH and ECDSA) for secure session key negotiation and digital signature of messages, preventing Man-in-the-Middle attacks.</li></ul>` },
                { title: "5. Role Segregation and Access Control", content: `<p>The system enforces strict role separation, defined at the code level and immutable:</p><ul><li><strong>"Rescuee" User (Requestor):</strong> Can access, modify, and delete exclusively their own data. Does not have privileges to consult other users' data.</li><li><strong>"Rescuer" User (Qualified Responder):</strong> Obtains temporary access to the Rescuee's health and location data only within the active context of a rescue mission. Access is logged and monitored.</li><li><strong>System Administrator:</strong> Manages the technical infrastructure but does not possess private keys to decrypt user health data, ensuring confidentiality even from the service provider.</li></ul>` },
                { title: "6. Retention Policy and Data Subject Rights", content: `<p><strong>Retention Period:</strong> Operational data is retained for the duration of the emergency. Afterward, it is archived for medico-legal purposes for the period prescribed by law (e.g., 10 years for medical liability) or irreversibly anonymized for statistical and research purposes.</p><p><strong>Exercise of Rights:</strong> You may exercise at any time the right of access, rectification, erasure ("right to be forgotten"), restriction, portability, and objection. You can withdraw consent via app settings, resulting in the deletion of local and remote data. For complaints, you may contact the national Privacy Authority.</p>` },
                { title: "7. Legal Information", content: `<p><strong>Data Controller:</strong> University of Salerno / Department of Computer Science.<br><strong>Contact:</strong> RescueCom@gmail.com</p><p><strong>DPO (Data Protection Officer):</strong> A Data Protection Officer (DPO) has not been appointed as the system is an academic proof of concept.</p><p><strong>Extra-EU Transfer:</strong> Personal data are not transferred outside the European Union.</p><p><strong>Supervisory Authority:</strong> The data subject has the right to lodge a complaint with the Data Protection Authority.</p><p><strong>Mandatory Nature of Provision:</strong> The provision of essential data is necessary for the provision of the emergency service. Failure to provide such data entails the impossibility of using the system.</p>` }
            ],
            'es': [
                { title: "1. Categorías de Datos Tratados y Finalidades", content: `<p>De conformidad con el principio de minimización de datos, recopilamos exclusivamente la información indispensable para la gestión eficaz de emergencias:</p><ul><li><strong>Datos Identificativos Comunes:</strong> Nombre, apellidos, fecha de nacimiento y un identificador de usuario único (UUID). Estos datos sirven para identificar inequívocamente a la persona que solicita rescate.</li><li><strong>Categorías Especiales de Datos (Datos de Salud):</strong> El tratamiento incluye datos sensibles críticos para el triaje médico, tales como: grupo sanguíneo, alergias farmacológicas conocidas, discapacidades específicas (motoras, sensoriales o cognitivas) y patologías crónicas relevantes (ej. diabetes, cardiopatías).</li><li><strong>Datos de Geolocalización:</strong> Coordenadas GPS precisas (latitud/longitud) adquiridas en tiempo real o introducidas manualmente, utilizadas exclusivamente para localizar el dispositivo en escenarios de crisis.</li><li><strong>Datos de Telemetría Técnica:</strong> Metadatos relativos al estado de la batería y conectividad, necesarios para evaluar la fiabilidad del nodo en la red mesh.</li></ul>` },
                { title: "2. Base Jurídica del Tratamiento", content: `<p>El tratamiento de sus datos personales está legitimado por las siguientes bases jurídicas:</p><ul><li><strong>Consentimiento Explícito:</strong> En cumplimiento del pseudorequisito técnico del sistema PR_L.1, el almacenamiento de datos de salud se produce solo previo consentimiento libre, específico e informado, manifestado a través de una acción positiva inequívoca (opt-in) en la aplicación.</li><li><strong>Protección de Intereses Vitales:</strong> En situaciones de emergencia donde el interesado se encuentre física o legalmente incapacitado para dar su consentimiento, el tratamiento es necesario para proteger la vida del interesado o de otra persona física.</li></ul>` },
                { title: "3. Arquitectura del Sistema y Modalidades de Tratamiento", content: `<p>El tratamiento se realiza mediante una infraestructura híbrida resiliente, diseñada para operar incluso en escenarios catastróficos:</p><ul><li><strong>Almacenamiento Local (Edge):</strong> Los datos residen principalmente en el dispositivo del usuario en una base de datos SQLite cifrada (SQLCipher). Esto garantiza que el usuario mantenga la posesión física de sus datos.</li><li><strong>Red Mesh Peer-to-Peer (P2P):</strong> En ausencia de internet, los datos viajan a través de una red de dispositivos interconectados vía Bluetooth LE o Wi-Fi Direct. Cada dispositivo actúa como repetidor, pero sin acceso a los datos (ver punto 4).</li><li><strong>Sincronización Cloud Segura:</strong> Cuando se restablece la conectividad, los datos críticos se sincronizan con el servidor central mediante API REST protegidas, garantizando la coherencia de los expedientes médicos de emergencia.</li></ul>` },
                { title: "4. Medidas de Seguridad Técnicas", content: `<p>Para mitigar riesgos de acceso no autorizado, pérdida o alteración, implementamos medidas de seguridad de última generación:</p><ul><li><strong>Cifrado AES-GCM-256:</strong> Todos los datos sensibles, tanto en reposo como en tránsito en la red mesh, están cifrados con Advanced Encryption Standard (AES) en modo Galois/Counter Mode (GCM) a 256 bits, garantizando confidencialidad e integridad autenticada.</li><li><strong>Protocolo Blind Relay (RF_16):</strong> Los dispositivos que reenvían mensajes en nombre de otros usuarios actúan como "blind relays" (nodos ciegos). Transportan paquetes cifrados sin poseer la clave de descifrado, haciendo técnicamente imposible el acceso al contenido de los mensajes de rescate por parte de terceros intermediarios.</li><li><strong>Gestión de Claves:</strong> Uso de curvas elípticas (ECDH y ECDSA) para la negociación segura de claves de sesión y firma digital de los mensajes, previniendo ataques Man-in-the-Middle.</li></ul>` },
                { title: "5. Segregación de Roles y Control de Acceso", content: `<p>El sistema impone una estricta separación de roles, definida a nivel de código e inmutable:</p><ul><li><strong>Usuario "Rescuee" (Solicitante):</strong> Puede acceder, modificar y eliminar exclusivamente sus propios datos. No tiene privilegios para consultar datos de otros usuarios.</li><li><strong>Usuario "Rescuer" (Rescatista Cualificado):</strong> Obtiene acceso temporal a los datos de salud y ubicación del Rescuee solo en el contexto activo de una misión de rescate. El acceso es registrado y monitoreado.</li><li><strong>Administrador del Sistema:</strong> Gestiona la infraestructura técnica pero no posee claves privadas para descifrar datos de salud de usuarios, garantizando confidencialidad incluso respecto al proveedor del servicio.</li></ul>` },
                { title: "6. Política de Retención y Derechos del Interesado", content: `<p><strong>Período de Conservación:</strong> Los datos operativos se conservan durante la emergencia. Posteriormente, se archivan con fines médico-legales por el período prescrito por la ley (ej. 10 años para responsabilidad médica) o se anonimizan irreversiblemente para fines estadísticos y de investigación.</p><p><strong>Ejercicio de Derechos:</strong> Puede ejercer en cualquier momento el derecho de acceso, rectificación, supresión ("derecho al olvido"), limitación, portabilidad y oposición. Puede retirar el consentimiento a través de la configuración de la aplicación, lo que conlleva la eliminación de datos locales y remotos. Para reclamaciones, puede dirigirse a la Autoridad de Privacidad nacional.</p>` },
                { title: "7. Información Legal ", content: `<p><strong>Responsable del Tratamiento:</strong> Universidad de Salerno / Departamento de Informática.<br><strong>Contacto:</strong> RescueCom@gmail.com</p><p><strong>DPO (Delegado de Protección de Datos):</strong> No se ha nombrado un DPO ya que el sistema es una prueba de concepto con fines académicos.</p><p><strong>Transferencia Extra-UE:</strong> Los datos personales no se transfieren fuera de la Unión Europea.</p><p><strong>Autoridad de Control:</strong> El interesado tiene derecho a presentar una reclamación ante la Autoridad de Protección de Datos Personales.</p><p><strong>Carácter Obligatorio de la Provisión:</strong> La provisión de datos esenciales es necesaria para la prestación del servicio de emergencia. La falta de provisión implica la imposibilidad de utilizar el sistema.</p>` }
            ],
            'fr': [
                { title: "1. Catégories de Données Traitées et Finalités", content: `<p>Conformément au principe de minimisation des données, nous collectons exclusivement les informations indispensables à une gestion efficace des urgences :</p><ul><li><strong>Données d'Identification Communes :</strong> Nom, prénom, date de naissance et un identifiant utilisateur unique (UUID). Ces données servent à identifier de manière certaine la personne demandant du secours.</li><li><strong>Catégories Particulières de Données (Données de Santé) :</strong> Le traitement inclut des données sensibles critiques pour le triage médical, telles que : groupe sanguin, allergies médicamenteuses connues, handicaps spécifiques (moteurs, sensoriels ou cognitifs) et pathologies chroniques pertinentes (ex. diabète, maladies cardiaques).</li><li><strong>Données de Géolocalisation :</strong> Coordonnées GPS précises (latitude/longitude) acquises en temps réel ou saisies manuellement, utilisées exclusivement pour localiser l'appareil en scénario de crise.</li><li><strong>Données de Télémétrie Technique :</strong> Métadonnées relatives à l'état de la batterie et à la connectivité, nécessaires pour évaluer la fiabilité du nœud dans le réseau maillé.</li></ul>` },
                { title: "2. Base Juridique du Traitement", content: `<p>Le traitement de vos données personnelles est légitimé par les bases juridiques suivantes :</p><ul><li><strong>Consentement Explicite :</strong> Conformément au pseudo-requis technique du système PR_L.1, le stockage des données de santé n'a lieu qu'après un consentement libre, spécifique et éclairé, manifesté par une action positive sans équivoque (opt-in) dans l'application.</li><li><strong>Sauvegarde des Intérêts Vitaux :</strong> Dans les situations d'urgence où la personne concernée se trouve dans l'incapacité physique ou juridique de donner son consentement, le traitement est nécessaire pour protéger la vie de la personne concernée ou d'une autre personne physique.</li></ul>` },
                { title: "3. Architecture du Système et Modalités de Traitement", content: `<p>Le traitement s'effectue via une infrastructure hybride résiliente, conçue pour fonctionner même dans des scénarios catastrophiques :</p><ul><li><strong>Stockage Local (Edge) :</strong> Les données résident principalement sur l'appareil de l'utilisateur dans une base de données SQLite chiffrée (SQLCipher). Cela garantit que l'utilisateur conserve la possession physique de ses données.</li><li><strong>Réseau Mesh Peer-to-Peer (P2P) :</strong> En l'absence d'internet, les données voyagent à travers un réseau d'appareils interconnectés via Bluetooth LE ou Wi-Fi Direct. Chaque appareil agit comme un relais, mais sans accès aux données (voir point 4).</li><li><strong>Synchronisation Cloud Sécurisée :</strong> Lorsque la connectivité est rétablie, les données critiques sont synchronisées avec le serveur central via des API REST sécurisées, garantissant la cohérence des dossiers médicaux d'urgence.</li></ul>` },
                { title: "4. Mesures de Sécurité Techniques", content: `<p>Pour atténuer les risques d'accès non autorisé, de perte ou d'altération, nous mettons en œuvre des mesures de sécurité de pointe :</p><ul><li><strong>Chiffrement AES-GCM-256 :</strong> Toutes les données sensibles, au repos comme en transit dans le réseau maillé, sont chiffrées avec Advanced Encryption Standard (AES) en mode Galois/Counter Mode (GCM) à 256 bits, garantissant confidentialité et intégrité authentifiée.</li><li><strong>Protocole Blind Relay (RF_16) :</strong> Les appareils relayant des messages pour le compte d'autres utilisateurs agissent comme des "blind relays" (nœuds aveugles). Ils transportent des paquets chiffrés sans posséder la clé de déchiffrement, rendant techniquement impossible l'accès au contenu des messages de secours par des tiers intermédiaires.</li><li><strong>Gestion des Clés :</strong> Utilisation de courbes elliptiques (ECDH et ECDSA) pour la négociation sécurisée des clés de session et la signature numérique des messages, empêchant les attaques Man-in-the-Middle.</li></ul>` },
                { title: "5. Ségrégation des Rôles et Contrôle d'Accès", content: `<p>Le système impose une séparation stricte des rôles, définie au niveau du code et immuable :</p><ul><li><strong>Utilisateur "Rescuee" (Demandeur) :</strong> Peut accéder, modifier et supprimer exclusivement ses propres données. N'a pas les privilèges pour consulter les données d'autres utilisateurs.</li><li><strong>Utilisateur "Rescuer" (Secouriste Qualifié) :</strong> Obtient un accès temporaire aux données de santé et de position du Rescuee uniquement dans le contexte actif d'une mission de secours. L'accès est journalisé et surveillé.</li><li><strong>Administrateur Système :</strong> Gère l'infrastructure technique mais ne possède pas les clés privées pour déchiffrer les données de santé des utilisateurs, garantissant la confidentialité même vis-à-vis du fournisseur de service.</li></ul>` },
                { title: "6. Politique de Conservation et Droits de la Personne Concernée", content: `<p><strong>Période de Conservation :</strong> Les données opérationnelles sont conservées pendant toute la durée de l'urgence. Ensuite, elles sont archivées à des fins médico-légales pour la période prescrite par la loi (par ex. 10 ans pour la responsabilité médicale) ou anonymisées de manière irréversible à des fins statistiques et de recherche.</p><p><strong>Exercice des Droits :</strong> Vous pouvez exercer à tout moment le droit d'accès, de rectification, d'effacement (« droit à l'oubli »), de limitation, de portabilité et d'opposition. Vous pouvez retirer votre consentement via les paramètres de l'application, entraînant la suppression des données locales et distantes. Pour les réclamations, vous pouvez contacter l'Autorité nationale de protection de la vie privée.</p>` },
                { title: "7. Informations Légales ", content: `<p><strong>Responsable du Traitement:</strong> Université de Salerne / Département d'Informatique.<br><strong>Contact:</strong> RescueCom@gmail.com</p><p><strong>DPO (Délégué à la Protection des Données):</strong> Un DPO n'a pas été nommé car le système est une preuve de concept à des fins académiques.</p><p><strong>Transfert Hors UE:</strong> Les données personnelles ne sont pas transférées en dehors de l'Union Européenne.</p><p><strong>Autorité de Contrôle:</strong> La personne concernée a le droit d'introduire une réclamation auprès de l'Autorité de Protection des Données.</p><p><strong>Caractère Obligatoire de la Fourniture:</strong> La fourniture des données essentielles est nécessaire pour la prestation du service d'urgence. Le non-respect de cette obligation entraîne l'impossibilité d'utiliser le système.</p>` }
            ],
            'de': [
                { title: "1. Kategorien verarbeiteter Daten und Zwecke", content: `<p>Gemäß dem Grundsatz der Datenminimierung erheben wir ausschließlich Informationen, die für ein wirksames Notfallmanagement unerlässlich sind:</p><ul><li><strong>Allgemeine Identifikationsdaten:</strong> Vorname, Nachname, Geburtsdatum und eine eindeutige Benutzerkennung (UUID). Diese Daten dienen der zweifelsfreien Identifizierung der Person, die Hilfe anfordert.</li><li><strong>Besondere Datenkategorien (Gesundheitsdaten):</strong> Die Verarbeitung umfasst sensible Daten, die für die medizinische Triage kritisch sind, wie: Blutgruppe, bekannte Medikamentenallergien, spezifische Behinderungen (motorisch, sensorisch oder kognitiv) und relevante chronische Erkrankungen (z.B. Diabetes, Herzerkrankungen).</li><li><strong>Geolokalisierungsdaten:</strong> Präzise GPS-Koordinaten (Breitengrad/Längengrad) acquired in real-time oder manuell eingegeben werden und ausschließlich zur Lokalisierung des Geräts in Krisenszenarien dienen.</li><li><strong>Technische Telemetriedaten:</strong> Metadaten zum Batteriestatus und zur Konnektivität, die zur Bewertung der Zuverlässigkeit des Knotens im Mesh-Netzwerk erforderlich sind.</li></ul>` },
                { title: "2. Rechtsgrundlage der Verarbeitung", content: `<p>Die Verarbeitung Ihrer personenbezogenen Daten wird durch folgende Rechtsgrundlagen legitimiert:</p><ul><li><strong>Ausdrückliche Einwilligung:</strong> In Übereinstimmung mit der technischen System-Pseudo-Anforderung PR_L.1 erfolgt die Speicherung von Gesundheitsdaten nur nach freier, spezifischer und informierter Einwilligung, die durch eine eindeutige bestätigende Handlung (Opt-in) in der App erfolgt.</li><li><strong>Schutz lebenswichtiger Interessen:</strong> In Notfallsituationen, in denen die betroffene Person physisch oder rechtlich nicht in der Lage ist, ihre Einwilligung zu geben, ist die Verarbeitung zum Schutz des Lebens der betroffenen Person oder einer anderen natürlichen Person erforderlich.</li></ul>` },
                { title: "3. Systemarchitektur und Verarbeitungsmethoden", content: `<p>Die Verarbeitung erfolgt über eine resiliente hybride Infrastruktur, die für den Betrieb auch in Katastrophenszenarien ausgelegt ist:</p><ul><li><strong>Lokale Speicherung (Edge):</strong> Daten befinden sich primär auf dem Gerät des Benutzers in einer verschlüsselten SQLite-Datenbank (SQLCipher). Dies stellt sicher, dass der Benutzer den physischen Besitz seiner Daten behält.</li><li><strong>Peer-to-Peer (P2P) Mesh-Netzwerk:</strong> Ohne Internet reisen Daten durch ein Netzwerk von Geräten, die über Bluetooth LE oder Wi-Fi Direct verbunden sind. Jedes Gerät fungiert als Relay, jedoch ohne Zugriff auf die Daten (siehe Punkt 4).</li><li><strong>Sichere Cloud-Synchronisation:</strong> Wenn die Konnektivität wiederhergestellt ist, werden kritische Daten über sichere REST-APIs mit dem zentralen Server synchronisiert, um die Konsistenz der Notfall-Gesundheitsakten zu gewährleisten.</li></ul>` },
                { title: "4. Technische Sicherheitsmaßnahmen", content: `<p>Um Risiken durch unbefugten Zugriff, Verlust oder Änderung zu mindern, implementieren wir Sicherheitsmaßnahmen auf dem neuesten Stand der Technik:</p><ul><li><strong>AES-GCM-256-Verschlüsselung:</strong> Alle sensiblen Daten, sowohl im Ruhezustand als auch bei der Übertragung im Mesh-Netzwerk, werden mit dem Advanced Encryption Standard (AES) im Galois/Counter Mode (GCM) mit 256 Bit verschlüsselt, was Vertraulichkeit und authentifizierte Integrität garantiert.</li><li><strong>Blind Relay Protokoll (RF_16):</strong> Geräte, die Nachrichten im Auftrag anderer Benutzer weiterleiten, fungieren als "Blind Relays" (blinde Knoten). Sie transportieren verschlüsselte Pakete, ohne den Entschlüsselungsschlüssel zu besitzen, was den Zugriff auf den Inhalt von Rettungsnachrichten durch dritte Vermittler technisch unmöglich macht.</li><li><strong>Schlüsselverwaltung:</strong> Verwendung elliptischer Kurven (ECDH und ECDSA) für die sichere Aushandlung von Sitzungsschlüsseln und die digitale Signatur von Nachrichten, um Man-in-the-Middle-Angriffe zu verhindern.</li></ul>` },
                { title: "5. Rollentrennung und Zugriffskontrolle", content: `<p>Das System erzwingt eine strikte Rollentrennung, die auf Code-Ebene definiert und unveränderlich ist:</p><ul><li><strong>Benutzer "Rescuee" (Antragsteller):</strong> Kann ausschließlich auf seine eigenen Daten zugreifen, diese ändern und löschen. Hat keine Berechtigungen, Daten anderer Benutzer einzusehen.</li><li><strong>Benutzer "Rescuer" (Qualifizierter Retter):</strong> Erhält temporären Zugriff auf die Gesundheits- und Standortdaten des Rescuee nur im aktiven Kontext einer Rettungsmission. Der Zugriff wird protokolliert und überwacht.</li><li><strong>Systemadministrator:</strong> Verwaltet die technische Infrastruktur, besitzt jedoch keine privaten Schlüssel zur Entschlüsselung von Benutzergesundheitsdaten, wodurch die Vertraulichkeit auch gegenüber dem Dienstanbieter gewahrt bleibt.</li></ul>` },
                { title: "6. Aufbewahrungsrichtlinie und Rechte der betroffenen Person", content: `<p><strong>Aufbewahrungsfrist:</strong> Betriebsdaten werden für die Dauer des Notfalls aufbewahrt. Danach werden sie zu medizinisch-rechtlichen Zwecken für den gesetzlich vorgeschriebenen Zeitraum (z. B. 10 Jahre für die ärztliche Haftung) archiviert oder irreversibel für statistische und Forschungszwecke anonymisiert.</p><p><strong>Ausübung der Rechte:</strong> Sie können jederzeit das Recht auf Auskunft, Berichtigung, Löschung („Recht auf Vergessenwerden“), Einschränkung, Übertragbarkeit und Widerspruch ausüben. Sie können Ihre Einwilligung über die App-Einstellungen widerrufen, was zur Löschung lokaler und entfernter Daten führt. Für Beschwerden können Sie sich an die nationale Datenschutzbehörde wenden.</p>` },
                { title: "7. Obligatorische Rechtsinformationen", content: `<p><strong>Verantwortlicher:</strong> Universität Salerno / Fachbereich Informatik.<br><strong>Kontakt:</strong> RescueCom@gmail.com</p><p><strong>DSB (Datenschutzbeauftragter):</strong> Ein Datenschutzbeauftragter (DSB) wurde nicht ernannt, da es sich beim System um einen akademischen Proof of Concept handelt.</p><p><strong>Übermittlung außerhalb der EU:</strong> Personenbezogene Daten werden nicht außerhalb der Europäischen Union übertragen.</p><p><strong>Aufsichtsbehörde:</strong> Die betroffene Person hat das Recht, Beschwerde bei der Datenschutzbehörde einzureichen.</p><p><strong>Verpflichtende Bereitstellung:</strong> Die Bereitstellung wesentlicher Daten ist für die Erbringung des Notdienstes erforderlich. Die Nichtbereitstellung führt dazu, dass das System nicht genutzt werden kann.</p>` }
            ],
        };

        return data[lang] || data['en'];
    }

    render() {
        // Imposta l'inglese come predefinito se la lingua non è impostata o non è supportata
        let lang = this.getAttribute('lang') || 'en';
        lang = ['it', 'en', 'es', 'fr', 'de'].includes(lang) ? lang : 'en';

        // Ottieni il contenuto Hero
        const heroContent = this.getContent(lang);

        // Ottieni i dati delle fisarmoniche
        const accordionsData = this.getAccordions(lang);

        let accordionHTML = `
            <section class="section-transparency-accordion">
                <div class="section-content">
                    <ul class="accordion-wrapper">
        `;

        accordionsData.forEach((item, index) => {
            accordionHTML += `
                <li class="accordion-item">
                    <button class="header-wrapper" aria-expanded="false">
                        <h2 class="accordion-headline">${item.title}</h2>
                        <div class="icon-plus"></div>
                    </button>
                    <div class="accordion-panel">
                        <div class="accordion-content">
                            ${item.content}
                        </div>
                    </div>
                </li>
            `;
        });

        accordionHTML += `
                    </ul>
                </div>
            </section>
        `;


        this.shadowRoot.innerHTML = `
            <style>
                ${this.getStyles()}
            </style>
            <section class="section-hero">
                <div class="section-content">
                    ${heroContent}
                </div>
            </section>
            ${accordionHTML}
        `;

        this.addEventListeners();
    }

    addEventListeners() {
        const accordions = this.shadowRoot.querySelectorAll('.accordion-item');
        accordions.forEach(item => {
            const header = item.querySelector('.header-wrapper');
            header.addEventListener('click', () => {
                const isOpen = item.classList.contains('active');
                item.classList.toggle('active');
                header.setAttribute('aria-expanded', !isOpen);
            });
        });

        const langLinks = this.shadowRoot.querySelectorAll('.lang-link');
        langLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const newLang = link.getAttribute('data-lang');
                this.setAttribute('lang', newLang);

                // Opzionale: aggiorna l'URL senza ricaricare per riflettere lo stato della lingua
                const url = new URL(window.location);
                url.searchParams.set('lang', newLang);
                window.history.pushState({}, '', url);
            });
        });
    }
}

customElements.define('rescue-gdpr', RescueGDPR);
