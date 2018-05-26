# Probe Blending using Linear Regression and given slides
# to optimize alphas (linear coefficients) for RMSE

import numpy as np
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def get_data():
    '''
    Loads probe and prediction data from desired models for blending.

    Returns matrix A = [A_0, A_1, A_2, ...A_M-1] where A_i is the predictions
    from the ith model on probe, and the results from probe data.
    '''
    print('Loading probe data...')
    probe = np.loadtxt('../data/um/probe.dta').astype(int)
    probe = np.delete(probe, 2, axis=1)

    print('Done loading probe data.')
    print('Loading probe predictions...')

    models = ['./out/svd_funny3_probe.dta', './out/NN2_probe_fixed.dta']


    for i, model in enumerate(models):
        A_model = np.loadtxt(model).astype(int)
        if len(probe) != len(A_model):
    	    print('Warning: number of predictions is not the same as size of probe')
        if i == 0:
            A = [A_model]
        else:
            A = np.append(A, [A_model], axis=0)

    A = A.T
    print('Done loading probe predictions.')
    return A, probe[:, 2]


def find_coefficients(A, probe):
    '''
    Uses simple linear regression to find optimal alphas for blending on probe.

    Returns matrix alphas, the optimal coefficients corresponding to the ith model
    for linear combination.
    '''
	# Create linear regression object
    regr = LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)

	# Train the model using the training sets
    regr.fit(A, probe)

    alphas = regr.coef_
    intercept = regr.intercept_
    print('Optimal coefficients: ', alphas)
    print('Intercept: ', intercept)
    return alphas, intercept

def generate_new_predictions(alphas, intercept, A, probe):
    '''
    Use linear coefficients to generate new predictions with a linear blend.

    Writes new predictions to file.
    '''
    with open('./out/probe_blend4_svdf3NN2.dta', 'w+') as new:
        prediction_vals = []
        for i, predictions in enumerate(A):

            new_val = intercept

            # Multiply coefficients by predictions
            for j in range(len(alphas)):
                new_val += alphas[j] * predictions[j]

            # Manually clamp results to be between 1 and 5
            if new_val < 1:
                new_val = 1
            elif new_val > 5:
                new_val = 5

            prediction_vals.append(new_val)
            # Write value to document
            new.write(str(new_val) + '\n')

        print('RMSE: ', math.pow(mean_squared_error(probe, prediction_vals), 0.5))


if __name__ == "__main__":
    A, probe = get_data()
    alphas, intercept = find_coefficients(A, probe)
    generate_new_predictions(alphas, intercept, A, probe)
