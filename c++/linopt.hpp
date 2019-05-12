#pragma once

class LinearRegression {
    LinearRegression(int size) {
        
    }
    void train(const std::vector< std::vector<double> > & x, const std::vector<double> & y) {
        
    }
    double predict(const std::vector<double> & features) {
        
    }
}

class LinOptimizer: public Optimizer {
private:
    double max_eps, min_eps;
    
public:
    LinOptimizer(Lhyra<T, U> * l) {
        max_eps = 0.9;
        min_eps = 0.1;
        lhyra = l;
    }
}