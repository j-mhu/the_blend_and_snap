import numpy

print('Loading qual set...')
Y_test = numpy.loadtxt('../data/um/qual.dta').astype(int)
print('Done loading qual set.')
Y_test = numpy.delete(Y_test, 2, axis=1)
print(Y_test.shape)

with open('./out/zeroes.dta','w+') as results:
    zeroes = 0
    for line in Y_test:
        zeroes += 1
        results.write("0\n")

print(zeroes)
