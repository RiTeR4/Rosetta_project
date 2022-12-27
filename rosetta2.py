import jsonpickle
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, log
import pandas as pd

#  Consts
R_Earth = 600000  # Радиус Земли, м
G_M_Earth = 6.674 * 5.9722 * 10 ** 13  # Гравитационная постоянная * масса Земли
geostationary_orbit_h = 35786000  # Высота геостационарной орбиты над экватором, м
M = 0.029  # Молярная масса воздуха, кг/моль
R = 8.314  # Универсальная газовая постоянная
T0 = 19  # Температура , град Цельсия
P0 = 760  # Давление, мм ртутного столба
# Общие параметры ракеты
# Зависимость коэффициента лобового аэродинамического сопротивления от числа Маха
Cx = [[0, 0.165], [0.5, 0.149], [0.7, 0.175], [0.9, 0.255], [1, 0.304], [1.1, 0.36], [1.3, 0.484], [1.5, 0.5],
      [2, 0.51], [2.5, 0.502], [3, 0.5], [3.5, 0.485], [4, 0.463], [4.5, 0.458], [5, 0.447]]
s = 1021.04
g = 9.81

# Get height from game stats
data = pd.read_csv('Выход на орбиту Земли.csv')
Altitudes = data['AltitudeFromTerrain']
Time = data['Time']
KSP_Velocity = data['Velocity'][:65]

json_file = open("data.json", 'r').read()
params = jsonpickle.decode(json_file)
F_min = params['F_min']
F_min2 = params['F_min2']
sigma_1 = params['sigma_1']
alpha1 = params['alpha1']
betta1 = params['betta1']
alpha2 = params['alpha2']
betta2 = params['betta2']
k1 = params['k1']
k2 = params['k2']
M_max = params['M_max']
M_max2 = params['M_max2']


# Метод для получения значения из таблицы коэффициентов лобового аэродинамического сопротивления
def GetCx(M):
    for i in range(len(Cx) - 1):
        if M == Cx[i][0]:
            return Cx[i][1]
        elif Cx[i][0] < M < Cx[i + 1][0]:
            return (Cx[i][1] + Cx[i + 1][1]) / 2
    return Cx[len(Cx) - 1][1]


# Зависимость температуры от высоты (T в град Цельсия)
def Temperature(h, T0):
    temp = h * (-0.0065) + T0
    if temp < 4 - 273.15:
        temp = 4 - 273.15
    return temp


# Зависимость давления от высоты
def Pressure(h, P0):
    return (P0 * 133.32) * np.exp(-(M * 9.81 * h) / (R * (Temperature(h, T0) + 273.15)))


# Зависимость плотности воздуха от высоты
def Density(h):
    if h >= 50000:
        return 0
    T = Temperature(h, T0) + 273.15
    P = Pressure(h, P0)
    return (P * M) / (R * T)


#  Formulas for 65-255
# f1 = (F_min2 - k * np.linalg.norm(x)) * np.sin(alpha2 + betta2 * t) / (M_max2 - k2 * t)
# f2 = (F_min2 - k * np.linalg.norm(y)) * np.cos(alpha2 + betta2 * t) / (M_max2 - k2 * t) - g

i = 0


def main():
    def f(t, x):
        global i
        x, y = x
        k = GetCx(M) * Density(Altitudes[i]) * s / 2
        i += 1
        f1 = (F_min + sigma_1 * t - k * np.linalg.norm(x)) * np.sin(alpha2 + betta2 * t) / (M_max - k1 * t)
        f2 = (F_min + sigma_1 * t - k * np.linalg.norm(y)) * np.cos(alpha2 + betta2 * t) / (M_max - k1 * t) - g

        return f1, f2

    sol = solve_ivp(f, [0, 65], [0, 0], method='BDF')
    t = sol.t
    x, y = sol.y
    velocity = [0] * len(x)
    for i in range(len(x)):
        velocity[i] = sqrt(x[i] ** 2 + y[i] ** 2)

    KSP_Velocity_short = []
    for i in range(len(t)):
        if int(t[i]) == 65: t[i] -= 1
        KSP_Velocity_short.append(KSP_Velocity[int(t[i])])

    # print(t)
    # print(velocity)
    # print(KSP_Velocity_short)

    # plotting data

    fig, ax = plt.subplots()
    plt.plot(t, velocity, label='model')
    plt.plot(t, KSP_Velocity_short, label='ksp')
    ax.set_xlabel('время (с)')
    ax.set_ylabel('скорость (м/с)')
    plt.title("Velocity 0-65 secs", fontsize=25, color="black")
    plt.legend()
    plt.show()

    # table data
    # print('Time model ksp')
    # for i in range(len(KSP_Velocity_short)):
    #     print(f'{int(t[i])} {str(KSP_Velocity_short[i])} {int(velocity[i])}')


if __name__ == '__main__':
    main()
