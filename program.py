#!/usr/bin/env python3
# encoding:utf-8

from lyftplan import *

pass_a = Session([
Line(kb_bred, "Långsam ned",                [(30,3), (40,3),(40,3),(40,3),(40,3),(40,3),(40,3),(40,3)]),
Line(kb_hs, "Fokus: hastighet, fulldjup",   [(50,2), (52.5,2), (55,2), (57.5, 2), (60,2), (65,1), (65,1), (65,1), (65,1), (65,1), (70,1), (70,1), (50,5)]),
Line(rygg_hangande_rodd, "",                [(5,), (5,)]),
Line(rygg_latsdrag, "Lätt: kontakt & pymp", [(10,), (10,)]),
Line(bp, "",                                [(40,5), (50,5), (60,1), (62.5,1), (62.5,1), (62.5,1)]),
Line(bp_pinpress, "",                       [(45,5), (47.5,5), (55,2), (55,2), (55,2), (55,2), (55,2)]),
Line(rygg_tryndrag, "Tungt",                [(20,), (15,), (10,)]),
Line(rumpa_klotsving, "",                      [(16,20), (16,20)]),
Line(ml_sumo, "",                           [(50,5), (60,5), (70,5), (80,3), (85,2), (90,1), (85,2), (85,2)]),
Line(rumpa_klotsving, "",                      [(20,10), (24,8)]),
Line(rygg_lyft, "Tungt",                    [(10,0), (5,10), (10,10), (10,10), (10,10), (10,10)])
])

pass_b = Session([
Line(kb_bred, "Långsam ned",                [(30,3), (40,3),(40,3),(40,3),(40,3),(40,3),(40,3),(40,3)]),
Line(kb_hs, "Fokus: hastighet, fulldjup",   [(50,2), (52.5,2), (55,2), (57.5, 2), (60,2), (65,1), (65,1), (65,1), (65,1), (65,1), (70,1), (70,1), (50,5)]),
Line(rygg_hangande_rodd, "",                [(5,), (5,)]),
Line(rygg_latsdrag, "Lätt: kontakt & pymp", [(10,), (10,)]),
Line(bp, "",                                [(40,5), (50,5), (60,1), (62.5,1), (62.5,1), (62.5,1)]),
Line(bp_pinpress, "",                       [(45,5), (47.5,5), (55,2), (55,2), (55,2), (55,2), (55,2)]),
Line(rygg_tryndrag, "Tungt",                [(20,), (15,), (10,)]),
Line(rumpa_klotsving, "",                      [(16,20), (16,20)]),
Line(ml_sumo, "",                           [(50,5), (60,5), (70,5), (80,3), (85,2), (90,1), (85,2), (85,2)]),
Line(rumpa_klotsving, "",                      [(20,10), (24,8)]),
Line(rygg_lyft, "Tungt",                    [(10,0), (5,10), (10,10), (10,10), (10,10), (10,10)])
])

pass_c = Session([
Line(kb_bred, "Långsam ned",                [(30,3), (40,3),(40,3),(40,3),(40,3),(40,3),(40,3),(40,3)]),
Line(kb_hs, "Fokus: hastighet, fulldjup",   [(50,2), (52.5,2), (55,2), (57.5, 2), (60,2), (65,1), (65,1), (65,1), (65,1), (65,1), (70,1), (70,1), (50,5)]),
Line(rygg_hangande_rodd, "",                [(5,), (5,)]),
Line(rygg_latsdrag, "Lätt: kontakt & pymp", [(10,), (10,)]),
Line(bp, "",                                [(40,5), (50,5), (60,1), (62.5,1), (62.5,1), (62.5,1)]),
Line(bp_pinpress, "",                       [(45,5), (47.5,5), (55,2), (55,2), (55,2), (55,2), (55,2)]),
Line(rygg_tryndrag, "Tungt",                [(20,), (15,), (10,)]),
Line(rumpa_klotsving, "",                      [(16,20), (16,20)]),
Line(ml_sumo, "",                           [(50,5), (60,5), (70,5), (80,3), (85,2), (90,1), (85,2), (85,2)]),
Line(rumpa_klotsving, "",                      [(20,10), (24,8)]),
Line(rygg_lyft, "Tungt",                    [(10,0), (5,10), (10,10), (10,10), (10,10), (10,10)])
])

pass_c = Session([
kb_bred("Långsam ned",                        sets("30x3 40x3 40x3 40x3 40x3 40x3 40x3 40x3")),
kb_hs("Fokus: hastighet, fulldjup",           sets("50x2 52.5x2 55x2 57.5x2 60x2 65x1 65x1 65x1 65x1 65x1 70x1 70x1 50x5")),
rygg_hangande_rodd("",                        sets("5 5")),
rygg_latsdrag("Lätt: kontakt & pymp",         sets("10 10")),
bp("",                                        sets("40x5 50x5 60x1 62.5x1 62.5x1 62.5x1")),
bp_pinpress("",                               sets("45x5 47.5x5 55x2 55x2 55x2 55x2 55x2")),
rygg_tryndrag("Tungt",                        sets("20 15 10")),
rumpa_klotsving("",                           sets("16x20 16x20")),
ml_sumo("",                                   sets("50x5 60x5 70x5 80x3 85x2 90x1 85x2 85x2")),
rumpa_klotsving("",                           sets("20x10 24x8")),
rygg_lyft("Tungt",                            sets("10 5x10 10x10 10x10 10x10 10x10")),
])

vecka_1 = Week([pass_a, pass_b, pass_c], date=(2018, 3, 5))

#Line(kb_bred, "Långsam ned", sets("30x3 40x3 40x3 40x3 40x3 40x3 40x3 40x3"))

# function call overloading?
#kb_bred("Långsam ned", sets("30x3 40x3 40x3 40x3 40x3 40x3 40x3 40x3"))

#a = rygg_lyft("Tungt",                    [(10,0), (5,10), (10,10), (10,10), (10,10), (10,10)])
#b = rygg_lyft("Tungt",                    sets("10x0 5x10 10x10 10x10 10x10 10x10"))



"""
c = "rygg_lyft Tungt | 10x0 5x10 10x10 10x10 10x10 10x10"
line = c
items = dict(globals().items())
for n, o in items.items():
    name = line.split()[0].strip()
    comment = line.split()[1].strip()
    setspec = line.split('|')[1].strip()

    print(name, comment, setspec, "vs", n, o)
    if n == name and isinstance(o, Exercise):
        print("calling {}({}, {}, {})".format(o, name, comment, sets(setspec)))
        l = o(comment, sets(setspec))
        print("l: {}".format(l))
"""



#
# App
#
def main():
    #print_lines(pass_a)

    test_sets()

    print("Vecka 1: {}".format(vecka_1.date))

    stats = Statistics(vecka_1)
    print_stats(stats)

    print()

    for i in range(len(vecka_1)):
        print("     Pass {}: {}".format(i+1, vecka_1[i].date))

        stats = Statistics(vecka_1[i])
        print_stats(stats, indent=1)

        print()


if __name__ == '__main__':
    main()


