import math
from scipy.stats import chi2

with open("/home/aroya/MSAD/Москва_2021.txt", 'r') as f:
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