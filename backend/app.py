from flask import Flask

import sqlalchemy as db
import pw


print("mysql://{pw.DBUSER}:{pw.DBPW}@{pw.DBHOST}:{pw.DBPORT}/{pw.DB}")
engine = db.create_engine(
    "mysql://{pw.DBUSER}:{pw.DBPW}@{pw.DBHOST}:{pw.DBPORT}/{pw.DB}"
)

app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/controlloPresenze", methods=["GET", "POST"])
def controlloPresenze():
    pass
