import numpy as np
import matplotlib.pyplot as plt
from prob2utils import train_model, get_err

def main():
    print("SVD. Training with 'hidden' set, validating with 'valid' set.")

    U = 458293  # number of users
    M = 17770   # number of movies

    Y_train = np.loadtxt('../data/um/hidden.dta').astype(int)
    Y_train = np.delete(Y_train, 2, axis=1)
    Y_val = np.loadtxt('../data/um/valid.dta').astype(int)
    Y_val = np.delete(Y_val, 2, axis=1)

    k = 50
    reg = 1
    eta = 0.03  # learning rate

    E_in = []
    E_val = []

    print("Factorizing with ", U, " users, ", M, " movies.")

    print("Training model with k = %s, eta = %s, reg = %s" % (k, eta, reg))
    U, V, e_in = train_model(U, M, k, eta, reg, Y_train, max_epochs=10)
    print("E_in = ", e_in)
    print("E_val = ", get_err(U, V, Y_val))

if __name__ == "__main__":
    main()
