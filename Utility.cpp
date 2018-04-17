#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <sstream>

const int N_USERS = 458293;  // total number of users
const int N_MOVIES = 17770;  // total number of movies
const int N_DATES = 2243;    // date number is between 1 and 2243 (in days)

const int BASE_SIZE = 94362233;
const int VALID_SIZE = 1965045;
const int HIDDEN_SIZE = 1964391;
const int PROBE_SIZE = 1374739;
const int QUAL_SIZE = 2749898;
const int ALL_SIZE = 102416306;

namespace Utility {
    void load(int **base, int **valid, int **hidden, int **probe, int **qual,
                std::string order = "um") {
        // Allocate array for `base` set.
        base = new int*[BASE_SIZE];
        for (int i = 0; i < BASE_SIZE; i++) {
            base[i] = new int[4];
        }
        // Allocate array for `valid` set.
        valid = new int*[VALID_SIZE];
        for (int i = 0; i < VALID_SIZE; i++) {
            valid[i] = new int[4];
        }
        // Allocate array for `hidden` set.
        hidden = new int*[HIDDEN_SIZE];
        for (int i = 0; i < HIDDEN_SIZE; i++) {
            hidden[i] = new int[4];
        }
        // Allocate array for `probe` set.
        probe = new int*[PROBE_SIZE];
        for (int i = 0; i < PROBE_SIZE; i++) {
            probe[i] = new int[3];
        }
        // Allocate array for `qual` set.
        qual = new int*[QUAL_SIZE];
        for (int i = 0; i < QUAL_SIZE; i++) {
            qual[i] = new int[3];
        }

        // Open the files `all.dta` and `all.idx` using order `mu` or `um`.
        std::ifstream inFileDta;
        std::ifstream inFileIdx;
        if (order.compare("mu") == 0) {
            inFileDta.open("../data/mu/all.dta");
            inFileIdx.open("../data/mu/all.idx");
        } else if (order.compare("um") == 0) {
            inFileDta.open("../data/um/all.dta");
            inFileIdx.open("../data/um/all.idx");
        } else {
            throw std::invalid_argument("input argument must be `mu` or `um`");
        }

        if (!inFileDta) {
            std::cout << "Unable to open " << "all.dta" << std::endl;
            exit(1);  // terminate with error
        }
        if (!inFileIdx) {
            std::cout << "Unable to open " << "all.idx" << std::endl;
            exit(1);  // terminate with error
        }

        // Read data from files.
        int x, i1 = 0, i2 = 0, i3 = 0, i4 = 0, i5 = 0;
        while (inFileIdx >> x) {
            std::string data;
            std::getline(inFileDta, data);
            std::istringstream datais(data);
            int n, j = 0;

            if (x == 1) {
                while (datais >> n) {
                    base[i1][j++] = n;
                }
                i1++;
            } else if (x == 2) {
                while (datais >> n) {
                    valid[i2][j++] = n;
                }
                i2++;
            } else if (x == 3) {
                while (datais >> n) {
                    hidden[i3][j++] = n;
                }
                i3++;
            } else if (x == 4) {
                while (datais >> n) {
                    probe[i4][j++] = n;
                }
                i4++;
            } else if (x == 5) {
                while (datais >> n) {
                    qual[i5][j++] = n;
                }
                i5++;
            }
        }
        inFileDta.close();
        inFileIdx.close();

        // Print the last element of each array.
        std::cout << base[BASE_SIZE-1][3] << std::endl;
        std::cout << valid[VALID_SIZE-1][3] << std::endl;
        std::cout << hidden[HIDDEN_SIZE-1][3] << std::endl;
        std::cout << probe[PROBE_SIZE-1][2] << std::endl;
        std::cout << qual[QUAL_SIZE-1][2] << std::endl;
    }

    void free(int **base, int **valid, int **hidden, int **probe, int **qual) {
        // Delete array for `base` set.
        for (int i = 0; i < BASE_SIZE; i++) {
            delete[] base[i];
        }
        delete[] base;
        // Delete array for `valid` set.
        for (int i = 0; i < VALID_SIZE; i++) {
            delete[] valid[i];
        }
        delete[] valid;
        // Delete array for `hidden` set.
        for (int i = 0; i < HIDDEN_SIZE; i++) {
            delete[] hidden[i];
        }
        delete[] hidden;
        // Delete array for `probe` set.
        for (int i = 0; i < PROBE_SIZE; i++) {
            delete[] probe[i];
        }
        delete[] probe;
        // Delete array for `qual` set.
        for (int i = 0; i < QUAL_SIZE; i++) {
            delete[] qual[i];
        }
        delete[] qual;
    }
}


int main() {
    int **base, **valid, **hidden, **probe, **qual;
    Utility::load(base, valid, hidden, probe, qual);

    std::cout << "back in main" << std::endl;

    // Print. This is where things start going wrong !!! :)))
    std::cout << base[BASE_SIZE-1][3] << std::endl;
    std::cout << valid[VALID_SIZE-1][3] << std::endl;
    std::cout << hidden[HIDDEN_SIZE-1][3] << std::endl;
    std::cout << probe[PROBE_SIZE-1][2] << std::endl;
    std::cout << qual[QUAL_SIZE-1][2] << std::endl;

    Utility::free(base, valid, hidden, probe, qual);

    return 0;
}
