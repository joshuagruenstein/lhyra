#pragma once

#include <vector>
#include <iostream>
#include <cmath>
#include <limits>
#include <stdlib.h>

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

std::pair<Point, Point> points_brute(std::vector<Point> points) {
	double min_dist =  std::numeric_limits<double>::max();
	std::pair<Point, Point> closest_pair;

	for (int i=0; i<points.size(); i++) {
		for (int j=i+1; j<points.size(); j++) {
			auto pair = std::pair<Point,Point>(points[i],points[j]);
			if (point_dist(pair) < min_dist) {
				min_dist = point_dist(pair);
				closest_pair = pair;
			}
		}
	}

	return closest_pair;
}

std::pair<Point, Point> points_smart(std::vector<Point> points) {
	if (points.size() <= 3) return points_brute(points);

	auto psorted = std::vector<Point>(points);
	std::sort(psorted.begin(), psorted.end(), [](const auto& l, const auto& r) {
		return l.x < r.x;
	});

	int halfway = psorted.size()/2;
	auto left = points_smart(std::vector<Point>(psorted.begin(), psorted.begin()+halfway));
	auto right = points_smart(std::vector<Point>(psorted.begin()+halfway, psorted.begin()+psorted.size()));
	
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

int main() {
	srand(0);

	auto points = std::vector<Point>();

	for (int i=0; i<1000; i++) points.push_back({doublerand(), doublerand()});

	std::cout << point_dist(points_brute(points)) << std::endl;

	std::cout << point_dist(points_smart(points)) << std::endl;

}