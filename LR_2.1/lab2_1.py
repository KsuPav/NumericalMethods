
"""lab2_1
"""

import math
import numpy as np
import matplotlib.pyplot as plt


# УСЛОВИЕ
def f(x):
    return 4**x-5*x-2


# ПРОИЗВОДНАЯ 1
def df(x):
    return np.log(4)*np.float_power(4,x) - 5


# ПРОИЗВОДНАЯ 2
def ddf(x):
    return np.log(4)**2*np.float_power(4,x)


# выделенный линейный член x = ф(x)
def phi(x):
    return (np.float_power(4,x)-2)/5


# ПРОИЗВОДНАЯ
def dphi(x):
    return np.log(4)*np.float_power(4,x)/5


# МЕТОД ПРОСТОЙ ИТЕРАЦИИ
def simpleIteration(phi, dphi, a, b, eps=0.001):
    q = max(abs(dphi(a)), abs(dphi(b)))
    x = (a + b) / 2
    k = 0
    go = True
    if q < 1:
        print(f'q = {q} < 1')
    else:
        return
    while go:
        k += 1
        x_cur = phi(x)

        print(f'x: {x_cur}, k: {k}, q/(1-q)*|x_cur - x|: {q * abs(x_cur - x) / (1 - q)}')
        if (q * abs(x_cur - x) / (1 - q)) <= eps:
            go = False

        x = x_cur
        if k == 1000:
            break
    return x_cur


# МЕТОД НЬЮТОНА
def newton(f, df, x0, eps=0.001):
    x = x0
    k = 0
    go = True
    while go:
        k += 1
        x_cur = x - f(x) / df(x)
        print(f'x: {x_cur}, k: {k}, |x_cur - x|: {abs(x_cur - x)}')
        if abs(x_cur - x) <= eps:
            go = False

        x = x_cur


# ГРАФИК
def show(f, df, x, step = 0.5, ddf = None):
    X = np.arange(x[0], x[-1], step)
    Y = [f(i) for i in X]
    dY = [df(i) for i in X]

    if ddf:
        ddY = [ddf(i) for i in X]

    fig, axis = plt.subplots()
    axis.plot(X, Y, label='f')
    axis.plot(X, dY, label='df')

    if ddf:
        axis.plot(X, ddY, label='ddf')

    axis.legend(loc='upper right')
    axis.grid()

    plt.show()


x = np.linspace(-3,5,100)
plt.plot(x,phi(x))
plt.plot(x,x)
plt.plot(x,dphi(x),linestyle='dashed')
plt.ylim(-2,2)
plt.legend(['phi','x','dphi'])
plt.show()


print("Simple iteration:")
x_SI = simpleIteration(phi, dphi, -1, 0, eps = 0.0000001)

print("The value of the function at the found point:")
f(x_SI)


x = np.linspace(-3,5,100)
plt.plot(x,f(x))
plt.plot(x,df(x))
plt.plot(x,ddf(x))
plt.xlim(-3,5)
plt.ylim(-10,10)
plt.hlines(0,-4,10,color='grey')
plt.legend(['f','df','ddf'])
plt.show()


print("Newton method:")
x0 = -0.5
newton(f, df, x0, 0.0000001)
