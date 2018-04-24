import numpy as np

def get_average_rating():
    """ Gets the average rating over the entire training set.
    I was too lazy to do this in C++ """
    total = 0.0
    n_ratings = 0

    print("Begin mu acquisition...")
    with open("../um/all.dta", 'r') as all:
        print("Loading file all.dta")

        print("Getting mean")
        for i, line in enumerate(all):
            if i % 100000 == 0:
                print(i)
            fields = line.split(' ')
            if len(fields) == 4:
                total += float(fields[3])
                n_ratings += 1
        print("Finished going through entire data set")
    print("Mean = " + str(total / n_ratings))

get_average_rating()
