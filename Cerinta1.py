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

#multime = lambda_inchidere(stari_initiale, delta)

#print(multime)

#print(stari)

#print(stari_initiale)

for stare in stari:
    #print(stare)
    primul_lambda = lambda_inchidere([stare], delta)
    #print(primul_lambda)
    for a in alfabet:
        prima_litera = set()
        for s in primul_lambda:
            for j in delta.get(s, {}).get(a, []):
                prima_litera.add(j)

        if prima_litera:
            al_doilea_lambda = lambda_inchidere(prima_litera, delta)
            print(f"Din --{stare}-- mergem cu lambda in {primul_lambda}, apoi cu --{a}-- in {prima_litera}, iar apoi cu lambda in --{al_doilea_lambda}--")

        else:
            print(f"Din --{stare}-- mergem cu lambda in {primul_lambda}, apoi MULTIMEA VIDA")
