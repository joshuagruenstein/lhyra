#pragma once

template<unsigned int SIZE>
class LinearRegression {
    LinearRegression() {
        
    }
    void train(const std::vector< std::vector<double> > & x, const std::vector<double> & y) {
        
    }
    double predict(const std::vector<double> & features) {
        
    }
}

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