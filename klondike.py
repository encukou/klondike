"""Hra Klondike Solitaire"""

from random import shuffle
import json
from itertools import zip_longest

# Karta = trojice (hodnota, barva, otočení)
# Srdcová dáma = (12, 'Sr', True)
# - hodnota     1=A, 2, 3, 4, ..., 10, 11='J', 12='Q', 13='K'
# - barva       'Sr', 'Pi', 'Ka', 'Kr'
# - je_licem_nahoru   True, False
# Poloha karty vyplává z toho, v jakém je balíčku.

# Balíček/sloupeček/hromádka = seznam karet
sloupecek = [
    (12, 'Sr', False),
    (4, 'Sr', True),
    (3, 'Kr', True),
    (2, 'Sr', True),
]

# Stav hry = slovník (jméno balíčku → balíček)
# např. 'V' → []

# Tah = řetězec se 2 písmenky, např. 'UV'


def popis_kartu(karta):
    """Vrátí popis karty, např. [Q ♥] nebo [6♣ ] nebo [???]

    Trojice čísla (2-13), krátkého řetězce ('Sr', 'Ka', 'Kr' nebo 'Pi')
    a logické hodnoty (True - lícem nahoru; False - rubem) se jednoduše
    zpracovává v Pythonu, ale pro "uživatele" není nic moc.
    Proto je tu tahle funkce, která kartu hezky "popíše".

    Aby měly všechny hodnoty jen jeden znak, desítka se vypisuje jako
    římská číslice "X".

    Aby se dalo rychle odlišit červené (♥♦) karty od černých (♣♠),
    mají červené mezeru před symbolem a černé za ním.
    """
    hodnota, barva, je_licem_nahoru = karta
    if not je_licem_nahoru:
        return '[???]'
    if hodnota == 11:
        popis_hodnoty = 'J'
    elif hodnota == 12:
        popis_hodnoty = 'Q'
    elif hodnota == 13:
        popis_hodnoty = 'K'
    elif hodnota == 1:
        popis_hodnoty = 'A'
    elif hodnota == 10:
        popis_hodnoty = 'X'
    else:
        popis_hodnoty = hodnota
    if barva == 'Sr':
        popis_barvy = ' ♥'
    elif barva == 'Ka':
        popis_barvy = ' ♦'
    elif barva == 'Pi':
        popis_barvy = '♠ '
    else:
        popis_barvy = '♣ '
    return f'[{popis_hodnoty}{popis_barvy}]'


def popis_balicek(balicek):
    """Vrátí popis všech karet v balíčku. Jednotlivé karty odděluje mezerami.
    """
    popisy_karet = []
    for karta in balicek:
        popisy_karet.append(popis_kartu(karta))
    # popisy_karet je např. ['[???]', '[4 ♥]']
    return ' '.join(popisy_karet)


def popis_vrchni_kartu(balicek):
    """Vrátí popis daného balíčku karet -- tedy vrchní karty, která je vidět."""
    if balicek:
        karta = balicek[-1]
        return popis_kartu(karta)
    else:
        return '[   ]'


def vytvor_balicek():
    """Vrátí balíček 52 karet – od esa (1) po krále (13) ve čtyřech barvách

    Všechny karty jsou otočené rubem nahoru.
    """
    balicek = []
    # karty všech 4 barev
    for barva in 'Sr', 'Pi', 'Ka', 'Kr':
        # pro každou barvu všech 13 hodnot
        for hodnota in range(1, 14):
            karta = hodnota, barva, False
            balicek.append(karta)
    shuffle(balicek)
    return balicek

#for karta in vytvor_balicek():
    #print(popis_kartu(karta))

def rozdej_sloupecky(balicek):
    """Rozdá z daného balíčku 7 "sloupečků" -- seznamů karet

    Karty ve sloupečcích jsou odstraněny z balíčku.
    Vrátí všechny sloupečky -- tedy seznam sedmi seznamů.
    """
    sloupecky = []
    for cislo_sloupce in range(7):
        sloupecek = []

        # n karet bez otočení
        for cislo_karty in range(cislo_sloupce):
            karta = balicek.pop()
            sloupecek.append(karta)

        # 1 karta lícem nahoru
        karta = balicek.pop()
        karta = otoc_kartu(karta, True)
        sloupecek.append(karta)

        sloupecky.append(sloupecek)
    return sloupecky

def udelej_hru():
    """Vytvoří nový stav hry s rozdanými kartami"""
    balicek = vytvor_balicek()
    hra = {
        'U': balicek,
    }
    for jmeno_pozice in 'VWXYZ':
        hra[jmeno_pozice] = []

    for jmeno_pozice, sloupecek in zip('ABCDEFG', rozdej_sloupecky(balicek)):
        hra[jmeno_pozice] = sloupecek

    return hra


def vypis_hru(hra):
    """Vypíše stav hry textově, např.:

      U     V          W     X     Y     Z
     [???] [   ]      [   ] [   ] [   ] [   ]

       A     B     C     D     E     F     G
     [3♣ ] [???] [???] [???] [???] [???] [???]
           [5 ♥] [???] [???] [???] [???] [???]
                 [6♣ ] [???] [???] [???] [???]
                       [5♠ ] [???] [???] [???]
                             [Q ♥] [???] [???]
                                   [4♠ ] [???]
                                         [3 ♦]

    Tato procedura je jen pro zobrazení, používá proto přímo funkci print()
    a nic nevrací.
    """
    # procedura
    print('  U     V           W     X     Y     Z')
    print(popis_vrchni_kartu(hra['U']), end=' ')
    print(popis_vrchni_kartu(hra['V']), end=' ')
    print('     ', end=' ')
    print(popis_vrchni_kartu(hra['W']), end=' ')
    print(popis_vrchni_kartu(hra['X']), end=' ')
    print(popis_vrchni_kartu(hra['Y']), end=' ')
    print(popis_vrchni_kartu(hra['Z']))
    print()
    print('  A     B     C     D     E     F     G')
    vypis_sloupecky(hra)


def vypis_sloupecky(hra):
    """Vypíše sloupečky A-G textově.

    Tato procedura je jen pro zobrazení, používá proto přímo funkci print()
    a nic nevrací.
    """
    for karty in zip_longest(
            hra['A'], hra['B'], hra['C'], hra['D'], hra['E'],
            hra['F'], hra['G']):
        for karta in karty:
            if karta == None:
                print('     ', end=' ')
            else:
                print(popis_kartu(karta), end=' ')
        print()


def zeptej_se_na_tah(hra):
    """Zeptá se hráče na tah; ptá se tak dlouho dokud hráč neodpoví správně."""
    while True:
        odpoved = input('Odkud a kam chceš hrát? ')
        odpoved = odpoved.upper()
        if len(odpoved) != 2:
            print('Zadej dvě písmenka, odkud a kam (např. UV)')
        elif odpoved[0] not in hra:
            print('Zadej jména pozice (A-G, U-Z)')
        elif odpoved[1] not in hra:
            print('Zadej jména pozice (A-G, U-Z)')
        else:
            return odpoved


def otoc_kartu(karta, licem_nahoru):
    """Vrátí kartu otočenou lícem nahoru (True) nebo rubem nahoru (False)

    Nemění původní trojici; vytvoří a vrátí novou.
    (Ani by to jinak nešlo – n-tice se, podobně jako řetězce čísla, měnit
    nedají.)

    Např. otoc_kartu((12, 'Sr', False), True) -> (12, 'Sr', True)
    """
    hodnota, barva, je_licem_nahoru = karta
    karta = hodnota, barva, licem_nahoru
    return karta


def presun_kartu(sloupecek_z, sloupecek_na, licem_nahoru):
    """Přesune vrchní kartu ze sloupce "odkud" do sloupce "kam".
    Karta bude otocena lícem nebo rubem nahoru podle argumentu "licem_nahoru".
    """
    karta = sloupecek_z.pop()
    karta = otoc_kartu(karta, licem_nahoru)
    sloupecek_na.append(karta)


def presun_nekolik_karet(sloupecek_z, sloupecek_na, pocet):
    """Přesune "pocet" vrchních karet ze sloupce "odkud" do sloupce "kam".
    Karty se přitom neotáčí.
    """
    karty = sloupecek_z[-pocet:]
    del sloupecek_z[-pocet:]
    sloupecek_na.extend(karty)


def udelej_tah(hra, tah):
    """Zahraje daný tah.

    Toto je procedura: mění stav hry, nic nevrací.
    """
    # tah je např. 'UV'
    jmeno_z, jmeno_na = tah
    # jmeno_z např. 'U'
    # jmeno_na např. 'V'
    sloupecek_z = hra[jmeno_z]
    if not sloupecek_z:
        raise ValueError(f'V "{jmeno_z}" nic není')
    # sloupecek_z bude seznam karet
    sloupecek_na = hra[jmeno_na]
    # sloupecek_na bude seznam karet
    if tah == 'UV':
        presun_kartu(sloupecek_z, sloupecek_na, True)
    elif tah == 'VU':
        if sloupecek_na:
            raise ValueError('Balíček "U" musí být prázdný')
        while sloupecek_z:
            presun_kartu(sloupecek_z, sloupecek_na, False)
    elif jmeno_z in 'VABCDEFG' and jmeno_na in 'WXYZ':
        ...
    # Můžeš použít funkce presun_kartu a presun_nekolik_karet


def hrac_vyhral(hra):
    """Vrátí True, pokud je daná hra vyhraná."""
    return False


def hra():
    """Hra Klondike Solitaire pro příkazovou řádku"""
    try:
        with open('stav.json', encoding='utf-8') as soubor:
            zakodovany_stav = soubor.read()
            hra = json.loads(zakodovany_stav)
    except FileNotFoundError:
        hra = udelej_hru()
    while not hrac_vyhral(hra):
        vypis_hru(hra)
        tah = zeptej_se_na_tah(hra)
        try:
            udelej_tah(hra, tah)
        except ValueError as e:
            print(e)
        with open('stav.json', mode='w', encoding='utf-8') as soubor:
            zakodovany_stav = json.dumps(hra)
            print(zakodovany_stav, file=soubor)

    os.remove('stav.json')
