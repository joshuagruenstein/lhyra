from matplotlib import pyplot as plt
from math import log2

xs = []
lhyra = []
merge = []
insertion = []
quick = []

with open('data.txt', 'r') as f:
	for line in f.readlines():
		x, l, m, i, q = tuple(line.split(' '))
		xs.append(log2(int(x)))
		lhyra.append((int(l)) / int(l))
		merge.append((int(m)) / int(l))
		insertion.append((int(i))/ int(l))
		quick.append((int(q))/ int(l))

plt.plot(xs, lhyra, label='lhyra')
plt.plot(xs, merge, label='merge')
plt.plot(xs, insertion, label='insertion')
plt.plot(xs, quick, label='quick')
plt.legend()
plt.show()