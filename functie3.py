from flask import Flask, request, jsonify
import mysql.connector


def creareTabelaUtilizatori():
    conn=mysql.connector.connect(host='localhost', user='root',  password='root', database='users')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `users`.`users` (`ID` INT NOT NULL AUTO_INCREMENT,`Nume` VARCHAR(45) NOT NULL,`Prenume` VARCHAR(45) NOT NULL,`Companie` VARCHAR(45) NOT NULL,`IdManager` INT NOT NULL,PRIMARY KEY (`ID`));")
    conn.commit()
    conn.close()

app=Flask(__name__)
@app.route('/user', methods=['POST'])
def inregistrareUtilizatori():
    try:
        input = request.json
        for key in ['Nume', 'Prenume', 'Companie','IdManager']:
            if key not in input:
                return jsonify({"eroare": f"Valoare negăsită pentru cheia '{key}'!"}), 400
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='users')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (Nume, Prenume, Companie, idManager)
            VALUES (%s, %s, %s, %s)
        """, (input['Nume'], input['Prenume'], input['Companie'], input['IdManager']))
        conn.commit()
        conn.close()
        return jsonify({"mesaj": "Perfect, date adăugate!"}), 200

    except Exception as e:
        return jsonify({"eroare": f"Ceva nu a mers cum trebuie: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
