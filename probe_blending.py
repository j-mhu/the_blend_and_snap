# Probe Blending using Linear Regression and given slides
# to optimize alphas (linear coefficients) for quiz

import numpy as np
import math
from numpy.linalg import inv

def get_data():
    '''
    Loads probe and prediction data from desired models for blending.

    Returns matrix A = [A_0, A_1, A_2, ...A_M-1] where A_i is the predictions
    from the ith model on probe.
    '''
    print('Loading probe data...')
    probe = np.loadtxt('../data/um/probe.dta').astype(int)
    probe = np.delete(probe, 2, axis=1)
    print('Done loading probe data.')
    print('Loading probe predictions...')
    models = ['./out/threes.dta', './out/fours.dta']
    # models = ['./out/svd_funny_2.dta', './out/svd++1.dta']
    # models = ['./out/svd_funny_2.dta', './out/svd4.dta']

    for i, model in enumerate(models):
        A_model = np.loadtxt(model).astype(int)
        if i == 0:
            A = [A_model]
        else:
            A = np.append(A, [A_model], axis=0)
    A = A.T
    print('Done loading probe predictions.')
    return A, probe

def find_coefficients(A, probe):
    '''
    Uses simple linear regression to find optimal alphas for blending on probe.

    Returns matrix alphas, the optimal coefficients corresponding to the ith model
    for linear combination.
    '''
    alphas = list(np.dot(np.linalg.pinv(A), probe[:, 2]))
    print('Optimal coefficients: ', alphas)
    return alphas

def generate_new_predictions(alphas, A, probe):
    '''
    Use linear coefficients to generate new predictions with a linear blend.

    Writes new predictions to file.
    '''
    with open('./out/probe_blend_threes_fours.dta', 'w+') as new:
        error = 0
        count = 0
        for i, predictions in enumerate(A):
            new_val = 0
            for j in range(len(alphas)):
                new_val += alphas[j] * predictions[j]
            if new_val < 1:
                new_val = 1
            elif new_val > 5:
                new_val = 5
            error += math.pow((new_val - probe[i][2]), 2)
            new.write(str(new_val) + '\n')
            count += 1
        error /= count
        error = math.pow(error, 0.5)
        print('Count of number of predictions: ', count)
        print('RMSE: ', error)


if __name__ == "__main__":
    A, probe = get_data()
    alphas = find_coefficients(A, probe)
    generate_new_predictions(alphas, A, probe)
