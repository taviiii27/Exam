from flask import Flask, request, jsonify
import os
import time, mysql.connector,shutil #pt mmutare


class Database:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connection = None
        self.cursor = None
    def conexiune(self):
        self.connection=mysql.connector.connect(host='localhost', user='root',  password='root', database='users')
        self.cursor=self.connection.cursor()
    def executeConexiune(self, query, values=None):
        self.conexiune()
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

class ManagerFisiere():
    def __init__(self, backup_folder, folder_entries):
        self.backup_folder = backup_folder
        self.folder_entries = folder_entries
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
    def Filemanager(self,db):
        entry_files=os.listdir(self.folder_entries)
        for file in entry_files:
            file_path=os.path.join(self.folder_entries,file)
            if os.path.isfile(file_path):
                nume_poarta, extensie=os.path.splitext(file) 
                nume_poarta=int(nume_poarta.replace,('Poarta', '')) #inlocuiesc poarta cu un numar
                with open(file_path, 'r') as fisier: #alatur fisierul in folderul corespunzator
                    data_access=fisier.read().split() #oferim acces
                query='INSERT INTO poarta_acces( `numar_poarta`,`tip_fisier`,data_acces`) VALUES (%s, %s, %s)' 
                values = (nume_poarta, extensie, ' '.join(data_access))
                db.executeConexiune(query,values)
                shutil.move(file_path,os.path.join(self.backup_folder,file))
class Poarta_fisiere_intrari:
    def __init__(self, backup_folder, folder_entries):
        self.file_manager = ManagerFisiere(backup_folder, folder_entries)
        self.db = Database(host='localhost', user='root', password='root', database='in_outs')
        self.db.executeConexiune("CREATE TABLE IF NOT EXISTS `in_outs`.`poarta_acces` ( `id` INT NOT NULL, `numar_poarta` INT NOT NULL,`tip_fisier` VARCHAR(45) NOT NULL,`data_acces` DATETIME NOT NULL,PRIMARY KEY (`id`));")
    def rulare(self):
        self.file_manager.Filemanager(self.db)
        time.sleep(20)

procesareFisier=Poarta_fisiere_intrari(backup_folder='backup', folder_entries='entries')
app=Flask(__name__)
@app.route('/files', methods=['GET'])
def processFile():
    try:
        procesareFisier.rulare()
        return jsonify({"mesaj":"functioneaza bine"}), 200
    except Exception as e:
        return jsonify({"eroare":"ceva nu a mers cum trb"}), 500
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)