from flask import Flask, request, jsonify
import json,os
import time, mysql.connector,shutil#pt mmutare

def Poarta_fisiere_intrari(file_path, backup_folder, folder_entries):
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
                shutil.move(file_path,os.path.join(backup_folder,file))
                conexiune.commit()
                
        time.sleep(20)



