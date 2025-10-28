import math
from scipy.stats import norm, chisquare, chi2
import random
import numpy as np

with open("/home/aroya/statistical_analysis/Москва_2021.txt", 'r') as f:
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

x_mean = round(xi_mean / sum(freqs), 4)
# конец

std = 0
for i in range(len(amounts)):
    j = sum(amounts[i]) / 2
    std += ((j - x_mean) ** 2) * freqs[i]
std = round(math.sqrt(std / sum(freqs)),4) # среднеквадратическое отклонение

print(f"среднее: {x_mean}")
print(f"среднеквадратическое отклонение: {std}")

# перевожу значнеия интервалов в z-значения (я гений)
i = amounts[0][0]
z = []
while i <= amounts[-1][-1]:
    j = (i - x_mean) / std
    z.append(j)
    i += interval

print("z-значения:", [round(x, 4) for x in z])

fz = [-0.5, -0.35, -0.1171, 0.1702, 0.3808, 0.4724, 0.496, 0.5]
pi = [round(fz[i + 1] - fz[i], 4) for i in range(len(fz) - 1)]
print(f"pi: {pi}")

ni = [len(a) * pi[i] for i in range(len(pi))]
print(f"ni: {ni}")

pirson = [round((freqs[i] - ni[i])**2 / ni[i], 4) for i in range(len(ni))]
print(f"критерий пирсона: {pirson}")
print(f"сумма критерия пирсона: {round(sum(pirson), 4)}")

k = groups - 1 - 2
print(f"число степеней свободы: {k}")
alpha = 0.05
chi2_crit = chi2.ppf(1 - alpha, k)
print(f"критическое значение хи-квадрат: {round(chi2_crit, 4)}")

if sum(pirson) < chi2_crit:
    print("гипотеза принимается")
else:
    print("гипотеза отвергается")

    


gamma = 0.95
t = 1.96
delta = 3 

average = sum(a) / len(a)
sum_for_variance = sum((x - average) ** 2 for x in a)
variance = sum_for_variance / len(a)
sigma = math.sqrt(variance)

n_sample = math.ceil((t ** 2 * sigma ** 2) / delta ** 2)
print(f"объем: {n_sample}")

random.seed()
sample_means = []
for i in range(36):
    sample = random.choices(a, k=n_sample) 
    sample_avg = sum(sample) / n_sample
    sample_means.append(math.ceil(sample_avg * 1000) / 1000)

print(f"для каждой из 36 выборок выборочные средние: {sample_means}")

minimum = math.floor(min(sample_means))
maximum = math.ceil(max(sample_means))

interval_bounds = []
current = minimum
while current < maximum:
    interval_bounds.append((current, current + 1))
    current += 1

print(f"интервальные ряды: {interval_bounds}")

absolute_average = sum(a)/len(a)
asd = math.sqrt(sum((x - absolute_average)**2 for x in sample_means)/(len(sample_means)-1))

print(f"ско: {asd}")

z = []
for i in range(minimum, maximum):
    z_left = round((i - absolute_average) / asd, 3)
    z_right = round((i + 1 - absolute_average) / asd, 3)
    z.append([z_left, z_right])
    print(f"для интервала [{i}, {i + 1}) - [{z_left}, {z_right}]")

p = []
for i in range(len(z)):
    f = round(norm.cdf(z[i][1]) - norm.cdf(z[i][0]), 3)
    p.append(f)
    print(f"вероятность попадания в интервал [{z[i][0]}, {z[i][1]}) = {f}")

expected_raw = [len(sample_means) * pi for pi in p]
print(f"сумма вероятностей: {sum(p)}")
print(f"сумма теоретических: {sum(expected_raw)}")

expected = np.array(expected_raw) * (len(sample_means) / sum(expected_raw))
print(f"сумма теоретически: {sum(expected)}")

n_rounded = [round(ex) for ex in expected]
print(f"искомые теоретические частоты: {n_rounded}")
print(f"cумма теоретических частот: {sum(n_rounded)}")
freqs = []
for i in range(len(z)):
    left = minimum + i
    right = left + 1
    count = sum(1 for x in sample_means if left <= x < right)
    freqs.append(count)

print(f"наблюдаемые частоты: {freqs}")
print(f"сумма наблюдаемых: {sum(freqs)}")

alpha = 0.05
s = len(freqs)
m = 2
df = s - 1 - m

stat, p_value = chisquare(f_obs=freqs, f_exp=expected)
chi2_crit = chi2.ppf(1 - alpha, df)

print(f"наблюдаемое = {round(stat, 3)}")
print(f"критическое = {round(chi2_crit, 3)}")
print(f"p-value = {round(p_value, 3)}")

if stat > chi2_crit:
    print("гипотеза отвергается")
else:
    print("гипотеза принимается")