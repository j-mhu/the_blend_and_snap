# Probe Blending using Linear Regression and given slides
# to optimize alphas (linear coefficients) for quiz

import numpy as np
from numpy.linalg import inv

def get_data():
    '''
    Loads prediction data from desired models for blending.

    Returns matrix A = [A_0, A_1, A_2, ...A_M-1] where A_i is the predictions
    from the ith model.
    '''
    print('Loading qual predictions...')
    models = ['./out/svd_funny_2.dta', './out/svd++1.dta']
    for i, model in enumerate(models):
        A_model = np.loadtxt(model).astype(int)
        if i == 0:
            A = [A_model]
        else:
            A = np.append(A, [A_model], axis=0)
    A = A.T
    print('Done loading qual predictions.')
    return A

def find_coefficients():
    '''
    Uses technique from given slides to find optimal alphas for blending on quiz.

    Returns matrix alphas, the optimal coefficients corresponding to the ith model
    for linear combination.
    '''
    zeroes_RMSE = 3.84358
    A = get_data()
    ATs = []
    for A_i in A.T:
        ATs.append(0.5 * (np.dot(A_i, A_i) + zeroes_RMSE * zeroes_RMSE))

    alphas = np.matmul(inv(np.matmul(A.T, A)), ATs)
    print(alphas)

if __name__ == "__main__":
    find_coefficients()
