'use strict';

import * as B from "./bank.js"
import * as E from './exercise.js'
E.register(B)

var cycle = new E.Cycle("Cyberman 18.2", [
new E.Week([
new E.Session(`
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
`),
new E.Session(`
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
`),
new E.Session(`
tryndrag                                    | 20 15 15
raka_latsdrag                       Kontakt | 15 15 15
sittande_rodd                       Kontakt | 15 15 15
negativa_rh                  Hela vägen ned | 1 1 1 1 1 1 1 1 1 1

enbensmark                                  | 10 10 10 10
kb_fram                                     | 30x5 35x5 40x5 45x5
kb                                          | 40x5 40x10 45x10

sumomark                                    | 55x5 65x5 75x5 75x5 75x5 75x5 75x5

pinpress                                    | 30x10 40x5 45x3 50x3 55x3 55x3 55x3

klotsving                                   | 16x20 20x20 24x20
tricepsrep                                  | 20 20 20 20 20
`)]),
new E.Week([
new E.Session(`
klotsving                                   | 16x20 20x15 24x10
negativa_rh Fokus varannan rep nere/uppe, 1 rep var 5-10 minut hela passet | 1
enbensmark  Växelvis arm/ben, sträck ut bak | 10 10 10
kb                                          | 20x10 30x10 40x5 45x5 50x5
kb_pin                                      | 30x4 35x4 40x4 45x4
raka_latsdrag                               | 15 15
bpfu                Lillfinger, stopp       | 30x5 40x5 50x3
bp                                          | 50x3 55x3 60x3 50x5 50x5
hangande_rodd                               | 10 10 10
sumomark       Maxat grepp, inget bälte     | 40x5 50x5 60x5 70x5 80x1 80x1 80x1 80x1 80x1
sittande_rodd                   Kontakt     | 10 10 10 10 10
militarpress                                | 25x5 25x5 25x5
tricepsrep                                  | 20 15 10 10
`),
])
], [2018,3,5])


function main() {
    var s = "<h1>Cycle <i>{}</i> ({})</h1>".format(cycle.title, cycle.date.ymdString())

    for (var week of cycle.weeks) {
        s += "<h2>Week {}</h2>".format(week.date.ymdString())

        for (var session of week.sessions) {
            var stats = new E.Statistics(session)

            let hours = Math.trunc(stats.minutes/60)
            let minutes = Math.trunc(stats.minutes%60)
            s += "<h3>Session {} ({} hours {} minutes)</h3>".format(session.date.ymdString(), hours, minutes)
           
            //print_prs(stats)
            console.log("-------------------------")
            print_stats(stats)

            // session & stats
            s += "<b>Session</b><ul>"

            // session
            for (var line of week.sessions[0].lines) {
                s += "<li>{}</li>".format(line.toString())
            }
            s += "</ul>"

            // stats
            s += "<b>Stats</b><ul>"

            for (var root of stats.roots) {
                let d = stats.data.get(root)
                s += "<li>{}</li>".format(d)
                /*
                s += "<li>{}: {} kg, {} reps, inol {}, intensity min/avg/max: {}/{}/{}</li>".format(
                    d.exercise, d.weight, d.rep_count, d.inol.toFixed(2), Math.trunc(d.min_set_percent), Math.trunc(d.avg_set_percent), Math.trunc(d.max_set_percent))
                */
            }
            
            s += "</ul>"
        }
    }

    document.getElementById('sessions').innerHTML = s
}

function print_prs(stats) {
    for (var ex of stats.data.keys()) {
        //if not 'prs' in stats.data[ex]['self']:

        // prs is a Map
        var prs = stats.data.get(ex).prs
        if (prs.size == 0)
            continue

        //b = list(zip(list(prs.keys()), list(prs.values())))
        //b.sort(key=lambda x: x[0])
        //print(ex, ", ".join("{} x {} ({})".format(b[0], a, b[1]) for a,b in b))
        //console.log(ex, ", ".join("{} x {} ({})".format(b[0], a, b[1]) for a,b in b))
        var b = [...prs.entries()].sort(function(a,b) {return a[1] > b[1]}).map(rw => "{}x{} ({})".format(rw[1][0], rw[0])).join(", ")
        console.log("PRS for {}: {}:".format(ex.toString(), b
        ))
    }
}

function print_stats(stats, print_chtildren=true) {
    for (var root of stats.roots) {
        console.info(stats.data.get(root))
    }
}

/*
function print_stats(stats, print_children=true) {
    def print_part(part):
        if part in stats.data:
            print_stats_ex(stats, part, indent, csv)

            if print_children:
                for child in part.children:
                    print_stats_ex(stats, child, indent+1, csv)
                printed_roots = {}
                for related in part.related:
                    if related in stats.exercises: #stats.data:
                        print_stats_ex(stats, related, indent+1, csv)


    kb_tavling = g_module.__dict__.get('kb_tavling')
    bp_tavling = g_module.__dict__.get('bp_tavling')
    ml_tavling = g_module.__dict__.get('ml_tavling')
    core = g_module.__dict__.get('core')
    rumpa = g_module.__dict__.get('rumpa')
    axlar = g_module.__dict__.get('axlar')
    armar = g_module.__dict__.get('armar')

    print_part(kb_tavling)
    print_part(bp_tavling)
    print_part(ml_tavling)
    print_part(core)
    print_part(rumpa)
    print_part(axlar)
    print_part(armar)
}
*/


////////////////////

function resolve(str) {return function() {eval(str)()}} 
window.addEventListener("load", resolve("main"))

