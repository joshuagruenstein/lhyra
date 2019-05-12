#pragma once

#include "lhyra.hpp"

#include <vector>
#include <array>
#include <fstream>
#include <iostream>

template<unsigned int SIZE>
class LinearRegression {
private:
    std::array<double, SIZE> coeffs;
    double bias;
public:
    LinearRegression() {
        for (int i=0; i<SIZE; i++) coeffs[i] = 0;
        bias = 0;
    }
    
    void train(const std::vector<std::array<double, SIZE>> & xs, const std::vector<double> & ys) {
        // for each x_i in x, get the mean, and sum the squared 
        // difference of each value of x and the mean

        int N = xs.size();
        double y_sum = 0;
        for (int j=0; j<N; j++) y_sum += ys[j];

        std::array<double, SIZE> column_sums;
        std::array<double, SIZE> covariance;
        double sum_of_squares = 0;
        for (int i=0; i<SIZE; i++) {
            
            covariance[i] = 0;

            column_sums[i] = 0;
            
            for (int j=0; j<N; j++) {
                double xij = xs[j][i];
                sum_of_squares += xij*xij;
                column_sums[i] += xij;
                covariance[i] += xij * ys[j];
            }

            sum_of_squares -= column_sums[i]*column_sums[i]/N;
            covariance[i]     -= column_sums[i]*y_sum/N;
        }

        for (int i=0; i<SIZE; i++) coeffs[i] = covariance[i] / sum_of_squares;


        bias = y_sum/N;
        for (int i=0; i<SIZE; i++) bias -= coeffs[i] * column_sums[i]/N;

        // generate coefficients
        std::cout << std::endl << "Coeffs: ";
        for (int i=0; i<SIZE; i++) {
            std::cout << coeffs[i] << ' ';
        }

        // generate y intercepts
        
        std::cout << std::endl << "Bias: " << bias << std::endl;
    }

    double predict(std::array<double, SIZE> features) {
        double result = bias;
        for (int i=0; i<SIZE; i++) result += features[i] * coeffs[i];

        return result;
    }
};

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

    std::cout << l.predict(x[3]) << std::endl;
}
/*
template<typename T, typename U, unsigned int SIZE>
class LinOptimizer: public Optimizer<T, U> {
private:
    double max_eps, min_eps, eps;
    double totaltime;
    std::vector<double> epoch_choices;
    std::vector< std::array<double, SIZE> > epoch_features;
    bool training;
    unsigned int num_solvers;
    
    std::vector<LinearRegression<SIZE>> regr;
    
public:
    LinOptimizer(Lhyra<T, U> * l, double maxeps = 0.9, double mineps = 0.1) {
        max_eps = 0.9;
        min_eps = 0.1;
        eps = max_eps;
        lhyra = l;
        
        num_solvers = l->solveN;        
        regr = std::vector< LinearRegression<SIZE> >();
        regr.reserve(num_solvers)
        for(int i = 0; i < num_solvers; i++) {
            regr.emplace_back(LinearRegression);
        }
        
        training = false;
        totaltime = 0;
    }
    
    void train(int iters, int sample, bool log) {
        training = true;
        
        std::vector<double> totaltimes;
        
        auto features = std::vector< std::vector< std::array<double, SIZE> > >(num_solvers);
        auto times = std::vector< std::vector<double> >(num_solvers);
        
        for(int episode = 0; episode < iters; episode++) {
            totaltimes.push_back(0);
            
            eps = max_eps + (episode/(iters-1))*(min_eps-max_eps);
            
            auto data = lhyra->datastore->get_data(sample);
            for(auto & datum : data) {
                lhyra->eval(datum);
                
                totaltimes.back() += lhyra.times[0];
                
                for(int i = 0; i < epoch_choicN; i++) {
                    features[epoch_choices[i]].push_back(epoch_features[i]);
                    times[epoch_choices[i]].push_back(lhyra->times[i]);
                }
                
                epoch_choices.clear();
                epoch_features.clear();
                lhyra->clear();
            }
            
            for(int i = 0; i < num_solvers; i++) {
                if(!features[i].empty()) {
                    regr[i].train(features[i], times[i]);
                }
            }
            
            totaltimes.back() /= sample;
        }
        
        training = false;
        
        if(log) {        
            auto f = std::ofstream("times.txt");
            
            for(auto& time : totaltimes) {
                f << time << std::endl;
            }
            
            f.close();
        }
    }
    void train() {
        train(100, 40, true);
    }
    
    Solver<T, U> & solver(const std::array<double, SIZE> & features) {
        int action;
        if(training && double(rand()) / RAND_MAX < eps) {
            action = rand() % num_solvers;
        }
        else {
            action = 0;
            double min_cost = regr[0].predict(features);
            for(int i = 1; i < num_solvers; i++) {
                double cost = regr[i].predict(features);
                if(cost < min_cost) {
                    min_cost = cost;
                    action = i;
                }
            }
        }
        
        if(training) {
            epoch_choices.push_back(action);
            epoch_features.push_back(features);
        }
        
        if(lhyra->vocal) {
            std::cout << action << std::endl;
        }
        
        return lhyra->solvers[action]
    }
}
*/