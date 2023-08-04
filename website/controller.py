import json
import pandas as pd


def recalc():
    from . import db
    from .models import User
    users = User.query.all()
    for user in users:
        user.vector = build_profile(user.preferences)
        db.session.commit()
    for user in users:
        names, numbers = similarity(10, user.vector)
        user.recommended_names = names
        user.recommended_numbers = numbers
        db.session.commit()


def build_profile(pref: json):  # returns user vector based on the preference vector
    from .const import nr_tags, tags, items
    result = nr_tags * [0.0]
    pref_list = json.loads(pref)
    for i in range(len(result)):
        tagVector = items[tags[i]].tolist()
        for f in range(len(tagVector)):
            result[i] += tagVector[f] * pref_list[f]
    return json.dumps(result)


def empty_profile(pref_length: int):
    return json.dumps(pref_length * [0])


def default_preferences(pref_length: int, beginning: list = []):
    return json.dumps(beginning + (pref_length - len(beginning)) * [0])


def similarity(threshold: int, user_vector_json: json):
    from .const import items, nr_items, nr_tags, idf
    user_vector = json.loads(user_vector_json)
    table = pd.DataFrame(index=range(nr_items), columns=range(2))
    table.columns = ['Title', 'Prediction']
    table['Title'] = items['Title'].copy()
    for index, row in items.iterrows():
        one_item = row.tolist()
        one_item.pop(0)
        table['Prediction'].iloc[index] = 0
        for i in range(nr_tags):
            table['Prediction'].iloc[index] += user_vector[i] * idf[i] * one_item[i]
    order = table.sort_values('Prediction', ascending=False)
    upper_names = order['Title'].head(threshold).tolist()
    upper_numbers = order['Prediction'].head(threshold).tolist()
    return json.dumps(upper_names), json.dumps(upper_numbers)


def addRating(idx, num):
    from flask_login import current_user
    from . import db
    result = json.loads(current_user.preferences)
    result[idx] = num
    current_user.preferences = json.dumps(result)
    db.session.commit()
