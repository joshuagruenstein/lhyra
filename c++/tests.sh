echo "Compiling and linking..."

g++ -I/usr/include -c sort_test.cpp -std=c++14 -o sort_test.o && g++ -L/usr/lib sort_test.o -lgsl -lgslcblas -lm -o sort_test -std=c++14

echo "Running code..."

./sort_test

echo "Generating training plot..."

python plot_progress.py

echo "Generating performance plot..."

python make_graph.py

echo "Uploading to imgur..."

cd ../python

python imgur.py