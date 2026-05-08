from abc import ABC, abstractmethod
from datetime import datetime


class Jarat(ABC):
    """Absztrakt osztály, amely definiálja a járat alapvető attribútumait."""

    def __init__(self, jaratszam: str, celallomas: str, jegyar: float, indulas: datetime):
        self.__jaratszam = jaratszam
        self.__celallomas = celallomas
        self.__jegyar = jegyar
        self.__indulas = indulas
        self.__szabad_helyek = 100

    # Getterek
    @property
    def jaratszam(self) -> str:
        return self.__jaratszam

    @property
    def celallomas(self) -> str:
        return self.__celallomas

    @property
    def jegyar(self) -> float:
        return self.__jegyar

    @property
    def indulas(self) -> datetime:
        return self.__indulas

    @property
    def szabad_helyek(self) -> int:
        return self.__szabad_helyek

    # Setterek
    @jaratszam.setter
    def jaratszam(self, ertek: str):
        if not ertek or not ertek.strip():
            raise ValueError("A járatszám nem lehet üres!")
        self.__jaratszam = ertek.strip()

    @celallomas.setter
    def celallomas(self, ertek: str):
        if not ertek or not ertek.strip():
            raise ValueError("A célállomás nem lehet üres!")
        self.__celallomas = ertek.strip()

    @jegyar.setter
    def jegyar(self, ertek: float):
        if ertek <= 0:
            raise ValueError("A jegyár csak pozitív szám lehet!")
        self.__jegyar = ertek

    @szabad_helyek.setter
    def szabad_helyek(self, ertek: int):
        if ertek < 0:
            raise ValueError("A szabad helyek száma nem lehet negatív!")
        self.__szabad_helyek = ertek

    def elerheto(self) -> bool:
        """Visszaadja, hogy a járat elérhető-e foglalásra."""
        return self.__szabad_helyek > 0 and self.__indulas > datetime.now()

    @abstractmethod
    def jarat_tipusa(self) -> str:
        """Visszaadja a járat típusát (absztrakt)."""
        pass

    @abstractmethod
    def jegyar_szamitas(self) -> float:
        """Kiszámítja a végső jegyárat (absztrakt)."""
        pass

    def __str__(self):
        return (
            f"[{self.jarat_tipusa()}] {self.__jaratszam} → {self.__celallomas} | "
            f"Indulás: {self.__indulas.strftime('%Y.%m.%d %H:%M')} | "
            f"Ár: {self.jegyar_szamitas():,.0f} Ft | "
            f"Szabad helyek: {self.__szabad_helyek}"
        )


class BelfoldiJarat(Jarat):
    """Belföldi járatokra vonatkozó osztály – olcsóbb és rövidebb."""

    __ADOKULCS = 0.05  # 5% belföldi adó

    def __init__(self, jaratszam: str, celallomas: str, jegyar: float, indulas: datetime):
        if jegyar > 50_000:
            raise ValueError("Belföldi járat jegyára nem haladhatja meg az 50 000 Ft-ot!")
        super().__init__(jaratszam, celallomas, jegyar, indulas)

    @Jarat.jegyar.setter
    def jegyar(self, ertek: float):
        if ertek <= 0:
            raise ValueError("A jegyár csak pozitív szám lehet!")
        if ertek > 50_000:
            raise ValueError("Belföldi járat jegyára nem haladhatja meg az 50 000 Ft-ot!")
        super(BelfoldiJarat, BelfoldiJarat).jegyar.fset(self, ertek)

    def jarat_tipusa(self) -> str:
        return "Belföldi"

    def jegyar_szamitas(self) -> float:
        return self.jegyar * (1 + self.__ADOKULCS)


class NemzetkoziJarat(Jarat):
    """Nemzetközi járatokra vonatkozó osztály – magasabb jegyárakkal."""

    __ADOKULCS = 0.27  # 27% ÁFA

    def __init__(self, jaratszam: str, celallomas: str, jegyar: float, indulas: datetime):
        if jegyar < 10_000:
            raise ValueError("Nemzetközi járat jegyára legalább 10 000 Ft kell legyen!")
        super().__init__(jaratszam, celallomas, jegyar, indulas)

    @Jarat.jegyar.setter
    def jegyar(self, ertek: float):
        if ertek <= 0:
            raise ValueError("A jegyár csak pozitív szám lehet!")
        if ertek < 10_000:
            raise ValueError("Nemzetközi járat jegyára legalább 10 000 Ft kell legyen!")
        super(NemzetkoziJarat, NemzetkoziJarat).jegyar.fset(self, ertek)

    def jarat_tipusa(self) -> str:
        return "Nemzetközi"

    def jegyar_szamitas(self) -> float:
        return self.jegyar * (1 + self.__ADOKULCS)
