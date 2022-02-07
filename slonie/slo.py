from icecream import ic

n = 10
masy = [3015, 4728, 4802, 4361, 135, 4444, 4313, 1413, 4581, 546]
pocz = [3, 10, 1, 8, 9, 4, 2, 7, 6, 5]
docel = [4, 9, 5, 3, 1, 6, 10, 7, 8, 2]
# n = 6
# masy = [2400, 2000, 1200, 2400, 1600, 4000]
# pocz = [1,4,5,3,6,2]
# docel = [5,3,2,4,6,1]

# Graf z danych wejściowych

graf_zmian = {}
for x in pocz:
    graf_zmian[x] = pocz[docel.index(x)]

print(graf_zmian)
print(graf_zmian[1])


cykle = {}  # pewnie można też to zrobić listą - do późniejszej optymalizacji
odw = [False] * n
c = 0   # numer cyklu

def sprawdz_wierzcholek(numer):
    if not odw[numer-1]:
        odw[numer-1] = True
        # print(f"Aktualny wierzchołek: {numer}. Następny wierzchołek: {graf_zmian[numer]}")
        # wierzchołek dodaj do cyklu
        cykle[c].append(numer)
        sprawdz_wierzcholek(graf_zmian[numer])

def masa(e):
    return masy[e-1]

for i in range (n):
    x = i + 1 # numer słonia
    print(f"i = {i}, x = {x}")
    if not odw[i]:
        c += 1
        cykle[c] = []
        # print(f"Wierzchołek {x} jest nieodwiedzony. Początek cyklu nr. {c}")
        sprawdz_wierzcholek(x)
        print(odw)
    # else: 
        # print(f"Wierzchołek {x} był odwiedzony")
    print()
print(f"Cykle: {cykle}\n\n")

min_ogol = 10000
sumy_cykli = []
min_cykli = []
for cykl in cykle:
    print(f"\nCykl: {cykl}: {cykle[cykl]}")
    suma_cyklu = 0
    min_cyklu = 10000
    for e in cykle[cykl]:
        print(f"e (słoń): {e}")
        print(f"masa słonia: {masa(e)}")
        suma_cyklu += masa(e)    # masa(e) - masa słonia e (wierzchołka)        # dodać do sumy_cykli
        min_cyklu = min(min_cyklu, masa(e))
        print(f"min_cyklu: {min_cyklu}")
    sumy_cykli.append(suma_cyklu)
    min_cykli.append(min_cyklu)
    min_ogol = min(min_ogol, min_cyklu)
    print(f"min_ogol: {min_ogol}")
    ic(sumy_cykli)

wynik = 0
print()
ic(cykle)
# ic(min_cykli)
for i in range(c):
    ic(i)
    ic(sumy_cykli[i])
    ic(len(cykle[i+1]))
    ic(min_cykli[i])
    metoda_1 = sumy_cykli[i] + (len(cykle[i+1]) - 2) * min_cykli[i]
    metoda_2 = sumy_cykli[i] + min_cykli[i] + (len(cykle[i+1]) + 1) * min_ogol
    ic(metoda_1)
    ic(metoda_2)
    wynik += min(metoda_1, metoda_2)

ic(wynik)
return wynik