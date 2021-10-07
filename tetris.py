import pygame
import sys
import time
import random
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP
maviRenk = (0,   0, 155)
kutuboyut = 20
genislik = 640
yukseklik = 480
tahtaBoyut = 10
skor = 0
parca_S = [['.....',
            '.....',
            '..xx.',
            '.xx..',
            '.....'],
           ['.....',
            '..x..',
            '..xx.',
            '...x.',
            '.....']]
parca_L = [['x....',
            'x....',
            'xx...',
            '.....',
            '.....'],

           ['..x..',
            'xxx..',
            '.....',
            '.....',
            '.....'],

           ['.xx..',
            '..x..',
            '..x..',
            '.....',
            '.....'],

           ['xxx..',
            'x....',
            '.....',
            '.....',
            '.....']]


parca_O = [['.....',
            '.....',
            '.xx..',
            '.xx..',
            '.....']]
parca_T = [['xxx..',
            '.x...',
            '.....',
            '.....',
            '.....'],

           ['x....',
            'xx...',
            'x....',
            '.....',
            '.....'],

           ['..x..',
            '.xx..',
            '..x..',
            '.....',
            '.....'],

           ['.x...',
            'xxx..',
            '.....',
            '.....',
            '.....']]
parca_I = [['..x..',
            '..x..',
            '..x..',
            '..x..',
            '.....'],

           ['.....',
            '.....',
            'xxxx.',
            '.....',
            '.....']]
parcalar = {
    'S': parca_S,
    'O': parca_O,
    'T': parca_T,
    'L': parca_L,
    'I': parca_I
    }

def baslat():
    pygame.init()
    ekran = pygame.display.set_mode((genislik, yukseklik))
    pygame.display.set_caption('Tetris Oyunu')
    oyunMatris = yeniOyunOlustur()
    sonParcaHareketi = time.time()
    parca = parcaOlustur()
    skor = 0
    while True:
        ekran.fill((0,   0,   0))
        if(time.time()-sonParcaHareketi > 0.3):
            parca['satir'] = parca['satir']+1
            sonParcaHareketi = time.time()
        ekranaCiz(ekran, parca)
        pygame.draw.rect(ekran,maviRenk,[100, 50, 10*20+10, 20*20+10], 5)
        tahtaCiz(ekran, oyunMatris)
        skorGoster(ekran, skor)
        kullaniciGirisi(oyunMatris, parca)
        if(not donebilirmi(oyunMatris, parca, tmpSutun=1)):
            oyunMatris = oyunGuncelle(oyunMatris, parca)
            silinenSatirSayisi = satirlariSil(oyunMatris)
            skor += silinenSatirSayisi
            parca = parcaOlustur()
        pygame.display.update()
        for e in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

def parcaOlustur():
    parca = {}
    rastgeleSekil = random.choice(list(parcalar.keys()))
    parca['sekil'] = rastgeleSekil
    parca['donus'] = 0
    parca['sutun'] = 2
    parca['satir'] = 0
    return parca
    
def oyunGuncelle(matris, parca):
    for i in range(5):
        for j in range(5):
            if(parcalar[parca['sekil']][parca['donus']][i][j] != '.'):
                matris[parca['satir']+i][parca['sutun']+j] = 'x'
    return matris
def ekranaCiz(ekran, parca):
    cizilecek = parcalar[parca['sekil']][parca['donus']]
    for satir in range(5):
        for sutun in range(5):
            if cizilecek[satir][sutun] != '.':
                kutuCiz(ekran, parca['satir']+satir, parca['sutun']+sutun, (11,3,255), (3,255,3))
def skorGoster(ekran, skor):
    font = pygame.font.Font('freesansbold.ttf', 20)
    ekran.blit(font.render('Skor: %s' % skor, True, (255, 255, 255)), (640 - 150, 20))

def donebilirmi(oyunMatris, parca, tmpSatir=0, tmpSutun=0):
    parcamatris = parcalar[parca['sekil']][parca['donus']]
    for satir in range(5):
        for sutun in range(5):
            if parcamatris[satir][sutun] == '.':
                continue
            if not tahtadaMi(parca['satir'] + satir + tmpSutun, parca['sutun'] + sutun + tmpSatir):
                return False
            if oyunMatris[parca['satir'] + satir + tmpSutun][parca['sutun'] + sutun + tmpSatir] != '.':
                return False
    return True

def satirKontrol(oyunMatris, satir):
    for sutun in range(10):
        if oyunMatris[satir][sutun] == '.':
            return False
    return True
def satirlariSil(oyunMatris):
    silinenSatirlar = 0
    for satir in range(20):
        if(satirKontrol(oyunMatris, satir)):
            for i in range(satir, 0, -1):
                for j in range(10):
                    oyunMatris[i][j] = oyunMatris[i-1][j]
            for k in range(10):
                oyunMatris[0][k] = '.'
            silinenSatirlar += 1
    return silinenSatirlar
def kullaniciGirisi(oyunMatris, parca):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if (event.key == K_LEFT) and donebilirmi(oyunMatris, parca, tmpSatir=-1):
                parca['sutun'] -= 1
            elif (event.key == K_RIGHT) and donebilirmi(oyunMatris, parca, tmpSatir=1):
                parca['sutun'] += 1
            elif (event.key == K_UP):
                parca['donus'] = (parca['donus']+1) % len(parcalar[parca['sekil']])
                if not donebilirmi(oyunMatris, parca):
                    parca['donus'] = (parca['donus']-1) % len(parcalar[parca['sekil']])

def tahtaCiz(ekran, matris):
    for satir in range(20):
        for sutun in range(10):
            if(matris[satir][sutun] != '.'):
                kutuCiz(ekran, satir, sutun, (254, 249, 27), (27, 254, 250))
def tahtadaMi(satir, sutun):
    return sutun >= 0 and sutun < 10 and satir < 20
def yeniOyunOlustur():
    oyunMasa = []
    for i in range(20):
        satir = []
        for j in range(10):
            satir.append('.')
        oyunMasa.append(satir)
    return oyunMasa
def kutuCiz(ekran, satir, sutun, renk, kenarlikRenk):
    x = 100 + 5 + (sutun*20+1)
    y = 50 + 5 + (satir*20+1)
    pygame.draw.rect(ekran, kenarlikRenk, [x, y, 20, 20])
    pygame.draw.rect(ekran, renk, [x, y, 18, 18])
def oyunBittimi(matris):
    for satir in range(10):
        if matris[satir][0]!='.':
            return True
    return False
def oyunBittiYazdir(ekran):
    font = pygame.font.Font('freesansbold.ttf', 20)
    ekran.blit(font.render('Oyun Bitti', True, (255, 255, 255)), (genislik/2,yukseklik/2))

baslat()
