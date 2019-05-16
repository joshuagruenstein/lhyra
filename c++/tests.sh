echo "Running code..."

./sort_test

echo "Generating training plot..."

python plot_progress.py

echo "Generating performance plot..."

python make_graph.py

echo "Uploading to imgur..."

cd ../python

python imgur.py