import scipy.special as sc
import matplotlib.pyplot as plt
from math import sin,cos,sqrt,log
import pandas as pd

# https://www.geeksforgeeks.org/data-visualization-using-matplotlib/




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

# accelaration from KSP
Acceleration = data['Acceleration']
plt.xlabel('Time')
plt.plot(Time[:65], Acceleration[:65])


# Accelaration
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
# for i in range(65,256):
#     valuation_x2[i-66] = Fmin2 * sin(a2 + b2 * Time[i]) / (M2 - K2 * Time[i])
#     valuation_y2[i-66] = Fmin2 * cos(a2 + b2 * Time[i]) / (M2 - K2 * Time[i]) - g
#     valuation2_sqrt[i-66] = sqrt(valuation_x2[i-66]**2 + valuation_y2[i-66]**2)

# print(f'valuation_x1{valuation_x1}')
# print(f'valuation_y1{valuation_y1}')
# print(f'valuation_x2{valuation_x2}')
# print(f'valuation_y2{valuation_y2}')

# print('Time a1x                 a1y                  sqrt')
# for i in range(len(valuation_x1)):
#     print(f'{i + 1}    {str(valuation_x1[i])[:16]}    {str(valuation_y1[i])[:16]}  {sqrt(valuation_x1[i]**2 + valuation_y1[i]**2)}')
print('Time model ksp')
for i in range(len(valuation_x1)):
    print(f'{int(Time[i])} {round((sqrt(valuation_x1[i]**2 + valuation_y1[i]**2)),2)} {Acceleration[i]}')

# plotting the data
# plt.plot(Time[:65], valuation_x1, label="x1''")
# plt.plot(Time[:65], valuation_y1, label="y1''")
plt.plot(Time[:65], valuation_sqrt, label='sqrt')



# plt.plot(Time[66:256], valuation_x2, label="x2''")
# plt.plot(Time[66:256], valuation_y2, label="y2''")
# plt.plot(Time[66:256], valuation2_sqrt, label='sqrt')
# plt.xlabel('Time')
# plt.title("Accelaration 66 - 255 secs", fontsize=25, color="green")
# plt.legend()



# Speed with double integral
# speed_x1 = [0]*65
# speed_y1 = [0]*65
# speed_sqrt = [0]*65
# for i in range(65):
#     speed_x1[i] = (-(M1 * p + Fmin * K_for_speed) * cos((a1 * K_for_speed + M1 * b1) / K_for_speed) * sc.expi(sin((b1 * Time[i] - (M1 * b1) / K_for_speed))) - (M1 * p + Fmin * K_for_speed) * sin((a1 * K_for_speed + M1 * b1) / K_for_speed) * sc.expi(cos((b1 * Time[i] - (M1 * b1) / K_for_speed)))) / K_for_speed ** 2 + (p * cos(b1 * Time[i] + a1)) / (b1 * K_for_speed)
#     speed_y1[i] = (-(M1 * p + Fmin * K_for_speed) * sin((M1 * K_for_speed) / K_for_speed + a1) * sc.expi(sin((b1 * Time[i] - (M1 * b1) / K_for_speed))) + (-M1 * p - Fmin * K_for_speed) * cos((M1 * b1) / K_for_speed + a1) * sc.expi(cos((b1 * Time[i] - (M1 * b1) / K_for_speed)))) / K_for_speed ** 2 - (p * sin(b1 * Time[i] + a1)) / (b1 * K_for_speed) - g * Time[i]
#     speed_sqrt[i] = sqrt(speed_x1[i]**2 + speed_y1[i]**2)
#
# plt.plot(Time[:65], speed_x1, label="vx1")
# plt.plot(Time[:65], speed_y1, label="vy1")
# plt.plot(Time[:65], speed_sqrt, label='sqrt')
# plt.xlabel('Time')
# plt.title("Velocity 0 - 65 secs", fontsize=25, color="green")
# plt.legend()


# Speed without integration
# speed_2_x1 = [0]*65
# speed_2_y1 = [0]*65
# speed_2_sqrt = [0]*65
# speed_2_x2 = [0]*190
# speed_2_y2 = [0]*190
# speed_2_sqrt_2 = [0]*190
# for i in range(65):
#     speed_2_x1[i] = (Fmin2 + p * Time[i]) * sin(a1 + b1 * Time[i]) / K1 * log(M1/(M1 - K1*Time[i]))
#     speed_2_y1[i] = (Fmin2 + p * Time[i]) * cos(a1 + b1 * Time[i]) / K1 * log(M1 / (M1 - K1 * Time[i]))
#     speed_2_sqrt[i] = sqrt(speed_2_x1[i] ** 2 + speed_2_y1[i] ** 2)
# for i in range(65,256):
#     speed_2_x2[i-66] = Fmin2 * sin(a2 + b2 * Time[i]) / K2 * log(M2 / (M2 - K2 * Time[i]))
#     speed_2_y2[i-66] = Fmin2 * cos(a2 + b2 * Time[i]) / K2 * log(M2 / (M2 - K2 * Time[i]))
#     speed_2_sqrt_2[i - 66] = sqrt(speed_2_x2[i-66] ** 2 + speed_2_y2[i-66] ** 2)

# print('Time v1x                 v1y                  sqrt')
# for i in range(len(speed_2_x1)):
#     print(f'{i + 1}    {speed_2_x1[i]}    {speed_2_y1[i]}  {sqrt(speed_2_x1[i]**2 + speed_2_y1[i]**2)}')
# print('Time v2x                 v2y                  sqrt')
# for i in range(len(speed_2_x2)):
#     print(f'{i + 66}    {speed_2_x2[i]}    {speed_2_y2[i]}  {sqrt(speed_2_x2[i]**2 + speed_2_y2[i]**2)}')

# plotting the data
# plt.plot(Time[:65], speed_2_x1, label="vx1")
# plt.plot(Time[:65], speed_2_y1, label="vy1")
# plt.plot(Time[:65], speed_2_sqrt, label='sqrt')
# plt.title("Velocity 0-65 secs", fontsize=25, color="green")

# plt.plot(Time[66:256], speed_2_x2, label="vx2")
# plt.plot(Time[66:256], speed_2_y2, label="vy2")
# plt.plot(Time[66:256], speed_2_sqrt_2, label='sqrt')
# plt.title("Velocity 66 - 255 secs", fontsize=25, color="green")
# plt.xlabel('Time')
# plt.legend()


plt.show()
