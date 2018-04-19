import numpy as np
import matplotlib.pyplot as plt
from prob2utils import train_model, get_err

def main():
    print('SVD. Training with `hidden` set, validating with `valid` set.')

    N_USERS = 458293
    N_MOVIES = 17770

    Y_train = np.loadtxt('../data/um/hidden.dta').astype(int)
    Y_train = np.delete(Y_train, 2, axis=1)
    Y_val = np.loadtxt('../data/um/valid.dta').astype(int)
    Y_val = np.delete(Y_val, 2, axis=1)
    Y_qual = np.loadtxt('../data/um/qual.dta').astype(int)
    Y_qual = np.delete(Y_qual, 2, axis=1)

    k = 50
    reg = 1
    eta = 0.03  # learning rate

    E_in = []
    E_val = []

    print('Factorizing with ', N_USERS, ' users, ', N_MOVIES, ' movies.')

    print('Training model with k = %s, eta = %s, reg = %s' % (k, eta, reg))
    U, V, e_in = train_model(N_USERS, N_MOVIES, k, eta, reg, Y_train, max_epochs=10)
    print('E_in = ', e_in)
    print('E_val = ', get_err(U, V, Y_val))

    outfile = open('out/svd1.dta', 'w')
    for i in range(Y_qual.shape[0]):
        user = Y_qual[i,0] - 1
        movie = Y_qual[i,1] - 1
        outfile.write('%.4f\n' % np.dot(U[user,:], V[:,movie]))
    outfile.close()

if __name__ == "__main__":
    main()
