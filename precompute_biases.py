import numpy as np

def precompute_biases():
    with open("../um/base.dta", "r") as base, \
    open("Numer_user_biases.dta", "w") as ub, \
    open("Numer_movie_biases.dta", "w") as mb, \
    open("user_counts.dta", "r") as uc:

        print("Successful opening")
        N_USERS = 458293
        N_MOVIES = 17770
        MU = 3.512599976023349

        ratings = np.zeros((N_USERS, N_MOVIES), dtype=np.int64)

        movie_biases = np.zeros(N_MOVIES)
        user_biases = np.zeros(N_USERS)
        factor = np.zeros(N_USERS)

        print("Filling in sparse and movie_bias matrix")
        for d, line in enumerate(base):
            if d % 500000 == 0:
                print("line " + str(d))
            fields = line.split(" ")
            ratings[int(fields[0]) - 1, int(fields[1]) - 1] = int(fields[3])
            movie_biases[int(fields[1]) - 1] += (int(fields[3]) - MU)


        print("Filling in user bias matrix")
        for u, user in enumerate(uc):
            if u % 10000 == 0:
                print(u)
            fields = user.split(' ')
            user_biases[u] = np.sum(ratings[u]) - MU * (int(fields[1]))
            factor[u] = int(fields[1])

        print("Writing to all movies")

        for i in range(N_MOVIES):
            if i % 10000 == 0:
                print(i)
            mb.write(str(movie_biases[i]) + '\n')
        print("Finished writing to all movies")

        print("Writing to all users")

        for u in range(N_USERS):
            if u % 100000 == 0:
                print(u)
            ub.write(str(user_biases[u]) + ' ' + str(factor[u]) + '\n')
        print("Finished writing to all users")
    return

precompute_biases()
