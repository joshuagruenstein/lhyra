from matplotlib import pyplot as plt

with open('times.txt', 'r') as f:
	s = f.read()

times = [float(t) / 10**6 for t in s.split('\n') if len(t) > 0]

plt.plot(list(range(len(times))), times)
plt.show()