'use strict';

import "../deps/utils.js"

export { KB, BP, ML, Rumpa, Core, Axlar, Armar, 
    Line, Session, Week, Cycle,
    Statistics,
    register }

var Exercise_NAME_WIDTH = 0
var Exercise_CLASS_WIDTH = 0
class Exercise {
    constructor(name, flavor, params) { //parent, related, reps, time) {
        this.name = name
        this.flavor = flavor

        this.parent = params ? params['parent'] : null;
        this.reps = params ? params['reps'] : null;
        var time = params ? params['time'] : null;
        var related = params ? params['related'] : null;

        this.children = []

        if (this.parent != null)
        {
            //print("Exercise. Appending", self, "as child of", parent)
            this.parent.children.push(this)
        }

        // All exercises related to me. Essentially, only KB, BP, ML
        // Reps and minutes are added from related, but not this.
        this.related = []

        if (related != null)
            related.relate(this)

        if (time != null)
        {
            //print(self, "has custom time", time)
            this.minutes_per_set = time
        }
        else
        {
            this.minutes_per_set = 4.5
        }

        var pretty = this.name
        if (this.flavor != "")
        {
            pretty = "{} ({})".format(this.name, this.flavor)
        }

        if (pretty.length > Exercise_NAME_WIDTH)
        {
            Exercise_NAME_WIDTH = pretty.length
        }

        if (this.constructor.name.length > Exercise_CLASS_WIDTH)
        {
            Exercise_CLASS_WIDTH = this.constructor.name.length
        }
    }

    relate(related) {
        this.related.push(related)
    }

    max1rm() {
        if (this.reps == null)
            return 0
        let max1 = this.reps.get(1, [0,''])
        return max1[0]
    }

    root() {
        if (this.parent == null)
            return this
        var p = this.parent
        var root = p
        while (p != null) {
            root = p
            p = p.parent
        }
        return root
    }

    toString() {
        var pretty = this.name
        if (this.flavor != "")
        {
            pretty = "{} ({})".format(this.name, this.flavor)
        }
        //return "{:<{}}".format(pretty, Exercise.NAME_WIDTH)
        return pretty
    }

    createLine(comment, setspec) {
        return new Line(this, comment, setspec)
    }
}

class KB extends Exercise {
    constructor(flavor, params=null) {//parent=null, related=null, reps=null, time=null) {
        super("Knäböj", flavor, params) //parent, related, reps, time)
    }
}

class BP extends Exercise {
    constructor(flavor, parent=null, related=null, reps=null, time=null) {
        super("Bänkpress", flavor, parent, related, reps, time)
    }
}

class ML extends Exercise {
    constructor(flavor, parent=null, related=null, reps=null, time=null) {
        super("Marklyft", flavor, parent, related, reps, time)
    }
}

class Rumpa extends Exercise {
    constructor(flavor, parent=null, related=null, reps=null, time=null) {
        super("Rumpa", flavor, parent, related, reps, time)
    }
}

class Core extends Exercise {
    constructor(flavor, parent=null, related=null, reps=null, time=null) {
        super("Bål", flavor, parent, related, reps, time)
    }
}
class Axlar extends Exercise {
    constructor(flavor, parent=null, related=null, reps=null, time=null) {
        super("Axlar", flavor, parent, related, reps, time)
    }
}

class Armar extends Exercise {
    constructor(flavor, parent=null, related=null, reps=null, time=null) {
        super("Armar", flavor, parent, related, reps, time)
    }
}



var g_module = null
function register(module) {
    g_module = new Map()
    for (let [k, o] of Object.entries(module)) {
        if (o instanceof Exercise) {
            g_module.set(k, o)
        }
    }
    //console.info(g_module)
}

const Line_PRINT_MODE_KG = 0
const Line_PRINT_MODE_PERCENT = 1
const Line_OUTPUT_TYPE_READABLE = 0
const Line_OUTPUT_TYPE_CSV = 1
class Line {
    constructor(exercise, note, sets) {
        this.exercise = exercise
        this.note = note
        this.sets = sets
        this.print_mode = Line_PRINT_MODE_KG
        this.output_type = Line_OUTPUT_TYPE_READABLE
        this.session = null
    }

    copy() {
        var line = new Line(this.exercise, this.note, this.sets.slice())
        line.print_mode = line.print_mode
        line.output_type = line.output_type
        line.session = line.session
        return line
    }

    toString() {
        if (this.output_type == Line_OUTPUT_TYPE_READABLE)
            return this._toStringReadable()
        else
            return this._ToStringCSV()
    }

    setsStringArray() {
        return this.sets.map(s => this._set2str(s))
    }

    inolString() {
        var inol = this.inol()
        var inoltext = "{}".format(inol.toFixed(2))
        if (inol <= 0) {
            inol = 0
            inoltext = ""
        }
        return inoltext
    }

    _toStringReadable() {
        var strsets = this.setsStringArray().join(", ")
        var inoltext = this.inolString()
        return "{} ({}): {}".format(this.exercise, inoltext, strsets)
        /*    
            
            exercise=self.exercise, rep_count=self.rep_count(), sets=strsets, avg_set_weight=self.avg_set_weight(), avg_set_percent=self.avg_set_percent(), inoltext=inoltext, root=self.exercise.root())
        */

    }
    _toStringCSV() {
        return "CSV"
    }

    reps(s) {
        if (s.length == 1)
            return s[0]
        else if (s.length == 2)
            return s[1]
        else if (s.length == 3)
            return (s[1] + s[2])/2
        else
            return 1
    }

    minutes() {
        return this.sets.length * this.exercise.minutes_per_set
    }

    weight(s) {
        if (s.length >= 2)
            return s[0]

        return 0
    }

    percent(s) {
        var max1rm = this.exercise.max1rm()
        if (max1rm > 0)
            return this.weight(s) / max1rm
        return 0
    }

    rep_count() {
        var reps = 0
        for (var s of this.sets)
            reps += this.reps(s)
        return reps
    }

    avg_set_weight() {
        let count = this.sets.length
        var weight = 0
        for (var s of this.sets)
            weight += this.weight(s)
        return weight/count
    }

    max_set_weight() {
        return Math.max(...[...this.sets.map(s => this.weight(s))])
    }

    max_set_percent() {
        let max1rm = this.exercise.max1rm()
        if (max1rm <= 0)
            return 0

        var nums = [...this.sets.map(s => this.weight(s)*100.0/max1rm)]
        var p =  Math.max(...nums)
        //console.log("max1rm: {}, max set percent: {} from {}".format(max1rm, p, nums))
        return p
    }

    min_set_percent() {
        let max1rm = this.exercise.max1rm()
        if (max1rm <= 0)
            //print("max1rm", self, " <= 0:", max1rm)
            return 0


        let values = this.sets.map(s => this.weight(s)*100.0/max1rm)
        //values = [self.weight(s)*100.0/max1rm for s in self.sets]
        //print("min:",self, values, "=", min(values))

        return Math.min(...values)
    }

    set_percent_list() {
        let max1rm = this.exercise.max1rm()
        if (max1rm <= 0)
            return []

        //return [self.weight(s)*100.0/max1rm for s in self.sets]

        return this.sets.map(s => this.weight(s)*100.0/max1rm)
    }

    avg_set_percent() {
        let max1rm = this.exercise.max1rm()
        if (max1rm > 0)
            return this.avg_set_weight()*100.0 / max1rm
        return 0
    }

    total_weight() {
        return this.sets.map(s => this.reps(s) * this.weight(s)).reduce((a,b) => a+b, 0)
    }

    inol() {
        if (this.total_weight() < 1)
            return 0

        var i = 0.0
        for (var s of this.sets) {
            let reps = this.reps(s)
            var percent = this.percent(s)
            i += reps / (100.0 - percent*100.0)
        }
        return i
    }


    _set2weightreps(aset) {
        /*
        Fill in missing weights if any and transform into proper string format.

        aset can be a tuple of 1, 2 or 3 items.

        (reps,) => (0, "reps")
        (weight,reps) => (weight, "reps")
        (weight,reps_from,reps_to) => (weight, "reps_from-reps_to")
        */
        //assert (len(aset) >= 1) and (len(aset) <= 3), ("set2str: invalid number ({}) of items in {}".format(len(aset), str(aset)))

        var what = aset[0]
        if (this.print_mode == Line_PRINT_MODE_PERCENT) {
            //max1 = this.exercise.reps.get(1, (0,''))
            var max1 = this.exercise.reps.get(1)
            if (max1 == undefined) {
                max1 = [0, '']
            }
            var max1kg = max1[0]
            if (max1kg > 1) {
                what = "{}% ".format(what*100.0/float(max1kg))
            }
        }

        switch (aset.length)
        {
        case 1:
            return [0, "{}".format(what)]
        case 2:
            return [what,"{}".format(aset[1])]
        case 3:
            return [what, "{}-{}".format(aset[1], aset[2])]
        default:
        }

        // doesn't happen
        return "<fel>"
    }


    _set2str(aset) {
        /*
        Return a string representation of aset.

        aset can be a tuple of 1, 2 or 3 items.

        (reps,)
        (weight,reps)
        (weight,reps_from,reps_to)
        */
        //assert (len(aset) >= 1) and (len(aset) <= 3), ("set2str: invalid number ({}) of items in {}".format(len(aset), str(aset)))

        var what = aset[0]
        if (this.print_mode == Line_PRINT_MODE_PERCENT) {
            //max1 = this.exercise.reps.get(1, (0,''))
            max1 = this.exercise.reps.get(1)
            if (max1 == undefined) {
                max1 = [0, '']
            }
            max1kg = max1[0]
            if (max1kg > 1) {
                what = "{:.0f}% ".format(what*100.0/float(max1kg))
            }
        }

        switch(aset.length) {
        case 1:
            return "{}".format(what)
        case 2:
            return "{}x{}".format(what, aset[1])
        case 3:
            return "{}x{}-{}".format(what, aset[1], aset[2])
        default:
        }

        // doesn't happen
        return "<fel>"
    }

    static sets(spec) {
        /*
        Return a list of tuples from a string on the following format:

        In: 30x3 40x3 40x3 40x3 40x3 40x3 40x3 40x3
        Out: [(30,3), (40,3), ...]

        In: 30x3-5 40x3 40x3-5 40x3 40x3 40x3 40x3 40x3
        Out: [(30,3,5), (40,3), (40,3,5) ...]

        In: 30 20 20
        Out: [(30,), (20,), (20,)]
        */
        let sets = spec.split(" ")
        var wrs = []
        for (var s of sets) {
            if (s.includes("x")) {
                let [w, r] = s.split("x")
                if (r.includes("-")) {
                    let [r1, r2] = r.split("-")
                    wrs.push([Number.parseFloat(w), Number.parseInt(r1), Number.parseInt(r2)])
                } else {
                    wrs.push([Number.parseFloat(w), Number.parseInt(r)])
                }
            } else {
                let i = Number.parseInt(s)
                //console.log("Parsed {} to {}".format(s, i))
                wrs.push([i])
            }
        }

        //console.log(wrs)
        return wrs
    }

    static instantiate(line) {
        //items = dict(globals().items())

        //g_module.__dict__.get(

        var items = []
        //items = [(name, g_module.__dict__.get(name)) for name in dir(g_module)]
        /*
        for (var [key, value] of g_module) {
            items.push([key, value])
        }

        for (var [n, o] of items) {
            name = line.split()[0].strip()
            setspec = line.split('|')[1].strip()
            comment = line.split('|')[0].strip()
            //comment = " ".join(comment.split()[1:]).strip()
            comment = comment.split().slice(1).join(" ").strip()
        }


        //print(name, comment, setspec, "vs", n, o)
        if (n == name && (o instanceof Exercise)) {
            if (comment == "|")
                comment = ""
            //print("calling {}({}, {}, {})".format(o, name, comment, sets(setspec)))
            return o.createLine(comment, sets(setspec))
        }
        */


        for (var [n, o] of g_module) {
            let name = line.split(" ")[0].trim()
            let setspec = line.split('|')[1].trim()
            let comm = line.split('|')[0].trim()
            let comment = comm.split(" ").slice(1).join(" ").trim()

            //print(name, comment, setspec, "vs", n, o)
            //console.log("n.toString: {}, name: {}".format( n.toString(), name))
            if (n.toString() == name) {
                if (comment == "|")
                    comment = ""
                //print("calling {}({}, {}, {})".format(o, name, comment, sets(setspec)))
                return o.createLine(comment, Line.sets(setspec))
            }
        }

        console.error("Invalid line: {}".format(line))
    }

    static instantiateLines(lines) {
        //console.log(lines)
        //console.log(lines.split("\n"))
        //console.log(lines.split("\n").filter(s => s.trim() != ""))
        var ok = lines.split("\n").filter(s => s.trim() != "")
        ok = ok.map(line => line.trim()).map(Line.instantiate)
        //console.log("instantiate: " + ok)
        //ok = [line.strip() for line in lines.split('\n') if len(line.strip()) > 0]
        //lines = list(map(instantiate_line, ok))
        return ok
    }
}


class Session {
    constructor(lines, date=null) {
        this.lines = lines
        var d = date
        if (d != null)
            d = new Date(date[0], date[1]-1, date[2])
        this.date = d
    }

    // Late binding since Line.instantiateLines() isn't available until after bank is registered
    resolve() {
        var ls = this.lines
        if (typeof this.lines == "string")
            ls = Line.instantiateLines(this.lines)

        this.lines = ls
        for (var line of ls) {
            line.session = this
        }
    }
}

class Week {
    constructor(sessions, date=null) {
        this.sessions = sessions
        var d = date
        if (d != null) {
            d = new Date(date[0], date[1]-1, date[2])
        }
        this.date = d

        // set date for each session if they don't have one.
        if (this.date != null) {
            var sessiondate = this.date
            for (var sess of sessions) {
                if (sess.date == null) {
                    sess.date = new Date(sessiondate)
                }
                sessiondate.setDate(sessiondate.getDate() + 2)
            }
        }
    }
    resolve() {
        for (var session of this.sessions) {
            session.resolve()
        }
    }
}


class Cycle {
    constructor(title, weeks, date=null) {
        this.title = title
        this.weeks = weeks
        var d = date
        if (d != null) {
            d = new Date(date[0], date[1]-1, date[2])
        }
        this.date = d

        // set date for each week and each session if they don't have one.
        if (this.date != null) {
            var weekdate = new Date(this.date)
            for (var week of this.weeks) {
                if (week.date == null) {
                    week.date = new Date(weekdate)
                }

                var sessiondate = new Date(week.date)
                for (var sess of week.sessions) {
                    if (sess.date == null) {
                        sess.date = new Date(sessiondate)
                    }
                    sessiondate.setDate(sessiondate.getDate() + 2)
                }
                weekdate.setDate(weekdate.getDate() + 7)
            }
        }
    }

    resolve() {
        for (var week of this.weeks) {
            week.resolve()
        }
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////
//
// Processing Functionality
//
//////////////////////////////////////////////////////////////////////////////////////////////////

class ExerciseStatistics {
    constructor(exercise, rep_count=0, inol=0, weight=0, avg_set_percent=0, max_set_percent=0, min_set_percent=100, minutes=0, prs=null) {
        this.exercise = exercise
        this.rep_count = rep_count
        this.inol = inol
        this.weight = weight
        this.avg_set_percent = avg_set_percent
        this.max_set_percent = max_set_percent
        this.min_set_percent = min_set_percent
        this.minutes = minutes
        this.prs = prs ? prs : new Map()

        this.count = 0
    }

    toString() {
        if (this.weight > 0) {
            return "{}: {} minutes, {} kg, {} reps, inol {}, intensity min/avg/max: {}/{}/{}</li>".format(
                    this.exercise, Math.trunc(this.minutes), this.weight, this.rep_count, this.inol.toFixed(2), Math.trunc(this.min_set_percent), Math.trunc(this.avg_set_percent), Math.trunc(this.max_set_percent))
        } else {
            return "{}: {} minutes, {} reps".format(this.exercise, Math.trunc(this.minutes), this.rep_count)
        }
    }
}

class Statistics {
    /*
    Calculates statistics based on a Session, a Week or a Cycle.

    Each of which is just a collection of lines, sessions or weeks.

    Session / week / cycle can have dates.
    Lines don't have dates.

    How to present dates for stats?
    Save date for line, too?
    */
    constructor(what) {
        // TODO: don't assume it's a list of sessions...
        if (what instanceof Array) {
            this.sessions = what
            console.log("what instanceof Array")
        }
        if (what instanceof Session) {
            this.sessions = [what]
        }
        else if (what instanceof Week) {
            this.sessions = what.sessions.map(s => s)
        }
        else if (what instanceof Cycle) {
            this.sessinos = []
            for (var week in what.weeks) {
                this.sessions.push(...week.sessions)
            }
        }
        this.date = what.date
        var lines = []
        for (var session of this.sessions) {
            lines.push(...session.lines)
        }

        // total number of minutes
        this.minutes = 0

        this.exercises = new Set() // only non-root exercises
        this.roots = new Set() // only root exercises
        this.data = new Map() // Exercxse : ExerciseStatistics


        //
        // Merge lines:
        //
        // e.g. two kbhs i the same sesssion
        // but also for having two sessions.
        //
        var line_exercise = new Map()
        for (var line of lines) {
            if (!line_exercise.has(line.exercise)) {
                line_exercise.set(line.exercise, line.copy())
            } else {
                line_exercise.get(line.exercise).sets.push(...line.sets)
            }
        }

        this.lines = [...line_exercise.values()]
        var data = this.data
        
        // Gather roots, create default stats
        var processed_roots = new Map()
        for (var line of this.lines) {
            var root = line.exercise.root()
            if (processed_roots.has(root))
                continue

            processed_roots.set(root, true)

            this.roots.add(root)

            data.set(root, new ExerciseStatistics(root))
        }

        // Produce statistics for all non-root exercises
        for (var line of this.lines) {
            var ex = line.exercise
            if (this.roots.has(ex))
                continue

            this.exercises.add(ex)

            // calculate max weights for different reps
            var prs = new Map()
            var linedate = null
            if (line.session != null) {
                linedate = line.session.date
            }
            for (var aset of line.sets) {
                if (aset.length == 2) {
                    var [w, r] = aset
                    if (!prs.has(r)) {
                        prs.set(r, [w, linedate])
                    }
                    if (prs.get(r)[0] < w) {
                        prs.get(r)[0] = w
                    }
                }
            }

            // Collect statistics per exercise (for root, this includes children)
            let exstats = new ExerciseStatistics(ex, line.rep_count(), line.inol(), line.total_weight(), 
                line.avg_set_percent(), line.max_set_percent(), line.min_set_percent(), 
                line.minutes(), prs)

            data.set(ex, exstats)
        }
        //console.log("-------------------------")

        var processed_children = new Map()
        for (var line of this.lines) {
            let root = line.exercise.root()

            /* 
             * Related: only rep-count and minutes
             * Children: Everything else.
            */
            for (var child of root.children) {
                if (!this.exercises.has(child))
                    continue

                if (processed_children.has(child))
                    continue

                processed_children.set(child, true)

                var rv = data.get(root)
                var cv = data.get(child)

                //console.log("Add self {} stats ({} minutes) of {} to total of root {}".format(cv, cv.minutes, child, root))
                //console.log("CHILDREN: Adding total of", child, "min", data[child]['self']['minutes'], "reps", data[child]['self']['rep-count'], "to", root)

                rv.count += 1 
                rv.rep_count += cv.rep_count
                rv.inol += cv.inol
                rv.weight += cv.weight
                rv.minutes += cv.minutes

                rv.avg_set_percent += cv.avg_set_percent
                if (rv.max_set_percent < cv.max_set_percent)
                    rv.max_set_percent = cv.max_set_percent

                if (rv.min_set_percent > cv.min_set_percent)
                    rv.min_set_percent = cv.min_set_percent
            }

            for (var related of root.related) {
                if (!this.exercises.has(related))
                    continue

                /*
                * TODO: Add related to their parent _and_ this exercise.
                *
                * e.g.: 
                */
                if (processed_children.has(related))
                    continue

                processed_children.set(related, true)

                var rv = data.get(root)
                var sv = data.get(related)

                //console.log("RELATED: Adding total of", related, "min", data[related]['self']['minutes'], "reps", data[related]['self']['rep-count'], "to", root)
                //console.log("related {} add {} min to root {}".format(related, rv.minutes, root)
                //
                rv.rep_count += sv.rep_count
                rv.minutes += sv.minutes
            }

        }


        // Process roots only.
        this.minutes = 0
        for (var root of this.roots) {
            var dk = data.get(root)

            dk.avg_set_percent /= dk.count
            this.minutes += dk.minutes
        }
    }
}


