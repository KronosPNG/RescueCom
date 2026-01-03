"""
data.py
Modulo contenente i dati mock per l'applicazione RescueCom.
Utilizzato per simulare il database durante lo sviluppo e test offline.
"""

MOCK_REQUESTS = [
    {
        "id": "1",
        "name": "Mario",
        "surname": "Rossi",
        "birthday": "1975-05-20",
        "age": 50,
        "bloodtype": "A+",
        "healthinfo": {
            "allergie": "antibiotici",
            "disabilita": "motoria",
            "malattie": "asma, diabete tipo 2, Portatore di Pacemaker, epilessia"
        },
        "emtype": "Incidente Stradale",
        "emdescription": "Sanguinamento grave, Arti bloccati, Respirazione faticosa",
        "emposition": "via parmenide Milano",
        "empicture": "/static/img/dummy_accident.png",
        "emscore": "grave",
        "location": {"lat": 45.4642, "lng": 9.1900} 
    },
    {
        "id": "2",
        "name": "Luigi",
        "surname": "Verdi",
        "birthday": "1994-11-10",
        "age": 30,
        "bloodtype": "0+",
        "healthinfo": {
            "allergie": "nessuna",
            "disabilita": "nessuna",
            "malattie": "nessuna"
        },
        "emtype": "Malore",
        "emdescription": "Svenimento improvviso",
        "emposition": "Piazza Duomo",
        "empicture": "/static/img/dummy_accident.png",
        "emscore": "moderato",
        "location": {"lat": 45.4641, "lng": 9.1919}
    },
    {
        "id": "3",
        "name": "Antonio",
        "surname": "Viola",
        "birthday": "2004-03-15",
        "age": 20,
        "bloodtype": "B-",
        "healthinfo": {
            "allergie": "polline",
            "disabilita": "nessuna",
            "malattie": "nessuna"
        },
        "emtype": "Trauma",
        "emdescription": "Caduta da bicicletta",
        "emposition": "Parco Sempione",
        "empicture": "/static/img/dummy_accident.png",
        "emscore": "lieve",
        "location": {"lat": 45.4720, "lng": 9.1770}
    },
     {
        "id": "4",
        "name": "Giulia",
        "surname": "Bianchi",
        "birthday": "1990-01-20",
        "age": 35,
        "bloodtype": "AB-",
        "healthinfo": {
            "allergie": "nessuna",
            "disabilita": "visiva",
            "malattie": "ipertesione"
        },
        "emtype": "Intossicazione",
        "emdescription": "Ingestione sostanza tossica",
        "emposition": "Via Roma 10",
        "empicture": "/static/img/dummy_accident.png",
        "emscore": "grave",
        "location": {"lat": 45.4600, "lng": 9.1800}
    }
]
