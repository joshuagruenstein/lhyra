#include <vector>
#include <iostream>

std::vector<double> merge_sort(std::vector<double> data) {
	if (data.size() <= 1) return data;

	int halfway = data.size()/2;

	auto sorted_first = merge_sort(std::vector<double>(data.begin(), data.begin() + halfway));
	auto sorted_second = merge_sort(std::vector<double>(data.begin()+halfway, data.begin() + data.size()));

	auto joined = std::vector<double>();

	int j=0, i=0;
	while (i+j < data.size()) {
		if (i == sorted_first.size() || (j != sorted_second.size() and sorted_first[i] > sorted_second[j]))
			joined.push_back(sorted_second[j++]);
		else joined.push_back(sorted_first[i++]);
	}

	return joined;
}

std::vector<double> insertion_sort(std::vector<double> data) {
	if (data.size() <= 1) return data;

	std::vector<double> sorted = data;

	for (int i=0; i<data.size()-1; i++) {
		int j = i;
		while (j >= 0 && sorted[j+1] < sorted[j]) {
			double temp = sorted[j];
			sorted[j] = sorted[j+1];
			sorted[j+1] = temp;
			j--;
		}
	}

	return sorted;
}

std::vector<double> quick_sort(std::vector<double> data) {
	if (data.size() <= 1) return data;

	std::vector<double> sorted = data;

	double pivot = sorted[sorted.size()/2];
	int i=0, j=sorted.size()-1;

	int pi;
	while (true) {
		while (sorted[i] < pivot) i++;
		while (sorted[j] > pivot) j--;
		if (i >= j) {
			pi = j;
			break;
		}

		double temp = sorted[i];
		sorted[i] = sorted[j];
		sorted[j] = temp;
	}

	auto sorted_first = quick_sort(std::vector<double>(sorted.begin(), sorted.begin() + pi));
	auto sorted_second = quick_sort(std::vector<double>(sorted.begin()+pi+1, sorted.begin() + sorted.size()));

	sorted_first.push_back(sorted[pi]);
	sorted_first.insert(sorted_first.end(), sorted_second.begin(), sorted_second.end());

	return sorted_first;
}