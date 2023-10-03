from flask import Flask, request

import sqlalchemy as db
import pw


print(f"mysql://{pw.DBUSER}:{pw.DBPW}@{pw.DBHOST}:{pw.DBPORT}/{pw.DB}")
engine = db.create_engine(
    f"mysql://{pw.DBUSER}:{pw.DBPW}@{pw.DBHOST}:{pw.DBPORT}/{pw.DB}"
)
connection = engine.connect()
metadata = db.MetaData()
dbpresenze = db.Table("presenze", metadata, autoload=True, autoload_with=engine)

app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)


@app.route("/controlloPresenze", methods=["GET", "POST"])
def controlloPresenze():
    codice = request.json["codice"]
    select = db.select([dbpresenze]).where(dbpresenze.columns.codice == f"{codice}")
    if select == None:
        response = {msg: "Codice non trovato", code: 404}
    else:
        pass
