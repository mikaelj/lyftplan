'use strict';

var lifters = ["johanna"]

import * as E from './lib/exercise.js'

function resolve(str) {return function() {eval(str)()}} 
window.addEventListener("load", resolve("main"))

function main(program) {
    // Components must be defined before 'new Vue'

    var app = new Vue({
        el: '#app',
        data : {
            selectedLifter: "",
            lifters: lifters,

            //selectedSession: '',
            selectedSessions: [],
            sessionData: "",
            sessions: [],

            selectedWeeks: [],
            weeks: [],

            checkedExercises: [],
            selectedWeeksExercise: [],

            selectedWeeksFrequency: [],
            frequencyHides: [],

            checkedTypes: ["volume", "intensity"],

            foo: "",

            B: undefined,
            P: undefined,

            cycles: [],
            selectedCycle: undefined,
        },

        mounted: function() {},
        watch: {
            selectedCycle: function() {
                console.log("selected cycle: " + this.selectedCycle)
                this.initializeCycle()
            },

            selectedLifter: function(lifter) {
                import("./{}/program.js".format(lifter))
                    .then((program) => {
                        this.P = program
                        import("./{}/bank.js".format(lifter))
                            .then((bank) => {
                                this.B = bank
                                E.register(bank)
                                for (var cycle of program.cycles)  {
                                    cycle.resolve()
                                }
                                this.initializeLifter(program)
                            })
                    })

            },
            selectedSessions: function(vals) {
                /*
                 * Print the actual sessions
                 */
                var s = ""
                for (var index of vals) {
                    var item = this.sessions[index]

                    var session = item.session
                    var stats = new E.Statistics(session)
                    let hours = Math.trunc(stats.minutes/60)
                    let minutes = Math.trunc(stats.minutes%60)

                    s += "<h1>Session {} ({} hours {} minutes)</h1>".format(session.date.ymdString(), hours, minutes)

                    s += "<table width='100%'>"
                    // session
                    var row = 0
                    var lineattribs = ""
                    var exattribs = ""
                    for (var line of session.lines) {
                        row += 1
                        if (line.exercise instanceof E.KB ||
                            line.exercise instanceof E.BP ||
                            line.exercise instanceof E.ML) {
                            exattribs = "style='font-weight: bold'"
                        }
                        else
                            exattribs = ""

                        s += "<tr {}><td><span {}>{}</span>{}</<td><td>{}</td></tr>".format(lineattribs, exattribs,
                            line.exercise + "<br/>", "<em>" +line.note + "</em>",
                            line.setsStringArray().join(", "))
                        lineattribs = row % 2 == 0 ? "" : "style='background-color: #f0f0f0'"
                    }
                    s += "</table>"
                }
                this.sessionData = s

                /*
                 * Chart statistics
                 */
                var items = []
                for (var index of vals) {
                    var item = this.sessions[index]
                    items.push(item.session)
                }

                var stats = new E.Statistics(items)

                var dataReps = []
                var dataIntensity = []
                var chartLabels = []
                
                for (var e of [this.B.kb_tavling, this.B.bp_tavling, this.B.ml_tavling]) {
                    if (stats.roots.has(e)) {
                        var reps = stats.data.get(e).rep_count
                        var avg_intensity = stats.data.get(e).avg_set_percent

                        dataReps.push(reps)
                        dataIntensity.push(avg_intensity)

                        chartLabels.push(e.toString())
                    }
                }

                sessionChart.data.datasets[0].data = dataReps
                sessionChart.data.datasets[1].data = dataIntensity

                sessionChart.data.labels = chartLabels
                sessionChart.update()
            },
            selectedWeeks: function(vals) {

                /*
                 * Chart statistics
                 */
                var items = []
                for (var index of vals) {
                    var item = this.weeks[index]
                    console.info(item)
                    items.push(item)
                }

                var dataReps = []
                var dataIntensity = []
                var chartLabels = []
                
                /*
                 * One sesssion is one data point
                 * - each data point belongs to three datasets: 0, 3 = kb, 1,4 = bp, 2,5 = ml
                 */
                var volumeKb = []
                var intKb = []
                var volumeBp = []
                var intBp = []
                var volumeMl = []
                var intMl = []
                var chartLabels = []
                
                for (var item of items) {
                    for (var session of item.week.sessions) {
                        console.info(session)
                        var stats = new E.Statistics(session)

                        chartLabels.push("W{} {}".format(item.index, session.date.ymdString()))

                        // KB
                        console.info(stats)
                        var es = stats.data.get(this.B.kb_tavling)
                        //console.log("KB_tavling")
                        //console.info(es)
                        volumeKb.push(es ? es.rep_count : 0)
                        intKb.push(es ? es.avg_set_percent : 0)

                        var es = stats.data.get(this.B.bp_tavling)
                        //console.log("BP_tavling")
                        //console.info(es)
                        volumeBp.push(es ? es.rep_count : 0)
                        intBp.push(es ? es.avg_set_percent : 0)

                        var es = stats.data.get(this.B.ml_tavling)
                        //console.log("ML_tavling")
                        //console.info(es)
                        volumeMl.push(es ? es.rep_count : 0)
                        intMl.push(es ? es.avg_set_percent : 0)
                    }
                }

                weekChart.data.datasets[0].data = volumeKb
                weekChart.data.datasets[0+3].data = intKb

                weekChart.data.datasets[1].data = volumeBp
                weekChart.data.datasets[1+3].data = intBp

                weekChart.data.datasets[2].data = volumeMl
                weekChart.data.datasets[2+3].data = intMl

                /*
                var i = 0
                for (var _ of volumeKb) {
                    weekChart.data.datasets[0].bars[i++].fillColor = 'red'
                    weekChart.data.datasets[0].bars[i++].fillColor = 'green'
                    weekChart.data.datasets[0].bars[i++].fillColor = 'blue'
                }
                */

                weekChart.data.labels = chartLabels
                weekChart.update()
                
                /*
                for (var e of [B.kb_tavling, B.bp_tavling, B.ml_tavling]) {

                    var stats = new E.Statistics(items)
                    if (stats.roots.has(e)) {
                        var reps = stats.data.get(e).rep_count
                        var avg_intensity = stats.data.get(e).avg_set_percent

                        dataReps.push(reps)
                        dataIntensity.push(avg_intensity)

                        chartLabels.push(e.toString())
                    }
                }

                chart.data.datasets[0].data = dataReps
                chart.data.datasets[1].data = dataIntensity

                chart.data.labels = chartLabels
                chart.update()
                */
            },

            // Per-exercise over time
            selectedWeeksExercise: function(vals) {
                this.updateSelectedWeeksExercise(vals)
            },
            checkedExercises: function(vals) {
                this.updateSelectedWeeksExercise(this.selectedWeeksExercise)
            },
            checkedTypes: function(vals) {
                this.updateSelectedWeeksExercise(this.selectedWeeksExercise)
            },

            // Frequency over time
            selectedWeeksFrequency: function(vals) {
                this.updateFrequencyExercise(vals)
            },
            frequencyHides: function(vals) {
                this.updateFrequencyExercise(this.selectedWeeksFrequency)
            },
        },
        computed: {},
        ready: function() {},
        //components: {statsItem: statsItem}
        methods: {
            initializeLifter(program) {
                var cycles = []
                var counter = 0
                for (var c of program.cycles) {
                    cycles.push({'index': counter, 'name': "{} ({})".format(c.name, c.date.ymdString()), 'cycle': c})
                    counter += 1
                }
                this.cycles = cycles
                document.getElementById("pickCycle").style.display = "block"
            },
            initializeCycle() {
                var cycle = this.cycles[this.selectedCycle].cycle
                console.info(this.cycles)
                console.log("cycle: "+cycle.toString())
                var counter = 0
                var week_counter = 0
                for (var week of cycle.weeks) {
                    this.weeks.push({
                        'index': week_counter,
                        'title': "Week {} ({})".format(week_counter+1, week.date.ymdString()),
                        'week': week
                    })
                    week_counter += 1
                    var session_counter = 0
                    for (var session of week.sessions) {
                        session_counter += 1
                        this.sessions.push({
                            'index': counter,
                            'title': "Week {}: session {} ({})".format(week_counter, session_counter, session.date.ymdString()),
                            'session': session
                        })
                        counter += 1
                    }
                }

                document.getElementById("content").style.display = "block"
            },
            updateSelectedWeeksExercise(vals) {
            /*
             * Chart statistics
             */
            var items = []
            for (var index of vals) {
                var item = this.weeks[index]
                console.info(item)
                items.push(item)
            }

            var dataReps = []
            var dataIntensity = []
            var chartLabels = []
            
            /*
             * One sesssion is one data point
             * - each data point belongs to three datasets: 0, 3 = kb, 1,4 = bp, 2,5 = ml
             */

            //console.log("---- checkedExercises:")
            //console.info(this.checkedExercises)

            let displayKb = this.checkedExercises.findIndex(x => x == "kb") >= 0
            let displayBp = this.checkedExercises.findIndex(x => x == "bp") >= 0
            let displayMl = this.checkedExercises.findIndex(x => x == "ml") >= 0
            let displayTotal = this.checkedExercises.findIndex(x => x == "total") >= 0

            let displayVolume = this.checkedTypes.findIndex(x => x == "volume") >= 0
            let displayIntensity = this.checkedTypes.findIndex(x => x == "intensity") >= 0

            //console.log("showing kb? {}, bp? {}, ml? {}, displayTotal? {}, volume? {}, intensity? {}".format(displayKb, displayBp, displayMl, displayTotal, displayVolume, displayIntensity))

            var volumeKb = []
            var intKb = []
            var volumeBp = []
            var intBp = []
            var volumeMl = []
            var intMl = []
            var volumeTot = []
            var intTot = []
            var chartLabels = []

            
            for (var item of items) {
                for (var session of item.week.sessions) {
                    //console.info(session)
                    var stats = new E.Statistics(session)

                    chartLabels.push("W{} {}".format(item.index, session.date.ymdString()))

                    var volumeTotal = 0
                    var intTotal = 0
                    var totalCount = 0

                    // KB
                    //console.info(stats)
                    var es = stats.data.get(this.B.kb_tavling)
                    console.log("KB_tavling")
                    //console.info(es)
                    volumeKb.push(es ? es.rep_count : 0)
                    intKb.push(es ? Math.trunc(es.avg_set_percent) : 0)

                    volumeTotal += es.rep_count
                    intTotal += Math.trunc(es.avg_set_percent)

                    var es = stats.data.get(this.B.bp_tavling)
                    console.log("BP_tavling")
                    //console.info(es)
                    volumeBp.push(es ? es.rep_count : 0)
                    intBp.push(es ? Math.trunc(es.avg_set_percent) : 0)

                    volumeTotal += es.rep_count
                    intTotal += Math.trunc(es.avg_set_percent)

                    var es = stats.data.get(this.B.ml_tavling)
                    console.log("ML_tavling")
                    //console.info(es)
                    volumeMl.push(es ? es.rep_count : 0)
                    intMl.push(es ? Math.trunc(es.avg_set_percent) : 0)

                    volumeTotal += es.rep_count
                    intTotal += Math.trunc(es.avg_set_percent)


                    intTotal /= 3

                    volumeTot.push(volumeTotal)
                    intTot.push(intTotal)

                }
            }
            let chart = weekExerciseChart
            chart.data.datasets[0].hidden = !displayKb || !displayIntensity
            chart.data.datasets[0+4].hidden = !displayKb || !displayVolume

            chart.data.datasets[1].hidden = !displayBp || !displayIntensity
            chart.data.datasets[1+4].hidden = !displayBp || !displayVolume

            chart.data.datasets[2].hidden = !displayMl || !displayIntensity
            chart.data.datasets[2+4].hidden = !displayMl || !displayVolume

            chart.data.datasets[3].hidden = !displayTotal || !displayIntensity
            chart.data.datasets[3+4].hidden = !displayTotal || !displayVolume

            chart.data.datasets[0].data = intKb
            chart.data.datasets[0+4].data = volumeKb

            chart.data.datasets[1].data = intBp
            chart.data.datasets[1+4].data = volumeBp

            chart.data.datasets[2].data = intMl
            chart.data.datasets[2+4].data = volumeMl

            chart.data.datasets[3].data = intTot
            chart.data.datasets[3+4].data = volumeTot

            chart.data.labels = chartLabels
            chart.update()
            },

            // Exercise frquency
            updateFrequencyExercise(vals) {
                let chart = weekFrequencyChart

                /*
                 * Chart statistics
                 */
                console.info(vals)
                var items = []
                for (var index of vals) {
                    var item = this.weeks[index]
                    console.info(item)
                    items.push(item)
                }

                var frequency = new Map()
                
                for (var item of items) {
                    for (var session of item.week.sessions) {
                        //console.info(session)
                        for (var line of session.lines) {
                            // Occurance of exercise
                            /*
                            var f = 0
                            if (frequency.has(line.exercise))
                            {
                                f += frequency.get(line.exercise)
                            }
                            frequency.set(line.exercise, f)
                            */

                            // Number of reps
                            var reps = line.rep_count()
                            if (!frequency.has(line.exercise)) {
                                frequency.set(line.exercise, reps)
                            } else {
                                frequency.set(line.exercise, reps + frequency.get(line.exercise))
                            }

                        }
                    }
                }

                var kb = []
                var kbl = []
                var bp = []
                var bpl = []
                var ml = []
                var mll = []
                var other = []
                var otherl = []
                var colors = []

                // populate labels
                for (let [ex, freq] of frequency) {
                    if (ex instanceof E.KB) {
                        kb.push(freq)
                        kbl.push(ex.toString())
                        colors.push('rgba(255,99,132,1)')
                    }
                    else if (ex instanceof E.BP) {
                        bp.push(freq)
                        bpl.push(ex.toString())
                        colors.push('rgba(55, 152, 80, 1)')
                    }
                    else if (ex instanceof E.ML) {
                        ml.push(freq)
                        mll.push(ex.toString())
                        colors.push('rgba(54, 162, 235, 1)')
                    }
                    else {
                        other.push(freq)
                        otherl.push(ex.toString())
                    }
                }

                let hideOther = this.frequencyHides.findIndex(x => x == "other") >= 0
                let hideMain = this.frequencyHides.findIndex(x => x == "main") >= 0


                if (hideOther) {
                    other = []
                    otherl = []
                }

                if (hideMain) {
                    kb = []
                    kbl = []
                    bp = []
                    bpl = []
                    ml = []
                    mll = []
                }

                var data = [...kb, ...bp, ...ml, ...other]
                var labels = [...kbl, ...bpl, ...mll, ...otherl]
                colors = new Array(data.length)
                var start = 0
                var end = kb.length
                colors.fill('rgba(255,99,132,1)', start, end)
                start = end
                end += bp.length
                colors.fill('rgba(55, 152, 80, 1)', start, end)
                start = end
                end += ml.length
                colors.fill('rgba(54, 162, 235, 1)', start, end)

                //console.info(data) //console.info(labels)

                chart.data.datasets[0].data = data
                //chart.data.datasets[0].borderColor = colors
                chart.data.datasets[0].backgroundColor = colors
                chart.data.labels = labels

                chart.update()
            }
        }
    })



    Chart.defaults.global.legend.display = false

    // Must load Vue before, since it throwns out(?) the DOM

    var ctx = document.getElementById("sessionChart").getContext('2d');
    var sessionChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Antal repetitioner',
                data: [],
                yAxisID: 'reps',
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(75, 255, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',

                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',

                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(153, 102, 255, 1)',
                ],
                borderWidth: 1
            },

            {
                type: 'bar',
                label: 'Intensitet',
                data: [],
                yAxisID: 'intensity',
                /*
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                */
                borderWidth: 1
            },
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    },
                    scaleLabel: {
                        labelString: 'Repetitioner',
                        display: true,
                    },
                    position: 'left',
                    id: 'reps',
                },
                {
                    ticks: {
                        beginAtZero: true,
                    },
                    scaleLabel: {
                        labelString: 'Intensitet (%)',
                        display: true,
                    },
                    position: 'right',
                    id: 'intensity',
                }]
            }
        }
    });

    //var ctx = document.getElementById("weekChart").getContext('2d');
    var weekChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                label: 'Knäböj',
                data: [],
                yAxisID: 'volume',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 1
                },

                {
                label: 'Bänkpress',
                data: [],
                yAxisID: 'volume',
                backgroundColor: 'rgba(75, 255, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
                },
                {
                label: 'Marklyft',
                data: [],
                yAxisID: 'volume',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
                },

                // Intensity
                {
                type: 'line',
                fill: false,
                label: 'Knäböj',
                data: [],
                yAxisID: 'intensity',
                borderColor: [
                    'rgba(255,99,132,1)',
                ],
                borderWidth: 2.5
                },

                {
                type: 'line',
                fill: false,
                label: 'Bänkpress',
                data: [],
                yAxisID: 'intensity',
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                ],
                borderWidth: 2.5
                },
                {
                type: 'line',
                fill: false,
                label: 'Marklyft',
                data: [],
                yAxisID: 'intensity',
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 2.5
                },

            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    },
                    scaleLabel: {
                        labelString: 'Volym',
                        display: true,
                    },
                    position: 'left',
                    id: 'volume',
                },
                {
                    ticks: {
                        beginAtZero: true,
                    },
                    scaleLabel: {
                        labelString: 'Intensitet (%)',
                        display: true,
                    },
                    position: 'right',
                    id: 'intensity',
                }]
            }
        }
    });



    var weekExerciseChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                // Intensity - currently avg set percentage. Should be....?
                {
                label: 'Intensitet knäböj',
                data: [],
                fill: false,
                yAxisID: 'intensity',
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 1.5,
                borderDash: [5, 5],
                },

                {
                label: 'Intensitet bänkpress',
                data: [],
                fill: false,
                yAxisID: 'intensity',
                borderColor: 'rgba(55, 152, 80, 1)',
                borderWidth: 1.5,
                borderDash: [5, 5],
                },
                {
                label: 'Intensitet marklyft',
                data: [],
                fill: false,
                yAxisID: 'intensity',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1.5,
                borderDash: [5, 5],
                },
                {
                label: 'Intensitet total',
                data: [],
                fill: false,
                yAxisID: 'intensity',
                borderColor: 'rgba(0, 0, 0, 1)',
                borderWidth: 1.5,
                borderDash: [5, 5],
                },

                // Volume = reps
                {
                type: 'line',
                fill: false,
                label: 'Volym knäböj',
                data: [],
                yAxisID: 'volume',
                borderColor: [
                    'rgba(255,99,132,1)',
                ],
                borderWidth: 2.5
                },

                {
                type: 'line',
                fill: false,
                label: 'Volym bänkpress',
                data: [],
                yAxisID: 'volume',
                borderColor:  'rgba(55, 152, 80, 1)',
                borderWidth: 2.5
                },
                {
                type: 'line',
                fill: false,
                label: 'Volym marklyft',
                data: [],
                yAxisID: 'volume',
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 2.5
                },
                {
                type: 'line',
                fill: false,
                label: 'Volym total',
                data: [],
                yAxisID: 'volume',
                borderColor: [
                    'rgba(0, 0, 0, 1)',
                ],
                borderWidth: 2.5
                },

            ]
        },
        options: {
            //responsive: true,
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    },
                    scaleLabel: {
                        labelString: 'Volym',
                        display: true,
                    },
                    position: 'left',
                    id: 'volume',
                },
                {
                    ticks: {
                        beginAtZero: true,
                    },
                    scaleLabel: {
                        labelString: 'Intensitet (%)',
                        display: true,
                    },
                    position: 'right',
                    id: 'intensity',
                }]
            }
        }
    });

    var weekFrequencyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Frekvens',
                data: [],
                borderColor: [],
                backgroundColor: [],
                //yAxisID: 'frekvens',
            },],
        },
        options: {
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true,
                        userCallback: function(label, index, labels) {
                            return Math.trunc(label)
                        }
                    },
                    scaleLabel: {
                        labelString: 'Frekvens (antal)',
                        display: true,
                    },
                    position: 'left',
                    id: 'frequency',
                }],
                xAxes: [{
                    ticks: {
                        autoSkip: false
                    }
                }],
            }
        }
    });




    //document.getElementById('sessions').innerHTML = s
}

function print_session(cycle) {

    var s = "<h1>Cycle <i>{}</i> ({})</h1>".format(cycle.name, cycle.date.ymdString())

    var counter = 0
    var week_counter = 0
    for (var week of cycle.weeks) {
        s += "<h2>Week {}</h2>".format(week.date.ymdString())

        week_counter += 1
        var session_counter = 0
        for (var session of week.sessions) {
            session_counter += 1
            var stats = new E.Statistics(session)
            let hours = Math.trunc(stats.minutes/60)
            let minutes = Math.trunc(stats.minutes%60)
            s += "<h3>Session {} ({} hours {} minutes)</h3>".format(session.date.ymdString(), hours, minutes)
           
            //print_prs(stats)
            //console.log("-------------------------")
            print_stats(stats)

            // session & stats
            s += "<b>Session</b><ul>"

            // session
            for (var line of session.lines) {
                s += "<li>{}</li>".format(line.toString())
            }
            s += "</ul>"

            counter += 1

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
        //console.info(stats.data.get(root))
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


