g++ -I/home/sydriax/gsl/include -c points.cpp -std=c++14
g++ -L/home/sydriax/gsl/lib points.o -lgsl -lgslcblas -lm -o points -std=c++14