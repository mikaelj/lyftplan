#!/usr/bin/env python3

from lyftplan import *

kb_tavling = KB("tävling", reps={1 : (110, "2017-11-11")})
bp_tavling = BP("tävling", reps={1 : (65, "2018-02-24")})
ml_tavling = ML("tävling", reps={1 : (130, "2018-01-20")})

bp = BP("pekfinger, stopp", parent=bp_tavling, reps={1 : (65, "2018-01-20")})
sumomark = ML("semisumo", ml_tavling)
rygg = Rygg("")
rumpa = Rumpa("")
axlar = Axlar("", related=bp_tavling)
armar = Armar("", related=bp_tavling)

# parent = ml, but intensity calculated against sumo's 1rm
smalmark = ML("smal", ml_tavling, reps={1 : (130, "2018-01-20")})
klotsving = Rumpa("klotsving", rumpa, related=ml_tavling)
enbensmark = Rumpa("enbensmark", rumpa, related=ml_tavling)

kb = KB("hög stång (utan bälte)", parent=kb_tavling, reps={1 : (85, "2017-11-11")})
bredboj = KB("bredböj", parent=kb_tavling, reps={1 : (70, "2017-11-11")})

negativa_rh = Rygg("Negativa RH", rygg, related=bp_tavling, time=1)
latsdrag = Rygg("latsdrag", rygg, related=bp_tavling)
raka_latsdrag = Rygg("raka latsdrag", rygg, related=bp_tavling)
rygglyft = Rygg("rygglyft", rygg, related=ml_tavling)
sittande_rodd = Rygg("sittande rodd", rygg, related=bp_tavling)

pinpress = BP("pinpress", bp, reps={1: (60, "2018-01-01")})
catapult = BP("Catapult", bp, reps={1: (90, "2018-01-01")})

tricepsrep = Armar("tricepsrep", armar, related=bp_tavling, time=1.5)

militarpress = Axlar("Militärpress", axlar, reps={1: (35, "2017-10-10")}, time=3)

hangande_rodd = Axlar("hängande rodd", axlar, related=bp_tavling)
tryndrag = Axlar("tryndrag", axlar, related=bp_tavling, time=1.5)

###########################################################################################
