from algorithm import Matching
import database
import demo
import numpy as np


### Question 5 ###

i = np.random.randint(0,10)
j = np.random.randint(0,10)

with open("songs.pickle", "rb") as handle:
    database = pickle.load(handle)
H1 = database[i]
H2 = database[j]
matching = Matching(H1,H2)
matching.display_scatterplot()


### Question 6 ###

i = np.random.randint(0,10)
j = np.random.randint(0,10)

with open("songs.pickle", "rb") as handle:
    database = pickle.load(handle)
H1 = database[i]
H2 = database[j]
matching = Matching(H1,H2)
matching.display_histogram
