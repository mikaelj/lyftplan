#!/usr/bin/env python3
# encoding:utf-8

class Exercise(object):
    NAME_WIDTH = 0
    CLASS_WIDTH = 0
    def __init__(self, name, flavor, parent, related, repsstats):
        """Initialize an Exercise object.

        flavor: competition, touch'n'go, etc.
        parent: which type of exercise is this, if any?
        related: what exercise is it related to, if any?
        repsstats: [(weight, reps, "date")]

        Usually, parent and related are mutex.  e.g. back extensions are related to deadlift, but isn't a child of.
        """
        self.name = name
        self.flavor = flavor
        self.parent = parent
        self.related = related
        self.repsstats = repsstats

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

        return "{:<{}}: {:<{}}".format(self.__class__.__name__, Exercise.CLASS_WIDTH, pretty, Exercise.NAME_WIDTH)

class KB(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps=None):
        super().__init__("Knäböj", flavor, parent, related, reps)

class BP(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps=None):
        super().__init__("Bänkpress", flavor, parent, related, reps)

class ML(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps=None):
        super().__init__("Marklyft", flavor, parent, related, reps)

class Rygg(Exercise):
    def __init__(self, flavor, parent=None, related=None, reps=None):
        super().__init__("Ryggövningar", flavor, parent, related, reps)

class Line(object):
    def __init__(self, exercise, note, sets):
        self.exercise = exercise
        self.note = note
        self.sets = sets

    def __str__(self):
        strsets = ", ".join([self._set2str(s) for s in self.sets])
        return "{exercise}: {sets}".format(exercise=self.exercise, sets=strsets)

    def __format__(self, spec):
        return str(self)


    def _set2str(self, aset):
        """Return a string representation of aset.

        aset can be a tuple of 1, 2 or 3 items.

        (reps,)
        (weight,reps)
        (weight,reps_from,reps_to)
        """
        assert (len(aset) >= 1) and (len(aset) <= 3), ("set2str: invalid number ({}) of items in {}".format(len(aset), str(aset)))

        if len(aset) == 1:
            return "{}".format(aset[0])
        elif len(aset) == 2:
            return "{}x{}".format(aset[0], aset[1])
        elif len(aset) == 3:
            return "{}x{}-{}".format(aset[0], aset[1], aset[2])

        # doesn't happen
        return "<fel>"


kb = KB("tävling", reps=[(80, 1, "2017-11-11")])
bp = BP("tävling", reps=[(65, 1, "2018-02-24")])
ml = ML("SMalmark", reps=[(130, 1, "2018-01-20")])
rygg = Rygg("ryggövningar")

ml_sumo = ML("sumo", ml, reps=[(130, 1, "2018-01-20")])

kb_hs = KB("hög stång (utan bälte)", parent=kb, reps=[(60, 1, "2017-11-11")])
kb_bred = KB("bredböj", kb)

bp_pinpress = BP("pinpress", bp)

rygg_hangande_rodd = Rygg("hängande rodd", rygg)
rygg_latsdrag = Rygg("latsdrag", rygg)
rygg_tryndrag = Rygg("tryndrag", rygg)
#marklyft_sumo = ("Sumomarklyft", mls)
ml_klotsving = ML("klotsving", related=ml)
rygg_lyft = Rygg("rygglyft", rygg)


###################################################################################################
#
# Utility functions
# 
###################################################################################################

def print_lines(lines):
    for line in lines:
        print(line)
        if line.note != "":
            print("{}\n".format(line.note))


