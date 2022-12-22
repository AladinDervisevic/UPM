import sys


def topo_sort(graf : dict): # O(n + m)
    n = len(graf)
    in_deg = [0] * (n + 1)

    for u in range(1, n + 1): # O(n + 2m)
        for v in graf[u]:
            in_deg[v] += 1

    sklad = [u for u in graf if in_deg[u] == 0]
    toposka_ureditev = []

    while sklad: # O(n + m)
        t = sklad.pop(0)
        toposka_ureditev.append(t)
        for v in graf[t]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                sklad.append(v)

    return toposka_ureditev


def main(): # O(m + n)
    vhod = sys.stdin.read().strip().split("\n\n")
    st_primerov = int(vhod.pop(0))
    izhod = ""

    for _ in range(st_primerov):

        primer = vhod.pop(0).split("\n")
        n, m = map(int, primer.pop(0).split(" "))

        sosedi = {i: set() for i in range(1, n + 1)}
        cene = {}
        for _ in range(m): # O(m)
            u, v, c = map(int, primer.pop(0).split(" "))
            sosedi[u] = sosedi[u] | {v}
            cene[(u, v)] = c

        s, f = map(int, primer.pop(0).split(" "))

        T = topo_sort(sosedi) # O(m + n)
        T = T[T.index(s): T.index(f)]

        while T:
            if f in sosedi[T[-1]]:
                break
            T = T[:-1]

        cena_poti = [0] * (n + 1)  # pot[i] = najdrazja pot od s do i

        for u in T:
            for v in sosedi[u]:
                cena_poti[v] = max(
                    cena_poti[v], 
                    cena_poti[u] + cene[(u, v)]
                )
        
        cena = cena_poti[f] if cena_poti[f] else -1
        izhod += str(cena) + "\n"

    print(izhod.strip())

main()