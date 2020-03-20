from collections import namedtuple


Nod = namedtuple('Nod', ['stare', 'd', 'g', 'pred'])  # definesc "tipul de data" specific unui nod


def citire_din_fisier(fisier):
    """
    Functie folosita pentru citirea din fisier
    :param fisier: calea catre fisierul care urmeaza sa fie citit
    :return: o lista de tupluri care cotin informatiile din fisier (<oras_x>, <oras_y>, <distanta>)
    """
    with open(fisier, 'r') as f:
        a = f.readlines()  # citesc toate liniile din fisier
    assert len(a[0].split(' ')) == 2, "Header error"  # verific daca in header am fix 2 elemente
    # (nr.orase si nr. drumuri)
    int_nr_drumuri = int(a[0].split(' ')[1])
    assert len(a) == int_nr_drumuri + 1, "Not enough roads"  # verific daca numarul de drumuri specificat in header
    # este respectat
    Drum = namedtuple("Drum", ['A', 'B', 'dist'])  # declar tuplul
    lst_drumuri = []  # creez lista de drumuri si o initializez cu lista vida
    for int_index in range(1, int_nr_drumuri + 1):  # pentru fiecare linie, de la a doua pana la ultima
        lst_linie = a[int_index].split(' ')  # extrag intr-o lista toate elementele dintr-o linie
        assert len(lst_linie) == 3, "Wrong format"  # verific ca am formatul corect pentru fiecare linie
        str_oras_x = lst_linie[0]
        str_oras_y = lst_linie[1]
        int_distanta = int(lst_linie[2])
        drum = Drum(str_oras_x, str_oras_y, int_distanta)  # creez un drum cu informatiile de mai sus
        lst_drumuri.append(drum)  # adaug drumul creat la lista de drumuri
    return lst_drumuri  # returnez lista de drumuri


def get_vecini_si_distante(lst_drumuri, oras):
    """
    Acaesta functie returneaza vecinii unui oras
    :param lst_drumuri: lista de drumuri
    :param oras: orasul ai carui vecini dorim sa ii aflam
    :return: o lista de tupluri de forma: (<vecin>, <distanta>)
    """
    lst_vecini = []  # creez si initializez cu lista vida lista de vecini
    for drum in lst_drumuri:  # parcurg fiecare drum
        if oras == drum.A:  # daca drumul pleaca din orasul de interes
            tpl_vecin = (drum.B, drum.dist)  # creez tuplul cu informatia despre vecin
            lst_vecini.append(tpl_vecin)  # adaug tuplul in lista de vecini
        if oras == drum.B:  # daca drumul ajunge in orasul de interes
            tpl_vecin = (drum.A, drum.dist)  # creez tuplul cu informatia despre vecin
            lst_vecini.append(tpl_vecin)  # adaug tuplul in lista de vecini
    return lst_vecini


def get_vecin_apropiat(lst_drumuri, oras):
    """
    Aceasta functie returneaza cel mai apropiat vecin al unui oras
    :param lst_drumuri: lista tuturor drumurilor de pe harta
    :param oras: orasul de interes
    :return: returneaza un tuplu de forma (<oras>, <distanta>) cu informatii despre cel mai apropiat vecin
    """
    contor = 0
    lst_vecini = get_vecini_si_distante(lst_drumuri, oras)  # aflu toti vecinii orasului de interes
    tpl_vecin_apropiat = lst_vecini[0]  # initializez cel mai apropiat vecin ca fiind primul vecin
    for tpl_vecin in lst_vecini:  # parcurg lista de vecini
        if tpl_vecin[1] < tpl_vecin_apropiat[1]:  # daca gasesc un vecin mai apropiat decat vechiul vecin apropiat
            print(contor)
            contor += 1
            tpl_vecin_apropiat = tpl_vecin  # vecinul cel mai apropiat devine vecinul de la iteratia curenta
    return tpl_vecin_apropiat  # returnez cel mai apropiat vecin


def expandare(nod, lst_drumuri):
    """
    Aceasta functie expandeaza informatia despre vecinii unui nod
    :param nod: nodul ai carui vecini trebuie sa ii expandam
    :param lst_drumuri: lista tuturor drumurilor
    :return: o lista de noduri care contine toti vecinii
    """
    # Extrag in variabile locale informaia pe care deja o am despre nod
    stare = nod.stare
    distanta = nod.d
    cost = nod.g
    pred = nod.pred
    # Compun lista de predecesori pentru nodurile vecine:
    pred = list(pred)
    pred.append(stare)
    pred = tuple(pred)
    lst_tupluri = []  # creez si initializez lista de noduri vecine
    lst_vecini = get_vecini_si_distante(lst_drumuri, stare)  # caut vecinii
    for tpl_vecin in lst_vecini:  # pentru fiecare vecin
        vecin = Nod(tpl_vecin[0], distanta + tpl_vecin[1], cost + 1, pred)  # cree un nod cu informatiile depre vecin
        if tpl_vecin[0] not in pred:
            lst_tupluri.append(vecin)  # adaug nodul la lista de noduri
    return lst_tupluri  # returnez lista de noduri


def selecteaza_nod_de_expandare(frontiera):
    """
    Functia cauta pe frontiera, primul element cu gradul cel mai mic
    :param frontiera: frontiera care trebuie parcursa
    :return: primul nod intalnit, cu gradul cel mai mic
    """
    nod_min = frontiera[0]  # initializez nodul cu distanta minima ca fiind primul nod din lista
    for nod in frontiera:  # parcurg frotiera
        if nod.d < nod_min.d:  # daca gasesc un nod cu o distanta mai mica decat cea veche
            # (am folosit mai mic pentru a-l obtine strict pe primul)
            nod_min = nod  # nodul cu distanta minima devine nodul curent
    return nod_min  # returnez nodul curent


def cautare_in_largime(nod_initial, stare_finala, lst_drumuri):
    """
    In aceasta functie este implementat algoritmul de cautare in largime
    :param nod_initial: nodul de la care plecam
    :param stare_finala: nodul la care vrem sa ajungem
    :param lst_drumuri: lista totala de drumuri
    :return: o lista cu nodurile care trebuie parcurse pentru a ajunge la destinatie
    """
    frontiera = [nod_initial]  # adaug nodul initial in frontiera
    while frontiera:  # cat timp frontiera nu este vida
        nod = selecteaza_nod_de_expandare(frontiera)  # aleg urmatorul nod de expandat
        if nod.stare == stare_finala:  # daca nodul curent este destinatia
            pred = list(nod.pred)
            pred.append(nod.stare)
            pred = tuple(pred)
            return pred  # returnez toate nodurile paarcurse pana la destinatie
        lst_elem_expandate = expandare(nod, lst_drumuri)  # expandez nodul curent
        # Inlocuiesc nodul curent de pe frontiera cu nodurile rezultate in urma expandarii
        index_nod = frontiera.index(nod)
        frontiera[index_nod:index_nod + 1] = lst_elem_expandate
    return []  # returnez o lista vida in caz de eroare


def selecteaza_nod_de_expandare_adancime(frontiera):
    """
    Functia cauta pe frontiera, primul element cu gradul cel mai mic
    :param frontiera: frontiera care trebuie parcursa
    :return: primul nod intalnit, cu gradul cel mai mic
    """
    nod_min = frontiera[-1]  # initializez nodul cu distanta minima ca fiind primul nod din lista
    # for nod in frontiera:  # parcurg frotiera
    #     if nod.d > nod_min.d:  # daca gasesc un nod cu o distanta mai mica decat cea veche
    #         # (am folosit mai mic pentru a-l obtine strict pe primul)
    #         nod_min = nod  # nodul cu distanta minima devine nodul curent
    return nod_min  # returnez nodul curent


def cautarea_in_adancime(nod_initial, stare_finala, lst_drumuri):
    """
    In aceasta functie este implementat algoritmul de cautare in largime
    :param nod_initial: nodul de la care plecam
    :param stare_finala: nodul la care vrem sa ajungem
    :param lst_drumuri: lista totala de drumuri
    :return: o lista cu nodurile care trebuie parcurse pentru a ajunge la destinatie
    """
    frontiera = [nod_initial]  # adaug nodul initial in frontiera
    while frontiera:  # cat timp frontiera nu este vida
        nod = selecteaza_nod_de_expandare_adancime(frontiera)  # aleg urmatorul nod de expandat
        if nod.stare == stare_finala:  # daca nodul curent este destinatia
            pred = list(nod.pred)
            pred.append(nod.stare)
            pred = tuple(pred)
            if len(pred) <= 5:  # pentru cautarea in adancime limitata
                return pred  # returnez toate nodurile paarcurse pana la destinatie
        lst_elem_expandate = expandare(nod, lst_drumuri)  # expandez nodul curent
        # Inlocuiesc nodul curent de pe frontiera cu nodurile rezultate in urma expandarii
        index_nod = frontiera.index(nod)
        frontiera[index_nod:index_nod + 1] = lst_elem_expandate
    return []  # returnez o lista vida in caz de eroare


def main():
    """
    Metoda main, principala
    :return: NA
    """
    lst_drumuri = citire_din_fisier("map_input.txt")  # citest toate drumurile
    nod_init = Nod('Arad', 0, 0, ())  # initializez nodul de start
    drum = cautare_in_largime(nod_init, 'Iasi', lst_drumuri)  # caut drumul pana la destinatie
    print(drum)  # Afisez drumul ce trebuie parcurs
    drum_adancime = cautarea_in_adancime(nod_init, 'Oradea', lst_drumuri)
    print(drum_adancime)


if __name__ == "__main__":
    main()
