'use strict'; 
import * as E from '../lib/exercise.js'
/*
 * Exist only as root exercises. No work done on them.
 */
export var kb_tavling = new E.KB("", {'reps': new Map([[1, [110, "2017-11-11"]]])})
export var bp_tavling = new E.BP("", {'reps': new Map([[1, [65, "2018-02-24"]]])})
export var ml_tavling = new E.ML("", {'reps': new Map([[1, [130, "2018-01-20"]]])})
export var core = new E.Core("")
export var rumpa = new E.Rumpa("")
export var axlar = new E.Axlar("")
export var armar = new E.Armar("")

/*
 * Exercises actually used.
 */
export var bp = new E.BP("pekfinger, stopp", {'parent': bp_tavling, 'reps': new Map([[1, [65, "2017-11-11"]]]), 'time': 5.1})
export var sumomark = new E.ML("semisumo", {'parent': ml_tavling, 'reps': new Map([[1, [130, "2017-11-11"]]])})

// parent = new E.ml, but intensity calculated against sumo's 1rm
export var smalmark = new E.ML("smal", {'parent':ml_tavling, 'reps': new Map([[1, [130, "2018-01-20"]]])})
export var kronlyft = new E.ML("kronlyft", {'parent': ml_tavling, 'reps': new Map([[1, [130, "2018-01-20"]]])})
export var rakmark = new E.ML("raka", {'parent': ml_tavling}) // TODO: add a number? calculate 1RM from nRM? //, 'reps': new Map([[10, [160, "2018-01-20"]]])})
export var klotsving = new E.Rumpa("klotsving", {'parent': rumpa})
export var enbensmark = new E.Rumpa("enbensmark", {'parent': rumpa, 'time': 2.6})

export var kb = new E.KB("hög stång (utan bälte)", {'parent': kb_tavling, 'reps': new Map([[1, [85, "2017-11-11"]]]), 'time': 3})
export var kb_pin = new E.KB("pinböj (hög stång, utan bälte)", {'parent': kb_tavling, 'reps': new Map([[1 , [70, "2017-11-11"]]]), 'time': 3})
export var bredboj = new E.KB("bredböj", {'parent': kb_tavling, 'reps': new Map([[1 , [70, "2017-11-11"]]])})
export var kb_fram = new E.KB("fram (utan bälte)", {'parent': kb_tavling, 'reps': new Map([[1, [70, "2017-11-11"]]])})
export var benspark = new E.KB("benspark", {'time': 1.5})

export var negativa_rh = new E.Core("Negativa RH", {'parent': core, 'time': 1.2})
export var latsdrag = new E.Core("latsdrag", {'parent': core, 'time': 2})
export var raka_latsdrag = new E.Core("raka latsdrag", {'parent': core, 'time': 2.1})
export var rygglyft = new E.Core("rygglyft", {'parent': core, 'time': 1.6})
export var sittande_rodd = new E.Core("sittande rodd", {'parent': core, 'time': 1.5})

export var pinpress = new E.BP("pinpress", {'parent': bp_tavling, 'reps': new Map([[1, [60, "2017-11-11"]]])})
export var catapult = new E.BP("Catapult", {'parent': bp_tavling, 'reps': new Map([[1, [90, "2018-01-01"]]])})
export var bpfu = new E.BP("FU, lill, stopp", {'parent': bp_tavling, 'reps': new Map([[1, [60, "2018-01-01"]]])})

export var tricepsrep = new E.Armar("tricepsrep", {'parent': armar, 'time': 1.5})

export var hantelflugor_omvanda = new E.Axlar("omvända hantelflugor", {"parent": axlar, "time": 1.5})
export var militarpress = new E.Axlar("Militärpress", {'parent': axlar, 'reps': new Map([[1, [35, "2017-10-10"]]]), 'time':3})

export var hangande_rodd = new E.Axlar("hängande rodd", {'parent': axlar})
export var tryndrag = new E.Axlar("tryndrag", {'parent': axlar, 'time':1.5})

