"""Create a spritesheet from the Kenney.nl card pack (individual images)"""

from PIL import Image

W = 140
H = 190

dest = Image.new('RGBA', (W*14, H*4), color=(0, 0, 0, 0))


for y, barva in enumerate(('Hearts', 'Spades', 'Diamonds', 'Clubs')):
    for hodnota in range(1, 14):
        h = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}.get(hodnota, hodnota)
        img = Image.open(f'kenney_cards/card{barva}{h}.png')
        dest.paste(img, (hodnota*W, y*H))

img = Image.open(f'kenney_cards/cardBack_green1.png')
dest.paste(img, (0, H*3))
img = Image.open(f'kenney_cards/cardBack_blue2.png')
dest.paste(img, (0, H*2))

dest.save('cards.png')
