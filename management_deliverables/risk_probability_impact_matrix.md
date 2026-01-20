# Risk Probability/Impact Matrix - RescueCom

## Matrice Probabilità/Impatto

Legenda livelli:
- **Probabilità**: 
  - Basso (B): 0.0-0.40
  - Medio (M): 0.41-0.65
  - Alto (A): 0.66-1.0

- **Impatto**:
  - Basso (B): 0.0-0.40
  - Medio (M): 0.41-0.65
  - Alto (A): 0.66-1.0

---

### Matrice

|                | **Impatto Basso (B)** | **Impatto Medio (M)** | **Impatto Alto (A)** |
|----------------|:---------------------:|:---------------------:|:--------------------:|
| **Prob. Alta (A)** |                       |                       |                      |
| **Prob. Media (M)** | R-13                  | R-05, R-07, R-09, R-17 | R-01, R-02, R-03, R-04, R-11, R-12, R-18 |
| **Prob. Bassa (B)** |                       | R-14                  | R-06, R-08, R-15, R-16 |

---

## Dettaglio Classificazione Rischi

### Probabilità ALTA (0.66-1.0) - Impatto ALTO (0.66-1.0)
Nessun rischio in questa categoria.

### Probabilità MEDIA (0.41-0.65) - Impatto ALTO (0.66-1.0)
- **R-01**: Requisiti ambigui/incompleti (P=0.55, I=0.70, Rank=0.385)
- **R-02**: Assunzioni errate sul processo di emergenza (P=0.40, I=0.75, Rank=0.300)
- **R-03**: Sottostima effort integrazione componenti (P=0.60, I=0.70, Rank=0.420)
- **R-04**: Stime dei test insufficienti (P=0.50, I=0.80, Rank=0.400)
- **R-11**: Scarsa comunicazione interna (P=0.60, I=0.65, Rank=0.390)
- **R-12**: Competenze tecniche insufficienti (P=0.50, I=0.75, Rank=0.375)
- **R-18**: Bug critici in funzionalità core (P=0.40, I=0.90, Rank=0.360)

### Probabilità MEDIA (0.41-0.65) - Impatto MEDIO (0.41-0.65)
- **R-05**: Buffer temporali insufficienti (P=0.45, I=0.60, Rank=0.270)
- **R-07**: Ritardi consegna documenti preparatori (P=0.45, I=0.60, Rank=0.270)
- **R-09**: Documentazione finale incompleta (P=0.45, I=0.60, Rank=0.270)
- **R-17**: Ambienti di sviluppo diversi (P=0.50, I=0.60, Rank=0.300)

### Probabilità MEDIA (0.41-0.65) - Impatto BASSO (0.0-0.40)
- **R-13**: Conflitti interpersonali non gestiti (P=0.35, I=0.60, Rank=0.210)

### Probabilità BASSA (0.0-0.40) - Impatto ALTO (0.66-1.0)
- **R-06**: Mancata coordinazione/pianificazione (P=0.50, I=0.65, Rank=0.325)
- **R-08**: Scope creep (P=0.50, I=0.70, Rank=0.350)
- **R-15**: Dipendenze esterne problematiche (P=0.45, I=0.70, Rank=0.315)
- **R-16**: Problemi di build/deploy all'ultimo momento (P=0.50, I=0.75, Rank=0.375)

### Probabilità BASSA (0.0-0.40) - Impatto MEDIO (0.41-0.65)
- **R-14**: Dipendenza su singolo membro per conoscenze critiche (P=0.40, I=0.75, Rank=0.300)

---

## Top 5 Rischi per Ranking

1. **R-03**: Sottostima effort integrazione componenti (Rank=0.420)
2. **R-04**: Stime dei test insufficienti (Rank=0.400)
3. **R-11**: Scarsa comunicazione interna (Rank=0.390)
4. **R-01**: Requisiti ambigui/incompleti (Rank=0.385)
5. **R-12**: Competenze tecniche insufficienti (Rank=0.375)

---

*Nota: I rischi sono stati mappati secondo i valori di probabilità e impatto del Risk Management Plan. La matrice evidenzia le aree che richiedono maggiore attenzione e mitigazione.*
