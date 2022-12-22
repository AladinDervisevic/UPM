import sys
from collections import deque

# V = vitez
# Z = zmaj
# h = stevilo vrstic
# w = stevilo stolpec

def naredi_graf(W, H): # O(h x w)
    graf = {}
    for i in range(H):
        for j in range(W):
            graf[(i,j)] = set()
            if j > 0:
                graf[(i, j)].add((i, j - 1))
            if j < W - 1:
                graf[(i, j)].add((i, j + 1))
            if i > 0:
                graf[(i, j)].add((i - 1, j))
            if i < H - 1:
                graf[(i, j)].add((i + 1, j))
    return graf

def desno(i, j):
    return (i, j+1)

def levo(i, j):
    return (i, j-1)

def gor(i, j):
    return (i+1, j)

def dol(i, j):
    return (i-1, j)

def preisci(smer, povratna, mreza, napadi, W, H, i, j):
    k = 0
    i, j = smer(i, j)
    while 0 <= i < H and 0 <= j < W and mreza[i][j] not in "#":
        k += 1
        i, j = smer(i, j)
    for l in range(k, -1, -1):
        i, j = povratna(i, j)
        napadi[l].add((i, j))

def main():
    vhod = sys.stdin.read().strip().split("\n\n")
    st_primerov = int(vhod.pop(0))
    izhod = ""

    for _ in range(st_primerov):

        primer = vhod.pop(0).split("\n") 
        W, H, L = map(int, primer.pop(0).split(" "))

        sosedi = naredi_graf(W, H) # O(h x w)
        vitez, zmaj = None, None
        
        razdalje_od_viteza = {}
        for i in range(H): # O(h x w)
            for j in range(W):
                razdalje_od_viteza[(i, j)] = float('inf')
                if primer[i][j] == "V":
                    vitez = (i, j)
                    razdalje_od_viteza[vitez] = 0
                if primer[i][j] == "Z":
                    zmaj = (i, j)
        
        Q = deque([vitez])
        while Q:
            loc = Q.popleft()
            for sosed in sosedi[loc]: # O(4)
                if primer[sosed[0]][sosed[1]] in "#Z":
                    continue
                if razdalje_od_viteza[sosed] == float('inf'):
                    Q.append(sosed)
                    razdalje_od_viteza[sosed] = razdalje_od_viteza[loc] + 1

        napadi = {}
        for i in range(max(H, W)):
            napadi[i] = set()

        for (i, j) in sosedi[zmaj]: 

            if primer[i][j] in "#":
                continue

            if (i, j) == desno(zmaj[0], zmaj[1]):

                preisci(gor, dol, primer, napadi, W, H, i, j)
                preisci(desno, levo, primer, napadi, W, H, i, j)
                preisci(dol, gor, primer, napadi, W, H, i, j)

            elif (i, j) == dol(zmaj[0], zmaj[1]):

                preisci(desno, levo, primer, napadi, W, H, i, j)
                preisci(dol, gor, primer, napadi, W, H, i, j)
                preisci(levo, desno, primer, napadi, W, H, i, j)

            elif (i, j) == levo(zmaj[0], zmaj[1]):
                preisci(gor, dol, primer, napadi, W, H, i, j)
                preisci(levo, desno, primer, napadi, W, H, i, j)
                preisci(dol, gor, primer, napadi, W, H, i, j)

            elif (i, j) == gor(zmaj[0], zmaj[1]):
                preisci(desno, levo, primer, napadi, W, H, i, j)
                preisci(gor, dol, primer, napadi, W, H, i, j)
                preisci(levo, desno, primer, napadi, W, H, i, j)

        moc_napada = ""

        for K in range(max(H, W) - 1, -1, -1):
            kandidati = napadi[K]
            while kandidati:
                kandidat = kandidati.pop()
                if K + razdalje_od_viteza[kandidat] <= L:
                    moc_napada = str(K + 1)
                    break
            if moc_napada:
                break

        if moc_napada:
            izhod += moc_napada + "\n"
        else:
            izhod += "0\n"

        
    print(f"{izhod.strip()}")

main()