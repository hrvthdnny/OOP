from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Szoba(ABC):
    def __init__(self, szobaszam):
        self.szobaszam = szobaszam

    @abstractmethod
    def ar_szamitas(self, datum):
        pass

    def foglalas(self, datum):
        return self.ar_szamitas(datum)

class EgyagyasSzoba(Szoba):
    def ar_szamitas(self, datum):
        return 5000

class KetagyasSzoba(Szoba):
    def ar_szamitas(self, datum):
        return 8000

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def uj_szoba(self, szoba):
        self.szobak.append(szoba)

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

def foglalas_szamitas(szoba, datum):
    return szoba.ar_szamitas(datum)

def foglalas_lemondas(foglalas_lista, foglalas):
    if foglalas in foglalas_lista:
        foglalas_lista.remove(foglalas)
        print("A foglalás sikeresen törölve.")
    else:
        print("Nincs ilyen foglalás.")

def foglalas_lista(foglalas_lista):
    if foglalas_lista:
        print("Összes foglalás:")
        for foglalas in foglalas_lista:
            print(f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")
    else:
        print("Nincs foglalás.")

def feltolt(szalloda):
    # Szobák létrehozása és hozzáadása a szállodához
    egyagyas1 = EgyagyasSzoba("101")
    egyagyas2 = EgyagyasSzoba("102")
    ketagyas1 = KetagyasSzoba("201")
    ketagyas2 = KetagyasSzoba("202")
    szalloda.uj_szoba(egyagyas1)
    szalloda.uj_szoba(egyagyas2)
    szalloda.uj_szoba(ketagyas1)
    szalloda.uj_szoba(ketagyas2)

    # Foglalások létrehozása
    foglalasok = []
    foglalasok.append(Foglalas(egyagyas1, datetime.now()))
    foglalasok.append(Foglalas(egyagyas2, datetime.now() + timedelta(days=2)))
    foglalasok.append(Foglalas(ketagyas1, datetime.now() + timedelta(days=5)))
    foglalasok.append(Foglalas(egyagyas1, datetime.now() + timedelta(days=7)))
    foglalasok.append(Foglalas(ketagyas1, datetime.now() + timedelta(days=10)))
    foglalasok.append(Foglalas(ketagyas2, datetime.now() + timedelta(days=5)))
    foglalasok.append(Foglalas(ketagyas2, datetime.now() + timedelta(days=7)))
    foglalasok.append(Foglalas(ketagyas2, datetime.now() + timedelta(days=10)))


    return foglalasok

def main():
    # Szalloda létrehozása
    szalloda = Szalloda("Példa Szálloda")

    # Rendszer feltöltése szobákkal és foglalásokkal
    foglalasok = feltolt(szalloda)

    # Felhasználói interfész
    while True:
        print("1: Szoba foglalása")
        print("2: Foglalás lemondása")
        print("3: Foglalások listázása")
        print("4: Kilépés")

        valasztas = input("Válassz egy műveletet: ")

        if valasztas == "1":
            print("Elérhető szobák:")
            for szoba in szalloda.szobak:
                print(f"  - {szoba.szobaszam}")

            szobaszam = input("Add meg a foglalandó szoba számát: ")
            datum_str = input("Add meg a foglalás dátumát (YYYY-MM-DD): ")
            datum = datetime.strptime(datum_str, "%Y-%m-%d")

            # Ellenőrzés: jövőbeni dátum
            if datum < datetime.now():
                print("Hibás dátum. Kérlek adj meg egy érvényes jövőbeli dátumot.")
                continue

            # Ellenőrzés: szoba elérhetősége
            foglalt = False
            for foglalas in foglalasok:
                if foglalas.szoba.szobaszam == szobaszam and foglalas.datum.date() == datum.date():
                    foglalt = True
                    break
            if foglalt:
                print("A szoba ekkor már foglalt.")
                continue

            # Szoba foglalása
            for szoba in szalloda.szobak:
                if szoba.szobaszam == szobaszam:
                    foglalasok.append(Foglalas(szoba, datum))
                    print("Foglalás sikeresen rögzítve.")
                    print(f"{szoba.ar_szamitas(szoba)}Ft")
                    break

        elif valasztas == "2":
            if foglalasok:
                print("Kérlek add meg a lemondandó foglalás adatait:")
                szobaszam = input("Szoba száma: ")
                datum_str = input("Foglalás dátuma (YYYY-MM-DD): ")
                datum = datetime.strptime(datum_str, "%Y-%m-%d")

                for foglalas in foglalasok:
                    if foglalas.szoba.szobaszam == szobaszam and foglalas.datum.date() == datum.date():
                        foglalas_lemondas(foglalasok, foglalas)
                        break
                else:
                    print("Nincs ilyen foglalás.")
            else:
                print("Nincs foglalás.")

        elif valasztas == "3":
            foglalas_lista(foglalasok)

        elif valasztas == "4":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás. Kérlek válassz a felsorolt lehetőségek közül.")

main()