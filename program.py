#!/usr/bin/env python3

from lyftplan import *

pass_a = [
Line(kb_bred, "Långsam ned",                [(30,3), (40,3),(40,3),(40,3),(40,3),(40,3),(40,3),(40,3)]),
Line(kb, "Fokus: hastighet, fulldjup",      [(50,2), (52.5,2), (55,2), (57.5, 2), (60,2), (65,1), (65,1), (65,1), (65,1), (65,1), (70,1), (70,1), (50,5)]),
Line(rygg_hangande_rodd, "",                [(5,), (5,)]),
Line(rygg_latsdrag, "Lätt: kontakt & pymp", [(10,), (10,)]),
Line(bp, "",                                [(40,5), (50,5), (60,1), (62.5,1), (62.5,1), (62.5,1)]),
Line(bp_pinpress, "",                       [(45,5), (47.5,5), (55,2), (55,2), (55,2), (55,2), (55,2)]),
Line(rygg_tryndrag, "Tungt",                [(20,), (15,), (10,)]),
Line(ml_klotsving, "",                      [(16,20), (16,20)]),
Line(ml_sumo, "",                           [(50,5), (60,5), (70,5), (80,3), (85,2), (90,1), (85,2), (85,2)]),
Line(ml_klotsving, "",                      [(20,10), (24,8)]),
Line(rygg_lyft, "Tungt",                    [(10,0), (5,10), (10,10), (10,10), (10,10), (10,10)])
]

#
# App
#
def main():
    print_lines(pass_a)
    print_stats(pass_a)

if __name__ == '__main__':
    main()


