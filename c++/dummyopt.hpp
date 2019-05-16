#pragma once

#include "lhyra.hpp"

template<typename T, typename U, unsigned int SIZE>
class DummyOptimizer: public Optimizer<T, U, SIZE> {
public:
	DummyOptimizer(): Optimizer<T, U, SIZE>() {}
	void init() {}
	Solver<T, U, SIZE> & solver(const std::array<double, SIZE> & features) {
        return this->lhyra->solvers[0];
	}
};