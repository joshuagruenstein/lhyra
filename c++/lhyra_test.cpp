#include "lhyra.hpp"

#include <stdlib.h>
#include <time.h>
#include <iostream>

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