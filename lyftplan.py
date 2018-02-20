#!/usr/bin/env python

kb = ("Knäböj (tävling)", None, [(80, 1, "2017-11-11")])
kb1 = ("Knäböj (hög stång)", kb, [(80, 1, "2017-11-11")])
kb2 = ("Knäböj (hög stång, bälte)", kb, [(80, "2017-11-11")])

pass_a = [
(kb_bredboj, "Långsam ned", [(30,3), (40,3),(40,3),(40,3),(40,3),(40,3),(40,3),(40,3)]),
(kb, "Fokus: hastighet, fulldjup", [(50,2), (52.5,2), (55,2), (57.5, 2), (60,2), (65,1), (65,1), (65,1), (65,1), (65,1), (70,1), (70,1), (50,5)]),
(rygg_hangande_rodd, "", [(5,), (5,)]),
(rygg_latsdrag, "Lätt: kontakt & pymp", [(10,), (10,)]),
(bp_tavling, "", [(40,5), (50,5), (60,1), (62.5,1), (62.5,1), (62.5,1)]),
(bp_pinpress, "", [(45,5), (47.5,5), (55,2), (55,2), (55,2), (55,2), (55,2)]),
(rygg_tryndrag, "Tungt", [(20,), (15,), (10,)]),
(marklyft_klotsving, "", [(16,20), (16,20)]),
(marklyft_sumo, "", [(50,5), (60,5), (70,5), (80,3), (85,2), (90,1), (85,2), (85,2)]),
(marklyft_klotsving, "", [(20,10), (24,8)]),
(rygg_lyft, "Tungt", [(10,0), (5,10), (10,10), (10,10), (10,10), (10,10)])
]

def print_session(sess):
    

def main():
    print_session(pass_a)

if __name__ == '__main__':
    main()


