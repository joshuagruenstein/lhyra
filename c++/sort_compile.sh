g++ -I/home/sydriax/gsl/include -c sort_test.cpp -std=c++11
g++ -L/home/sydriax/gsl/lib sort_test.o -lgsl -lgslcblas -lm -o sort_test -std=c++11