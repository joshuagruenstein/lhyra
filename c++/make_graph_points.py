from matplotlib import pyplot as plt
from math import log2

xs = []
lhyra = []
smart = []
brute = []

with open('data.txt', 'r') as f:
	for line in f.readlines():
		x, l, s, b = tuple(line.split(' '))
		xs.append(log2(int(x)))
		lhyra.append(log2(int(l)))
		smart.append(log2(int(s)))
		brute.append(log2(int(b)))

plt.plot(xs, lhyra, label='lhyra')
plt.plot(xs, smart, label='smart')
plt.plot(xs, brute, label='brute')
plt.legend()

plt.savefig('relative_plot_points.png')