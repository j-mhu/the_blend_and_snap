import numpy as np
from sys import platform
import os
def get_user_movie_counts():
    """ Gets the user and movie counts needed to calculate
    user and movie biases over the entire
    training set. I was too lazy to do this in C++ also

    Returns:
       user_counts : (458293, 1) array of elements where
             the elements are the # movies rated by the user on that
             line
       movie_counts : (17770, 1) array of elements where the
             elements are the # users who rated the movie on that line
    """

    user_counts = np.zeros(458293, dtype=np.int8)
    movie_counts = np.zeros(17770, dtype=np.int8)

    if platform != "win32":
        all_file_path = "../um/all.dta"
        user_counts_path = "../um/user_counts.dta"
        movie_counts_path = "../um/movie_counts.dta"

    else:
        all_file_path = "../data/um/all.dta"
        user_counts_path = "../data/um/user_counts.dta"
        movie_counts_path = "../data/um/movie_counts.dta"

    print("Starting biases...")
    with open(all_file_path, "r") as all_um, \
    open(user_counts_path, "w") as ub, \
    open(movie_counts_path, "w") as mb:
        print("Loading file all.dta in user-movie order")

        print("Getting frequencies")
        for i, line in enumerate(all_um):
            if i % 100000 == 0:
                print("Finished line " + str(i))
            fields = line.split(' ')
            if len(fields) == 4:
                user_id = int(fields[0]) - 1
                movie_id = int(fields[1]) - 1
                # print(user_id, movie_id)
                user_counts[user_id] += 1
                # print(user_counts[user_id])
                movie_counts[movie_id] += 1
                # print(movie_counts[movie_id])

        print("Writing frequencies to file")
        for i in range(len(user_counts)):
            if i % 100000 == 0:
                print("Finished user " + str(i))
            user_l = str(i+1) + ' ' + str(user_counts[i]) + '\n'
            ub.write(user_l)

        print(" Finished writing frequencies to user bias file ")

        for i in range(len(movie_counts)):
            if i % 10000 == 0:
                print("Finished movie " + str(i))
            movie_l = str(i+1) + ' ' + str(movie_counts[i]) + '\n'
            mb.write(movie_l)
        print("Completed writing")
    return user_counts, movie_counts

get_user_movie_counts()
