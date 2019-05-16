#include "lhyra.hpp"
#include "linopt.hpp"
#include "dummyopt.hpp"
#include "sorting.hpp"

#include <vector>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <algorithm>


// Data generator for sorting. Yes, you modify the globals to change the behavior. Sorry.
int LIST_LENGTH = 1000;
double NEARLY_SORTED = 0;
void shuffle_slice(std::vector<double> & a, int start, int stop) {
	int i = start;
	while(i < stop-1) {
		int idx = rand() % (1+stop-i) + i;
		double temp = a[i];
		a[i] = a[idx];
		a[idx] = temp;
		i++;
	}
}
std::vector<double> random_list() {
	std::vector<double> list;
	list.reserve(LIST_LENGTH);
	for(int i = 0; i < LIST_LENGTH; i++) {
		list.emplace_back(i);
	}
	if(double(rand()) / RAND_MAX < NEARLY_SORTED) {
		// Create 8 sections of length 5 which are shuffled:
		for(int i = 0; i < 8; i++) {
			int start = rand() % (LIST_LENGTH-5);
			shuffle_slice(list, start, start+5);
		}
	}
	else shuffle_slice(list, 0, LIST_LENGTH-1);
	return list;
}

// Feature extractor for sorting
class SortFeatureExtractor: public FeatureExtractor<std::vector<double>, FEATURE_SIZE> {
public:
	SortFeatureExtractor(){}

	double random_sorted(const std::vector<double> & data, int num_pts) {
		std::vector<int> pts;
		pts.reserve(num_pts);
		for(int i = 0; i < num_pts; i++) pts.emplace_back(rand() % data.size());
		// Insertion sort pts
		for(int i = 0; i < num_pts-1; i++) for(int j = i; j >= 0 && pts[j+1] < pts[j]; j--) {
			int temp = pts[j];
			pts[j] = pts[j+1];
			pts[j+1] = temp;
		}
		// Confirm that samples are in order.
		for(int i = 1; i < num_pts; i++) {
			//std::cout << pts[i-1] << ' ' << pts[i] << "        ";
			//std::cout.flush();
			//std::cout << data[pts[i-1]] << ' ' << data[pts[i]] << std::endl;
			if(data[pts[i]] < data[pts[i-1]]) return 0;
		}
		return 1;
	}

	std::array<double, FEATURE_SIZE> operator()(const std::vector<double> & data) {
		std::array<double, FEATURE_SIZE> features;
		double is_sorted = data.size() > 1 ? random_sorted(data, 10) : 1; // 1/1024 odds of mistake
		features[0] = data.size();
		features[1] = data.size()*data.size();
		features[2] = is_sorted;
		features[3] = is_sorted*data.size();
		return features;
	}
};


/* FOR TESTING LHYRA:

Order of initialization:

1. Create datastore
2. Create feature extractor
3. Create optimizer<in_type, out_type, extractor.size>
4. Create LHYRA

*/


int main() {

	srand(1); // Repeatability

	//std::function<std::vector<double>(std::vector<double>,
	//	std::function<std::vector<double>(std::vector<double>)>)> s = foo;


	// Create vector of solvers:

	std::vector<Solver<std::vector<double>, std::vector<double>, FEATURE_SIZE>> solvers;
	solvers.push_back(&merge_sort);
	solvers.push_back(&insertion_sort);
	solvers.push_back(&quick_sort);

	// Create data generator
	DataGenerator<std::vector<double>> dg{random_list};

	// Create feature extractor
	SortFeatureExtractor sfg;

	// Test feature extractor
	/*
	auto test_data = dg.get_data(1)[0];
	std::array<double, 3> features = sfg(test_data);
	std::cout << features[0] << ' ' << features[1] << ' ' << features[2] << std::endl;
	*/

	// Create optimizer
	LinOptimizer<std::vector<double>, std::vector<double>, FEATURE_SIZE> linopt{};

	Lhyra<std::vector<double>, std::vector<double>, FEATURE_SIZE> lhyra {
		solvers,
		&dg,
		&sfg,
		&linopt
	};

	//std::cout << "Checkpoint 1" << std::endl;

	linopt.train(200, 40, true);

	//std::cout << "Checkpoint " << std::endl;

	for(int i = 0; i < 3; i++) {
		linopt.regr[i].pretty_print(std::cout);
		std::cout << std::endl;
	}

	const int NUM_DATA = 100;

	std::ofstream f("data.txt");

	// Create Lhyras for merge, insertion, and quick sort.
	std::vector<Solver<std::vector<double>, std::vector<double>, FEATURE_SIZE>> merge_solvers;
	std::vector<Solver<std::vector<double>, std::vector<double>, FEATURE_SIZE>> insert_solvers;
	std::vector<Solver<std::vector<double>, std::vector<double>, FEATURE_SIZE>> quick_solvers;
	merge_solvers.push_back(&merge_sort);
	insert_solvers.push_back(&insertion_sort);
	quick_solvers.push_back(&quick_sort);

	DummyOptimizer<std::vector<double>, std::vector<double>, FEATURE_SIZE> merge_opt;
	DummyOptimizer<std::vector<double>, std::vector<double>, FEATURE_SIZE> insert_opt;
	DummyOptimizer<std::vector<double>, std::vector<double>, FEATURE_SIZE> quick_opt;

	Lhyra<std::vector<double>, std::vector<double>, FEATURE_SIZE> merge_lhyra {
		merge_solvers,
		&dg,
		&sfg,
		&merge_opt
	};
	Lhyra<std::vector<double>, std::vector<double>, FEATURE_SIZE> insert_lhyra {
		insert_solvers,
		&dg,
		&sfg,
		&insert_opt
	};
	Lhyra<std::vector<double>, std::vector<double>, FEATURE_SIZE> quick_lhyra {
		quick_solvers,
		&dg,
		&sfg,
		&quick_opt
	};


	for(LIST_LENGTH = 16; LIST_LENGTH <= 4096; LIST_LENGTH *= 2) {

		std::cout << "Starting list of length " << LIST_LENGTH << std::endl;

		auto test_data = dg.get_data(NUM_DATA);
	    auto t1 = std::chrono::high_resolution_clock::now();
		for(int i = 0; i < NUM_DATA; i++) {
			lhyra(test_data[i]);
		}
	    auto t2 = std::chrono::high_resolution_clock::now();
		for(int i = 0; i < NUM_DATA; i++) {
			merge_lhyra(test_data[i]);
		}
	    auto t3 = std::chrono::high_resolution_clock::now();
		for(int i = 0; i < NUM_DATA; i++) {
			insert_lhyra(test_data[i]); // Doesn't matter anyway
		}
	    auto t4 = std::chrono::high_resolution_clock::now();
		for(int i = 0; i < NUM_DATA; i++) {
			quick_lhyra(test_data[i]);
		}
	    auto t5 = std::chrono::high_resolution_clock::now();
		for(int i = 0; i < NUM_DATA; i++) {
			std::vector<double> test_data_copy = test_data[i];
			std::sort(test_data_copy.begin(), test_data_copy.end());
		}
	    auto t6 = std::chrono::high_resolution_clock::now();

	    f << LIST_LENGTH << ' ';
	    f << std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count() << ' ';
	    f << std::chrono::duration_cast<std::chrono::microseconds>(t3 - t2).count() << ' ';
	    f << std::chrono::duration_cast<std::chrono::microseconds>(t4 - t3).count() << ' ';
	    f << std::chrono::duration_cast<std::chrono::microseconds>(t5 - t4).count() << ' ';
	    f << std::chrono::duration_cast<std::chrono::microseconds>(t6 - t5).count() << std::endl;
	}

	f.close();


    /*
    std::cout << "Lhyra: " << std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count() << std::endl;
    std::cout << "Merge: " << std::chrono::duration_cast<std::chrono::microseconds>(t3 - t2).count() << std::endl;
    std::cout << "Insert: " << std::chrono::duration_cast<std::chrono::microseconds>(t4 - t3).count() << std::endl;
    std::cout << "Quick: " << std::chrono::duration_cast<std::chrono::microseconds>(t5 - t4).count() << std::endl;
    */
}