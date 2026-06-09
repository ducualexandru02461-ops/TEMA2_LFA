f = open("Cerinta2.in")
w = open("Cerinta2.out", "w")

stari = {x for x in f.readline().strip().split(" ")}
alfabet = [x for x in f.readline().strip().split(" ")]
nr_tranzitii = f.readline().strip()

graf = {}
for s in stari:
    graf[s] = {}

for i in range(int(nr_tranzitii)):
    tranzitie = f.readline().strip().split(" ")
    s_init = tranzitie[0]
    s_fin = tranzitie[1]
    simbol = tranzitie[2]
    
    if s_fin in graf[s_init]:
        graf[s_init][s_fin] = graf[s_init][s_fin] + "+" + simbol
    else:
        graf[s_init][s_fin] = simbol

stare_initiala = f.readline().strip()
stari_finale = set(f.readline().strip().split(" "))

graf["S_nou"] = {}
graf["S_nou"][stare_initiala] = "lambda"

graf["F_nou"] = {}
for sf in stari_finale:
    if sf not in graf:
        graf[sf] = {}
    
    if "F_nou" in graf[sf]:
        graf[sf]["F_nou"] += "+lambda"
    else:
        graf[sf]["F_nou"] = "lambda"

def concateneaza(r1, r_bucla, r2):
    if r1 == "lambda": r1 = ""
    if r2 == "lambda": r2 = ""
    
    if r_bucla:
        if len(r_bucla) > 1 and "+" in r_bucla:
            mijloc = f"({r_bucla})*"
        else:
            mijloc = f"{r_bucla}*"
    else:
        mijloc = ""
        
    rezultat = f"{r1}{mijloc}{r2}"
    if rezultat == "": 
        return "lambda"
    return rezultat

for stare_curenta in stari:
    intrari = []
    iesiri = []
    
    for nod in graf:
        if nod != stare_curenta and stare_curenta in graf[nod]:
            intrari.append(nod)
            
    for vecin in graf.get(stare_curenta, {}):
        if vecin != stare_curenta:
            iesiri.append(vecin)
            
    r_bucla = graf.get(stare_curenta, {}).get(stare_curenta, None)
    
    for intrare in intrari:
        for iesire in iesiri:
            r_in = graf[intrare][stare_curenta]
            r_out = graf[stare_curenta][iesire]
            
            noua_cale = concateneaza(r_in, r_bucla, r_out)
            
            if len(noua_cale) > 1 and "+" in noua_cale:
                 noua_cale = f"({noua_cale})"
            
            if iesire in graf[intrare]:
                r_direct = graf[intrare][iesire]
                graf[intrare][iesire] = f"({r_direct}+{noua_cale})"
            else:
                graf[intrare][iesire] = noua_cale

    if stare_curenta in graf:
        del graf[stare_curenta]
    for nod in graf:
        if stare_curenta in graf[nod]:
            del graf[nod][stare_curenta]


expresie_regulata = graf["S_nou"]["F_nou"]

w.write("Expresia regulata rezultata este:\n")
w.write(expresie_regulata + "\n")

f.close()
w.close()
