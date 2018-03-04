#!/usr/bin/env python3
# encoding:utf-8

import datetime

###################################################################################################
#
# Core functions
# 
###################################################################################################

class Exercise(object):
    NAME_WIDTH = 0
    CLASS_WIDTH = 0
    def __init__(self, name, flavor, parent, related, reps):
        """Initialize an Exercise object.

        flavor: competition, touch'n'go, etc.
        parent: which type of exercise is this, if any?
        related: what exercise is it related to, if any?
        reps: {reps : (weight, "date")}

        Usually, parent and related are mutex.  e.g. back extensions are related to deadlift, but isn't a child of.
        """
        self.name = name
        self.flavor = flavor
        self.parent = parent
        self.related = related
        self.reps = reps

        pretty = self.name
        if self.flavor != "":
            pretty = "{} ({})".format(self.name, self.flavor)

        if len(pretty) > Exercise.NAME_WIDTH:
            Exercise.NAME_WIDTH = len(pretty)

        if len(self.__class__.__name__) > Exercise.CLASS_WIDTH:
            Exercise.CLASS_WIDTH = len(self.__class__.__name__)

    def __str__(self):
        pretty = self.name
        if self.flavor != "":
            pretty = "{} ({})".format(self.name, self.flavor)

        #classname = self.__class__.__name__ + ": "
        classname = ""

        return "{:<{}}{:<{}}".format(classname, Exercise.CLASS_WIDTH, pretty, Exercise.NAME_WIDTH)


    def __call__(self, comment, setspec):
        return Line(self, comment, setspec)

    def max1rm(self):
        max1 = self.reps.get(1, (0,''))
        return max1[0]

    def root(self):
        if self.parent == None:
            return self
        p = self.parent
        root = p
        while p != None:
            root = p
            p = p.parent
        return root

class KB(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}):
        super().__init__("Knäböj", flavor, parent, related, reps)

class BP(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}):
        super().__init__("Bänkpress", flavor, parent, related, reps)

class ML(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}):
        super().__init__("Marklyft", flavor, parent, related, reps)

class Rumpa(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}):
        super().__init__("Rumpövningar", flavor, parent, related, reps)

class Rygg(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}):
        super().__init__("Ryggövningar", flavor, parent, related, reps)

class Line(object):
    PRINT_MODE_KG = 0
    PRINT_MODE_PERCENT = 1
    def __init__(self, exercise, note, sets):
        self.exercise = exercise
        self.note = note
        self.sets = sets
        self.print_mode = Line.PRINT_MODE_KG

    def __str__(self):
        strsets = ", ".join([self._set2str(s) for s in self.sets])
        inol = self.inol()
        inoltext = "=> {:.2f} INOL".format(inol)
        if inol <= 0:
            inol = 0
            inoltext = ""
        return "{exercise}: {sets}\n{rep_count} | {avg_set_weight:.1f} / {avg_set_percent:2.0f}% {inoltext}\nRoot: {root}".format(exercise=self.exercise, rep_count=self.rep_count(), sets=strsets, avg_set_weight=self.avg_set_weight(), avg_set_percent=self.avg_set_percent(), inoltext=inoltext, root=self.exercise.root())

    def __format__(self, spec):
        return str(self)

    def reps(self, s):
        if len(s) == 1:
            return s[0]
        elif len(s) == 2:
            return s[1]
        elif len(s) == 3:
            return (s[1] + s[2])/2
        else:
            return 1

    def weight(self, s):
        if len(s) >= 2:
            return s[0]

        return 0

    def percent(self, s):
        max1rm = self.exercise.max1rm()
        if max1rm > 0:
            return self.weight(s) / max1rm
        return 0

    def rep_count(self):
        reps = 0
        for s in self.sets:
            reps += self.reps(s)
        return reps

    def avg_set_weight(self):
        count = len(self.sets)
        weight = 0
        for s in self.sets:
            weight += self.weight(s)
        return weight/count

    def max_set_weight(self):
        return max(self.weight(s) for s in self.sets)

    def max_set_percent(self):
        max1rm = self.exercise.max1rm()
        if max1rm <= 0:
            return 0

        return max(self.weight(s)*100.0/max1rm for s in self.sets)

    def min_set_percent(self):
        max1rm = self.exercise.max1rm()
        if max1rm <= 0:
            return 0

        return min(self.weight(s)*100.0/max1rm for s in self.sets)

    def set_percent_list(self):
        max1rm = self.exercise.max1rm()
        if max1rm <= 0:
            return []

        return [self.weight(s)*100.0/max1rm for s in self.sets]

    def avg_set_percent(self):
        max1rm = self.exercise.max1rm()
        if max1rm > 0:
            return self.avg_set_weight()*100.0 / max1rm
        return 0

    def total_weight(self):
        return sum(self.reps(s) * self.weight(s) for s in self.sets)

    def inol(self):
        inol = 0.0
        for s in self.sets:
            reps = self.reps(s)
            percent = self.percent(s)
            inol += reps / (100.0 - percent*100.0)
        return inol


    def _set2str(self, aset):
        """Return a string representation of aset.

        aset can be a tuple of 1, 2 or 3 items.

        (reps,)
        (weight,reps)
        (weight,reps_from,reps_to)
        """
        assert (len(aset) >= 1) and (len(aset) <= 3), ("set2str: invalid number ({}) of items in {}".format(len(aset), str(aset)))

        what = aset[0]
        if self.print_mode == Line.PRINT_MODE_PERCENT:
            max1 = self.exercise.reps.get(1, (0,''))
            max1kg = max1[0]
            if max1kg > 1:
                what = "{:.0f}% ".format(what*100.0/float(max1kg))

        if len(aset) == 1:
            return "{}".format(what)
        elif len(aset) == 2:
            return "{}x{}".format(what, aset[1])
        elif len(aset) == 3:
            return "{}x{}-{}".format(what, aset[1], aset[2])

        # doesn't happen
        return "<fel>"


kb = KB("hög stång, bälte", reps={1 : (110, "2017-11-11")})
bp = BP("maxbrett", reps={1 : (65, "2018-02-24")})
ml_sumo = ML("sumo", reps={1 : (130, "2018-01-20")})
ml = ml_sumo
rygg = Rygg("")
rumpa = Rumpa("")

# parent = ml, but intensity calculated against sumo's 1rm
ml_smal = ML("smal", ml, reps={1 : (130, "2018-01-20")})

kb_hs = KB("hög stång (utan bälte)", parent=kb, reps={1 : (85, "2017-11-11")})
kb_bred = KB("bredböj", kb, reps={1 : (70, "2017-11-11")})

bp_pinpress = BP("pinpress", bp)

rygg_hangande_rodd = Rygg("hängande rodd", rygg)
rygg_latsdrag = Rygg("latsdrag", rygg)
rygg_tryndrag = Rygg("tryndrag", rygg)
#marklyft_sumo = ("Sumomarklyft", mls)
rumpa_klotsving = Rumpa("klotsving", rumpa, related=ml)
rygg_lyft = Rygg("rygglyft", rygg, related=ml)

class Session(object):
    def __init__(self, lines, date=None):
        self.lines = lines
        if date != None:
            date = datetime.date(*date)
        self.date = date

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

class Week(object):
    def __init__(self, sessions, date=None):
        self.sessions = sessions
        if date != None:
            date = datetime.date(*date)
        self.date = date

        # set date for each session if they don't have one.
        if self.date != None:
            sessiondate = self.date
            for sess in sessions:
                if sess.date == None:
                    sess.date = sessiondate
                sessiondate += datetime.timedelta(days=1)

    def __len__(self):
        return len(self.sessions)

    def __getitem__(self, index):
        return self.sessions[index]

class Cycle(object):
    def __init__(self, weeks, date=None):
        self.weeks = weeks
        if date != None:
            date = datetime.date(*date)
        self.date = date

        # set date for each week and each session if they don't have one.
        if self.date != None:
            weekdate = self.date
            for week in weeks:
                if not week.date:
                    week.date = weekdate

                sessiondate = weekdate
                for session in week:
                    if not session.date:
                        session.date = sessiondate
                    sessiondate += datetime.timedelta(days=1)

                weekdate += datetime.timedelta(days=7)

    def __len__(self):
        return len(self.weeks)

    def __getitem__(self, index):
        return self.weeks[index]


###################################################################################################
#
# Processing functions
# 
###################################################################################################

class Statistics(object):
    """Calculates statistics based on a Session, a Week or a Cycle.

    Each of which is just a collection of lines, sessions or weeks.

    Session / week / cycle can have dates.
    Lines don't have dates.

    How to present dates for stats?
    Save date for line, too?
    """
    def __init__(self, what):
        if type(what) == Session:
            self.sessions = [what]
        elif type(what) == Week:
            self.sessions = [what[i] for i in range(len(what))]
        elif type(what) == Cycle:
            self.sessions = []
            for week in what:
                self.sessions.extend([week[i] for i in range(len(week))])

        self.date = what.date
        self.session_count = len(self.sessions)
        self.lines = [line for sess in self.sessions for line in sess.lines]

        self.data = {}
        data = self.data

        for line in self.lines:
            ex = line.exercise

            root = ex.root()
            if not root in data:
                data[root] = {'count': 0,
                              'rep-count': 0,
                              'inol': 0.0,
                              'total-weight': 0.0,
                              'avg-set-percent': 0,
                              'max-set-percent': 0,
                              'min-set-percent': 100}

            data[root]['count'] += 1
            data[root]['rep-count'] += line.rep_count()
            data[root]['inol'] += line.inol()
            data[root]['total-weight'] += line.total_weight()
            data[root]['avg-set-percent'] += line.avg_set_percent()

            if data[root]['max-set-percent'] < line.max_set_percent():
                data[root]['max-set-percent'] = line.max_set_percent()

            if data[root]['min-set-percent'] > line.min_set_percent():
                data[root]['min-set-percent'] = line.min_set_percent()


        for key, value in data.items():
            data[key]['avg-set-percent'] /= data[key]['count']

def sets(spec):
    """"Return a list of tuples from a string on the following format:

    In: 30x3 40x3 40x3 40x3 40x3 40x3 40x3 40x3
    Out: [(30,3), (40,3), ...]

    In: 30x3-5 40x3 40x3-5 40x3 40x3 40x3 40x3 40x3
    Out: [(30,3,5), (40,3), (40,3,5) ...]

    In: 30 20 20
    Out: [(30,), (20,), (20,)]
    """
    sets = spec.split()
    wrs = []
    for s in sets:
        if 'x' in s:
            w, r = s.split('x')
            if '-' in r:
                r1, r2 = r.split('-')
                wrs.append((float(w), int(r1), int(r2)))
            else:
                wrs.append((float(w), int(r)))
        else:
            wrs.append((int(s),))

    return wrs

def test_sets():
    print("Running automatic tests")
    assert sets("30x3 40x3 40x3") == [(30,3), (40,3), (40,3)], sets("30x3 40x3 40x3")
    assert sets("30x3-5 40x3 40x3-5 40x3") == [(30,3,5), (40,3), (40,3,5), (40,3)], "error 2"
    assert sets("30 20 20") == [(30,), (20,), (20,)], "error 3"


###################################################################################################
#
# Utility functions
# 
###################################################################################################

def print_lines(lines):
    for line in lines:
        line.print_mode = Line.PRINT_MODE_PERCENT
        print(line)
        if line.note != "":
            print("{}\n".format(line.note))
        print("\n")

def print_stats2(lines, sessions=1, indent=0):
    data = {}
    exstats = {}
    """
    for line in lines:
        ex = line.exercise

        root = ex.root()
        if not root in data:
            data[root] = [0,0,0,0,0,0,100]

        if not root in exstats:
            exstats[root] = [0]

        data[root][0] += 1
        data[root][1] += line.rep_count()
        data[root][2] += line.inol()
        data[root][3] += line.total_weight()
        data[root][4] += line.avg_set_percent()

        if data[root][5] < line.max_set_percent():
            data[root][5] = line.max_set_percent()

        if data[root][6] > line.min_set_percent():
            data[root][6] = line.min_set_percent()

        #print("{}".format(line.set_percent_list()))
    """

    stats = Statistics(lines)

    #print("INOL and reps")
    padding = indent * "  "
    for ex, d in stats.data.items():
        count = d['count']
        rep = d['rep-count']
        inol = d['inol']
        weight = d['total-weight']
        avg_percent = d['avg-set-percent']
        max_set_percent = d['max-set-percent']
        min_set_percent = d['min-set-percent']

        inol_indicator = ""
        if inol > float(sessions) * 1.33:
            inol_indicator = "(high)"
        if inol < float(sessions) * 0.8:
            inol_indicator = "(low)"

        if avg_percent > 0:
            percent = "{:2.0f}%, min: {:2.0f}% max: {:2.0f}%".format(avg_percent, min_set_percent, max_set_percent)
        else:
            percent = "         -            "
        if inol > 0:
            print("{}{} => {:3d} reps {:4.2f} ton ({}) -> INOL {:3.2f} {}".format(
                padding, ex, rep, weight/1000.0, percent, inol, inol_indicator))
        else:
            print("{}{} => {:3d} reps {:4.2f} ton ({})".format(padding, ex, rep, percent, weight/1000.0))


def print_stats(stats, indent=0):
    padding = indent * "   "
    for ex, d in stats.data.items():
        count = d['count']
        rep = d['rep-count']
        inol = d['inol']
        weight = d['total-weight']
        avg_percent = d['avg-set-percent']
        max_set_percent = d['max-set-percent']
        min_set_percent = d['min-set-percent']

        inol_indicator = ""
        if inol > float(len(stats.sessions)) * 1.33:
            inol_indicator = "(high)"
        if inol < float(len(stats.sessions)) * 0.8:
            inol_indicator = "(low)"

        if avg_percent > 0:
            percent = "{:2.0f}%, min: {:2.0f}% max: {:2.0f}%".format(avg_percent, min_set_percent, max_set_percent)
        else:
            percent = "         -            "
        if inol > 0:
            print("{}{} => {:3d} reps {:4.2f} ton ({}) -> INOL {:3.2f} {}".format(
                padding, ex, rep, weight/1000.0, percent, inol, inol_indicator))
        else:
            print("{}{} => {:3d} reps {:4.2f} ton ({})".format(padding, ex, rep, percent, weight/1000.0))





















































