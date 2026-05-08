from datetime import datetime
from jarat import Jarat


class JegyFoglalas:
    """A járatok foglalásához szükséges osztály – egy utazásra szóló jegy foglalását tárolja."""

    __kovetkezo_id = 1

    def __init__(self, utas_neve: str, jarat: Jarat):
        if not utas_neve or not utas_neve.strip():
            raise ValueError("Az utas neve nem lehet üres!")
        if not jarat.elerheto():
            raise ValueError(
                f"A(z) {jarat.jaratszam} járat nem elérhető foglalásra "
                f"(nincs szabad hely vagy a járat már elindult)!"
            )

        self.__foglalas_id = JegyFoglalas.__kovetkezo_id
        JegyFoglalas.__kovetkezo_id += 1

        self.__utas_neve = utas_neve.strip()
        self.__jarat = jarat
        self.__foglalas_ideje = datetime.now()
        self.__ar = jarat.jegyar_szamitas()

        # Foglalás rögzítése: szabad helyek csökkentése
        jarat.szabad_helyek = jarat.szabad_helyek - 1

    # Getterek
    @property
    def foglalas_id(self) -> int:
        return self.__foglalas_id

    @property
    def utas_neve(self) -> str:
        return self.__utas_neve

    @property
    def jarat(self) -> Jarat:
        return self.__jarat

    @property
    def foglalas_ideje(self) -> datetime:
        return self.__foglalas_ideje

    @property
    def ar(self) -> float:
        return self.__ar

    # Setter
    @utas_neve.setter
    def utas_neve(self, ertek: str):
        if not ertek or not ertek.strip():
            raise ValueError("Az utas neve nem lehet üres!")
        self.__utas_neve = ertek.strip()

    def __str__(self):
        return (
            f"Foglalás #{self.__foglalas_id:04d} | "
            f"Utas: {self.__utas_neve} | "
            f"Járat: {self.__jarat.jaratszam} → {self.__jarat.celallomas} | "
            f"Indulás: {self.__jarat.indulas.strftime('%Y.%m.%d %H:%M')} | "
            f"Fizetett ár: {self.__ar:,.0f} Ft | "
            f"Foglalva: {self.__foglalas_ideje.strftime('%Y.%m.%d %H:%M')}"
        )
