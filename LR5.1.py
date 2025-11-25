import math
import pandas as pd

with open("Москва_2021.txt", 'r') as f:
    a = list(map(int, f))
groups = 7
interval = math.ceil((max(a) - min(a))/groups)
a.sort()
uniques = list(set(a))
discrete = []
crimes = []
for i in range(len(uniques)):
    age = uniques[i]
    count = a.count(uniques[i])
    discrete.append([age, count])
df = pd.DataFrame(discrete)
crimes = discrete
df.columns = ["возраст преступника (x)", "кол-во преступлений (y)"]
print(df)

print('\nалгоритм структурной идентификации')
structural_identification = []
dependencies_types = ['y = ax + b', 'y = ax^b', 'y = ab^x', 'y = a + b/x', 'y = 1/(ax + b)', 'y = x/(ax + b)', 'y = alnx + b']
for i in dependencies_types:
    if i == 'y = ax + b':
        x1 = (crimes[0][0] + crimes[0][-1])/2
        y1 = (crimes[1][0] + crimes[1][-1])/2
        for j in range(len(crimes[0]) - 1):
            if crimes[0][j] <= x1 <= crimes[0][j+1]:
                xi = crimes[0][j]
                xi1 = crimes[0][j+1]
                break
        for j in range(len(crimes[1]) - 1):
            if crimes[1][j] <= y1 <= crimes[1][j+1]:
                yi = crimes[1][j]
                yi1 = crimes[1][j+1]
                break
        ys = yi + ((yi1 - yi)/(xi1-xi))*(x1-xi)
        s = y1 - ys
        structural_identification.append([i, x1, y1, ys, s])
print(structural_identification)