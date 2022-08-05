from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import sys
import pygame


def conversion1(image):
    im = Image.open(image)
    t = im.size
    l = list(im.getdata())
    r = [[0 for j in range(t[0])] for i in range(t[1])]
    g = [[0 for j in range(t[0])] for i in range(t[1])]
    b = [[0 for j in range(t[0])] for i in range(t[1])]
    for i in range(t[1]):
        for j in range(t[0]):
            r[i][j] = l[i*t[0]+j][0]
            g[i][j] = l[i*t[0]+j][1]
            b[i][j] = l[i*t[0]+j][2]
    return r, g, b


def voisin1(t, i, j):
    i += 1
    j += 1
    return [t[i+1][j], t[i+1][j-1], t[i][j-1], t[i-1][j-1], t[i-1][j], t[i-1][j+1], t[i][j+1], t[i+1][j+1], t[i][j]]


def voisin2(t, i, j):
    i += 2
    j += 2
    return [t[i+1][j], t[i+1][j-1], t[i][j-1], t[i-1][j-1], t[i-1][j], t[i-1][j+1], t[i][j+1], t[i+1][j+1], t[i][j], t[i-2][j], t[i-2][j+1],
            t[i-2][j+2], t[i-1][j+2], t[i][j+2], t[i+1][j+2], t[i+2][j +
                                                                     2], t[i+2][j+1], t[i+2][j], t[i+2][j-1], t[i+2][j-2], t[i+1][j-2],
            t[i][j-2], t[i-1][j-2], t[i-2][j-2], t[i-2][j-1]]


def tri_rapide(l):
    n = len(l)
    if n <= 1:
        return l
    else:
        l1, l2 = [], []
        for i in range(1, n):
            if l[i] > l[0]:
                l2.append(l[i])
            else:
                l1.append(l[i])
        return tri_rapide(l1)+[l[0]]+tri_rapide(l2)


def mediane(l):
    n = len(l)
    if n % 2 != 0:
        med = l[(n-1)//2]
    else:
        med = (l[(n//2)-1]+l[n//2])/2
    return med


def medianfilter1(t):
    m = [[0 for i in range(len(t[0]))] for j in range(len(t))]
    for i in range(len(t)-2):
        for j in range(len(t[0])-2):
            m[i][j] = mediane(tri_rapide(voisin1(t, i, j)))
    return m


def medianfilter2(t):
    m = [[0 for i in range(len(t[0]))] for j in range(len(t))]
    for i in range(len(t)-4):
        for j in range(len(t[0])-4):
            m[i][j] = mediane(tri_rapide(voisin2(t, i, j)))
    return m


def dessin1(image, nomImage):
    im = Image.open(image)
    r, g, b = conversion1(image)
    l = len(r)
    c = len(r[0])
    screen = pygame.display.set_mode((2*c, l))
    for i in range(l):
        r[i] = [0] + r[i] + [0]
        g[i] = [0] + g[i] + [0]
        b[i] = [0] + b[i] + [0]
    r = [[0 for i in range(c+2)]] + r + [[0 for i in range(c+2)]]
    g = [[0 for i in range(c+2)]] + g + [[0 for i in range(c+2)]]
    b = [[0 for i in range(c+2)]] + b + [[0 for i in range(c+2)]]
    r = medianfilter1(r)
    g = medianfilter1(g)
    b = medianfilter1(b)
    draw = ImageDraw.Draw(im)
    for i in range(l):
        for j in range(c):
            draw.point([j, i], fill=(int(r[i][j]), int(g[i][j]), int(b[i][j])))
    im.save(nomImage, "PNG")
    pygame.display.set_caption("Debruiteur")
    imageDebruitee = pygame.image.load(nomImage)
    imageBruitee = pygame.image.load(image)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            screen.fill((0, 0, 0))
            screen.blit(imageBruitee, (0, 0))
            screen.blit(imageDebruitee, (c, 0))
            pygame.display.flip()


def dessin2(image, nomImage):
    im = Image.open(image)
    r, g, b = conversion1(image)
    l = len(r)
    c = len(r[0])
    screen = pygame.display.set_mode((2*c, l))
    for i in range(l):
        r[i] = [0, 0] + r[i] + [0, 0]
        g[i] = [0, 0] + g[i] + [0, 0]
        b[i] = [0, 0] + b[i] + [0, 0]
    r = [[0 for i in range(c+4)]] + [[0 for i in range(c+4)]] + \
        r + [[0 for i in range(c+4)]] + [[0 for i in range(c+4)]]
    g = [[0 for i in range(c+4)]] + [[0 for i in range(c+4)]] + \
        g + [[0 for i in range(c+4)]] + [[0 for i in range(c+4)]]
    b = [[0 for i in range(c+4)]] + [[0 for i in range(c+4)]] + \
        b + [[0 for i in range(c+4)]] + [[0 for i in range(c+4)]]
    r = medianfilter2(r)
    g = medianfilter2(g)
    b = medianfilter2(b)
    draw = ImageDraw.Draw(im)
    for i in range(l):
        for j in range(c):
            draw.point([j, i], fill=(int(r[i][j]), int(g[i][j]), int(b[i][j])))
    im.save(nomImage, "PNG")
    pygame.display.set_caption("Debruiteur")
    imageDebruitee = pygame.image.load(nomImage)
    imageBruitee = pygame.image.load(image)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            screen.fill((0, 0, 0))
            screen.blit(imageBruitee, (0, 0))
            screen.blit(imageDebruitee, (c, 0))
            pygame.display.flip()


def main():

    pygame.init()

    print("Ce programme va vous permettre de debruiter votre image !\n")

    print("Il y a plusieurs modes :")
    print("Le premier s'applique aux images extremements bruitees/abimees mais risque de legerement flouter ces dernieres;")
    print("Le second s'applique aux images legerements bruitees;\n")

    mode = 0

    while mode != "1" and mode != "2":
        mode = input("Quel mode desirez-vous utiliser ? (1/2) : ")

    image = input(
        "\nSpécifiez le chemin d'accès à l'image que vous souhaitez debruiter : ")

    nomImage = input(
        "\nChoisissez maintenant un nom pour l'image finale (nomImage.png) : ")

    if mode == "1":
        dessin1(image, nomImage)
    else:
        dessin2(image, nomImage)


if __name__ == "__main__":
    main()
