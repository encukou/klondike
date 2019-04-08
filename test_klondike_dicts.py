import pytest
import klondike
import textwrap
import re

@pytest.mark.parametrize('cislo_sloupecku', range(7))
def test_delka_sloupecku(cislo_sloupecku):
    """Sloupeček č. 0 má mít 1 kartu, další 2, další 3, atd."""
    balicek = klondike.vytvor_balicek()
    sloupecky = klondike.rozdej_sloupecky(balicek)
    assert len(sloupecky[cislo_sloupecku]) == cislo_sloupecku + 1


@pytest.mark.parametrize('cislo_sloupecku', range(7))
def test_posledni_karta_licem_nahoru(cislo_sloupecku):
    """Poslední karta sloupečku má být lícem nahoru"""
    balicek = klondike.vytvor_balicek()
    sloupecky = klondike.rozdej_sloupecky(balicek)
    posledni_karta = sloupecky[cislo_sloupecku][-1]
    hodnota, barva, je_licem_nahoru = posledni_karta
    assert je_licem_nahoru


@pytest.mark.parametrize('cislo_sloupecku', range(7))
def test_prvni_karty_rubem_nahoru(cislo_sloupecku):
    """Všechny karty sloupečku kromě poslední mají být rubem nahoru"""
    balicek = klondike.vytvor_balicek()
    sloupecky = klondike.rozdej_sloupecky(balicek)
    for hodnota, barva, je_licem_nahoru in sloupecky[cislo_sloupecku][:-1]:
        assert not je_licem_nahoru


def test_zmenseni_balicku():
    """Po rozdání sloupečků má být balíček menší o počet rozdaných karet"""
    balicek = klondike.vytvor_balicek()
    pocet_na_zacatku = len(balicek)
    sloupecky = klondike.rozdej_sloupecky(balicek)
    assert len(balicek) == pocet_na_zacatku - (1+2+3+4+5+6+7)

def test_klicu():
    """Hra by měl být slovník s klíči A až G a U až Z."""
    hra = klondike.udelej_hru()
    assert sorted(hra) == list('ABCDEFGUVWXYZ')


@pytest.mark.parametrize('pismenko', 'ABCDEFGUVWXYZ')
def test_pocty_karet(pismenko):
    """Počty karet v jednotlivých sloupcích jsou dané."""
    hra = klondike.udelej_hru()

    POCTY = {
        'U': 24,
        'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0,
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7,
    }
    pozadovany_pocet = POCTY[pismenko]

    assert len(hra[pismenko]) == pozadovany_pocet


def test_otoceni_karet_balicku():
    """Karty balíčku by měly být rubem nahoru"""
    hra = klondike.udelej_hru()
    for hodnota, barva, licem_nahoru in hra['U']:
        assert not licem_nahoru


@pytest.mark.parametrize('pismenko', 'ABCDEFG')
def test_otoceni_karet_sloupecku(pismenko):
    """Karty sloupečků by měly být rubem nahoru, kromě té poslední"""
    hra = klondike.udelej_hru()
    sloupecek = hra[pismenko]

    # Poslední karta
    posledni_karta = sloupecek[-1]
    hodnota, barva, licem_nahoru = posledni_karta
    assert licem_nahoru

    # Ostatní karty
    for hodnota, barva, licem_nahoru in sloupecek[:-1]:
        assert not licem_nahoru


def test_zamichani():
    """Každá hra by měla být jiná"""
    hra1 = klondike.udelej_hru()
    hra2 = klondike.udelej_hru()

    # Je šance 1 z 80658175170943878571660636856403766975289505440883277824000000000000,
    # že dvě náhodné hry budou stejné.
    # Nejspíš je pravděpodobnější, že v průběhu testu odejde počítač,
    # na kterém test běží, než aby se ty karty zamíchaly stejně.
    assert hra1 != hra2, 'Karty nejsou zamíchané!'



def test_vsech_karet():
    """Hra by měla obsahovat všech 52 karet, bez duplikátů."""
    hra = klondike.udelej_hru()

    # Uděláme seznam dvojic (hodnota, barva), tedy karet s ignorovaným otočením
    dvojice_z_hry = []
    for balicek in hra.values():
        for hodnota, barva, licem_nahoru in balicek:
            dvojice_z_hry.append((hodnota, barva))
    # Seznam seřadíme -- na pořadí nezáleží
    dvojice_z_hry.sort()

    # Uděláme seznam dvojic (hodnota, barva) všech karet, kteŕe ve hře mají být
    pozadovane_dvojice = []
    for hodnota in range(1, 14):
        for barva in 'Ka', 'Kr', 'Pi', 'Sr':
            pozadovane_dvojice.append((hodnota, barva))
    # Tenhle seznam by měl být už seřazený, ale opatrnosti není nikdy dost
    pozadovane_dvojice.sort()

    # Ty dva seznamy (ten ze hry a ten z testu) by měly být stejné
    assert dvojice_z_hry == pozadovane_dvojice

def check(got, expected):
    got = re.sub(' +\n', '\n', got)  # odstraní mezery z konců řádků
    print(got)
    assert got.strip() == textwrap.dedent(expected).strip()



# I `print` jde testovat, dělá se to pomocí "capsys" a "readouterr".

def test_ruby(capsys):
    """Kontrola výpisu hry, kde jsou všechny karty rubem nahoru"""
    hra = {
        'U': [(13, 'Pi', False)],
        'V': [],
        'W': [],
        'X': [],
        'Y': [],
        'Z': [],
        'A': [(13, 'Pi', False)] * 2,
        'B': [(13, 'Pi', False)] * 3,
        'C': [(13, 'Pi', False)] * 4,
        'D': [(13, 'Pi', False)] * 5,
        'E': [(13, 'Pi', False)] * 6,
        'F': [(13, 'Pi', False)] * 7,
        'G': [(13, 'Pi', False)] * 8,
    }
    klondike.vypis_hru(hra)
    out, err = capsys.readouterr()
    check(out, """
          U     V           W     X     Y     Z
        [???] [   ]       [   ] [   ] [   ] [   ]

          A     B     C     D     E     F     G
        [???] [???] [???] [???] [???] [???] [???]
        [???] [???] [???] [???] [???] [???] [???]
              [???] [???] [???] [???] [???] [???]
                    [???] [???] [???] [???] [???]
                          [???] [???] [???] [???]
                                [???] [???] [???]
                                      [???] [???]
                                            [???]
    """)


def test_zacatek_hry(capsys):
    """Kontrola výpisu hry, kde jsou karty i rubem lícem nahoru"""
    hra = {
        'U': [(13, 'Pi', False)],
        'V': [(8, 'Kr', True), (13, 'Pi', True)],
        'W': [],
        'X': [],
        'Y': [],
        'Z': [],
        'A': [(13, 'Pi', False)] * 0 + [(8, 'Kr', True)],
        'B': [(13, 'Pi', False)] * 1 + [(9, 'Ka', True)],
        'C': [(13, 'Pi', False)] * 2 + [(10, 'Sr', True)],
        'D': [(13, 'Pi', False)] * 3 + [(1, 'Ka', True)],
        'E': [(13, 'Pi', False)] * 4 + [(4, 'Pi', True)],
        'F': [(13, 'Pi', False)] * 5 + [(9, 'Kr', True)],
        'G': [(13, 'Pi', False)] * 6 + [(12, 'Sr', True)],
    }
    klondike.vypis_hru(hra)
    out, err = capsys.readouterr()
    check(out, """
          U     V           W     X     Y     Z
        [???] [K♠ ]       [   ] [   ] [   ] [   ]

          A     B     C     D     E     F     G
        [8♣ ] [???] [???] [???] [???] [???] [???]
              [9 ♦] [???] [???] [???] [???] [???]
                    [X ♥] [???] [???] [???] [???]
                          [A ♦] [???] [???] [???]
                                [4♠ ] [???] [???]
                                      [9♣ ] [???]
                                            [Q ♥]
    """)


def test_rozehrana(capsys):
    """Kontrola výpisu rozehrané hry"""
    hra = {
        'U': [(13, 'Pi', False)],
        'V': [(8, 'Kr', True), (13, 'Pi', True)],
        'W': [(1, 'Pi', True)],
        'X': [(1, 'Kr', True)],
        'Y': [(1, 'Sr', True)],
        'Z': [(1, 'Ka', True), (2, 'Ka', True)],
        'A': [(13, 'Pi', False)] * 1 + [(8, 'Kr', True)],
        'B': [(13, 'Pi', False)] * 8 + [(9, 'Ka', True)],
        'C': [(13, 'Pi', False)] * 2 + [(10, 'Sr', True), (9, 'Kr', True), (8, 'Ka', True)],
        'D': [(13, 'Pi', False)] * 6 + [(3, 'Ka', True)],
        'E': [(13, 'Pi', False)] * 1 + [(4, 'Pi', True)],
        'F': [(13, 'Pi', False)] * 9 + [(9, 'Kr', True)],
        'G': [(13, 'Pi', False)] * 5 + [(12, 'Sr', True), (11, 'Pi', True)],
    }
    klondike.vypis_hru(hra)
    out, err = capsys.readouterr()
    check(out, """
          U     V           W     X     Y     Z
        [???] [K♠ ]       [A♠ ] [A♣ ] [A ♥] [2 ♦]

          A     B     C     D     E     F     G
        [???] [???] [???] [???] [???] [???] [???]
        [8♣ ] [???] [???] [???] [4♠ ] [???] [???]
              [???] [X ♥] [???]       [???] [???]
              [???] [9♣ ] [???]       [???] [???]
              [???] [8 ♦] [???]       [???] [???]
              [???]       [???]       [???] [Q ♥]
              [???]       [3 ♦]       [???] [J♠ ]
              [???]                   [???]
              [9 ♦]                   [???]
                                      [9♣ ]
    """)

def check(got, expected):
    got = re.sub(' +\n', '\n', got)  # odstraní mezery z konců řádků
    print(got)
    assert got.strip() == textwrap.dedent(expected).strip()



# I `print` jde testovat, dělá se to pomocí "capsys" a "readouterr".

def test_ruby(capsys):
    """Kontrola výpisu sloupečků, kde jsou všechny karty rubem nahoru"""
    sloupecky = [
        [(13, 'Pi', False)] * 2,
        [(13, 'Pi', False)] * 3,
        [(13, 'Pi', False)] * 4,
        [(13, 'Pi', False)] * 5,
        [(13, 'Pi', False)] * 6,
        [(13, 'Pi', False)] * 7,
        [(13, 'Pi', False)] * 8,
    ]
    klondike.vypis_sloupecky(sloupecky)
    out, err = capsys.readouterr()
    check(out, """
        [???] [???] [???] [???] [???] [???] [???]
        [???] [???] [???] [???] [???] [???] [???]
              [???] [???] [???] [???] [???] [???]
                    [???] [???] [???] [???] [???]
                          [???] [???] [???] [???]
                                [???] [???] [???]
                                      [???] [???]
                                            [???]
    """)


def test_zacatek_hry(capsys):
    """Kontrola výpisu sloupečků, kde jsou karty i rubem lícem nahoru"""
    sloupecky =  [
        [(13, 'Pi', False)] * 0 + [(8, 'Kr', True)],
        [(13, 'Pi', False)] * 1 + [(9, 'Ka', True)],
        [(13, 'Pi', False)] * 2 + [(10, 'Sr', True)],
        [(13, 'Pi', False)] * 3 + [(1, 'Ka', True)],
        [(13, 'Pi', False)] * 4 + [(4, 'Pi', True)],
        [(13, 'Pi', False)] * 5 + [(9, 'Kr', True)],
        [(13, 'Pi', False)] * 6 + [(12, 'Sr', True)],
    ]
    klondike.vypis_sloupecky(sloupecky)
    out, err = capsys.readouterr()
    check(out, """
        [8♣ ] [???] [???] [???] [???] [???] [???]
              [9 ♦] [???] [???] [???] [???] [???]
                    [X ♥] [???] [???] [???] [???]
                          [A ♦] [???] [???] [???]
                                [4♠ ] [???] [???]
                                      [9♣ ] [???]
                                            [Q ♥]
    """)


def test_rozehrana(capsys):
    """Kontrola výpisu sloupečků rozehrané hry"""
    sloupecky = [
        [(13, 'Pi', False)] * 1 + [(8, 'Kr', True)],
        [(13, 'Pi', False)] * 8 + [(9, 'Ka', True)],
        [(13, 'Pi', False)] * 2 + [(10, 'Sr', True), (9, 'Kr', True), (8, 'Ka', True)],
        [(13, 'Pi', False)] * 6 + [(3, 'Ka', True)],
        [(13, 'Pi', False)] * 1 + [(4, 'Pi', True)],
        [(13, 'Pi', False)] * 9 + [(9, 'Kr', True)],
        [(13, 'Pi', False)] * 5 + [(12, 'Sr', True), (11, 'Pi', True)],
    ]
    klondike.vypis_sloupecky(sloupecky)
    out, err = capsys.readouterr()
    check(out, """
        [???] [???] [???] [???] [???] [???] [???]
        [8♣ ] [???] [???] [???] [4♠ ] [???] [???]
              [???] [X ♥] [???]       [???] [???]
              [???] [9♣ ] [???]       [???] [???]
              [???] [8 ♦] [???]       [???] [???]
              [???]       [???]       [???] [Q ♥]
              [???]       [3 ♦]       [???] [J♠ ]
              [???]                   [???]
              [9 ♦]                   [???]
                                      [9♣ ]
    """)
