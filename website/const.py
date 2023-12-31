import json

import pandas as pd

items = pd.read_csv('items.csv')
nr_items = items.shape[0]
nr_tags = items.shape[1] - 1
tags = ['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem',
        'Hentai', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial Arts', 'Mecha', 'Military', 'Music',
        'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo',
        'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life', 'Space', 'Sports', 'Super Power', 'Supernatural',
        'Thriller', 'Vampire', 'Yaoi', 'Yuri']
idf = [0.6607763179677045, 0.7879202994635734, 2.1614130395140676, 0.4753011587671395, 1.6630506575148583,
       1.5035093058286846, 0.8085779375355088, 1.3794688001132849, 0.7456867971358444, 1.6886675848546933,
       1.648776784127788, 0.874993716228969, 1.199617392184297, 1.5768437803464406, 2.2245668401275416,
       0.8788948450118859, 1.2163370687990818, 1.6578988238884207, 1.2082603536878032, 1.4546760117960091,
       0.9857573817806657, 1.3467449553046615, 1.4389275683513483, 1.80669818488731, 1.671422858605084,
       0.9530282649897102, 1.9086877234246413, 1.004913987435148, 0.8359405873824265, 1.2931531926942037,
       1.3887384629915982, 2.3457454278625347, 0.9194024650785984, 2.232186236997734, 0.9724528542690655,
       1.5339855764978112, 1.3762438262699974, 1.430351658173298, 1.0515073175156429, 2.1005732496635545,
       2.067780736267247, 2.393170077790673, 2.387637589190712]
default_recommendation_names = json.dumps(
    ['Oshi no Ko', 'Fullmetal Alchemist: Brotherhood', 'Shingeki no Kyojin: The Final Season - Kanketsu-hen',
     'Bleach: Sennen Kessen-hen', 'Gintama', 'Kaguya-sama wa Kokurasetai: Ultra Romantic',
     'Shingeki no Kyojin Season 3 Part 2', 'Gintama: The Final', 'Hunter x Hunter (2011)', 'Ginga Eiyuu Densetsu'])
default_recommendation_numbers = json.dumps([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
