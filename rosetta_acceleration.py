import matplotlib.pyplot as plt
from math import sin,cos,sqrt
import pandas as pd



# Consts
Fmin = 2203000  # H
Fmin3 = 1800000  # подгон для скорости
Fmin2 = 500000
K1 = 947.69  # km/sec
K_for_speed = 1095  # km/sec
K2 = 185.68  # km/sec
p = 3.5  # H/c
M1 = 127630  # kg
M2 = 66030  # kg
a1 = 0
b1 = 0.004027682135  # град/c
a2 = 0.2617993878
b2 = 0.0051128048153846  # град/c
g = 9.81

data = pd.read_csv('Выход на орбиту земли с ускорением.csv')
Time = data['Time']

fig, ax = plt.subplots()

# Accelaration from KSP
Acceleration = data['Acceleration']
plt.xlabel('Time')
plt.plot(Time[:65], Acceleration[:65], label='ksp')

# Calculate Accelaration
valuation_x1 = [0]*65
valuation_y1 = [0]*65
valuation_sqrt = [0]*65
valuation_x2 = [0]*190
valuation_y2 = [0]*190
valuation2_sqrt = [0]*190

for i in range(65):
    valuation_x1[i] = (Fmin + p * Time[i]) * sin(a1 + b1 * Time[i]) / (M1 - K1*Time[i])
    valuation_y1[i] = (Fmin + p * Time[i]) * cos(a2 + b2 * Time[i]) / (M1 - K1 * Time[i]) - g
    valuation_sqrt[i] = sqrt(valuation_x1[i]**2 + valuation_y1[i]**2)

# plotting the data
# plt.plot(Time[:65], valuation_x1, label="x1''")
# plt.plot(Time[:65], valuation_y1, label="y1''")
plt.plot(Time[:65], valuation_sqrt, label='model')



plt.title("Accelaration 0 - 65 secs", fontsize=25, color="black")
ax.set_xlabel('время (с)')
ax.set_ylabel('ускорение (м/с^2)')
plt.legend()
plt.show()