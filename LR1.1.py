import matplotlib.pyplot as plt
import math

with open("Москва_2021.txt", 'r') as f:
    a = list(map(int, f))
groups = 7
interval = math.ceil((max(a) - min(a))/groups)
a.sort()
uniques = list(set(a))
number_of_repetitions = []
print("дискретные ряды:")
print("№, число кол-во повторений вероятность")
for i in range(len(uniques)):
    x = uniques[i]
    y = a.count(uniques[i])
    z = round(y/len(a), 3)
    print(i + 1, ':', x, '       ', y, '           ', z)
for i in range(len(uniques)):
    m = a.count(uniques[i])
    number_of_repetitions.append(m)

intervals = []
current = min(a)
for i in range(groups + 1):
    intervals.append(current)
    current += interval 

freqs = []
for i in range(len(intervals)-1):
    lower_bound = intervals[i]
    upper_bound = intervals[i+1]
    bin_count = sum(1 for x in a if lower_bound <= x < upper_bound)
    freqs.append(bin_count)

def mean():
    summa = 0
    for i in range(len(uniques)):
        x = uniques[i]
        y = a.count(uniques[i])
        summa += x * y
    return summa / len(a)

def dispersion(mean):
    sq_sum = 0
    for i in range(len(uniques)):
        x = uniques[i]
        y = a.count(uniques[i])
        sq_sum += ((x - mean) ** 2) * y
    return sq_sum / len(a)

def mode():
    greatest_freq = -1
    greatest_var = -1000
    for i in range(len(uniques)):
        freq = a.count(uniques[i])
        if freq > greatest_freq:
            greatest_var = uniques[i]
            greatest_freq = freq
    return greatest_var, greatest_freq

def median():
    if len(a) % 2 == 0:
        return (a[len(a) // 2] + a[len(a) // 2 + 1]) // 2
    else:
        return a[len(a) // 2 + 1]

mean_disc = round(mean(), 3)
disp_disc = round(dispersion(mean_disc), 3)
deviation_disc = round(disp_disc ** 0.5, 3)
coef_variation_disc = round(deviation_disc / mean_disc * 100, 3)
mode_disc = mode()
median_disc = median()
min_value = min(a)
max_value = max(a)
scope = max_value - min_value

print("\nХарактеристики дискретного ряда:")
print(f'Мат. ожидание: {mean_disc}')
print(f'Дисперсия: {disp_disc}')
print(f'СКО: {deviation_disc}')
print(f'Коэфф. вариации: {coef_variation_disc}')
print(f'Мода: {mode_disc}')
print(f'Медиана: {median_disc}')
print(f'Мин. значение: {min_value}')
print(f'Макс. значение: {max_value}')
print(f'Размах: {scope}')


#  ИНТЕРВАЛЬНЫЙ РЯД 
freqs = []
amounts = []
for i in range(groups):
    j = min(a) + i * interval
    b = j + interval
    amounts.append((j, b))
    freqs.append(sum(1 for x in a if j <= x < b))

print("\nИнтервальный ряд:")
for (j, b), f in zip(amounts, freqs):
    print(f"[{j}; {b}) : {f}")

# середины интервалов
midpoints = [(j + b) / 2 for j, b in amounts]
n = len(a)

#  Характеристики интервального ряда 
def mean_interval():
    return sum(m * f for m, f in zip(midpoints, freqs)) / n

def dispersion_interval(mean_val):
    return sum(f * (m - mean_val) ** 2 for m, f in zip(midpoints, freqs)) / n

def median_interval():
    N = n
    cum_freq = 0
    for i, f in enumerate(freqs):
        cum_freq_next = cum_freq + f
        if cum_freq_next >= N/2:
            L = amounts[i][0]
            h = amounts[i][1] - amounts[i][0]
            F_prev = cum_freq
            f_med = f
            return L + ((N/2 - F_prev) / f_med) * h
        cum_freq = cum_freq_next

def mode_interval():
    m = freqs.index(max(freqs))
    L = amounts[m][0]
    h = amounts[m][1] -amounts[m][0]
    f_m = freqs[m]
    f_prev = freqs[m-1] if m > 0 else 0
    f_next = freqs[m+1] if m < len(freqs)-1 else 0
    return L + ((f_m - f_prev) / ((f_m - f_prev) + (f_m - f_next))) * h

mean_int = round(mean_interval(), 3)
disp_int = round(dispersion_interval(mean_int), 3)
deviation_int = round(disp_int ** 0.5, 3)
median_int = round(median_interval(), 3)
mode_int = round(mode_interval(), 3)
scope_int = amounts[-1][1] - amounts[0][0]

coef_variation_int = round(deviation_int / mean_int * 100, 3)
median_int = round(median_interval(), 3)
mode_int = round(mode_interval(), 3)
scope_int = amounts[-1][1] - amounts[0][0]

print("\nХарактеристики интервального ряда:")
print(f'Мат. ожидание: {mean_int}')
print(f'Дисперсия: {disp_int}')
print(f'СКО: {deviation_int}')
print(f'Медиана: {median_int}')
print(f'Мода: {mode_int}')
print(f'Размах: {scope_int}')
print(f'Коэффициент вариации: {coef_variation_int}%')

interval_labels = []
for i in range(len(intervals)-1):
    label = f"{intervals[i]}-{intervals[i+1]}"
    interval_labels.append(label)

print("Метки интервалов:", interval_labels)
print("Количество меток:", len(interval_labels))
print("Количество значений:", len(freqs))

plt.switch_backend('Agg')
plt.figure(figsize=(14, 6))

# ГИСТОГРАММА
plt.subplot(1, 2, 1)
bars = plt.bar(interval_labels, freqs, alpha=0.7, color='skyblue', edgecolor='black', width=1.0)
plt.title('гистограмма')
plt.xlabel('возраст')
plt.ylabel('частота')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

for bar, freq in zip(bars, freqs):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             str(freq), ha='center', va='bottom', fontsize=9)

# ПОЛИГОН
plt.subplot(1, 2, 2)
sorted_uniques = sorted(uniques)
sorted_repetitions = [a.count(x) for x in sorted_uniques]

plt.plot(sorted_uniques, sorted_repetitions, 'o-', linewidth=2, markersize=8, color='red', markerfacecolor='white')
plt.title('Полигон')
plt.xlabel('возраст')
plt.ylabel('частота')
plt.grid(True, alpha=0.3)

for i, (x, y) in enumerate(zip(sorted_uniques, sorted_repetitions)):
    plt.text(x, y + 100, str(y), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('histogram_polygon.png')

