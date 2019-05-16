echo "Compiling and linking..."

g++ -I/usr/include -c sort_test.cpp -std=c++14 -o sort_test.o && g++ -L/usr/lib sort_test.o -lgsl -lgslcblas -lm -o sort_test -std=c++14
g++ -I/usr/include -c points.cpp -std=c++14 -o points.o && g++ -L/usr/lib points.o -lgsl -lgslcblas -lm -o points_test -std=c++14

echo "Running sorting code..."

./sort_test

echo "Generating plots..."

python make_graph_training.py
mv training_times.png progress_sorting.png
python make_graph.py

echo "Running points code..."

./points_test

echo "Generating plot..."

python make_graph_training.py
mv training_times.png progress_points.png
python make_graph_points.py

echo "Uploading to imgur..."

cd ../python

python imgur.py