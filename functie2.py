from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def create_table():
    conn = mysql.connector.connect(host='localhost', user='root', password='root', database='virtuals')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS poarta2 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data DATETIME NOT NULL,
            sens VARCHAR(45) NOT NULL,
            idPersoana INT NOT NULL,
            idPoarta INT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
create_table()

@app.route('/Poarta2', methods=['POST'])
def JSONFile():
    try:
        input = request.json
        for key in ['data', 'sens', 'idPersoana', 'idPoarta']:
            if key not in input:
                return jsonify({"eroare": f"Valoare negăsită pentru cheia '{key}'!"}), 400
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='virtuals')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO poarta2 (data, sens, idPersoana, idPoarta)
            VALUES (%s, %s, %s, %s)
        """, (input['data'], input['sens'], input['idPersoana'], input['idPoarta']))
        conn.commit()
        conn.close()
        return jsonify({"mesaj": "Perfect, date adăugate!"}), 200

    except Exception as e:
        return jsonify({"eroare": f"Ceva nu a mers cum trebuie: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

