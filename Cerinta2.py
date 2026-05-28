f = open("Cerinta2.in")
w = open("Cerinta2.out", "w")

# Citim datele de intrare exact cum le aveai tu
stari = {x for x in f.readline().strip().split(" ")}
alfabet = [x for x in f.readline().strip().split(" ")]
nr_tranzitii = f.readline().strip()

# Initializam graful (GNFA-ul) unde vom memora expresiile regulate pe tranzitii
graf = {}
for s in stari:
    graf[s] = {}

# Citim tranzitiile si construim graful initial
for i in range(int(nr_tranzitii)):
    tranzitie = f.readline().strip().split(" ")
    s_init = tranzitie[0]
    s_fin = tranzitie[1]
    simbol = tranzitie[2]
    
    # Daca exista deja o litera intre 2 stari, le reunim cu "+" (ex: a+b)
    if s_fin in graf[s_init]:
        graf[s_init][s_fin] = graf[s_init][s_fin] + "+" + simbol
    else:
        graf[s_init][s_fin] = simbol

stare_initiala = f.readline().strip()
stari_finale = set(f.readline().strip().split(" "))

### STANDARDIZAREA
# Adaugam starea initiala noua
graf["S_nou"] = {}
graf["S_nou"][stare_initiala] = "lambda"

# Adaugam starea finala noua si legam vechile stari finale de ea cu "lambda"
graf["F_nou"] = {}
for sf in stari_finale:
    # Ne asiguram ca starea exista in graf ca nod de plecare
    if sf not in graf:
        graf[sf] = {}
    
    if "F_nou" in graf[sf]:
        graf[sf]["F_nou"] += "+lambda"
    else:
        graf[sf]["F_nou"] = "lambda"

### FUNCTIE AJUTATOARE: Construirea noului string fara "lambda"-uri inutile
def concateneaza(r1, r_bucla, r2):
    # Daca r1 sau r2 sunt doar lambda, le ignoram in text
    if r1 == "lambda": r1 = ""
    if r2 == "lambda": r2 = ""
    
    # Gestionam bucla: daca exista, punem steluta
    if r_bucla:
        if len(r_bucla) > 1 and "+" in r_bucla:
            mijloc = f"({r_bucla})*"
        else:
            mijloc = f"{r_bucla}*"
    else:
        mijloc = ""
        
    rezultat = f"{r1}{mijloc}{r2}"
    if rezultat == "": # Daca toate au fost lambda si s-au sters
        return "lambda"
    return rezultat


### ELIMINAREA STARILOR INTERMEDIARE
# Iteram prin setul initial de stari pentru a le elimina pe rand
for stare_curenta in stari:
    intrari = []
    iesiri = []
    
    # Cautam stările din care primim sageti (X)
    for nod in graf:
        if nod != stare_curenta and stare_curenta in graf[nod]:
            intrari.append(nod)
            
    # Cautam stările spre care pleaca sageti din starea curenta (Y)
    for vecin in graf.get(stare_curenta, {}):
        if vecin != stare_curenta:
            iesiri.append(vecin)
            
    # Verificam daca starea curenta are o bucla (sageata spre ea insasi)
    r_bucla = graf.get(stare_curenta, {}).get(stare_curenta, None)
    
    # Refacem legaturile: din fiecare intrare direct catre fiecare iesire
    for intrare in intrari:
        for iesire in iesiri:
            r_in = graf[intrare][stare_curenta]
            r_out = graf[stare_curenta][iesire]
            
            noua_cale = concateneaza(r_in, r_bucla, r_out)
            
            # Daca drumul nou calculat e complex, il punem intre paranteze
            if len(noua_cale) > 1 and "+" in noua_cale:
                 noua_cale = f"({noua_cale})"
            
            # Daca exista deja o legatura directa, le adunam: (DrumVechi + DrumNou)
            if iesire in graf[intrare]:
                r_direct = graf[intrare][iesire]
                graf[intrare][iesire] = f"({r_direct}+{noua_cale})"
            else:
                graf[intrare][iesire] = noua_cale

    # Dupa ce am salvat toate caile ocolitoare, STERgem starea complet din graf
    if stare_curenta in graf:
        del graf[stare_curenta]
    for nod in graf:
        if stare_curenta in graf[nod]:
            del graf[nod][stare_curenta]


### AFISAREA REZULTATULUI FINAL
expresie_regulata = graf["S_nou"]["F_nou"]

w.write("Expresia regulata rezultata este:\n")
w.write(expresie_regulata + "\n")

f.close()
w.close()
