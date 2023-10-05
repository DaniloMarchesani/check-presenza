from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pw

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

# Configurazione del database
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql://{pw.DBUSER}:{pw.DBPW}@{pw.DBHOST}:{pw.DBPORT}/{pw.DB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inizializzazione dell'estensione SQLAlchemy
db = SQLAlchemy(app)


class Utenti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30))
    cognome = db.Column(db.String(30))
    codice = db.Column(db.String(10), unique=True, nullable=False)
    presente = db.Column(db.Boolean, default=False)


class Presenze(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    giorno = db.Column(db.String(10))
    entrata = db.Column(db.TIMESTAMP)
    uscita = db.Column(db.TIMESTAMP)
    codice = db.Column(db.String(10))
    valido = db.Column(db.Boolean, default=False)


@app.route("/controlloPresenze", methods=["GET", "POST"])
def controlloPresenze():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    giorno = now.date()
    codice = request.json["codice"]
    # Prendo gli utenti con quel codice dal database
    fetchutenti = Utenti.query.filter_by(codice=codice).all()
    # fetchutenti=db.session.execute(db.select(Utenti).filter_by(codice=codice).all())
    # Controllo se è stato trovato un record
    print(fetchutenti)
    if not fetchutenti:
        response = jsonify({"msg": "Codice non trovato", "code": 404})
    else:
        sqlpresenze = Presenze.query.filter_by(codice=codice).filter_by(giorno=giorno)
        presenze_list = [
            {
                "id": presenza.id,
                "giorno": presenza.giorno,
                "entrata": presenza.entrata,
                "uscita": presenza.uscita,
                "codice": presenza.codice,
                "valido": presenza.valido,
            }
            for presenza in sqlpresenze
        ]
        print(presenze_list)
        # se non esiste il record della presenza lo crea con l'entrata
        if not presenze_list:
            insert = Presenze(codice=codice, giorno=giorno)  # , entrata=timestamp)
            db.session.add(insert)
            db.session.commit()
            response = jsonify({"msg": "Entrata registrata", "code": 201})
        else:  # altrimenti aggiorno l'uscita
            sqlpresenze.uscita = timestamp
            db.session.commit()
            response = jsonify({"msg": "Uscita registrata", "code": 202})

    return response
