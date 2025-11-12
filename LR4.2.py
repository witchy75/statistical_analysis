import math
from math import isclose
from scipy.stats import rankdata

f = open('Москва_2021.txt', 'r')
data = sorted([int(i) for i in f.read().split()])
groups = 7   # число интервалов
uniques = sorted(list(set(data)))
interval = math.ceil((max(data) - min(data)) / groups)

# интервальный ряд
amounts = []
freqs = []
for i in range(groups):
    a = min(data) + i * interval
    b = a + interval if i < groups - 1 else max(data) + 1  
    amounts.append((a, b))
    freqs.append(sum(1 for x in data if a <= x < b))

# print("\nИнтервальный ряд:")
# for (a, b), f in zip(amounts, freqs):
#     print(f"[{a}; {b}) : {f}")

number_of_repetitions = {}
# print("Дискретные ряды:")
# print("№, Число Кол-во повторений")
for i in range(len(uniques)):
    x = uniques[i]
    frequences = data.count(uniques[i])
    # print(i + 1, ':', x, '       ', frequences)
    number_of_repetitions[x] = frequences

# print(number_of_repetitions)

''' Для вычисления внутригрупповой дисперсии, необходимо вычислить
груповую дисперсию. Для вычисления групповой дисперсии нужно найти 
групповую среднюю. Групповая средняя = 
'''

# 1 - вычислить внутригрупповую и межгрупповую дисперсию, проверить справедливость формулы общей дисперсии. 

group_mean = []  # групповая средняя
for (a, b) in amounts:
    # Отбираем данные, попадающие в текущий интервал
    group_data = [x for x in data if a <= x < b]
    ''' if len(group_data) == 0:
        group_mean.append(None)  # если данных нет, то None
        continue '''

    # вычисляем среднее по формуле
    x_sum = sum(x * number_of_repetitions[x] for x in uniques if a <= x < b)
    N_j = sum(number_of_repetitions[x] for x in uniques if a <= x < b)
    x_mean_j = x_sum / N_j
    group_mean.append(x_mean_j)

# вывод групповых средних
# print("\nГрупповые средние:")
# for i, (interval_bounds, mean) in enumerate(zip(amounts, group_mean), start=1):
#     a, b = interval_bounds
#     print(f"Группа {i}: [{a}; {b}) → средняя = {mean:.4f}")


# вычисление внутригрупповой, межгрупповой и общей дисперсий 

N_total = len(data)
overall_mean = sum(data) / N_total

group_stats = []
for (a, b), mean_j in zip(amounts, group_mean):
    group_data = [x for x in data if a <= x < b]
    N_j = len(group_data)

    # групповая дисперсия по формуле 𝐷𝑗гр = (1/𝑁𝑗) * sum(𝑥𝑖 − 𝑥̅𝑗)^2 ∙ 𝑛i
    D_j_gr = sum(((x - mean_j) ** 2) * number_of_repetitions[x] 
                 for x in uniques if a <= x < b) / N_j
    group_stats.append((N_j, mean_j, D_j_gr))

# print(*[group_stats[i][2] for i in range(groups)])

# Внутригрупповая: взвешенное среднее по объёмам групп 𝐷внгр = (1/𝑁) * sum(𝐷𝑗гр ∙ 𝑁j)
D_within = 0.0  # начальное значение внутригрупповой дисперсии
for gs in group_stats:
    N_j = gs[0]   # число элементов в группе
    D_j = gs[2]   # групповая дисперсия

    D_within += D_j * N_j
D_within = D_within / N_total

# Межгрупповая: дисперсия групповых средних относительно общей средней 𝐷межгр = (1/𝑁) * sum(𝑥̅𝑗 − 𝑥̅)^2 * 𝑁j
D_between = 0.0
for gs in group_stats:
    N_j = gs[0]
    mean_j = gs[1] # среднее группы
    D_between += (mean_j - overall_mean) ** 2 * N_j 
D_between = D_between / N_total


# общая дисперсия по всей совокупности 𝐷общ = 1/𝑁 * sum(𝑥𝑖 − 𝑥̅)^2 ∙ 𝑛i
D_overall = sum(((x - overall_mean) ** 2) * number_of_repetitions[x] 
                for x in uniques) / N_total

# Вывод
print("\nСтатистика по группам")
for idx, ((a,b), (N_j, mean_j, D_j)) in enumerate(zip(amounts, group_stats), start=1):
    print(f"Группа {idx}: [{a};{b}) — сумма частот в группе ={N_j}, групповая ср. = {mean_j:.4f}, групповая дисп.= {D_j:.6f}")

print("\nДисперсии")
print(f"Общая средняя (N={N_total}): {overall_mean:.4f}")
print(f"Внутригрупповая D_вн_гр = {D_within:.6f}")
print(f"Межгрупповая  D_меж_гр = {D_between:.6f}")
print(f"Общая D_общ = {D_overall:.6f}")

# Проверка теоремы D_общ = D_вн_гр + D_меж_гр
sum_parts = D_within + D_between
diff = D_overall - sum_parts
print(f"\nПроверка теоремы D_вн_гр + D_меж_гр = D_общ")
if D_within + D_between == D_overall:
    print('Теорема выполняется')
    print(f"{D_within:.3f} + {D_between:.3f} = {D_overall:.3f}")
else:
    print('Теорема не выполняется')
    print(f"{D_within:.3f} + {D_between:.3f} = {D_overall:.3f}")


# 2 - Вычислить корреляционное отношение
'''
Корреляционной называется зависимость, при которой каждому значению величины X 
ставится в соответствие среднее значение величины Y

Корреляционное отношение показывает тесноту и форму связи между двумя переменными
Оно измеряет, насколько хорошо одна переменная может быть предсказана на основе другой, 
и всегда принимает значения от 0 до 1, где 1 означает полную зависимость вариации y от х. 
 η^2 = Dмежгрупп/Dобщ
'''
eta_squared = D_between / D_overall
print('\n№ 2')
print(f"Корреляционное отношение η² = {eta_squared:.4f}")
print(f"Корреляционное отношение η = {math.sqrt(eta_squared):.4f}")


# 3 - Найти коэффициент ранговой корреляции Спирмена

# X — уникальные значения возраста
X = uniques.copy()

# Y — частоты появления каждого возраста
Y = [number_of_repetitions[x] for x in X]

# присвоение рангов (средний ранг при повторениях)
rank_X = rankdata(X)
rank_Y = rankdata(Y)
print("\n№ 3 — Ранговая корреляция Спирмена")

# print("X(возраст): | Y (частоты): | Ранг X | Ранг Y")
# print("-" * 50)
# for i in range(len(X)):
#     print(f"{X[i]:10} | {Y[i]:8} | {rank_X[i]:10} | {rank_Y[i]:8}")

# Проверяем, есть ли повторяющиеся ранги
unique_ranks_X = len(set(rank_X)) == len(rank_X)
unique_ranks_Y = len(set(rank_Y)) == len(rank_Y)

# Если все ранги уникальны, то простая формула
if unique_ranks_X and unique_ranks_Y:
    d_squared_sum = 0.0
    for i in range(len(rank_X)):
        d_squared_sum += (rank_X[i] - rank_Y[i]) ** 2
    n = len(rank_X)
    r_s = 1 - (6 * d_squared_sum) / (n * (n ** 2 - 1))
    print(f"\nСумма квадратов разностей рангов: {d_squared_sum:.4f}")

else:
    mean_rank_X = sum(rank_X) / len(rank_X)
    mean_rank_Y = sum(rank_Y) / len(rank_Y)

    numerator = 0
    sum_sq_x = 0
    sum_sq_y = 0

    for i in range(len(rank_X)):
        dx = rank_X[i] - mean_rank_X
        dy = rank_Y[i] - mean_rank_Y
        numerator += dx * dy
        sum_sq_x += dx ** 2
        sum_sq_y += dy ** 2

    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    r_s = numerator / denominator if denominator != 0 else 0

    print(f"\nСредние значения рангов: X̄ = {mean_rank_X:.3f}, Ȳ = {mean_rank_Y:.3f}")

print(f"Коэффициент ранговой корреляции Спирмена r_s = {r_s:.4f}")

# if r_s == 1:
#     print("Идеальная положительная монотонная связь: ранги полностью совпадают.")
# elif r_s == -1:
#     print("Идеальная отрицательная монотонная связь: ранги полностью противоположны.")
# elif r_s == 0:
#     print("Отсутствие монотонной связи между переменными.")
# else:
#     direction = "положительная" if r_s > 0 else "отрицательная"
#     abs_r_s = abs(r_s)

#     if 0.1 <= abs_r_s < 0.3:
#         strength = "слабая"
#     elif 0.3 <= abs_r_s < 0.5:
#         strength = "умеренная"
#     elif 0.5 <= abs_r_s < 0.7:
#         strength = "заметная"
#     elif 0.7 <= abs_r_s < 0.9:
#         strength = "высокая"
#     elif 0.9 <= abs_r_s < 1:
#         strength = "весьма высокая"
#     else:
#         strength = "очень слабая или отсутствует"

#     print(f"{strength.capitalize()} {direction} монотонная связь (r_s = {r_s:.4f}).")
