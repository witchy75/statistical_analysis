import math
from scipy.stats import norm, chi2
import random

with open("Москва_2021.txt", 'r') as f:
    a = list(map(int, f))

groups = 7
interval = math.ceil((max(a) - min(a))/groups)

freqs = [] # частоты
amounts = [] # интервалы
for i in range(groups):
    j = min(a) + i * interval
    b = j + interval
    amounts.append((j, b))
    freqs.append(sum(1 for x in a if j <= x < b))

print("\nинтервальный ряд:")
for (j, b), f in zip(amounts, freqs):
    print(f"[{j}; {b}) : {f}")

# начал среднего
xi_mean = 0
for i in range(len(amounts)):
    xi_mean += (sum(amounts[i])/2) * freqs[i]

x_mean = xi_mean / sum(freqs)
# конец

std = 0
for i in range(len(amounts)):
    j = sum(amounts[i]) / 2
    std += ((j - x_mean) ** 2) * freqs[i]
std = math.sqrt(std / sum(freqs)) # среднеквадратическое отклонение

print(f"среднее: {x_mean}")
print(f"среднеквадратическое отклонение: {std}")

# перевожу значения интервалов в z-значения (я гений)
z_values = []
for left, right in amounts:
    z_left = (left - x_mean) / std
    z_right = (right - x_mean) / std
    z_values.append((z_left, z_right))

print("z-значения интервалов:")
for i, (z_l, z_r) in enumerate(z_values):
    print(f"[{amounts[i][0]}; {amounts[i][1]}) -> [{z_l:.4f}; {z_r:.4f})")

pi = []
for i, (z_l, z_r) in enumerate(z_values):
    if i == 0:
        p = norm.cdf(z_r)
    elif i == len(z_values) - 1:
        p = 1.0 - norm.cdf(z_l)
    else:
        p = norm.cdf(z_r) - norm.cdf(z_l)
    pi.append(float(p))

print("pi:", [round(p, 4) for p in pi])

ni = [float(len(a) * p) for p in pi]
print("ni:", [round(n, 2) for n in ni])

# НАКОНЕЦ-ТООООО Я СДЕЛАЛААААА / кто бы мог подумать
pirson = []
print("Расчет критериев Пирсона:")
for i in range(len(ni)):
    chi_val = (freqs[i] - ni[i])**2 / ni[i]
    pirson.append(float(chi_val))
    print(f"интервал {i + 1} = {chi_val:.10f}")

total_pirson = sum(pirson)
print(f"Xнабл (сумма критериев пирсона): {total_pirson:.10f}")

k = groups - 1 - 2
print(f"число степеней свободы: {k}")
alpha = 0.05
chi2_crit = chi2.ppf(1 - alpha, k)
print(f"критическое хи-квадрат: {chi2_crit:.10f}")

if total_pirson < chi2_crit:
    print("1 гипотеза принимается")
else:
    print("1 гипотеза отвергается")

gamma = 0.95
t = 1.96
delta = 3

average = sum(a) / len(a)
sigma = math.sqrt(sum((x - average) ** 2 for x in a) / len(a))
n_sample = math.ceil((t ** 2 * sigma ** 2) / delta ** 2)
print(f"объем выборки: {n_sample}")

random.seed()
sample_means = []
for i in range(36):
    sample = random.choices(a, k=n_sample)
    sample_means.append(sum(sample) / n_sample)

print(f"выборочные средние: {[round(x, 3) for x in sample_means]}")

min_val = math.floor(min(sample_means))
max_val = math.ceil(max(sample_means))
intervals = [(i, i+1) for i in range(min_val, max_val)]

print("\nинтервальный ряд распределения средних:")
freqs = []
for left, right in intervals:
    count = sum(1 for x in sample_means if left <= x < right)
    freqs.append(count)
    print(f"[{left}; {right}) : {count}")

x_mean = sum(sample_means) / len(sample_means)
std = math.sqrt(sum((x - x_mean) ** 2 for x in sample_means) / len(sample_means))

print(f"\nсреднее: {x_mean}")
print(f"среднеквадратическое отклонение: {std}")

z_values = []
for left, right in intervals:
    z_left = (left - x_mean) / std
    z_right = (right - x_mean) / std
    z_values.append((z_left, z_right))

print("z-значения интервалов:")
for i, (z_l, z_r) in enumerate(z_values):
    print(f"[{intervals[i][0]}; {intervals[i][1]}) -> [{z_l:.4f}; {z_r:.4f})")

pi = []
for i, (z_l, z_r) in enumerate(z_values):
    if i == 0:
        p = norm.cdf(z_r)
    elif i == len(z_values) - 1:
        p = 1.0 - norm.cdf(z_l)
    else:
        p = norm.cdf(z_r) - norm.cdf(z_l)
    pi.append(float(p))

print(f"pi: {[round(p, 4) for p in pi]}")

ni = [float(len(sample_means) * p) for p in pi]
print(f"ni: {[round(n, 2) for n in ni]}")

print("расчет критериев Пирсона:")
pirson = []
for i in range(len(ni)):
    chi_val = (freqs[i] - ni[i])**2 / ni[i]
    pirson.append(chi_val)
    print(f"интервал {i+1} = {chi_val:.10f}")

total_pirson = sum(pirson)
print(f"Xнабл (сумма критериев пирсона): {total_pirson:.10f}")

k = len(intervals) - 1 - 2
chi2_crit = chi2.ppf(1 - 0.05, k)

print(f"число степеней свободы: {k}")
print(f"критическое хи-квадрат: {chi2_crit:.10f}")

if total_pirson < chi2_crit:
    print("2 гипотеза принимается")
else:
    print("2 гипотеза отвергается")