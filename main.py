<<<<<<< HEAD
from ChiulangiiSiSilitori import *
def main():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'virtuals'
    }
    
    email_trimitator = 'petrucretu03@gmail.com'
    email_password = os.getenv('EMAIL_PASSWORD')  
    db = BazaDeDate(**db_config)
    prezenta = Prezenta(db)
    generator_rapoarte = GeneratorDeRapoarte('backup_reports')
    trimite_notificari = TrimitereNotificari(email_trimitator, email_password)

   
    data_curenta = datetime.now().strftime('%Y-%m-%d')
    ore_lucrate = prezenta.oreDeLucru(data_curenta)
    ore_necesare = 8  
    angajatiNotificati, angajatiSilitori = prezenta.Notificari(ore_lucrate, ore_necesare)

    
    generator_rapoarte.generareRapoarte(angajatiNotificati, angajatiSilitori)


    trimite_notificari.notificareAngajat(angajatiNotificati, angajatiSilitori)

if __name__ == "__main__":
    main()



=======
from functie4 import *

if __name__=="__main__":

    db = BazaDeDate(host='localhost', password='root', user='root', database='virtuals') #din virtuals luam majoritatea datelor 
    procesareInfoBazadate=InitiereBazaDate(db)
    generareRapoarte=generatorDeRapoarte(folder_backup='backup')
    generatorNotificari = trimitereNotificari(db)


    today=datetime.now.strftime('%Y-%m-%d')
    ore_lucrate=procesareInfoBazadate.calculate_ore_lucrate(today)
    angajatiNotificati=procesareInfoBazadate.get_angajatiNotificati(today)
    if angajatiNotificati:
        generatorDeRapoarte.generareRapoarte(angajatiNotificati)
        trimitereNotificari.trimiteMail(angajatiNotificati)
>>>>>>> functie1


