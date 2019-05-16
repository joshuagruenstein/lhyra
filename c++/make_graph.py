from matplotlib import pyplot as plt
from math import log2

xs = []
lhyra = []
merge = []
insertion = []
quick = []
std = []

with open('data.txt', 'r') as f:
	for line in f.readlines():
		x, l, m, i, q, s = tuple(line.split(' '))
		xs.append(log2(int(x)))
		lhyra.append(log2(int(l)))
		merge.append(log2(int(m)))
		insertion.append(log2(int(i)))
		quick.append(log2(int(q)))

plt.plot(xs, lhyra, label='lhyra')
plt.plot(xs, merge, label='merge')
plt.plot(xs, insertion, label='insertion')
plt.plot(xs, quick, label='quick')

plt.xlabel('Log of List Length')
plt.ylabel('Log of Time (in microseconds)')

plt.legend()

plt.savefig('relative_plot.png')