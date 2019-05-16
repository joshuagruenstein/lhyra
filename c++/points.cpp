#include <vector>
#include <iostream>
#include <cmath>
#include <limits>
#include <stdlib.h>
#include <algorithm>

#include "lhyra.hpp"
#include "linopt.hpp"
#include "dummyopt.hpp"

struct Point {
	double x;
	double y;
};

double point_dist(Point p1, Point p2) {
	return sqrt(pow(p1.x - p2.x,2) + pow(p1.y - p2.y,2));
}

double point_dist(std::pair<Point, Point> points) {
	return point_dist(points.first, points.second);
}

std::pair<Point, Point> points_brute(const std::vector<Point> & points,
	Lhyra<std::vector<Point>, std::pair<Point, Point>, 1> & lhyra) {
	//std::cout << "Brute solver; size=" << points.size() << std::endl;
	double min_dist =  std::numeric_limits<double>::max();
	std::pair<Point, Point> closest_pair;

	for (int i=0; i<points.size(); i++) {
		//std::cout << "Boop" << std::endl;
		for (int j=i+1; j<points.size(); j++) {
			auto pair = std::pair<Point,Point>(points[i],points[j]);
			if (point_dist(pair) < min_dist) {
				min_dist = point_dist(pair);
				closest_pair = pair;
			}
		}
	}
	//std::cout << "Leaving brute solver" << std::endl;

	return closest_pair;
}

std::pair<Point, Point> points_smart(const std::vector<Point> & points,
	Lhyra<std::vector<Point>, std::pair<Point, Point>, 1> & lhyra) {
	// std::cout << "Smart solver" << std::endl;
	if (points.size() <= 3) return points_brute(points, lhyra);


	auto psorted = std::vector<Point>(points);
	std::sort(psorted.begin(), psorted.end(), [](const auto& l, const auto& r) {
		return l.x < r.x;
	});

	int halfway = psorted.size()/2;
	auto left = lhyra(std::vector<Point>(psorted.begin(), psorted.begin()+halfway));
	auto right = lhyra(std::vector<Point>(psorted.begin()+halfway, psorted.begin()+psorted.size()));
	
	double mid = psorted[halfway].x;
	double dleft = point_dist(left), dright = point_dist(right);
	double d = std::min(dleft,dright);

	auto strip = std::vector<Point>();

	for (const auto& p : points) if (point_dist(p, {mid, p.y}) <= d) strip.push_back(p);

	std::sort(strip.begin(), strip.end(), [](const auto& l, const auto& r) {
		return l.y < r.y;
	});

	double min_dist = d;
	std::pair<Point, Point> closest_pair;
	bool found_closer = false;

	for	(int i=0; i<strip.size(); i++) {
		for (int j=i+1; j<std::min((int) strip.size(), i+8); j++) {
			if (point_dist(strip[i],strip[j]) < min_dist) {
				min_dist = point_dist(strip[i],strip[j]);
				closest_pair = std::pair<Point, Point>(strip[i],strip[j]);
				found_closer = true;
			}
		}
	}

	if (!found_closer) return dleft < dright ? left : right;

	return closest_pair;
}

// tests and stuff

double doublerand() {
    return (double) rand() / RAND_MAX;
}

int LIST_LENGTH = 1000;
std::vector<Point> random_list() {
	std::vector<Point> answer;
	answer.reserve(LIST_LENGTH);
	for (int i = 0; i < LIST_LENGTH; ++i) {
		answer.push_back({doublerand(), doublerand()});
	}
	return answer;
}

class PointFeatureExtractor: public FeatureExtractor<std::vector<Point>, 1> {
public:
	PointFeatureExtractor() {}
	std::array<double, 1> operator()(const std::vector<Point> & t) {
		return {t.size()}; //std::array<double, 1>
	}
};

int main() {
	srand(0);

	std::vector<Solver<std::vector<Point>, std::pair<Point, Point>, 1>> solvers;
	solvers.push_back(&points_brute);
	solvers.push_back(&points_smart);
	// Create data generator
	DataGenerator<std::vector<Point>> dg{random_list};

	// Create feature extractor
	PointFeatureExtractor sfg;

	// Test feature extractor
	/*
	auto test_data = dg.get_data(1)[0];
	std::array<double, 3> features = sfg(test_data);
	std::cout << features[0] << ' ' << features[1] << ' ' << features[2] << std::endl;
	*/

	// Create optimizer
	LinOptimizer<std::vector<Point>, std::pair<Point, Point>, 1> linopt{};

	Lhyra<std::vector<Point>, std::pair<Point, Point>, 1> lhyra {
		solvers,
		&dg,
		&sfg,
		&linopt
	};

	std::vector<Solver<std::vector<Point>, std::pair<Point, Point>, 1>> smart_solvers;
	std::vector<Solver<std::vector<Point>, std::pair<Point, Point>, 1>> brute_solvers;
	smart_solvers.push_back(&points_smart);
	brute_solvers.push_back(&points_brute);

	DummyOptimizer<std::vector<Point>, std::pair<Point, Point>, 1> smart_opt;
	DummyOptimizer<std::vector<Point>, std::pair<Point, Point>, 1> brute_opt;

	Lhyra<std::vector<Point>, std::pair<Point, Point>, 1> brute_lhyra {
		brute_solvers,
		&dg,
		&sfg,
		&brute_opt
	};

	Lhyra<std::vector<Point>, std::pair<Point, Point>, 1> smart_lhyra {
		smart_solvers,
		&dg,
		&sfg,
		&smart_opt
	};

	linopt.train(10,10,true);


	std::vector<Point> points; points.reserve(4000);
	std::ofstream f("data.txt");
	const int NUM_DATA = 100;
	for(LIST_LENGTH = 16; LIST_LENGTH <= 4096; LIST_LENGTH *= 2) {

		std::cout << "Starting list of length " << LIST_LENGTH << std::endl;

		auto test_data = dg.get_data(NUM_DATA);
	    auto t1 = std::chrono::high_resolution_clock::now();
		for(int i = 0; i < NUM_DATA; i++) {
			lhyra(test_data[i]);
		}
	    auto t2 = std::chrono::high_resolution_clock::now();
		for(int i = 0; i < NUM_DATA; i++) {
			smart_lhyra(test_data[i]);
		}
	    auto t3 = std::chrono::high_resolution_clock::now();
		for(int i = 0; i < NUM_DATA; i++) {
			brute_lhyra(test_data[i]); 
		}
	    auto t4 = std::chrono::high_resolution_clock::now();

	    f << LIST_LENGTH << ' ';
	    f << std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count() << ' ';
	    f << std::chrono::duration_cast<std::chrono::microseconds>(t3 - t2).count() << ' ';
	    f << std::chrono::duration_cast<std::chrono::microseconds>(t4 - t3).count() << std::endl;
	}

	f.close();

}