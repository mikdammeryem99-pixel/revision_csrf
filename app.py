from flask import Flask, request, render_template, session
import secrets

app = Flask(__name__)

# Secret key (في production خاصها تكون variable d’environnement)
app.secret_key = "dev-secret"

# Génération d'un CSRF token
def generate_csrf_token():
    token = secrets.token_hex(16)
    session["csrf_token"] = token
    return token

# Page principale
@app.route("/")
def index():
    token = generate_csrf_token()
    return render_template("form.html", csrf_token=token)

# Traitement du formulaire
@app.route("/submit", methods=["POST"])
def submit():
    form_token = request.form.get("csrf_token")
    session_token = session.get("csrf_token")

    # Vérification CSRF
    if not form_token or form_token != session_token:
        return " Échec CSRF - requête invalide."

    message = request.form.get("message")
    return f" Requête acceptée. Message reçu : {message}"

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
