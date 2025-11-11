import math
import matplotlib.pyplot as plt

# (1)
def excess(data):
    n = len(data)
    mean = sum(data) / n

    # центральные моменты 𝑀[𝑋 − 𝑀(𝑋)^k]
    mu2 = sum((x - mean) ** 2 for x in data) / n # =дисперсия
    mu4 = sum((x - mean) ** 4 for x in data) / n

    sigma = math.sqrt(mu2) # СКО
    excess = mu4 / (sigma ** 4) - 3

    return excess


def asymmetry(data):
    n = len(data)
    mean = sum(data) / n

    # центральные моменты 𝑀[𝑋 − 𝑀(𝑋)^k]
    mu2 = sum((x - mean) ** 2 for x in data) / n # =дисперсия
    mu3 = sum((x - mean) ** 3 for x in data) / n

    sigma = math.sqrt(mu2) # СКО
    asymmetry = mu3 / (sigma ** 3)

    return asymmetry


# (2)

def three_sigms(data):
    n = len(data)
    mean = sum(data) / n

    sigma = math.sqrt(sum((x - mean) ** 2 for x in data) / n)

    count_1 = sum(1 for x in data if mean - sigma <= x <= mean + sigma)
    count_2 = sum(1 for x in data if mean - 2*sigma <= x <= mean + 2*sigma)
    count_3 = sum(1 for x in data if mean - 3*sigma <= x <= mean + 3*sigma)

    # доли распределения
    fractions = [count_1 / n, count_2 / n, count_3 / n]

    expected = [0.683, 0.954, 0.997]

    differences = [0, 0, 0]

    for i in range(3):
        differences[i] = abs(fractions[i] - expected[i])
        if differences[i] >= 0.005:
            print(f'\nИнтервал ±{i + 1}σ:',
                  f'Ожидаемое значение: {expected[i] * 100}%',
                  f'Полученное значение: {fractions[i] * 100}%',
                  f'Разница составляет {differences[i] * 100}% > 0.5%.', sep='\n')
        else:
            print(f'\nИнтервал ±{i + 1}σ:',
                  f'Ожидаемое значение: {expected[i] * 100}%',
                  f'Полученное значение: {fractions[i] * 100}%',
                  f'Разница составляет {differences[i] * 100}% < 0.5%.', sep='\n')
            
    # результаты
    if all(differences[k] < 0.005 for k in range(3)):
        print('\nВывод: правило трёх сигм выполняется → распределение похоже на нормальное.')
    else:
        print('\nВывод: правило трёх сигм не выполняется → распределение ' \
              'отличается от нормального. Cлучайная величина не подлежит правилу трех сигм, '\
              'то есть вероятность отклонений ' \
              'за пределы трех стандартных отклонений от среднего намного выше 0,5%. ' \
              'Такое несоответствие может указывать на наличие аномальных значений (выбросов), ' \
              'искажение данных, или что данные происходят из другого типа распределения, ' \
              'а не из нормального')



f = open('Москва_2021.txt', 'r')
data = [int(i) for i in f.read().split()]
three_sigms(data)
print('\nЭксцесс', excess(data), 'Ассиметрия', asymmetry(data), sep='\n')
print('\nРаспределение слегка смещено вправо (есть более крупные значения, которые тянут хвост вправо)')
print('\nПо форме оно почти нормальное, так как эксцесс очень близок к нулю')


with open("/home/aroya/MSAD/Москва_2021.txt", 'r') as f:
    a = list(map(int, f))
interval = math.ceil((max(a) - min(a))/7)
a.sort()
uniques = list(set(a))

intervals = []
current = min(a)
while current <= max(a):
    intervals.append(current)
    current += interval

amounts = []
for i in range(len(intervals)-1):
    lower_bound = intervals[i]
    upper_bound = intervals[i+1] - 1
    bin_count = sum(a.count(x) for x in uniques if lower_bound <= x <= upper_bound)
    amounts.append(bin_count)

print("накопленные частоты")
s = [amounts[0]]
for i in range(1, len(amounts)):
    k = s[-1] + amounts[i]
    s.append(k)

print(s)

plt.figure(figsize=(12, 8))

sorted_uniques = sorted(uniques)

cumulative_probs = []
current_prob = 0

for value in sorted_uniques:
    prob = a.count(value) / len(a) 
    current_prob += prob
    cumulative_probs.append(current_prob)

x_points = [sorted_uniques[0] - 1] 
y_points = [0]

for i in range(len(sorted_uniques)):
    x_points.append(sorted_uniques[i])
    y_points.append(cumulative_probs[i])
    
    if i < len(sorted_uniques) - 1:
        x_points.append(sorted_uniques[i])
        y_points.append(cumulative_probs[i])
        x_points.append(sorted_uniques[i + 1])
        y_points.append(cumulative_probs[i])

x_points.append(sorted_uniques[-1] + 1)
y_points.append(1.0)

plt.step(x_points, y_points, where='post', linewidth=2, color='blue')
plt.grid(True, alpha=0.3)
plt.xlabel('Значения', fontsize=12)
plt.ylabel('Вероятность', fontsize=12)
plt.title('Статистическая функция распределения (по дискретному ряду)', fontsize=14)
plt.xlim(min(a) - 1, max(a) + 1)
plt.ylim(0, 1.05)

plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth=0.5)
plt.grid(which='minor', linestyle=':', linewidth=0.5)

plt.savefig('images/statistical_distribution_function.png', dpi=300, bbox_inches='tight')
plt.show()
