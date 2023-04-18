import pandas as pd


def recalc():
    from . import items, idf, nr_tags, nr_items, db
    from .models import User
    users = User.query.all()
    for user in users:
        print(user.email)
        prof = buildProfile(user.preferences)
        print("Calculated user profile:", prof)
        user.vector = str(prof)[1:-1].replace(",", " ")
        print("Added to database, calculated user profile:", str(prof)[1:-1].replace(",", " "))
        db.session.commit()
    print("Realculated")


def buildProfile(pref):  # returns user vector based on the preference vector
    from . import items, idf, nr_tags, nr_items, tags, db
    result = nr_tags * [0.0]
    prefListTmp = pref.split()
    prefList = [int(x) for x in prefListTmp]
    for i in range(len(result)):
        tagVector = items[tags[i]].tolist()
        for f in range(len(tagVector)):
            result[i] += tagVector[f] * prefList[f]
    return result


def emptyProfile(count):
    profile = " "
    for i in range(count):
        profile += "0 "
    return profile


def defaultPreferences(count, start):
    profile = " "
    for item in start:
        profile += str(item) + " "
    for i in range(len(start), count):
        profile += "0 "
    return profile


def similarity(nr, userVector):
    from . import items, idf, nr_tags, nr_items, tags, db
    res = nr * [""]
    return res
