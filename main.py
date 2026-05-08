"""
Repulojegy Foglalasi Rendszer
Foprogram - felhasznaloi interfesz es elokezites.
"""

from datetime import datetime
from jarat import BelfoldiJarat, NemzetkoziJarat
from legi_tarsasag import LegiTarsasag


#  Segédfüggvények

def elvalaszto(hossz: int = 65):
    print("-" * hossz)


def cim_kiiras(szoveg: str):
    elvalaszto()
    print(f"  {szoveg}")
    elvalaszto()


def jaratok_kilistazasa(legi_tarsasag: LegiTarsasag):
    jaratok = legi_tarsasag.jaratok_listazasa()
    if not jaratok:
        print("  Jelenleg nincs elérhető járat.")
        return
    for jarat in jaratok:
        elerheto = "Foglalható" if jarat.elerheto() else "Nem foglalható"
        print(f"  {jarat}  [{elerheto}]")


def foglalas_kilistazasa(legi_tarsasag: LegiTarsasag):
    foglalasok = legi_tarsasag.foglalasok_listazasa()
    if not foglalasok:
        print("  Nincsenek aktuális foglalások.")
        return
    for f in foglalasok:
        print(f"  {f}")



#  Műveletek

def menu_jegy_foglalas(legi_tarsasag: LegiTarsasag):
    cim_kiiras("JEGY FOGLALÁSA")
    print("  Elérhető járatok:\n")
    jaratok_kilistazasa(legi_tarsasag)
    elvalaszto()

    jaratszam = input("  Adja meg a járatszámot: ").strip().upper()
    utas_neve = input("  Adja meg az utas nevét: ").strip()

    try:
        foglalas = legi_tarsasag.jegy_foglalasa(utas_neve, jaratszam)
        print(f"\n  Sikeres foglalas!")
        print(f"  {foglalas}")
        print(f"\n  Fizetendo osszeg: {foglalas.ar:,.0f} Ft")
    except ValueError as e:
        print(f"\n  Hiba: {e}")


def menu_foglalas_lemondasa(legi_tarsasag: LegiTarsasag):
    cim_kiiras("FOGLALÁS LEMONDÁSA")
    print("  Aktuális foglalások:\n")
    foglalas_kilistazasa(legi_tarsasag)
    elvalaszto()

    if not legi_tarsasag.foglalasok_listazasa():
        return

    try:
        foglalas_id_str = input("  Adja meg a lemondani kívánt foglalás azonosítóját (#): ").strip()
        foglalas_id = int(foglalas_id_str)
        lemondott = legi_tarsasag.foglalas_lemondasa(foglalas_id)
        print(f"\n  A foglalas sikeresen lemondva!")
        print(f"  {lemondott}")
    except ValueError as e:
        print(f"\n  Hiba: {e}")


def menu_foglalasok_listazasa(legi_tarsasag: LegiTarsasag):
    cim_kiiras("OSSZES AKTUALIS FOGLALAS")
    foglalas_kilistazasa(legi_tarsasag)


# Elokezites - adatok betoltese

def adatok_betoltese() -> LegiTarsasag:
    """Betolti az elore definialt legitarsasagot, 3 jaratot es 6 foglalast."""
    wizz = LegiTarsasag("Wizz Air Hungary")

    # 3 jarat letrehozasa
    j1 = BelfoldiJarat(
        jaratszam="W61001",
        celallomas="Debrecen",
        jegyar=15_000,
        indulas=datetime(2026, 6, 10, 8, 30)
    )
    j2 = BelfoldiJarat(
        jaratszam="W61002",
        celallomas="Pécs",
        jegyar=12_000,
        indulas=datetime(2026, 6, 15, 14, 0)
    )
    j3 = NemzetkoziJarat(
        jaratszam="W62001",
        celallomas="London Luton",
        jegyar=45_000,
        indulas=datetime(2026, 7, 1, 6, 45)
    )

    wizz.jarat_hozzaadasa(j1)
    wizz.jarat_hozzaadasa(j2)
    wizz.jarat_hozzaadasa(j3)

    # 6 elore betoltott foglalas (2 jaraton kent)
    elofoglalasok = [
        ("Kovacs Bela",   "W61001"),
        ("Nagy Anna",     "W61001"),
        ("Horvath Peter", "W61002"),
        ("Toth Maria",    "W61002"),
        ("Szabo Laszlo",  "W62001"),
        ("Kiss Katalin",  "W62001"),
    ]

    for nev, jszam in elofoglalasok:
        wizz.jegy_foglalasa(nev, jszam)

    return wizz


# Fomenu

def foprogram():
    legi_tarsasag = adatok_betoltese()

    while True:
        print()
        cim_kiiras(f"REPULOJEGY FOGLALASI RENDSZER  |  {legi_tarsasag.nev}")
        print("  1. Jegy foglalasa")
        print("  2. Foglalas lemondasa")
        print("  3. Foglalasok listazasa")
        print("  4. Jaratok listazasa")
        print("  0. Kilepes")
        elvalaszto()

        valasztas = input("  Valasszon menupontot: ").strip()

        if valasztas == "1":
            menu_jegy_foglalas(legi_tarsasag)
        elif valasztas == "2":
            menu_foglalas_lemondasa(legi_tarsasag)
        elif valasztas == "3":
            menu_foglalasok_listazasa(legi_tarsasag)
        elif valasztas == "4":
            cim_kiiras("JARATOK LISTAJA")
            jaratok_kilistazasa(legi_tarsasag)
        elif valasztas == "0":
            print("\n  Viszontlatasra!\n")
            break
        else:
            print("\n  Ervenytelen menupont! Kerem, valasszon 0-4 kozott.")

        input("\n  [Enter a folytatáshoz...]")


if __name__ == "__main__":
    foprogram()
