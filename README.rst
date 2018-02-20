==========
Lyftplan
==========
Syfte
=============
Beskriva träningsprogram med data som möjliggör uträkningar (snitt-%, snitt-reps, snitt-set).

Dataformat
=============
Övningsdefinition::

    # (namn, relaterad övning, [(max i kg, antal reps, datum när max sattes)]

    kb = ("Knäböj (tävling)", None, [(80, 1, "2017-11-11")])
    kb1 = ("Knäböj (hög stång)", kb, [(80, 1, "2017-11-11")])
    kb2 = ("Knäböj (hög stång, bälte)", kb, [(80, "2017-11-11")])

    # skall benspark-reps och set räknas med? saknar (ju) vikt.
    # låt bli att räkna med i snittintensitet om de saknar vikt, men ha med som set/reps?
    ben1 = ("Benspark", kb
