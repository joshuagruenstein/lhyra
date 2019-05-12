#pragma once

#include <vector>
#include <array>


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
    void train(const std::vector<double*> & xs, const std::vector<double> & ys) {
        // for each x_i in x, get the mean, and sum the squared 
        // difference of each value of x and the mean

        std::array<double, SIZE> sum_of_squares;
        std::array<double, SIZE> xs_sums;
        for (int i=0; i<SIZE; i++) {
            double xi_squared_sum = 0;
            xs_sums[i] = 0;
            
            for (int j=0; j<xs.size(); j++) {
                double xij = xs[j][i];
                xi_squared_sum += xij*xij;
                xs_sums[i] += xij;
            }

            sum_of_squares[i] = xi_squared_sum - xs_sums[i]*xs_sums[i]/SIZE;
        }

        double ys_sum = 0;
        for (int j=0; j<ys.size(); j++) {
            ys_sum += ys[j];
        }

        // generate covariances
        std::array<double, SIZE> covariances;
        for (int i=0; i<SIZE; i++) {
            covariances[i] = 0;

            double column_avg = 0;
            for (int j=0; j<ys.size(); j++) {
                column_avg += xs[j][i];
                covariances += xs[j][i] * ys[j];
            }

            column_avg /= xs.size();
            covariances[i] -= ys_sum*column_avg;
        }

        // generate coefficients
        for (int i=0; i<SIZE; i++) coeffs[i] = covariances[i] / sum_of_squares[i];

        // generate y intercepts
        bias = ys_sum/ys.size();
        for (int i=0; i<SIZE; i++) bias -= coeffs[i] * xs_sums[i];
    }

    double predict(double* features) {
        double result = bias;
        for (int i=0; i<SIZE; i++) result += features[i] * coeffs[i];

        return result;
    }
};

template<unsigned int SIZE>
class LinOptimizer: public Optimizer {
private:
    double max_eps, min_eps;
    
    std::vector<LinearRegression> regr;
    
public:
    LinOptimizer(Lhyra<T, U> * l, maxeps = 0.9, mineps = 0.1) {
        max_eps = 0.9;
        min_eps = 0.1;
        lhyra = l;
        
        size = std::vector<size>
        regr = std::vector
    }
}