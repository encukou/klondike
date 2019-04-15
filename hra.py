from klondike import udelej_hru, vypis_hru, udelej_tah

def nacti_tah():
    while True:
        tah = input('Tah? ')
        try:
            jmeno_zdroje, jmeno_cile = tah.upper()
        except ValueError:
            print('Tah zadávej jako dvě písmenka, např. UV')
        else:
            return jmeno_zdroje, jmeno_cile


hra = udelej_hru()

while not hrac_vyhral(hra):
    vypis_hru(hra)
    jmeno_zdroje, jmeno_cile = nacti_tah()
    try:
        udelej_tah(hra, jmeno_zdroje, jmeno_cile)
    except ValueError as e:
        print('Něco je špatně:', e)

vypis_hru(hra)
print('Gratuluji!')
