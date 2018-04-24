//
// svd.hh
//
//

#include <vector>
#include <iostream>
#include <string>
#include <random>

#define N_USERS = 458293;
#define N_MOVIES = 17770;
#define N_DAYS = 2243;

using namespace Eigen;

typedef Eigen::SparseMatrix<double> SpMat;
typedef Eigen::Triplet<double> T;
typedef EigenMatrix<double, Dynamic, Dynamic, RowMajor> matrix;
typedef Eigen::Matrix<double, 1, Dynamic> RowVector4i;

class SVD {
  private:
    SpMat &X;
    matrix &U, &V;
    double eta;
    double lambda;
    int n_lfactors;
    std::vector<T> &data;
  //private:
    //double means[];
    //double stdevs[];
    //bool computed_means;
    //bool computed_stdvs;

  public:
    // Constructor
    SVD(SpMat &X, matrix &U, matrix &V, std::vector<T> &data, int n_lfactors);

    // Helper functions for training the model

      // Gradient descent
    void update(std::vector<double> &rowU, std::vector<double> &colV,
                                                  double eta, double lambda);

    double predict(int user, int movie);
    vector<matrix> train(int iterations);
}
