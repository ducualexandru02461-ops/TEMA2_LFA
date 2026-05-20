from collections import deque

f = open("Cerinta1.in")
w = open("Cerinta1.out", "w")

#nr_stari = f.readline().strip()
stari = {x for x in f.readline().strip().split(" ")}

alfabet = [x for x in f.readline().strip().split(" ")]
nr_tranzitii = f.readline().strip()


delta = {}
for i in range (int(nr_tranzitii)): # Cream dictionarul pentru functia tranzitie
    tranzitie = f.readline().strip().split(" ")
    stare_initiala = tranzitie[0]
    stare_finala = tranzitie[1]
    litera = tranzitie[2]
    if stare_initiala not in delta:
        delta[stare_initiala] = {}
    if litera not in delta[stare_initiala]:
        delta[stare_initiala][litera] = []
    delta[stare_initiala][litera].append(stare_finala)
print(delta)

stare_initiala = f.readline().strip()
#print(stare_initiala)

def lambda_inchidere(stari_initiale, delta):
    inchidere = set(stari_initiale)
    stiva = list(stari_initiale)
    while stiva:
        stare_curenta = stiva.pop()
        for stare_urmatoare in delta.get(stare_curenta, {}).get("lambda", []):
            if stare_urmatoare not in inchidere:
                inchidere.add(stare_urmatoare)
                stiva.append(stare_urmatoare)
    return inchidere

def subset_construction(stare_initiala, alfabet, delta):
    start = frozenset(lambda_inchidere([stare_initiala], delta))
    queue = deque([start])
    vizitate = {start}
    dfa = {}
    while queue:
        stare_curenta = queue.popleft()
        dfa[stare_curenta] = {}
        for simbol in alfabet:
            urmatoare = set()
            for stare in stare_curenta:
                for vecin in delta.get(stare, {}).get(simbol, []):
                    urmatoare.update(
                        lambda_inchidere([vecin], delta)
                    )
            urmatoare = frozenset(urmatoare)
            dfa[stare_curenta][simbol] = urmatoare
            w.write(f"Din {stare_curenta} mergem cu {simbol} in {urmatoare}\n")
            if urmatoare not in vizitate:
                vizitate.add(urmatoare)
                queue.append(urmatoare)
    return dfa

subset_construction(stare_initiala, alfabet, delta)
