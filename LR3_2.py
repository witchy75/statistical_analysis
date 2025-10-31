import math
from scipy.stats import norm
import scipy.stats as stats
import numpy as np
import random

with open("Москва_2021.txt", 'r') as f:
    a = list(map(int, f.read().split()))

average = sum(a)/len(a) # среднее значение по всей совокупности
sum_for_variance = 0
for i in range(len(a)):
    sum_for_variance += (a[i] - average)**2
variance = sum_for_variance / (len(a) - 1)  # несмещённая дисперсия
asd = math.sqrt(variance)

accuracy = 3
t = 1.96
sample_size = math.ceil((t**2 * asd**2) / accuracy**2) # объем выборки

sample1 = random.sample(a, sample_size)
sample2 = random.sample(a, sample_size)

# 2.1

# дисперсия несмещенная
var1 = np.var(sample1, ddof=1) # ddof=1 -> делитель (n-1) -> несмещенная дисперсия
var2 = np.var(sample2, ddof=1)

# F-наблюдаемое (берём отношение большей дисперсии к меньшей)
if var1 >= var2:
    F = var1 / var2
    # степени свободы: df1 для числителя (большей дисперсии), df2 для знаменателя (меньшей дисперсии)
    df1 = sample_size - 1
    df2 = sample_size - 1
else:
    F = var2 / var1
    # степени свободы: df1 для числителя (большей дисперсии), df2 для знаменателя (меньшей дисперсии)
    df1 = sample_size - 1
    df2 = sample_size - 1 

alpha = 0.05 # уровень значимости - вероятность ошибки I рода

# проверка H1: D1 > D2 (односторонняя - правосторонняя)
F_crit_one_sided = stats.f.ppf(1 - alpha, df1, df2) # Критическая точка 𝐹кр(𝛼; 𝑘1; 𝑘2)

print('1) Проверить нулевую гипотезу о равенстве дисперсий генеральных совокупностей')
print("\nПроверка гипотезы H1: D1 > D2")
print(f"Fнабл = {F:.4f}")
print(f"Fкр = {F_crit_one_sided:.4f}")

# Если отношение 𝑠1/𝑠2 больше критической точки, то дисперсии различаются между собой с вероятностью p = 1 – α

if F > F_crit_one_sided:
    print('Fнабл > Fкрит')
    print("→ Отвергаем H0: дисперсии различаются (D1 > D2)")
else:
    print('Fнабл < Fкрит')
    print("→ Не отвергаем H0: дисперсии равны")

# проверка H1: D1 ≠ D2 (двусторонняя)
# Для проверки гипотезы Н0 при конкурирующей гипотезе H1: D (X) ≠ D(Y)
# достаточно найти правую критическую точку F2 = Fкp (alpha/2; k1; k2).
F_lower = stats.f.ppf(alpha/2, df1, df2) # левая граница критической области
F_upper = stats.f.ppf(1 - alpha/2, df1, df2) # правая

print("\nПроверка гипотезы H1: D1 ≠ D2")
print(f"Fнабл = {F:.4f}")
print(f"Критическая область: F < {F_lower:.4f} или F > {F_upper:.4f}")

if F < F_lower or F > F_upper:
    print('Fнабл < Fправ или Fнабл > Fверх')
    print("→ Отвергаем H0: дисперсии различаются")
else:
    print('Fправ < Fнабл < Fверх')
    print("→ Не отвергаем H0: дисперсии равны")

# Вывод дисперсий для отчёта
print("\nВыборочная дисперсия 1:", round(var1, 3))
print("Выборочная дисперсия 2:", round(var2, 3))


# 2.2
# Проверка гипотезы о равенстве дисперсии одной выборки и известного σ²
print("\n2) Проверка нулевой гипотезы о равенстве генеральной дисперсии и σ²")

mean_a = sum(a) / len(a)
gen_variance = (sum((x - mean_a)**2 for x in a)) / len(a)  # генеральная дисперсия
# χнабл^2 = (n-1)s^2/σ^2
# 𝑠 - выборочная дисперсия, σ — известная дисперсия генеральной совокупности
print(f"генеральная совокупность: {gen_variance}")

# Выбираем одну из выборок
sample = sample1
n = len(sample) # размер выборки
alpha = 0.05

# Статистика χ²
# χ² = (n-1)s²/σ²
s2 = np.var(sample, ddof=1)  # выборочная дисперсия этой выборки
chi2_stat = (n - 1) * s2 / gen_variance
print(f"s^2 - выборочная дисп: {s2}")

print("\nПроверка гипотезы о равенстве ген. дисперсии и σ²")
print(f"χ²набл = {chi2_stat:.4f}")

# a) H1: D > σ²
chi2_crit_right = stats.chi2.ppf(1 - alpha, n - 1) # даёт критическое значение χ² для заданной вероятности q и df = n-1.
# Для правосторонней проверки берём верхнюю границу 1 − α.

print(f"Правосторонняя проверка H1: D > σ²")
print(f"χ²крит = {chi2_crit_right:.4f}")
if chi2_stat > chi2_crit_right:
    print('𝜒2 > 𝜒2кр')
    print("→ Отвергаем H0: дисперсия выборки больше σ²")
else:
    print('𝜒2 < 𝜒2кр')
    print("→ Не отвергаем H0: дисперсия равна σ²")

# б) H1: D ≠ σ²
chi2_crit_lower = stats.chi2.ppf(alpha/2, n - 1)
chi2_crit_upper = stats.chi2.ppf(1 - alpha/2, n - 1)
print(f"\nДвусторонняя проверка H1: D ≠ σ²")
print(f"Критическая область: χ² < {chi2_crit_lower:.4f} или χ² > {chi2_crit_upper:.4f}")

if chi2_stat < chi2_crit_lower or chi2_stat > chi2_crit_upper:
    print('𝜒2набл < 𝜒2кр1 или 𝜒2набл > 𝜒2кр2')
    print("→ Отвергаем H0: дисперсия различается")
else:
    print('𝜒2кр1 < 𝜒2набл < 𝜒2кр2')
    print("→ Не отвергаем H0: дисперсия равна σ²")

# в) H1: D < σ²
chi2_crit_left = stats.chi2.ppf(alpha, n - 1)
print(f"\nЛевосторонняя проверка H1: D < σ²")
print(f"χ²крит = {chi2_crit_left:.4f}")
if chi2_stat < chi2_crit_left:
    print('𝜒2набл < 𝜒2кр')
    print("→ Отвергаем H0: дисперсия выборки меньше σ²")
else:
    print('𝜒2набл > 𝜒2кр')
    print("→ Не отвергаем H0: дисперсия равна σ²")
