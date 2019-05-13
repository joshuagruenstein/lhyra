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
using Solver = std::function<U(T, std::function<U(T)>)>;

template<typename T>
class FeatureExtractor {
public:
    virtual std::vector<double> operator()(const T & t) = 0;
};

// Early declaration for the compiler
template<typename T, typename U> class Lhyra;

template<typename T, typename U>
class Optimizer {
protected:
    Lhyra<T, U> * lhyra;
public:
    Optimizer(Lhyra<T, U> * l) {
        lhyra = l;
    }
    virtual Solver<T, U> & solver(const std::vector<double> & features) = 0;
};

template<typename T, typename U>
class Lhyra {
private:
    std::vector<Solver<T, U>> solvers;
    DataStore<T> * datastore;
    FeatureExtractor<T> * extractor;
    Optimizer<T, U> * optimizer;
    bool vocal;
public:
    std::vector<double> times;
    
    Lhyra(const std::vector<Solver<T, U>> & s,
              const DataStore<T> * ds,
              const FeatureExtractor<T> * e,
              const Optimizer<T, U> * o):
              solvers(s) {
        optimizer = o;
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
        
        auto features = (*extractor)(data);
        auto solver = optimizer->solver(features);
        auto hook = std::function<U(const T&)>(&operator());
        auto sol = solver(data, hook);
        
        auto t2 = std::chrono::high_resolution_clock::now();
        
        times.push_back(std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1).count());
        
        return sol;
    }
    U vocal_eval(const T & data) {
        vocal = true;
        U answer = (*this)(data);
        vocal = false;
        return answer;
    }
    
};