from flask import Flask, request, jsonify
import json,os
import time, mysql.connector,shutil#pt mmutare

def Poarta_fisiere_intrari(file_path, backup_folder, folder_entries):
    file_path='Poarta1.txt'
    backup_folder='backup_intrari'
    folder_entries='intrari'
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    conexiune=mysql.connector.connect(host='localhost', user='root', password='root', database='in_outs')
    cursor=conexiune.cursor()
    cursor.execute("CREATE TABLE `in_outs`.`poarta_acces` ( `id` INT NOT NULL, `numar_poarta` VARCHAR(45) NULL,`tip_fisier` VARCHAR(45) NULL,`data_acces` DATETIME NULL,PRIMARY KEY (`id`));")
    conexiune.commit()
    while True:
        entry_files=os.listdir(folder_entries)
        for file in entry_files:
            file_path=os.path.join(backup_folder,file)
            if os.path.isfile(file_path):
                nume_poarta, extensie=os.path.splitext(file) 
                nume_poarta=int(nume_poarta.replace,('Poarta', ' ')) #inlocuiesc poarta cu un numar
                with open(os.path.join(folder_entries,file), 'r') as fisier: #alatur fisierul in folderul corespunzator
                    data_access=fisier.read().split() #oferim acces
                cursor.execute('INSERT INTO poarta_acces( `numar_poarta`,`tip_fisier`,data_acces`) VALUES (%s, %s, %s)' )(nume_poarta, extensie, data_access)
                conexiune.commit()
                
        time.sleep(20)



from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Funcție pentru crearea tabelei dacă nu există
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
        input_data = request.json
        for key in ['data', 'sens', 'idPersoana', 'idPoarta']:
            if key not in input_data:
                return jsonify({"eroare": f"Valoare negăsită pentru cheia '{key}'!"}), 400

        # Conectează-te la baza de date
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='virtuals')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO poarta2 (data, sens, idPersoana, idPoarta)
            VALUES (%s, %s, %s, %s)
        """, (input_data['data'], input_data['sens'], input_data['idPersoana'], input_data['idPoarta']))

        # Confirmă schimbările și închide conexiunea
        conn.commit()
        conn.close()
        return jsonify({"mesaj": "Perfect, date adăugate!"}), 200

    except Exception as e:
        return jsonify({"eroare": f"Ceva nu a mers cum trebuie: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

