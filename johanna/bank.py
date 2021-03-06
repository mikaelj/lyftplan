#!/usr/bin/env python3

from lyftplan import *

kb_tavling = KB("tävling", reps={1 : (110, "2017-11-11")})
bp_tavling = BP("tävling", reps={1 : (65, "2018-02-24")})
ml_tavling = ML("tävling", reps={1 : (130, "2018-01-20")})

"""
bp = BP("pekfinger, stopp", parent=bp_tavling, reps={1 : (65, "2018-01-20")}, time=5.1)
sumomark = ML("semisumo", ml_tavling)
core = Core("")
rumpa = Rumpa("")
axlar = Axlar("")
armar = Armar("")

# parent = ml, but intensity calculated against sumo's 1rm
smalmark = ML("smal", ml_tavling, reps={1 : (130, "2018-01-20")})
klotsving = Rumpa("klotsving", rumpa, related=ml_tavling)
enbensmark = Rumpa("enbensmark", rumpa, related=kb_tavling, time=2.6)

kb = KB("hög stång (utan bälte)", parent=kb_tavling, reps={1 : (85, "2017-11-11")}, time=3)
kb_pin = KB("pinböj (hög stång, utan bälte)", parent=kb_tavling, reps={1 : (70, "2017-11-11")}, time=3)
bredboj = KB("bredböj", parent=kb_tavling, reps={1 : (70, "2017-11-11")})
kb_fram = KB("fram (utan bälte)", parent=kb_tavling, reps={1 : (70, "2017-11-11")})
benspark = KB("benspark", related=kb_tavling, time=1.5)

negativa_rh = Core("Negativa RH", core, time=1.2)
latsdrag = Core("latsdrag", core, time=2)
raka_latsdrag = Core("raka latsdrag", core, time=2.1)
rygglyft = Core("rygglyft", core, related=ml_tavling, time=1.6)
sittande_rodd = Core("sittande rodd", core, time=1.5)

pinpress = BP("pinpress", bp_tavling, reps={1: (60, "2018-01-01")})
catapult = BP("Catapult", bp_tavling, reps={1: (90, "2018-01-01")})
bpfu = BP("FU, lill, stopp", bp_tavling, reps={1: (60, "2018-01-01")})

tricepsrep = Armar("tricepsrep", armar, related=bp_tavling, time=1.5)

militarpress = Axlar("Militärpress", axlar, reps={1: (35, "2017-10-10")}, time=3)

hangande_rodd = Axlar("hängande rodd", axlar, related=bp_tavling)
tryndrag = Axlar("tryndrag", axlar, related=bp_tavling, time=1.5)
"""

bp = BP("pekfinger, stopp", parent=bp_tavling, reps={1 : (65, "2018-01-20")}, time=5.1)
sumomark = ML("semisumo", ml_tavling)
core = Core("")
rumpa = Rumpa("")
axlar = Axlar("")
armar = Armar("")

# parent = ml, but intensity calculated against sumo's 1rm
smalmark = ML("smal", ml_tavling, reps={1 : (130, "2018-01-20")})
kronlyft = ML("kronlyft", ml_tavling, reps={1 : (130, "2018-01-20")})
rakmark = ML("raka", ml_tavling, reps={10 : (60, "2018-01-20")})
klotsving = Rumpa("klotsving", rumpa)
enbensmark = Rumpa("enbensmark", rumpa, time=2.6)

kb = KB("hög stång (utan bälte)", parent=kb_tavling, reps={1 : (85, "2017-11-11")}, time=3)
kb_pin = KB("pinböj (hög stång, utan bälte)", parent=kb_tavling, reps={1 : (70, "2017-11-11")}, time=3)
bredboj = KB("bredböj", parent=kb_tavling, reps={1 : (70, "2017-11-11")})
kb_fram = KB("fram (utan bälte)", parent=kb_tavling, reps={1 : (70, "2017-11-11")})
benspark = KB("benspark", time=1.5)

negativa_rh = Core("Negativa RH", core, time=1.2)
latsdrag = Core("latsdrag", core, time=2)
raka_latsdrag = Core("raka latsdrag", core, time=2.1)
rygglyft = Core("rygglyft", core, time=1.6)
sittande_rodd = Core("sittande rodd", core, time=1.5)

pinpress = BP("pinpress", bp_tavling, reps={1: (60, "2018-01-01")})
catapult = BP("Catapult", bp_tavling, reps={1: (90, "2018-01-01")})
bpfu = BP("FU, lill, stopp", bp_tavling, reps={1: (60, "2018-01-01")})

tricepsrep = Armar("tricepsrep", armar, time=1.5)

hantelflugor_omvanda = Axlar("omvända hantelflugor", axlar, time=1.5)
militarpress = Axlar("militärpress", axlar, reps={1: (35, "2017-10-10")}, time=3)

hangande_rodd = Axlar("hängande rodd", axlar)
tryndrag = Axlar("tryndrag", axlar, time=1.5)

###########################################################################################

