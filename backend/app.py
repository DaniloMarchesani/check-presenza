# IMPORTS #
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

import pw
# ---#


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
    """
    Class 'Utenti'

    -   This Class represents the 'Utenti' model table
        in the 'checkPresenze' database
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30))
    cognome = db.Column(db.String(30))
    codice = db.Column(db.String(10), unique=True, nullable=False)
    presente = db.Column(db.Boolean, default=False)


class Presenze(db.Model):
    """
    Class 'Presenze'

    -   This Class represents the 'Presenze' model table
        in the 'checkPresenze' database   
    """
    id = db.Column(db.Integer, primary_key=True)
    giorno = db.Column(db.String(10))
    entrata = db.Column(db.TIMESTAMP)
    uscita = db.Column(db.TIMESTAMP)
    codice = db.Column(db.String(10))
    valido = db.Column(db.Boolean, default=False)


@app.route("/controlloPresenze", methods=["GET", "POST"])
def controlloPresenze():
    codice = request.json["codice"]
    time = datetime.now()
    giorno = time.date()

    #Dato il codice eseguo un select alla tabella utenti filtrato per id per ricevere i dati
    #dell'utente
    fetchutenti = Utenti.query.filter_by(codice=codice).all()

    #Controllo se è stato trovato un utente
    if not fetchutenti:
        #Se il codice immesso non appartiene a nessun utente in database
        #Ritorna il messaggio "Codice non trovato" con codice 404
        response = jsonify({"msg": "Codice non trovato", "code": 404})
    else:
        # In caso di utente trovato, vado a prelevare dal database le sue presenze 'aperte'
        # ovvero quelle da cui non è ancora stata registrata l'uscita
        presenza_list = []
        sqlpresenze = (
            Presenze.query.filter_by(codice=codice)
            .filter_by(giorno=giorno)
            .filter_by(valido=1)
        )
        for presenza in sqlpresenze:
            presenza_dict = {"id": presenza.id,
                             "giorno": presenza.giorno,
                             "entrata": presenza.entrata,
                             "uscita": presenza.uscita,
                             "codice": presenza.codice,
                             "valido": presenza.valido,
                             }
            presenza_list.append(presenza_dict)

        # Nel caso di NESSUNA presenza 'aperta' si procede con la creazione di essa al
        # tempo corrente
        # Ritorna il messaggio "Entrata registrata" con codice 201
        if not presenza_list:
            insert = Presenze(codice=codice, giorno=giorno,
                              entrata=time, valido=1)
            db.session.add(insert)
            db.session.commit()
            response = jsonify({"msg": "Entrata registrata", "code": 201})

        # Altrimenti, se ESISTE una presenza 'aperta' si procede con la sua chiusura al tempo
        # corrente
        # Ritorna il messaggio "Uscita registrata" con codice 202
        else:
            update = (
                Presenze.query.filter_by(codice=codice)
                .filter_by(giorno=giorno)
                .filter_by(valido=1)
                .update(dict(uscita=time, valido=0))
            )
            db.session.commit()
            response = jsonify({"msg": "Uscita registrata", "code": 202})

    return response
