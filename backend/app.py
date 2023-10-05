from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

import pw

app = Flask(__name__)
CORS(app)

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
    time = datetime.now()
    giorno = time.date()
    print(request.json)
    codice = request.json["codice"]
    # Prendo gli utenti con quel codice dal database
    fetchutenti = Utenti.query.filter_by(codice=codice).all()
    # fetchutenti=db.session.execute(db.select(Utenti).filter_by(codice=codice).all())
    # Controllo se è stato trovato un record

    if not fetchutenti:
        response = jsonify({"msg": "Codice non trovato", "code": 404})
    else:
        sqlpresenze = (
            Presenze.query.filter_by(codice=codice)
            .filter_by(giorno=giorno)
            .filter_by(valido=1)
        )
        presenza_list = [
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

        # se non esiste il record della presenza lo crea con l'entrata

        if not presenza_list:
            insert = Presenze(codice=codice, giorno=giorno, entrata=time, valido=1)
            # print("insert:\n" + insert)
            db.session.add(insert)
            db.session.commit()
            response = jsonify({"msg": "Entrata registrata", "code": 201})
        else:  # altrimenti aggiorno l'uscita
            update = (
                Presenze.query.filter_by(codice=codice)
                .filter_by(giorno=giorno)
                .filter_by(valido=1)
                .update(dict(uscita=time, valido=0))
            )
            db.session.commit()
            response = jsonify({"msg": "Uscita registrata", "code": 202})

    return response
