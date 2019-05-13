#include "lhyra.hpp"
#include "linopt.hpp"

#include <stdlib.h>
#include <time.h>
#include <iostream>

/* FOR TESTING LHYRA:

Order of initialization:

1. Create datastore
2. Create feature extractor
3. Create optimizer<in_type, out_type, extractor.size>
4. Create LHYRA


*/

constexpr int LIST_SIZE = 4;

struct random_list {
    std::vector<double> operator()() {
        std::vector<double> answer;
        for(int i = 0; i < LIST_SIZE; i++) {
            answer.emplace_back(double(rand()) / RAND_MAX);
        }
        return answer;
    }
};

//*

#include <stdlib.h>
#include <time.h>
int main() {
    auto l = LinearRegression<2>();
    srand(0);

    auto x = std::vector < std::array<double, 2> >(4);
    for(int i = 0; i < 4; i++) {
        for(int j = 0; j < 2; j++) {
            x[i][j] = rand()%11;
            std::cout << x[i][j] << ' ';
        }
        std::cout << std::endl;
    }

    auto y = std::vector<double>(4);
    for(int i = 0; i < 4; i++) {
        y[i] = rand()%4;
        std::cout << y[i] << ' ';
    }

    l.train(x, y);
    std::cout << std::endl;

    std::cout << l.predict(x[0]) << std::endl;
}
//*/

/*
int main() {
    srand(time(NULL));
    
    auto d = DataGenerator< std::vector<double> >(random_list());
    
    auto data = d.get_data(8);
    for(int a = 0; a < 8; a++) {
        for(int b = 0; b < LIST_SIZE; b++) {
            std::cout << data[a][b] << ' ';
        }
        std::cout << std::endl;
    }
}
//*/