import numpy as np
import matplotlib.pyplot as plt


def function(x):
    return np.exp(x) + x


# вычисление произведения элементов в методе Лагранжа (лагранжевы многочлены влияния)
def multiplyLagrange(x0, x, n, index):
    
    multiply = 1
    
    for i in range(0, n):
        if index != i:
            multiply = multiply * (x0 - x[i])/(x[index] - x[i])
    
    return multiply


# интерполяционный многочлен Лагранжа
def polynomOfLagrange(x0, x, n):
    summary = 0
    
    for i in range(0, n):
        summary = summary + function(x[i]) * multiplyLagrange(x0, x, n, i)
    
    return summary


# Разделенные разности
def divideddifference(x, n):
    if n > 2:
        x1 = np.zeros(n-1)
        x2 = np.zeros(n-1)
        for i in range(0, n):
            if i != n - 1:
                x1[i] = x[i]
            if i != 0:
                x2[i - 1] = x[i]
        return (divideddifference(x1, n - 1) - divideddifference(x2, n - 1)) / (x[0] - x[n - 1])

    if n == 2:
        return (function(x[0]) - function(x[1])) / (x[0] - x[1])
    if n == 1:
        return function(x[0])

        
# вычисление произведения элементов в методе Ньютона
def multiplyNewton(x0, x, n):
    multiply = 1

    for i in range(0, n):
            multiply = multiply * (x0 - x[i])

    return multiply


# интерполяционный многочлен Ньютона
def polynomOfNewton(x0, x, n):

    summary = 0
    for i in range(0, n):
        dd = divideddifference(x, i+1)
        summary = summary + dd * multiplyNewton(x0, x, i)
    
    return summary


x0 = -0.5
x = [[-2, -1, 0, 1],[-2, -1, 0, 1, 2]]

print("Получим ошибки в точке X* для метода Лагранжа:")
for x_ in x:
  lagr = polynomOfLagrange(x0, x_, len(x_))

  print("L" + str(len(x_) - 1) + "(" + str(x0) + ") = " + str(lagr))
  print("y(" + str(x0) + ") = " + str(function(x0)))
  print("Ошибка = " + str(abs(function(x0) - lagr)))

test = np.linspace(-2, 2, 10)
y_lagr = np.zeros(len(test))
for i in range(0, len(test)):
    y_lagr[i] = polynomOfLagrange(test[i], xa, n)

fig, ax = plt.subplots()
ax.plot(test, y_lagr)
ax.plot(test, function(test))
ax.legend(["Полином Лагранжа","$e^x+x$"])
plt.xlim()
plt.show()


print("Получим ошибки в точке X* для метода Ньютона:")
for x_ in x:
  newton = polynomOfNewton(x0, x_, len(x_))

  y_newt = np.zeros(len(test))
  for i in range(0, len(test)):
      y_newt[i] = polynomofnewton(test[i], x_, len(x_))

  print("P" + str(len(x_) - 1) + "(" + str(x0) + ") = " + str(newton))
  print("y(" + str(x0) + ") = " + str(function(x0)))
  print("Interpolation error = " + str(abs(function(x0) - newton)))

fig, ax = plt.subplots()
ax.plot(test, y_newt)
ax.plot(test, function(test))
ax.legend(["Полином Ньютона", "$e^x+x$"])
plt.show()
