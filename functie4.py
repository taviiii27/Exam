import os,csv
import mysql.connector
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class BazaDeDate:
    def __init__(self, host, user, password, database):
        self.host=host
        self.user=user
        self.password=password 
        self.database=database
        self.connection=None
        self.cursor=None
    def connect(self):
        self.connection=mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        self.cursor=self.connection.cursor()
    def executeConnection(self, query, values=None):
        self.connect()
        if values:
            self.cursor.execute(query,values)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        self.close()
    def resultConnection(self, query, values=None):
        self.connect()
        if values:
            self.cursor.execute(query,values)
        else:
            self.cursor.execute(query)
        result=self.cursor.fetchall()
        self.connection.commit()
        self.close()
        return result
    def close(self):
        if self.cursor:
            self.cursor.close()
        else:
            self.connection.close()


class InitiereBazaDate:
    def __init__(self,db):
        self.db=db
class Prezenta(InitiereBazaDate):
    def oreDeLucru(self, data):
        query="SELECT idPersoana, MIN(data) as intrare and MAX(data) as iesire FROM virtuals where DATE(data) = %s AND sens IN ('intrare', 'iesire') GROUP BY idPersoana"
        rezultatConexiune=self.db.resultConnection(query, (data,))
        ore_lucrate={}#persoana si ore lucrate 
        for row in rezultatConexiune:
            id_Persoana, entry, exits = row
            if entry and exits:
                worked_hours=(exits-entry).total_seconds()/3600 # asa aflam cu exactitate nr de ore lucrate 
                ore_lucrate[id_Persoana]=worked_hours
        return ore_lucrate #dictionar cu ore lucrate/persoana 
    def Notificari(self, ore_lucrate, ore_necesare):
        ore_necesare=8
        iduri=tuple(ore_lucrate.keys())
        query="SELECT id, Nume from users WHERE id IN %s "
        self.cursor.execute(query, (tuple(iduri),))
        rezultatConexiune=self.db.rezultatConexiune(query, iduri)
        angajatiNotificati=[]
        for row in rezultatConexiune:
            id, nume=row
            if ore_lucrate.get(id,0)<ore_necesare:
                angajatiNotificati.append(nume)
        return angajatiNotificati
    
class generatorDeRapoarte(InitiereBazaDate):
    def __init__(self, folder_backup):
        self.folder_backup=folder_backup
        if not os.path.exists(folder_backup):
            os.makedirs(folder_backup)
    def generareRapoarte(self, angajatiNotificati):
        dataCurenta=datetime.now.strftime('%Y-%M-%d')
        fisierCSV=os.path.join(self.folder_backup,f'{dataCurenta}_chiulangii.csv')
        fisierTXT=os.path.join(self.folder_backup, f'{dataCurenta}_chiulangii.txt')

        with open(fisierCSV, 'w') as file:
            writer=csv.writer(file)
            writer.writerow(['Nume'], ['ore_lucrate'])
            for name in angajatiNotificati:
                file.write([name, 'a lucrat <8h\n'])

        with open (fisierTXT, 'w') as file:
            for name in angajatiNotificati:
                file.write([name, 'a lucrat <8h\n'])
    

class trimitereNotificari:
    def __init__(self, db):
        self.db=db
    def trimiteMail(self, angajatiNotificati):
        email_trimitator='petrucretu03@gmail.com'
        email_destinatar='study.with.tavi@gmail.com'
        subiect='ore de lucru insuficiente'
        mesaj='buna ziua draga angajat, din nefericire trebuie sa va informam ca in aceasta saptamana in zilele de joi si vineri nu ati lucrat 8h, conform programului full-time al companiei. luati masuri! zi buna'
        for angajat in angajatiNotificati:
            return f'{angajat}, notificat'
        
        message = MIMEMultipart()#am scris asa pt ca un mail are subiect, mesaj propriu-zis si atasament 
        message['from']=email_trimitator
        message['to']=email_destinatar
        message['subject']=subiect
        message.attach(MIMEText(mesaj,'plain'))
        try:
            with smtplib ('petrucretu03@gmail.com', 587) as server:
                server.startlls()
                server.login(email_trimitator, 'sender_password')
                server.TrimiteMesaj(message)
                print("mail trimis cu succes!")
        except Exception as e:
            print("eroare:ceva s a intamplat")