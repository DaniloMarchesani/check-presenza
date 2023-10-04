from flask import Flask, request, jsonify
import flask_cors

import sqlalchemy as db
import json
from datetime import datetime

import pw


print(f"mysql://{pw.DBUSER}:{pw.DBPW}@{pw.DBHOST}:{pw.DBPORT}/{pw.DB}")
engine = db.create_engine(
    f"mysql://{pw.DBUSER}:{pw.DBPW}@{pw.DBHOST}:{pw.DBPORT}/{pw.DB}"
)
connection = engine.connect()
metadata = db.MetaData()
dbutenti = db.Table("utenti", metadata, autoload=True, autoload_with=engine)
dbpresenze = db.Table("presenze", metadata, autoload=True, autoload_with=engine)

app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)


@app.route("/controlloPresenze", methods=["GET", "POST"])
def controlloPresenze():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    giorno = ""  # ricavare il giorno dal timestamp
    codice = request.json["codice"]
    fetchutenti = db.select([dbutenti]).where(dbpresenze.columns.codice == f"{codice}")
    if fetchutenti == None:
        response = jsonify({"msg": "Codice non trovato", "code": 404})

    else:
        fetchpresenze = db.select([dbpresenze]).where(
            dbpresenze.columns.codice == f"{codice}"
        )  # dovrei filtrarlo anche per giorno con: .where(dbpresenze.columns.entrata == f"{giorno}")
        if fetchpresenze == None:
            stmt = db.insert([dbpresenze]).values(
                entrata=f"{giorno}", codice=f"{codice}"
            )
            connection.execute(stmt)
        else:
            upd = (
                db.update([dbpresenze])
                .values(uscita=f"{timestamp}")
                .where(codice=f"{codice}", entrata=f"{giorno}")
            )
            connection.execute(upd)
    response = jsonify({"msg": "ok", "code": 200})

    return response
