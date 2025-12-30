# mock_data.py
def get_mock_richieste():
    return [
        {
            "id": 1,
            "stato": "IN ATTESA",
            "timestamp": "2025-12-30 10:45",
            "posizione": "Via Roma 10, Torino",
            "descrizione": "Gamba rotta",
            "priorita": "MEDIA",
            "utente": {"nome": "Mario", "cognome": "Rossi"}
        },
        {
            "id": 2,
            "stato": "IN GESTIONE",
            "timestamp": "2025-12-30 11:20",
            "posizione": "Corso Milano 5, Torino",
            "descrizione": "Braccio rotto",
            "priorita": "ALTA",
            "utente": {"nome": "Luigi", "cognome": "Bianchi"}
        }
    ]