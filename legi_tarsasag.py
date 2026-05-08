from jarat import Jarat
from jegy_foglalas import JegyFoglalas


class LegiTarsasag:
    """Légitársaság osztály – tartalmazza a járatokat és saját attribútumait."""

    def __init__(self, nev: str):
        if not nev or not nev.strip():
            raise ValueError("A légitársaság neve nem lehet üres!")
        self.__nev = nev.strip()
        self.__jaratok: list[Jarat] = []
        self.__foglalasok: list[JegyFoglalas] = []

    # Getterek
    @property
    def nev(self) -> str:
        return self.__nev

    @property
    def jaratok(self) -> list[Jarat]:
        return list(self.__jaratok)

    @property
    def foglalasok(self) -> list[JegyFoglalas]:
        return list(self.__foglalasok)

    # Setter
    @nev.setter
    def nev(self, ertek: str):
        if not ertek or not ertek.strip():
            raise ValueError("A légitársaság neve nem lehet üres!")
        self.__nev = ertek.strip()

    # Jarat kezeles
    def jarat_hozzaadasa(self, jarat: Jarat):
        """Hozzáad egy járatot a légitársasághoz."""
        if any(j.jaratszam == jarat.jaratszam for j in self.__jaratok):
            raise ValueError(f"Már létezik '{jarat.jaratszam}' járatszámú járat!")
        self.__jaratok.append(jarat)

    def jarat_keresese(self, jaratszam: str) -> Jarat:
        """Megkeresi és visszaadja a járatot járatszám alapján."""
        for jarat in self.__jaratok:
            if jarat.jaratszam == jaratszam:
                return jarat
        raise ValueError(f"Nem található '{jaratszam}' járatszámú járat!")

    # Foglalas muveletek
    def jegy_foglalasa(self, utas_neve: str, jaratszam: str) -> JegyFoglalas:
        """
        Jegyet foglal a megadott járatra az utas nevére.
        Visszaadja a létrehozott foglalást (benne az árral).
        """
        jarat = self.jarat_keresese(jaratszam)
        foglalas = JegyFoglalas(utas_neve, jarat)
        self.__foglalasok.append(foglalas)
        return foglalas

    def foglalas_lemondasa(self, foglalas_id: int) -> JegyFoglalas:
        """
        Lemondja a megadott azonosítójú foglalást.
        Visszaadja a lemondott foglalást.
        """
        for foglalas in self.__foglalasok:
            if foglalas.foglalas_id == foglalas_id:
                self.__foglalasok.remove(foglalas)
                # Szabad hely visszaállítása
                foglalas.jarat.szabad_helyek = foglalas.jarat.szabad_helyek + 1
                return foglalas
        raise ValueError(f"Nem található #{foglalas_id:04d} azonosítójú foglalás!")

    def foglalasok_listazasa(self) -> list[JegyFoglalas]:
        """Visszaadja az összes aktuális foglalást."""
        return list(self.__foglalasok)

    def jaratok_listazasa(self) -> list[Jarat]:
        """Visszaadja az összes járatot."""
        return list(self.__jaratok)

    def __str__(self):
        return (
            f"{self.__nev} | "
            f"Jaratok: {len(self.__jaratok)} | "
            f"Aktiv foglalasok: {len(self.__foglalasok)}"
        )
