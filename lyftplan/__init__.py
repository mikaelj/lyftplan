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
    MINUTES_PER_SET_DEFAULT = 4.5
    def __init__(self, name, flavor, parent, related, reps, time):
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
        self.reps = reps

        self.children = []
        if self.parent:
            #print("Exercise. Appending", self, "as child of", parent)
            self.parent.children.append(self)

        # All exercises related to me. Essentially, only KB, BP, ML
        # Reps and minutes are added from related, but not this.
        self.related = []

        if related:
            related.relate(self)

        if time is not None:
            #print(self, "has custom time", time)
            self.minutes_per_set = time
        else:
            self.minutes_per_set = Exercise.MINUTES_PER_SET_DEFAULT

        pretty = self.name
        if self.flavor != "":
            pretty = "{} ({})".format(self.name, self.flavor)

        if len(pretty) > Exercise.NAME_WIDTH:
            Exercise.NAME_WIDTH = len(pretty)

        if len(self.__class__.__name__) > Exercise.CLASS_WIDTH:
            Exercise.CLASS_WIDTH = len(self.__class__.__name__)

    def relate(self, related):
        self.related.append(related)

    def __str__(self):
        pretty = self.name
        if self.flavor != "":
            pretty = "{} ({})".format(self.name, self.flavor)

        #classname = self.__class__.__name__ + ": "
        classname = ""

        #return "{:<{}}{:<{}}".format(classname, Exercise.CLASS_WIDTH, pretty, Exercise.NAME_WIDTH)
        return "{:<{}}".format(pretty, Exercise.NAME_WIDTH)


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
    def __init__(self, flavor, parent=None, related=None, reps={}, time=None):
        super().__init__("Knäböj", flavor, parent, related, reps, time)

class BP(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}, time=None):
        super().__init__("Bänkpress", flavor, parent, related, reps, time)

class ML(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}, time=None):
        super().__init__("Marklyft", flavor, parent, related, reps, time)

class Rumpa(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}, time=None):
        super().__init__("Rumpa", flavor, parent, related, reps, time)
        if time is None:
            self.minutes_per_set = 2.5

class Rygg(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}, time=None):
        super().__init__("Rygg", flavor, parent, related, reps, time)
        if time is None:
            self.minutes_per_set = 2.5

class Axlar(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}, time=None):
        super().__init__("Axlar", flavor, parent, related, reps, time)
        if time is None:
            self.minutes_per_set = 2

class Armar(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps={}, time=None):
        super().__init__("Armar", flavor, parent, related, reps, time)
        if time is None:
            self.minutes_per_set = 1.5

class Line(object):
    PRINT_MODE_KG = 0
    PRINT_MODE_PERCENT = 1
    OUTPUT_TYPE_READABLE = 0
    OUTPUT_TYPE_CSV = 1
    def __init__(self, exercise, note, sets):
        self.exercise = exercise
        self.note = note
        self.sets = sets
        self.print_mode = Line.PRINT_MODE_KG
        self.output_type = Line.OUTPUT_TYPE_READABLE
        self.session = None

    def copy(self):
        line = Line(self.exercise, self.note, list(self.sets))
        line.print_mode = self.print_mode
        line.output_type = self.output_type
        line.session = self.session
        return line

    def _str_readable(self):
        strsets = ", ".join([self._set2str(s) for s in self.sets])
        inol = self.inol()
        inoltext = "{:.2f}".format(inol)
        if inol <= 0:
            inol = 0
            inoltext = ""
        #return "{exercise}: {sets}\n{rep_count} | {avg_set_weight:.1f} / {avg_set_percent:2.0f}% {inoltext}\nRoot: {root}".format(exercise=self.exercise, rep_count=self.rep_count(), sets=strsets, avg_set_weight=self.avg_set_weight(), avg_set_percent=self.avg_set_percent(), inoltext=inoltext, root=self.exercise.root())

        return "{exercise} ({inoltext}): {sets}".format(exercise=self.exercise, rep_count=self.rep_count(), sets=strsets, avg_set_weight=self.avg_set_weight(), avg_set_percent=self.avg_set_percent(), inoltext=inoltext, root=self.exercise.root())

    def _str_csv(self):
        def _weight_formatter(w):
            w = float(w)
            if w.is_integer():
                return "{:.0f}".format(w)
            else:
                return "{:.2f}".format(w)

        #setreps = [self._set2rep(s) for s in self.sets]
        #setweights = [self._set2rep(s) for s in self.sets]

        setweightreps = [self._set2weightreps(s) for s in self.sets]

        inol = self.inol()
        inoltext = "{:.2f}".format(inol)
        if inol <= 0:
            inol = 0
            inoltext = ""

        reps = "#".join(list(map(lambda x: x[1], setweightreps)))
        weights = ""
        if any(map(lambda x: x[0] > 0, setweightreps)):
            # print second line
            weights = "#".join(map(lambda x: _weight_formatter(x[0]), setweightreps))


        line1 = reps
        line2 = ""
        if weights:
            line1 = weights
            line2 = reps

        s = "{exercise}#{line1}".format(exercise=str(self.exercise).strip(), rep_count=self.rep_count(), line1=line1, avg_set_weight=self.avg_set_weight(), avg_set_percent=self.avg_set_percent(), inoltext=inoltext, root=self.exercise.root())

        if line2 or self.note:
            s += "\n{note}#{line2}".format(note=self.note,line2=line2)
        return s

    def __str__(self):
        if self.output_type == Line.OUTPUT_TYPE_READABLE:
            return self._str_readable()
        else:
            return self._str_csv()

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

    def minutes(self):
        #print("MINUTES", self, "setcount", len(self.sets), "minutes-per-set", self.exercise.minutes_per_set)
        return len(self.sets) * self.exercise.minutes_per_set

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
            #print("max1rm", self, " <= 0:", max1rm)
            return 0

        values = [self.weight(s)*100.0/max1rm for s in self.sets]
        #print("min:",self, values, "=", min(values))

        return min(values)

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
        if self.total_weight() < 1:
            return 0
        inol = 0.0
        for s in self.sets:
            reps = self.reps(s)
            percent = self.percent(s)
            inol += reps / (100.0 - percent*100.0)
        return inol


    def _set2weightreps(self, aset):
        """Fill in missing weights if any and transform into proper string format.

        aset can be a tuple of 1, 2 or 3 items.

        (reps,) => (0, "reps")
        (weight,reps) => (weight, "reps")
        (weight,reps_from,reps_to) => (weight, "reps_from-reps_to")

        """
        assert (len(aset) >= 1) and (len(aset) <= 3), ("set2str: invalid number ({}) of items in {}".format(len(aset), str(aset)))

        what = aset[0]
        if self.print_mode == Line.PRINT_MODE_PERCENT:
            max1 = self.exercise.reps.get(1, (0,''))
            max1kg = max1[0]
            if max1kg > 1:
                what = "{:.0f}% ".format(what*100.0/float(max1kg))

        if len(aset) == 1:
            return (0, "{}".format(what))
        elif len(aset) == 2:
            return (what,"{}".format(aset[1]))
        elif len(aset) == 3:
            return (what, "{}-{}".format(aset[1], aset[2]))

        # doesn't happen
        return "<fel>"

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


##############################################################
#
# Exercise Bank
#
##############################################################

g_module = None
def register(module):
    #print(module)
    #print(dir(module))
    global g_module

    g_module = module


###################################################################################################
#
# Schedule Structure
# 
###################################################################################################

def instantiate_line(line):
    #items = dict(globals().items())

    #g_module.__dict__.get(

    items = [(name, g_module.__dict__.get(name)) for name in dir(g_module)]
    for n, o in items:
        name = line.split()[0].strip()
        setspec = line.split('|')[1].strip()
        comment = line.split('|')[0].strip()
        comment = " ".join(comment.split()[1:]).strip()

        #print(name, comment, setspec, "vs", n, o)
        if n == name and isinstance(o, Exercise):
            if comment == '|': comment = ""
            #print("calling {}({}, {}, {})".format(o, name, comment, sets(setspec)))
            return o(comment, sets(setspec))

    import sys
    sys.exit("Invalid line: {}".format(line))

def instantiate_lines(lines):
    ok = [line.strip() for line in lines.split('\n') if len(line.strip()) > 0]
    lines = list(map(instantiate_line, ok))
    return lines

class Session(object):
    def __init__(self, lines, date=None):
        if type(lines) == str:
            lines = instantiate_lines(lines)

        self.lines = lines
        if date != None:
            date = datetime.date(*date)
        self.date = date
        for line in lines:
            line.session = self

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
                sessiondate += datetime.timedelta(days=2)

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
            #print("session stats:, count sessions:", len(self.sessions))
        elif type(what) == Week:
            self.sessions = [what[i] for i in range(len(what))]
            #print("week stats:, count sessions:", len(self.sessions))
        elif type(what) == Cycle:
            self.sessions = []
            for week in what:
                self.sessions.extend([week[i] for i in range(len(week))])

        self.date = what.date
        self.session_count = len(self.sessions)
        lines = [line for sess in self.sessions for line in sess.lines]
        #        print("count lines:", len(lines))

        #
        # Merge lines:
        #
        # e.g. two kbhs i the same sesssion
        # but also for having two sessions.
        #
        line_exercise = {}
        for line in lines:
            if not line.exercise in line_exercise:
                line_exercise[line.exercise] = line.copy()
            else:
                line_exercise[line.exercise].sets.extend(line.sets)

        self.lines = [line for ex, line in line_exercise.items()]

        self.data = {}
        self.exercises = set()
        data = self.data

        # Produce statistics for all exercises, without adding in children.
        for line in self.lines:
            ex = line.exercise

            self.exercises.add(ex)

            # calculate max weights for different reps
            prs = {}
            linedate = None
            if line.session:
                linedate = line.session.date
            for aset in line.sets:
                if len(aset) == 2:
                    w, r = aset
                    if not r in prs:
                        prs[r] = [w, linedate]
                    if prs[r][0] < w:
                        prs[r][0] = w

            #print("Calculating for exercise", ex, ex.name, ex.flavor)
            data[ex] = {'self': {
                            'count': 1,
                            'rep-count': line.rep_count(),
                            'inol': line.inol(),
                            'weight': line.total_weight(),
                            'avg-set-percent': line.avg_set_percent(),
                            'max-set-percent': line.max_set_percent(),
                            'min-set-percent': line.min_set_percent(),
                            'minutes': line.minutes(),
                            'prs': prs},

                        'total': {
                            'count': 1,
                            'rep-count': line.rep_count(),
                            'inol': line.inol(),
                            'weight': line.total_weight(),
                            'avg-set-percent': line.avg_set_percent(),
                            'max-set-percent': line.max_set_percent(),
                            'min-set-percent': line.min_set_percent(),
                            'minutes': line.minutes()}
                       }

        processed_children = {}
        for line in self.lines:
            root = line.exercise.root()
            if not root in data:
                #print("Calculating and processing children for root", root, root.name, root.flavor)
                data[root] = {'self': {
                                'count': 1,
                                'rep-count': line.rep_count(),
                                'inol': line.inol(),
                                'weight': line.total_weight(),
                                'avg-set-percent': line.avg_set_percent(),
                                'max-set-percent': line.max_set_percent(),
                                'min-set-percent': line.min_set_percent(),
                                'minutes': line.minutes()},

                            'total': {
                                'count': 0,#,1,
                                'rep-count': 0,#,line.rep_count(),
                                'inol': 0,#,line.inol(),
                                'weight': 0,#,line.total_weight(),
                                'avg-set-percent': 0,#,line.avg_set_percent(),
                                'max-set-percent': 0,#,line.max_set_percent(),
                                'min-set-percent': 0,#,line.min_set_percent(),
                                'minutes': 0}#,line.minutes()}
                           }

            # 
            # Related: only rep-count and minutes
            # Children: Everything else.
            #
            #print("- children: ", ["{} ({})".format(e.name, e.flavor) for e in root.children])
            for child in root.children:
                if not child in self.exercises:
                    continue

                if child in processed_children:
                    continue

                processed_children[child] = True

                #print("CHILDREN: Adding total of", child, "min", data[child]['self']['minutes'], "reps", data[child]['self']['rep-count'], "to", root)

                data[root]['total']['count'] += data[child]['self']['count']
                data[root]['total']['rep-count'] += data[child]['self']['rep-count']
                data[root]['total']['inol'] += data[child]['self']['inol']
                data[root]['total']['weight'] += data[child]['self']['weight']
                data[root]['total']['minutes'] += data[child]['self']['minutes']

                if data[root]['total']['max-set-percent'] < data[child]['self']['max-set-percent']:
                    data[root]['total']['max-set-percent'] = data[child]['self']['max-set-percent']

                if data[root]['total']['min-set-percent'] > data[child]['self']['min-set-percent']:
                    data[root]['total']['min-set-percent'] = data[child]['self']['min-set-percent']

                """
                data[root]['total']['count'] += 1
                data[root]['total']['rep-count'] += line.rep_count()
                data[root]['total']['inol'] += line.inol()
                data[root]['total']['weight'] += line.total_weight()
                data[root]['total']['avg-set-percent'] += line.avg_set_percent()
                data[root]['total']['max-set-percent'] += line.max_set_percent()
                data[root]['total']['min-set-percent'] += line.min_set_percent()
                data[root]['total']['minutes'] += line.minutes()

                if data[root]['total']['max-set-percent'] < line.max_set_percent():
                    data[root]['total']['max-set-percent'] = line.max_set_percent()

                if data[root]['total']['min-set-percent'] > line.min_set_percent():
                    data[root]['total']['min-set-percent'] = line.min_set_percent()
                """


            for related in root.related:
                if not related in self.exercises:
                    continue

                #print("RELATED: Adding total of", related, "min", data[related]['self']['minutes'], "reps", data[related]['self']['rep-count'], "to", root)

                data[root]['total']['rep-count'] += data[related]['self']['rep-count']
                data[root]['total']['minutes'] += data[related]['self']['minutes']

        # Process root data
        for key, value in data.items():
            #print("key", key, "total:", data[key]['total'])
            data[key]['total']['avg-set-percent'] /= data[key]['total']['count']

        """
        # Produce statistics for all roots
        for line in self.lines:
            ex = line.exercise

            root = ex.root()

            if not root in data:
                #print("Initializing", root)
                data[root] = {'count': 0,
                              'rep-count': 0,
                              'total-rep-count': line.rep_count(),
                              'inol': 0.0,
                              'total-weight': 0.0,
                              'avg-set-percent': 0,
                              'max-set-percent': 0,
                              'min-set-percent': 100,
                              'total-minutes': 0,
                              'minutes': line.minutes()}

            data[root]['count'] += 1
            data[root]['total-rep-count'] += line.rep_count()
            data[root]['inol'] += line.inol()
            data[root]['total-weight'] += line.total_weight()
            data[root]['avg-set-percent'] += line.avg_set_percent()
            data[root]['total-minutes'] += line.minutes()

            if data[root]['max-set-percent'] < line.max_set_percent():
                data[root]['max-set-percent'] = line.max_set_percent()

            if data[root]['min-set-percent'] > line.min_set_percent():
                #print(data[root]['min-set-percent'], " > ",  line.min_set_percent())
                data[root]['min-set-percent'] = line.min_set_percent()

        # Process data
        for key, value in data.items():
            data[key]['avg-set-percent'] /= data[key]['count']
        """

        """
        # Add time and rep information from ancillary exercisess to base movements
        counted_roots = {}
        for ex, info in data.items():
            if ex.related:
                for related in ex.related:
                    root = related.root()
                    if not root in counted_roots:
                        counted_roots[root] = True
                        #print("Time for", root, "is", data[root]['minutes'])
                        data[ex]['total-minutes'] += data[root]['minutes']
                        data[ex]['total-rep-count'] += data[root]['rep-count']
        """

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
    #print("Running automatic tests")
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

def print_session(sess, csv=False):
    #print("Övning#set")
    total_minutes = 0
    for line in sess.lines:
        #line.print_mode = Line.PRINT_MODE_PERCENT
        if csv:
            line.output_type = Line.OUTPUT_TYPE_CSV
        print(line)
        total_minutes += line.minutes()
        #print("\n")

    h = int(total_minutes / 60)
    m = int(total_minutes)
    if h > 0:
        m = int(total_minutes%60)
        print("ca {} timmar {} minuter".format(h, m))
    else:
        print("ca {} minuter".format(m))


def print_stats_ex(stats, ex, indent=0, csv=False):
    if not ex in stats.data:
        #print("ex not in stats.data:", ex)
        return
    d = stats.data[ex]['total']

    padding = indent * "   "
    minutes = int(d['minutes'])
    #print("print_stats_ex:", ex, "with minutes=", minutes)
    count = d['count']
    rep = d['rep-count']
    inol = d['inol']
    weight = d['weight']
    avg_percent = d['avg-set-percent']
    max_set_percent = d['max-set-percent']
    min_set_percent = d['min-set-percent']

    if avg_percent == 0:
        avg_percent = ""
    else:
        avg_percent = "{}".format(int(avg_percent))

    if max_set_percent == 0:
        max_set_percent = ""
    else:
        max_set_percent = "{}".format(int(max_set_percent))

    if min_set_percent == 0:
        min_set_percent = ""
    else:
        min_set_percent = "{}".format(int(min_set_percent))

    inol_indicator = ""
    if inol > float(len(stats.sessions)) * 1.33:
        inol_indicator = "(high)"
    if inol < float(len(stats.sessions)) * 0.8:
        inol_indicator = "(low)"
    if inol == 0:
        inol = ""
    else:
        inol = "{:3.2f}".format(inol)
    ton = weight/1000.0
    if weight == 0:
        ton = ""
    else:
        ton = "{:3.2f}".format(ton)

    if csv:
        padding = "> " * indent
        print("{}{}#{}#{}#{}#{}#{}#{}#{}".format(padding, str(ex).strip(), rep, minutes, inol, ton, avg_percent, min_set_percent, max_set_percent))
        """
        if avg_percent > 0:
            percent = "{:2.0f}%, min: {:2.0f}% max: {:2.0f}%".format(avg_percent, min_set_percent, max_set_percent)
        else:
            percent = "         -            "
        if inol > 0:
            print("{}{} => {:3d} reps {:4.2f} ton ({}) -> INOL {:3.2f} {}".format(
                padding, ex, rep, weight/1000.0, percent, inol, inol_indicator))
        else:
            print("{}{} => {:3d} reps {:4.2f} ton ({})".format(padding, ex, rep, percent, weight/1000.0))
              """
    else:

        if ton:
            ton += " ton"

        if avg_percent:
            percent = "{}%, min: {}% max: {}%".format(avg_percent, min_set_percent, max_set_percent)
        else:
            percent = "" #"         -            "
        if inol:
            print("{}{} => {:3d} reps ({} minuter) {} ({}) -> INOL {} {}".format(
                padding, ex, rep, minutes, ton, percent, inol, inol_indicator))
        else:
            if percent:
                print("{}{} => {:3d} reps ({} minuter) {} ({})".format(padding, ex, rep, minutes, ton, percent))
            else:
                print("{}{} => {:3d} reps ({} minuter)".format(padding, ex, rep, minutes))

def print_stats(stats, indent=0,csv=False,print_children=True):
    if csv:
        print("Övning#Reps#Minuter#INOL#Ton#Snitt%#Min%#Max%")
    total_minutes = 0

    #print(stats.exercises)

    """
    if kb in stats.data:
        total_minutes += stats.data[kb]['total']['minutes']
        #print(kb, stats.data[kb]['minutes'])
        print_stats_ex(stats, kb, indent, csv)
        for child in kb.children:
            print_stats_ex(stats, child, indent+1, csv)
        printed_roots = {}
        for related in kb.related:
            for child in related.children:
                print_stats_ex(stats, child, indent+1, csv)
    """

    kb_tavling = g_module.__dict__.get('kb_tavling')
    bp_tavling = g_module.__dict__.get('bp_tavling')
    ml_tavling = g_module.__dict__.get('ml_tavling')
    if kb_tavling in stats.data:
        total_minutes += stats.data[kb_tavling]['total']['minutes']
        print_stats_ex(stats, kb_tavling, indent, csv)

        if print_children:
            for child in kb_tavling.children:
                print_stats_ex(stats, child, indent+1, csv)
            printed_roots = {}
            for related in kb_tavling.related:
                if related in stats.exercises: #stats.data:
                    print_stats_ex(stats, related, indent+1, csv)

    if bp_tavling in stats.data:
        total_minutes += stats.data[bp_tavling]['total']['minutes']
        print_stats_ex(stats, bp_tavling, indent, csv)
        if print_children:
            for child in bp_tavling.children:
                print_stats_ex(stats, child, indent+1, csv)
            printed_roots = {}
            for related in bp_tavling.related:
                if related in stats.exercises: #stats.data:
                    print_stats_ex(stats, related, indent+1, csv)

    if ml_tavling in stats.data:
        total_minutes += stats.data[ml_tavling]['total']['minutes']
        print_stats_ex(stats, ml_tavling, indent, csv)
        if print_children:
            for child in ml_tavling.children:
                print_stats_ex(stats, child, indent+1, csv)
            printed_roots = {}
            for related in ml_tavling.related:
                if related in stats.exercises: #stats.data:
                    print_stats_ex(stats, related, indent+1, csv)

    """
    if ml_tavling in stats.data:
        total_minutes += stats.data[ml_tavling]['total']['minutes']
        print_stats_ex(stats, ml_tavling, indent, csv)
        for child in ml_tavling.children:
            print_stats_ex(stats, child, indent+1, csv)
        printed_roots = {}
        for related in ml_tavling.related:
            if len(related.children) > 0:
                for child in related.children:
                    print_stats_ex(stats, child, indent+1, csv)
            else:
                print_stats_ex(stats, related, indent+1, csv)
    """

    """
    for ex, d in stats.data.items():
        minutes = d['minutes']
        total_minutes += minutes
        minutes = int(minutes)

        if ex == kb or ex == ml or ex == bp:
            continue

        print_stats_ex(stats, ex, d, indent, csv)
    """


    h = int(total_minutes / 60)
    m = int(total_minutes)
    if h > 0:
        m = int(total_minutes%60)
        print("ca {} timmar {} minuter".format(h, m))
    else:
        print("ca {} minuter".format(m))


def print_pr(stats):
    for ex in stats.data:
        if not 'prs' in stats.data[ex]['self']:
            continue
        prs = stats.data[ex]['self']['prs']
        if not prs:
            continue
        b = list(zip(list(prs.keys()), list(prs.values())))
        b.sort(key=lambda x: x[0])
        print(ex, ", ".join("{} x {} ({})".format(b[0], a, b[1]) for a,b in b))


