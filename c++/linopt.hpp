#pragma once

#include "lhyra.hpp"

#include <gsl/gsl_matrix.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_multifit.h>

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

    void train(const std::vector< std::array<double, SIZE> > & xs, const std::vector<double> & ys) {
        // for each x_i in x, get the mean, and sum the squared 
        // difference of each value of x and the mean

        gsl_matrix *X = gsl_matrix_calloc(xs.size(), SIZE+1);
        gsl_vector *Y = gsl_vector_alloc(ys.size());
        gsl_vector *beta = gsl_vector_alloc(SIZE+1);

        for (int i=0; i<xs.size(); i++) {
            for (int j=0; j<SIZE; j++) gsl_matrix_set(X,i,j,xs[i][j]);
            gsl_matrix_set(X, i,SIZE,1);
            gsl_vector_set(Y, i, ys[i]);
        }

        double chisq;
        gsl_matrix *cov = gsl_matrix_alloc(SIZE+1, SIZE+1);
        gsl_multifit_linear_workspace * wspc = gsl_multifit_linear_alloc(xs.size(), SIZE+1);
        gsl_multifit_linear(X, Y, beta, cov, &chisq, wspc);

        for (int i=0; i<SIZE; i++) coeffs[i] = gsl_vector_get(beta, i);
        bias = gsl_vector_get(beta,SIZE);

        gsl_matrix_free(X);
        gsl_matrix_free(cov);
        gsl_vector_free(Y);
        gsl_vector_free(beta);
        gsl_multifit_linear_free(wspc);
    }

    double predict(std::array<double, SIZE> features) {
        double result = bias;
        for (int i=0; i<SIZE; i++) result += features[i] * coeffs[i];

        return result;
    }

    void pretty_print(std::ostream & o) {
        o << "[Coeffs=<";
        for(int i = 0; i < SIZE; i++) o << coeffs[i] << ',';
        o << ">; Bias=" << bias << ']';
    }
};

template<typename T, typename U, unsigned int SIZE>
class LinOptimizer: public Optimizer<T, U, SIZE> {
private:
    double max_eps, min_eps, eps;
    double totaltime;
    std::vector<int> epoch_choices;
    std::vector< std::array<double, SIZE> > epoch_features;
    bool training;
    unsigned int num_solvers;
    
public:
    std::vector<LinearRegression<SIZE>> regr; // Exposing temporarily to get coeffs.
    
    LinOptimizer(): Optimizer<T, U, SIZE>() {
        max_eps = 0.9;
        min_eps = 0.1;
    }

    void init() {
        
        num_solvers = this->lhyra->solvers.size();        
        regr = std::vector< LinearRegression<SIZE> >();
        regr.reserve(num_solvers);
        for(int i = 0; i < num_solvers; i++) {
            regr.emplace_back(LinearRegression<SIZE>());
        }
        
        training = false;
        totaltime = 0;

        eps = max_eps;
    }
    
    void train(int iters, int sample, bool log) {
        training = true;
        
        std::vector<double> totaltimes;
        
        auto features = std::vector< std::vector< std::array<double, SIZE> > >(num_solvers);
        auto times = std::vector< std::vector<double> >(num_solvers);
        
        //std::cout << "Checkpoint 1.2" << std::endl;
        for(int episode = 0; episode < iters; episode++) {
            totaltimes.push_back(0);
            
            eps = max_eps + (episode/(iters-1))*(min_eps-max_eps);
            
            auto data = this->lhyra->datastore->get_data(sample);
            //std::cout << "Checkpoint 1.3" << std::endl;
            for(T & datum : data) {
                (*(this->lhyra))(datum);
                //std::cout << "Checkpoint 1.4" << std::endl;
                
                totaltimes.back() += this->lhyra->times[0];
                
                for(int i = 0; i < epoch_choices.size(); i++) {
                    features[epoch_choices[i]].push_back(epoch_features[i]);
                    times[epoch_choices[i]].push_back(this->lhyra->times[i]);
                }
                
                epoch_choices.clear();
                epoch_features.clear();
                this->lhyra->clear();
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

            f << std::fixed;
            
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
        
        if(this->lhyra->vocal) {
            std::cout << action << std::endl;
        }
        
        return this->lhyra->solvers[action];
    }
};