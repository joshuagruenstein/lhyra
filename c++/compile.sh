gcc -Wall -I/home/sydriax/gsl/include -c linopt.cpp
gcc -L/home/sydriax/gsl/lib linopt.o -lgsl -lgslcblas -lm -o linopt