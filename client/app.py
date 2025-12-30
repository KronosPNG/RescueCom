from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/detail/<id>")
def detail(id):
    return render_template("detail.html", id=id)

# Catch-all for other static templates if needed, but explicit is better.
# We'll stick to explicit routes for now to avoid the previous error.

if __name__ == "__main__":
    print("RescueCom Client running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
