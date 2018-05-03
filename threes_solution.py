import numpy
import math

print('Loading probe set...')
Y_test = numpy.loadtxt('../data/um/probe.dta').astype(int)
print('Done loading probe set.')
Y_test = numpy.delete(Y_test, 2, axis=1)
print(Y_test.shape)

with open('./out/threes.dta','w+') as results:
    error = 0
    threes = 0
    for line in Y_test:
        threes += 1
        results.write("3\n")
        error += math.pow((line[2] - 3), 2)

error /= threes
error = math.pow(error, 0.5)
print(threes)
print('RMSE: ', error)
