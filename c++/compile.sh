g++ -I/home/sydriax/gsl/include -c lhyra_test.cpp -std=c++11
g++ -L/home/sydriax/gsl/lib lhyra_test.o -lgsl -lgslcblas -lm -o lhyra_test -std=c++11