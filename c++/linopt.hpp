#pragma once

#include <ofstream>

template<unsigned int SIZE>
class LinearRegression {
    LinearRegression() {
        
    }
    void train(const std::vector< std::vector<double> > & x, const std::vector<double> & y) {
        
    }
    double predict(const std::vector<double> & features) {
        
    }
}

template<typename T, typename U, unsigned int SIZE>
class LinOptimizer: public Optimizer<T, U> {
private:
    double max_eps, min_eps, eps;
    double totaltime;
    std::vector<double> epoch_choices;
    std::vector< std::array<double, SIZE> > epoch_features;
    bool training;
    unsigned int num_solvers;
    
    std::vector<LinearRegression> regr;
    
public:
    LinOptimizer(Lhyra<T, U> * l, maxeps = 0.9, mineps = 0.1) {
        max_eps = 0.9;
        min_eps = 0.1;
        eps = max_eps;
        lhyra = l;
        
        num_solvers = l->solvers.size()        
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
                
                totaltimes.back() += self.lhyra.times[0];
                
                for(int i = 0; i < epoch_choices.size(); i++) {
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