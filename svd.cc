//
// svd.cc
//
//

#include "Eigen/Sparse"
#include <vector>
#include <iostream>
#include <string>
#include "math.h"
#include <random>
#include svd.hh

using namespace Eigen;

SVD::SVD(SpMat &X, matrix &U, matrix &V, std::vector<T> &data, int n_lfactors)
{
  double r = ((double) rand() / RAND_MAX) + 1)
  n_lfactors = n_lfactors;
  lambda = 0.01;
  eta = 0.2;
  U = MatrixXd::Constant(X.rows(), n_lfactors, r);
  V = MatrixXd::Constant(X.cols(), n_lfactors, r);
}

double SVD::predict(int user, int movie) {
  return U.row(user).dot(V.row(movie))
}

void SVD::update(int i, int j, T &datum) {
  double t = U.row(i).dot(V.col(j));
  U.row(i) -= (lambda * U.row(i) - (datum.value() - t * V.col(j))) * eta;
  V.row(j) -= (lambda * V.col(j) - (datum.value() - t * U.row(i))) * eta;
}

double SVD::error(matrix &U, matrix&V, vector<T> &data) {
  double err = (lambda / 2) * (U.squaredNorm() + V.squaredNorm());
  int user, movie;
  for (std::vector<T>::iterator it = data.begin(); it != data.end(); it++) {
    user = *it.row(), movie = *it.col();
    err += (0.5) * (*it.value() - this->predict(user, movie))**2 //- dot product );
  }
  return err / data.size();
}
