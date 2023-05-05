import sys

#-----------------------------------------------------------------------------
# MIN KOPICA
#-----------------------------------------------------------------------------

class MinKopica():
    def __init__(self, sez = []): # O(1)
        self.sez = []
        for v in sez:
            self.push(v)

    def __str__(self):
        return f"Kopica({self.sez})"

    def __repr__(self):
        return f"Kopica({self.sez})"

    def otroka(self, i): # O(1)
        return (2 * i + 1, 2 * i + 2)

    def push(self, x): # O(logn)
        s = self.sez
        s.append(x)
        i = len(s) - 1
        while i != 0 and s[i] < s[(i-1) // 2]:
            s[(i-1) // 2], s[i] = s[i], s[(i-1) // 2]
            i = (i-1) // 2
        self.sez = s

    # odstranimo minimum in ga vrnemo
    def pop(self): # O(logn)
        s = self.sez
        IZHOD = s[0]
        s[0] = s[-1]
        s.pop()
        if s:
            i = 0
            while True:
                levi, desni = self.otroka(i)
                if levi < len(s):
                    C1 = s[levi]
                else:
                    C1 = s[i]
                if desni < len(s):
                    C2 = s[desni]
                else:
                    C2 = s[i]
                if C1 < C2 and C1 < s[i]:
                    s[i], s[levi] = s[levi], s[i]
                    i = levi
                elif C1 >= C2 and C2 < s[i]:
                    s[i], s[desni] = s[desni], s[i]
                    i = desni
                else:
                    break
        self.sez = s
        return IZHOD

    # vrne indeks elementa "v" v kopici
    def najdi_indeks(self, v, i = 0): # O(logn)
        if i >= len(self.sez):
            return 0
        if self.sez[i] == v:
            return i
        levi, desni = self.otroka(i)
        return self.najdi_indeks(v, levi) + self.najdi_indeks(v, desni)

    def posodobi(self, staro, novo): # O(logn)
        s = self.sez
        i = self.najdi_indeks(staro)
        if s[i] != staro:
            raise ValueError("Staro ni v kopici.")
        s[i] = novo
        while i != 0 and s[i] < s[(i-1) // 2]:
            s[(i-1) // 2], s[i] = s[i], s[(i-1) // 2]
            i = (i-1) // 2
        self.sez = s

#-----------------------------------------------------------------------------
# DIJKSTRA 
#-----------------------------------------------------------------------------

# O(n + logn + n x logn + m x logn) = O((n + m) x logn)
def dijkstra(graf, utezi, s, t, C, D, maxh):
    n = len(graf)

    dolzina_poti = {}
    cena_poti = {}

    for i in range(1, n + 1): # O(n)
        dolzina_poti[i] = "inf"
        cena_poti[i] = "inf"

    dolzina_poti[s] = 0 # O(1)
    cena_poti[s] = 0  # O(1)

    kopica = MinKopica()  # (dolzina, cena, vozlisce) O(1)
    kopica.push( # O(logn)
        (dolzina_poti[s], cena_poti[s], s)
        ) 

    while kopica.sez:
        _, _, u = kopica.pop() # odstranimo min v O(n x logn)

        for v in graf[u]: # O(m)
            for povezava in utezi[(u, v)]:

                visina = povezava[0]

                if visina > maxh:
                    continue

                nova_dolzina = dolzina_poti[u] + povezava[1]
                nova_cena = cena_poti[u] + povezava[2]

                if nova_dolzina > D or nova_cena > C:
                    continue
                
                # ce sosed neobiskan, mu nastavimo d,c in dodamo v kopico
                if dolzina_poti[v] == "inf":
                    kopica.push( # O(logn)
                        (nova_dolzina, nova_cena, v)
                        )

                    dolzina_poti[v] = nova_dolzina
                    cena_poti[v] = nova_cena
                    continue

                # sicer, preverimo ce je pot s->...->u->v 
                # boljsa kot obstojeca pot s->...->v
                stara_dolzina = dolzina_poti[v]
                stara_cena = cena_poti[v]

                if ( (nova_dolzina < stara_dolzina and nova_cena <= C) or
                (nova_dolzina == stara_dolzina and nova_cena < stara_cena) ):

                    staro = (stara_dolzina, stara_cena, v)
                    novo = (nova_dolzina, nova_cena, v)

                    kopica.posodobi(staro, novo) # O(logn)

                    dolzina_poti[v] = nova_dolzina
                    cena_poti[v] = nova_cena

    return (dolzina_poti[t], cena_poti[t])

#-----------------------------------------------------------------------------
# CESTE
#-----------------------------------------------------------------------------

# n vozlisc
# m usmerjenih povezav
# s zacetek
# t cilj 
# C max skupna cena
# D max skupna dolzina

# Izpisemo 3 stevlike:
# min visina da sploh pridemo od s do t, ter dolzina in cena najkrajse in najcenejse
# med potmi s potrebno najvec visino iz prvega izhoda 
# Če obstaja vec najkrajsih poti, uzames najcenejso izmed njih

def main():
    vhod = sys.stdin.read().strip().split("\n\n")
    st_primerov = int(vhod.pop(0))
    izhod = ""

    for _ in range(1, st_primerov + 1): # O(T)

        primer = vhod.pop(0).split("\n")
        n, m, s, t = map(int, primer.pop(0).split(" "))
        C, D = map(int, primer.pop(0).split(" "))

        graf = {i: set() for i in range(1, n + 1)} # O(n)
        utezi = {}

        for _ in range(m): # O(m)
            u, v, c, d, h = map(int, primer.pop(0).split(" "))
            graf[u] = graf[u] | {v}
            utezi[(u, v)] = utezi.get((u, v), set()) | {(h, d, c)}

        visine = sorted(e[0] for povezave in utezi.values() for e in povezave)
        
        maxh = "inf"
        while visine:
            maxh = visine[0]
            visine = visine[1:]
            mind, minc = dijkstra(graf, utezi, s, t, C, D, maxh)
            if mind != "inf" and mind <= D and minc <= C:
                break

        if mind == "inf":
            izhod += "-1\n"
        else:
            izhod += f"{maxh} {mind} {minc}\n"

    print(izhod.strip())

main()