#!/usr/bin/env python3
# encoding:utf-8

from lyftplan import *

###########################################################################################


johanna_2018_3_5 = Week([
Session("""
enbensmark  Växelvis arm/ben, sträck ut bak | 10 10 10
kb              Kontrollerat, korrekt stil! | 25x5 25x5 25x5 25x5

tryndrag                                    | 20 15 15
raka_latsdrag                               | 15 15 15
bp                                          | 40x8 40x8 45x4 45x4 50x2 50x2 60x1 60x1

sumomark                                    | 40x5 50x5 60x5 60x5 70x5 60x5
negativa_rh            Huvudet över stången | 1 1 1 1 1 1 1 1 1 1

kb              Kontrollerat, korrekt stil! | 25x5 25x5

militarpress                                | 20x8 20x8 20x8
latsdrag                                    | 20 15 10 10 10
tricepsrep                                  | 20 15 10 10 10

"""),
Session("""

tryndrag                                    | 20 15 15
sittande_rodd                       Kontakt | 15 15 15
bp                                          | 40x5 45x5 50x5 55x4 60x2 62.5x2 62.5x2
raka_latsdrag                       Kontakt | 10 15

enbensmark                                  | 10 10 10 10
sumomark                                    | 60x5 70x5 80x5 70x5 70x5

negativa_rh                                 | 1 1 1 1 1 1 1 1 1 1

kb                                          | 30x5 30x5 30x5 30x5 30x5 30x5 30x5 30x5
rygglyft                                    | 10 10
latsdrag                  Tungt med kontakt | 15 15 15 15
tricepsrep                                  | 15 15 15
"""
)], date = (2018,3,5))



#
# Totalt antal ton, eller kanske åtminstone reps, kan räknas i related-övningen som en separat klump.
#

#
# App
#
def main():
    test_sets()

    vecka = johanna_2018_3_5

    #print("Vecka 1: {}".format(vecka.date))
    print()


    for i in range(len(vecka)):
        print("Pass {}: {}".format(i+1, vecka[i].date))
        print_stats(Statistics(vecka[i]), indent=1)
        print()

    print("\nVecka:")
    print_stats(Statistics(vecka), indent=1)

    print("\n=======================================\n")

    for i in range(len(vecka)):
        print("Pass {}: {}".format(i+1, vecka[i].date))
        print_session(vecka[i])
        print()

    print("\nPass A:", vecka[0].date)
    print_session(vecka[0], csv=True)
    print("\nPass B:", vecka[1].date)
    print_session(vecka[1], csv=True)
    #print("Pass C\n")
    #print_session(vecka[2], csv=True)

    print("\nStatistik för vecka med start", vecka[0].date)
    stats = Statistics(vecka)
    print_stats(stats,csv=True)

    print()

    print_pr(stats)

if __name__ == '__main__':
    main()


