# Lhyra [![Build Status](https://travis-ci.org/joshuagruenstein/lhyra.svg?branch=master)](https://travis-ci.org/joshuagruenstein/lhyra)

*Learned HYbrid Recursive Algorithms*

Lhyra is a framework designed to automatically find efficient recursive trees given arbitrary solvers, data distributions, and optimization criteria, as described by our [paper](https://github.com/joshuagruenstein/lhyra/raw/master/paper/main.pdf).  Lhyra was created for *6.890: Learning Augmented Algorithms*, taught in Spring 2019 by Profs Daskalakis and Indyk at MIT.

This repository contains Lhyra implementations in C++ and Python, with instances created for both Sorting and Closest Pair of Points.  As research was done in Python before transitioning to C++, you can find discarded optimizers in that directory.  We recommend running the C++ in order to best measure performance, which requires the [GNU Scientific Library](https://www.gnu.org/software/gsl/).  An easy way to do that is through our Docker container, which you can build with `docker build -t lhyra .` in the parent directory.  You can then drop into a shell using `docker run -rm -it lhyra /bin/ash`, or run our example with `docker run lhyra`.

We've set up Travis CI to automatically build and run the Docker container whenever we push to master.  You can click [here](https://travis-ci.org/joshuagruenstein/lhyra) to see build status, and look at the console output to see some plots produced from the most recent push.
