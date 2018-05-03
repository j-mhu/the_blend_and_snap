# Probe Blending using Linear Regression and given slides
# to optimize alphas (linear coefficients) for quiz

import numpy as np
import math
from numpy.linalg import inv

def get_data():
    '''
    Loads prediction data from desired models for blending.

    Returns matrix A = [A_0, A_1, A_2, ...A_M-1] where A_i is the predictions
    from the ith model.
    '''
    print('Loading qual predictions...')
    # models = ['./out/svd_funny_2.dta', './out/svd++1.dta']
    models = ['./out/svd_funny_2.dta', './out/svd4.dta']
    RMSEs = [.91903, 0.94985]
    # RMSEs = [.91903, 0.97918]

    for i, model in enumerate(models):
        A_model = np.loadtxt(model).astype(int)
        if i == 0:
            A = [A_model]
        else:
            A = np.append(A, [A_model], axis=0)
    A = A.T
    print('Done loading qual predictions.')
    return A, RMSEs

def find_coefficients(A, RMSEs):
    '''
    Uses technique from given slides to find optimal alphas for blending on quiz.

    Returns matrix alphas, the optimal coefficients corresponding to the ith model
    for linear combination.
    '''
    NUM_POINTS = 2749898
    zeroes_RMSE = 3.84358 * 3.84358 * NUM_POINTS
    new_RMSEs = [math.pow(r, 2) * NUM_POINTS for r in RMSEs]
    ATs = []
    for i, A_i in enumerate(A.T):
        ATs.append(0.5 * (np.dot(A_i, A_i) + zeroes_RMSE - new_RMSEs[i]))
        # ATs.append(0.5 * (np.dot(A_i, A_i) + zeroes_RMSE * zeroes_RMSE - RMSEs[i]))

    alphas = np.matmul(inv(np.matmul(A.T, A)), ATs)
    print(alphas)
    return alphas

def generate_new_predictions(alphas, A):
    '''
    Use linear coefficients to generate new predictions with a linear blend.

    Writes new predictions to file.
    '''
    with open('./out/probe_blend_(funny2_svd4).dta', 'w+') as new:
        count = 0
        for predictions in A:
            new_val = 0
            for j in range(len(alphas)):
                new_val += alphas[j] * predictions[j]
            if new_val < 1:
                new_val = 1
            elif new_val > 5:
                new_val = 5
            new.write(str(new_val) + '\n')
            count += 1
        print('Count of number of predictions: ', count)


if __name__ == "__main__":
    A, RMSEs = get_data()
    alphas = find_coefficients(A, RMSEs)
    generate_new_predictions(alphas, A)
