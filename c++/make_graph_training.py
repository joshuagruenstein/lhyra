from matplotlib import pyplot as plt


with open('times.txt', 'r') as f:
	times = [float(line)/1000 for line in f.readlines()]

plt.plot(range(1, len(times)+1), times)
plt.xlabel('Training Epoch')
plt.ylabel('Time (in microseconds)')
plt.savefig('training_times.png')