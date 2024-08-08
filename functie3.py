from abc import ABC, abstractmethod
from flask import Flask, request, jsonify
import mysql.connector

class initializareInregistrare(ABC):
    def __init__(self, db):
        self.db = db

    @abstractmethod
    def creareTabelaUtilizatori(self):
        pass
    @abstractmethod
    def inregistrareUtilizatori(self):
        pass 

class Database():
    def __init__(self, host, user, password, database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.connection=None
    def conexiune(self):
        self.connection=mysql.connector.connect(host='localhost', user='root',  password='root', database='users')
        self.cursor=self.connection.cursor()
    def executareaConexiune(self, query, values):
        self.conexiune()
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        self.close()
    def rezultatConexiune(self, query, values=None):
        self.conexiune()
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        rezultatInregistrare=self.cursor.fetchall()
        self.close()
        return rezultatInregistrare
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
class formareTabel(initializareInregistrare):
    def creareTabelaUtilizatori(self):
        query="CREATE TABLE IF NOT EXISTS `users`.`users` (`ID` INT NOT NULL AUTO_INCREMENT,`Nume` VARCHAR(45) NOT NULL,`Prenume` VARCHAR(45) NOT NULL,`Companie` VARCHAR(45) NOT NULL,`IdManager` INT NOT NULL,PRIMARY KEY (`ID`));"
        self.db.executareaConexiune(query)
    def inregistrareDate(self, input):
        query="""INSERT INTO users (Nume, Prenume, Companie, idManager) VALUES (%s, %s, %s, %s)
        """
        values = (input['Nume'], input['Prenume'], input['Companie'], input['IdManager'])
        self.db.executareaConexiune(query,values)
db = Database(host='localhost', user='root', password='root', database='users')
formare_tabel = formareTabel(db)
formare_tabel.creareTabelaUtilizatori()

app=Flask(__name__)
@app.route('/user', methods=['POST'])
def inregistrareUtilizatori():
    try:
        input = request.json
        for key in ['Nume', 'Prenume', 'Companie','IdManager']:
            if key not in input:
                return jsonify({"eroare": f"Valoare negăsită pentru cheia '{key}'!"}), 400
            formare_tabel.inregistrareDate(input)
            return jsonify({"mesaj": "Perfect, date adăugate!"}), 200
    except Exception as e:
        return jsonify({"eroare": f"Ceva nu a mers cum trebuie: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)







    
