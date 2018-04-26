#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <sstream>
#include <time.h>
#include "armadillo-8.500.0/include/armadillo"
#include <tuple>

// call as g++ -std=c++0x file.cc -o file

using namespace std;
using namespace arma;

const int N_USERS = 458293;
const int N_MOVIES = 17770;
const int N_DAYS = 2243;

const int BASE_SIZE = 94362233;
const int VALID_SIZE = 1965045;
const int HIDDEN_SIZE = 1964391;
const int PROBE_SIZE = 1374739;
const int QUAL_SIZE = 2749898;
const int ALL_SIZE = 102416306;
const double MU = 3.512599976023349;


/*
    Loads the first n data points from a file and returns the data as a matrix.
    Also takes whether or not the data set is labeled. (`base.dta`, `valid.dta`,
    `hidden.dta`, or `probe.dta` are labeled, `qual.dta` is not.) Also takes
    whether or not the data set is concerning the ratings, or the counts of users
    and movies. (Additional parameters)
*/
mat load_data(string filename, int n, bool labeled = true){
  // Declare array to store data.
  int c = 3 - ((int) !labeled);
  mat Y(n, c);
  // Open the input file.
  ifstream infile;
  infile.open(filename);
  if (!infile) {
    cout << "Unable to open data file" << endl;
    exit(1);
  }
  // Read data from the file line by line.
  int i = 0;
  while (i < n) {
    string line;
    getline(infile, line);
    istringstream lineis(line);
    float row, col, date, rating;
    if (labeled) {
      lineis >> row >> col >> date >> rating;
      Y(i, 0) = row;
      Y(i, 1) = col;
      Y(i, 2) = rating;

    } else {
      lineis >> row >> col >> date;
      Y(i, 0) = row;
      Y(i, 1) = col;
    }
    i++;
  }
  return Y;
}

mat load_counts(string filename, int n) {
    // Declare array to store data.
    mat Y(n, 1);
    // Open the input file.
    ifstream infile;
    infile.open(filename);
    if (!infile) {
        cout << "Unable to open data file" << endl;
        exit(1);  // terminate with error
    }
    // Read data from the file line by line.
    int i = 0;
    while (i < n) {
        string line;
        getline(infile, line);
        istringstream lineis(line);
        float id, count;
        lineis >> id >> count;
        // Y(i,0) = id;
        Y(i,0) = count;
        i++;
    }
    return Y;
}

mat load_biases(string filename, int n, bool forUsers = true){
  // Declare array to store data.
  int c = 2 - ((int) !forUsers);
  mat Y(n, c);
  // Open the input file.
  ifstream infile;
  infile.open(filename);
  if (!infile) {
    cout << "Unable to open data file" << endl;
    exit(1);
  }
  // Read data from the file line by line.
  int i = 0;
  while (i < n) {
    string line;
    getline(infile, line);
    istringstream lineis(line);
    float bias, count;
    if (forUsers) {
      lineis >> bias >> count;
      Y(i, 0) = bias;
      Y(i, 1) = count;

    } else {
      lineis >> bias;
      Y(i, 0) = bias;
    }
    i++;
  }
  return Y;
}

const mat user_biases = load_biases("Numer_user_biases.dta", N_USERS);
const mat movie_biases = load_biases("Numer_movie_biases.dta", N_MOVIES, false);
const mat user_counts = load_counts("user_counts.dta", N_USERS);
const mat movie_counts = load_counts("movie_counts.dta", N_MOVIES);

/*
  Takes as input the index of the movie (movie id - 1), and a regularization
  parameter, and the user bias. Computes the bias term for movie (j + 1).
*/

float bias_movie(int j, float reg1=0.0) {
  return as_scalar(movie_biases(j)) / (reg1 + as_scalar(movie_counts(j)));
}


/*
  Takes as input the index of the movie (movie id - 1), and a regularization
  parameter, and the user bias. Computes the bias term for movie (j + 1).
*/
float bias_user(int i, float reg2=0.0) {
  return as_scalar(user_biases(i)) / (reg2 + as_scalar(user_counts(i)));
}

float bias_factor(int i, float reg3=0.0) {
  return as_scalar(user_counts(i)) / (reg3 + as_scalar(user_counts(i)));
}

/*
    Takes as input a matrix Y of triples (i, j, Y_ij) where i is the index of a
    user, j is the index of a movie, and Y_ij is user i's rating of movie j and
    user/movie matrices U and V.
    Returns the regularized RMSE of predictions made by estimating Y_{ij} as the
    dot product of the ith row of U and the jth column of V^T.
*/

float get_err(mat U, mat V, mat Y, float reg=0.0, float reg1=0.0,
      float reg2=0.0, float reg3=0.0) {
  float err = 0.0;
  // Compute total squared error.
  // cout << "Entered get_err" << endl;
  for (int n = 0; n < Y.n_rows; n++) {
      int i = Y(n,0) - 1;
      int j = Y(n,1) - 1;
      int Yij = Y(n, 2);
      // cout << "Got em, " << j << endl;
      // cout << movie_counts.n_cols << endl;
      float mb = bias_movie(j, reg1);
      // cout << "Got movie bias" << endl;

      float ub = bias_user(i, reg2);
      float f2 = bias_factor(i, reg3);

      // cout << "Got user bias and y-factor" << endl;

      float f1 = 1 / pow(as_scalar(user_counts(i)), 0.5);
      mat Vj = V.col(j);
      // cout << "Got factor 1" << endl;
      float Y_est = MU + ub + mb + dot(Vj, (U.row(i) + f1 * f2));
      // cout << "Got estimate for Yij" << endl;
      err += (0.5 * pow((Yij - Y_est), 2));

      // Add error penalty due to regularization.
      if (reg != 0.0) {
          err += 0.5 * reg * pow(norm(U.row(i), "fro"), 2);
          err += 0.5 * reg * pow(norm(V.col(j), "fro"), 2);
          err += 0.5 * reg * pow(ub, 2);
          err += 0.5 * reg * pow(mb, 2);
      }
  }

  // Return square root of the mean of the regularized error.
  return sqrt(err / Y.n_rows);
}

/*
    Takes as input Ui (the ith row of U), a training point Yij, the column
    vector Vj (the jth column of V), reg (the regularization parameter lambda),
    and eta (the learning rate). Computes the estimated rating with user, item,
    and global bias, and returns the gradient of the regularized loss function
    with respect to Ui, multiplied by eta.
*/
mat grad_U(mat Ui, float Yij, mat Vj, float reg, float eta,
  float reg1, float reg2, float reg3, int i, int j)
{
  float movie_bias = bias_movie(j, reg1);
  float user_bias = bias_user(i, reg2);
  float factor2 = bias_factor(i, reg3);

  float factor1 = 1 / pow(as_scalar(user_counts(i)), 0.5);

  float Y_est = MU + user_bias + movie_bias + dot(Vj, (Ui + factor1 * factor2));
  return (1 - reg * eta) * Ui + eta * Vj.t() * (Yij - Y_est);
}

/*
    Takes as input the column vector Vj (the jth column of V), a training point
    Yij, Ui (the ith row of U), reg (the regularization parameter lambda), and
    eta (the learning rate). Computes the estimated rating with user, item,
    and global bias, and returns the gradient of the regularized loss function
    with respect to Vj, multiplied by eta.
*/
mat grad_V(mat Vj, float Yij, mat Ui, float reg, float eta,
  float reg1, float reg2, float reg3, int i, int j)
{
  float movie_bias = bias_movie(j, reg1);
  float user_bias = bias_user(i, reg2);
  float factor2 = bias_factor(i, reg3);

  float factor1 = 1 / pow(as_scalar(user_counts(i)), 0.5);

  float Y_est = MU + user_bias + movie_bias + dot(Vj, (Ui + factor1 * factor2));

  return Vj * (1 - reg * eta) + eta * Ui.t() * (Yij - Y_est);
}

/*
    Given a training data matrix Y containing rows (i, j, Y_ij)
    where Y_ij is user i's rating on movie j, learns an
    M x K matrix U and N x K matrix V such that rating Y_ij is approximated
    by (UV)_ij.

    Uses a learning rate of <eta> and regularization of <reg>. Stops after
    <max_epochs> epochs, or once the magnitude of the decrease in regularized
    MSE between epochs is smaller than a fraction <eps> of the decrease in
    MSE after the first epoch.

    Returns a tuple (U, V, err) consisting of U, V, and the unregularized MSE
    of the model.
*/
tuple<mat, mat, float> train_model(int M, int N, int K, float eta, float reg,
                float reg1, float reg2, float reg3, mat Y,
                float eps=0.0001, int max_epochs=100)
{
  // Initialize U, V to random numbers.
  arma_rng::set_seed_random(); mat U(M,K); U.randu(); U = U - 0.5;
  arma_rng::set_seed_random(); mat V(K,N); V.randu(); V = V - 0.5;

  int size = Y.n_rows;
  float delta = 0.0;
  ivec indices = conv_to<ivec>::from(linspace(0, size - 1, size));

  for (int epoch = 0; epoch < max_epochs; epoch++) {
    cout << "Getting error" << endl;
    float E_in_before = get_err(U, V, Y, reg, reg1, reg2, reg3);
    // Run an iteration of SGD, shuffling the data points.
    arma_rng::set_seed_random(); indices = shuffle(indices);
    for (int n = 0; n < size; n++) {
      int ndx = indices(n);
      int i = Y(ndx, 0) - 1;
      int j = Y(ndx, 1) - 1;
      int Yij = Y(ndx, 2);
      U.row(i) = grad_U(U.row(i), Yij, V.col(j), reg, eta, reg1, reg2, reg3, i, j);
      V.col(j) = grad_V(V.col(j), Yij, U.row(i), reg, eta, reg1, reg2, reg3, i, j);
    }
    // Get and print the regularized RMSE for each epoch.
    float E_in = get_err(U, V, Y, reg, reg1, reg2, reg3);
    cout << "Epoch " << (epoch + 1) << ", E_in (regularized RMSE): " <<
         E_in << endl;
    // Early stopping condition.
    if (epoch == 0) {
      delta = E_in_before - E_in;
    }
    else if (E_in_before - E_in < eps * delta) break;
  }
  return make_tuple(U, V, get_err(U, V, Y));
}

int main() {
  /***************************** SVD Parameters *****************************/
  int k = 100;        // number of latent factors
  float eta = 0.02;   // learning rate
  float reg = 0.05;    // regularization parameter
  /**************************************************************************/
  float reg1 = 0.01, reg2 = 0.01, reg3 = 0.01;

  clock_t t1, t2;

  // Load data from files.
  t1 = clock();
  mat Y_train = load_data("../um/base.dta", BASE_SIZE);
  mat Y_val = load_data("../um/probe.dta", PROBE_SIZE);
  t2 = clock();
  cout << "Finished loading 'base.dta' and 'probe.dta' in " <<
      ((float) t2 - (float) t1 ) / (60 * CLOCKS_PER_SEC) << " minutes." << endl;

  // Run SVD++ algorithm.
  cout << "Running SVD++ with k = " << k << ", eta = " << eta << ", reg = " <<
      reg << ", reg1 = " << reg1 << ", reg2 = " << ", reg3 = " << reg3 << endl;
  t1 = clock();

  auto svdpp = train_model(N_USERS, N_MOVIES, k, eta, reg, reg1, reg2,
    reg3, Y_train);
  cout << "Finished running SVD++ in " <<
     ((float) t2 - (float) t1) / (60*CLOCKS_PER_SEC) << " minutes." << endl;
  mat U = get<0>(svdpp);
  mat V = get<1>(svdpp);
  float err = get<2>(svdpp);
  cout << "Training RMSE = " << err << endl;

  // Get validation error.
  float err_val = get_err(U, V, Y_val);
  float percent = (0.9514 - err_val) / 0.9514 * 100;
  printf("Validation RMSE = %.5f (%.3f%% above water\n)", err_val, percent);

  // Make predictions on 'qual' set and write to file.
  t1 = clock();
  mat Y_qual = load_data("../um/qual.dta", QUAL_SIZE, false);
  ofstream outfile;
  outfile.open("out/svd++1.dta");
  for (int n = 0; n < QUAL_SIZE; n++) {
    int i = Y_qual(n, 0) - 1;
    int j = Y_qual(n, 1) - 1;
    mat Vj = V.col(j);
    float movie_bias = bias_movie(j, reg1);
    float user_bias = bias_user(i, reg2);
    float factor2 = bias_factor(i, reg3);
    float factor1 = 1 / pow(as_scalar(user_counts(i)), 0.5);
    float predict = MU + user_bias + movie_bias + dot(Vj, (U.row(i) + factor1 * factor2));

    if (predict < 1.0) {
      predict = 1.0;
    } else if (predict > 5.0) {
      predict = 5.0;
    }
    outfile << setprecision(5) << predict << endl;
  }
  outfile.close();
  t2 = clock();
  cout << "Finished calculating and writing 'qual' predictions in " <<
    ((float) t2 - (float) t1) / (60*CLOCKS_PER_SEC) << " minutes." << endl;

  return 0;
}
