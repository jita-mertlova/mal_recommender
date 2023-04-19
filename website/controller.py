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


def similarity(nr, userVectorRaw):
    from . import items, idf, nr_tags, nr_items, tags, db
    userVectorTmp = userVectorRaw.split()
    userVector = [float(x) for x in userVectorTmp]
    table = pd.DataFrame(index=range(nr_items), columns=range(2))
    table.columns = ['Title', 'Prediction']
    table['Title'] = items['Title'].copy()
    for index, row in items.iterrows():
        oneItem = row.tolist()
        oneItem.pop(0)
        table['Prediction'].iloc[index] = 0
        for i in range(nr_tags):
            table['Prediction'].iloc[index] += userVector[i] * idf[i] * oneItem[i]
    order = table.sort_values('Prediction', ascending=False)
    upper = order['Title'].head(nr).tolist()
    print(order)
    print(upper)
    return upper
