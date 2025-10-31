import math
import random
import matplotlib.pyplot as plt

with open("Москва_2021.txt", 'r') as f:
    a = list(map(int, f))

gamma = 0.95
t = 1.96
delta = 3 

h = 36

average = sum(a) / len(a)
sum_for_variance = sum((x - average) ** 2 for x in a)
variance = sum_for_variance / len(a)
sigma = math.sqrt(variance)

n = math.ceil((t ** 2 * sigma ** 2) / delta ** 2)
print(f"объем: {n}")

random.seed()
sample_means = []
for i in range(h):
    sample = random.choices(a, k=n) 
    sample_avg = sum(sample) / n
    sample_means.append(math.ceil(sample_avg * 1000) / 1000)

print(f"для каждой из 36 выборок выборочные средние: {sample_means}")

minimum = math.floor(min(sample_means))
maximum = math.ceil(max(sample_means))

interval_bounds = []
current = minimum
while current < maximum:
    interval_bounds.append((current, current + 1))
    current += 1

formatted_intervals = [f'[{interval[0]}, {interval[1]})' for interval in interval_bounds]
print(f"интервальные ряды: {', '.join(formatted_intervals)}")

frequencies = []
relative_freqs = []
for i in range(len(interval_bounds)):
    count = 0
    for mean in sample_means:
        if i == len(interval_bounds) - 1:
            if interval_bounds[i][0] <= mean <= interval_bounds[i][1]:
                count += 1
        else:
            if interval_bounds[i][0] <= mean < interval_bounds[i][1]:
                count += 1
    frequencies.append(count)
    rel = math.ceil((count / h) * 1000) / 1000 if h > 0 else 0
    relative_freqs.append(rel)
    print(f"относительная частота для интервала [{interval_bounds[i][0]}, {interval_bounds[i][1]}): {rel}")

if interval_bounds:
    centers = [interval[0] + 0.5 for interval in interval_bounds]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(centers, relative_freqs, width=1, edgecolor='black', alpha=0.7, align='center')

    for bar, rel in zip(bars, relative_freqs):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                 str(rel), ha='center', va='bottom')

    plt.xlabel('Интервалы')
    plt.ylabel('Относительная частота')
    plt.title('Гистограмма распределения выборочных средних')
    plt.grid(axis='y', alpha=0.3)
    
    plt.xticks(centers, [f'[{b[0]}, {b[1]})' for b in interval_bounds], rotation=45)
    plt.ylim(0, 1)

    plt.savefig('/home/aroya/statistical_analysis/histogram.png', dpi=300, bbox_inches='tight') 
    plt.show()