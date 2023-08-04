import pandas as pd
from .const import items, idf, tags, nr_tags, nr_items
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def recalc():
    from . import db
    from .models import User
    users = User.query.all()
    for user in users:
        prof = build_profile(user.preferences)
        user.vector = str(prof)[1:-1].replace(",", " ")
        db.session.commit()
    for user in users:
        reccNames, reccNumbers = similarity(10, user.vector)
        user.reccommended_names = reccNames
        user.reccommended_numbers = reccNumbers
        db.session.commit()


def build_profile(pref):  # returns user vector based on the preference vector
    result = nr_tags * [0.0]
    prefListTmp = pref.split()
    prefList = [int(x) for x in prefListTmp]
    for i in range(len(result)):
        tagVector = items[tags[i]].tolist()
        for f in range(len(tagVector)):
            result[i] += tagVector[f] * prefList[f]
    return result


def empty_profile(count):
    profile = " "
    for i in range(count):
        profile += "0 "
    return profile


def default_preferences(count, start):
    profile = " "
    for item in start:
        profile += str(item) + " "
    for i in range(len(start), count):
        profile += "0 "
    return profile


def similarity(nr, userVectorRaw):
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
    upperNames = order['Title'].head(nr).tolist()
    upperNumbers = order['Prediction'].head(nr).tolist()
    return str(upperNames), str(upperNumbers)

def addRating(idx,num):
    from flask_login import current_user
    from . import db
    resTmp = current_user.preferences.split()
    result = [int(x) for x in resTmp]
    result[idx] = num
    current_user.preferences = str(result)[1:-1].replace(",", " ")
    db.session.commit()
    pass
