#pragma once

#include <vector>
#include <functional>
#include <chrono>

template<typename T>
class DataStore {
public:
    virtual std::vector<T> get_data(int batch_size) = 0;
};

template<typename T>
class DataGenerator: public DataStore<T> {
private:
    std::function<T()> method;
public:    
    DataGenerator(const std::function<T()> & m) {
        method = m;
    }
    std::vector<T> get_data(int batch_size) {
        std::vector<T> data;
        data.reserve(batch_size);
        for(int i = 0; i < batch_size; i++) {
            data.emplace_back(method());
        }
        return data;
    }
};

/*
template<typename T, typename U>
class Solver {
public:
    //std::function<U(T)> hook
    //virtual Solver(const std::function<U(T)> & h) {
    //    hook = h;
    //}
    virtual U operator()(const T & t) = 0;
}*/

template<typename T, typename U>
using Solver = std::function<U(const T &, std::function<U(const T &)> &)>;

template<typename T, unsigned int SIZE>
class FeatureExtractor {
public:
    virtual std::array<double, SIZE> operator()(const T & t) = 0;
};

// Early declaration for the compiler
template<typename T, typename U, unsigned int SIZE> class Lhyra;

/*
When subclassing Optimizer, Constructor should be basically blank.
Instead, use init(), which is called by Lhyra, to do initializaiton.
*/
template<typename T, typename U, unsigned int SIZE>
class Optimizer {
protected:
    Lhyra<T, U, SIZE> * lhyra;
public:
    Optimizer() { lhyra = NULL; }
    void set_lhyra(Lhyra<T, U, SIZE> * l) {
        lhyra = l;
        init();
    }
    virtual void init() = 0;
    virtual Solver<T, U> & solver(const std::array<double, SIZE> & features) = 0;
};

// For debugging:
#include <iostream>
// End

template<typename T, typename U, unsigned int SIZE>
class Lhyra {
private:
    FeatureExtractor<T, SIZE> * extractor;
    Optimizer<T, U, SIZE> * optimizer;
public:
    // The optimizer needs to see these:
    DataStore<T> * datastore;
    std::vector<Solver<T, U>> solvers;
    bool vocal;
    std::vector<double> times;
    
    Lhyra(std::vector<Solver<T, U>> & s,
              DataStore<T> * ds,
              FeatureExtractor<T, SIZE> * e,
              Optimizer<T, U, SIZE> * o):
              solvers(s) {
        optimizer = o;
        optimizer->set_lhyra(this);
        extractor = e;
        datastore = ds;
        vocal = false;
        clear();
    }
    void clear() {
        times.clear();
        // C++ doesn't specify if it reallocates, but we'd like it not to.
    }
    U operator()(const T & data) {
        
        auto t1 = std::chrono::high_resolution_clock::now();
        
        //std::cout << "Checkpoint 5.1" << std::endl;
        auto features = (*extractor)(data);
        //std::cout << "Checkpoint 5.2" << std::endl;
        auto solver = optimizer->solver(features);
        //std::cout << "Checkpoint 5.3" << std::endl;
        std::function<U(const T&)> hook = std::bind(*this, std::placeholders::_1);
        auto sol = solver(data, hook);
        
        auto t2 = std::chrono::high_resolution_clock::now();
        
        times.push_back(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count());
        //std::cout << times.back() << std::endl;
        
        return sol;
    }
    U vocal_eval(const T & data) {
        vocal = true;
        U answer = (*this)(data);
        vocal = false;
        return answer;
    }
    static U static_eval(Lhyra & lhyra, const T & data) {
        return lhyra(data);
    }
};