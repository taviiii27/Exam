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


