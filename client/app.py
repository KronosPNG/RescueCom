from flask import Flask, render_template
from data import MOCK_REQUESTS

app = Flask(__name__, template_folder="templates", static_folder="static")

"""
RescueCom Client Application
Questa applicazione Flask gestisce la dashboard per la ricezione delle richieste di soccorso.
Utilizza il Server-Side Rendering (SSR) per visualizzare i dati in modo efficiente e affidabile.
"""

@app.route("/")
def index():
    """
    Rotta principale.
    Reindirizza l'utente direttamente alla dashboard.
    """
    return dashboard()

@app.route("/dashboard")
def dashboard():
    """
    Rotta per la Dashboard.
    Raggruppa le richieste di soccorso per priorità (grave, moderato, lieve)
    e le passa al template per il rendering.
    """
    # Raggruppa le richieste per priorità
    grouped_requests = {
        "grave": [],
        "moderato": [],
        "lieve": []
    }
    
    for req in MOCK_REQUESTS:
        # Ottieni lo score, default a 'lieve' se manca
        score = req.get("emscore", "lieve").lower()
        
        if score in grouped_requests:
            grouped_requests[score].append(req)
        else:
            grouped_requests["lieve"].append(req)

    return render_template("dashboard.html", groups=grouped_requests)

@app.route("/detail/<id>")
def detail(id):
    """
    Rotta per il Dettaglio Richiesta.
    Cerca una specifica richiesta per ID nei dati mock e la visualizza.
    """
    # Cerca la richiesta con l'ID specificato
    request_data = next((r for r in MOCK_REQUESTS if r["id"] == id), None)
    
    if not request_data:
        return "Richiesta non trovata", 404
        
    return render_template("detail.html", request=request_data)

if __name__ == "__main__":
    print("RescueCom Client in esecuzione su http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
