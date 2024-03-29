import numpy as np
import math

"""Лабораторная работа 1, задача 5, вариант 17"""


# QR АЛГОРИТМ
def QR(a):    
  h = np.zeros((n, n))
  hk = np.zeros((n, n))
  r = np.zeros((n, n))

  E = np.zeros((n, n))
  res_d = 0
  res_x1 = 0
  res_x2 = 0
  res_y1 = 0
  res_y2 = 0

  prev_d = 0
  prev_x1 = 0
  prev_x2 = 0
  prev_y1 = 0
  prev_y2 = 0
  flag = 0
  for i in range(n):
      for j in range(n):
          if i != j:
              E[i][j] = 0
              h[i][j] = 0
          else:
              E[i][j] = 1
              h[i][j] = 1

  counter = 0
  v = np.zeros(n)
  while True:
      counter = counter + 1

      for i in range(n-1):
          norma = get_norm_of_row(a, i)
          signum = 0
          for j in range(0, n):
              if j >= i:
                  v[j] = a[j][i]
                  if i == j:
                      signum = sign(a[j][i])
                      v[j] += signum * norma
              else:
                  v[j] = 0

          hk = multiplyQR(v)

          for k in range(n):
              for j in range(n):
                  if k == j:
                      hk[k][j] = 1 - hk[k][j]
                  else:
                      hk[k][j] = -hk[k][j]

          # получаем матрицу Хаусхолдера
          h = multiply(h, hk)

          # изменяем матрицу А = А*h
          a = multiply(hk, a)
          # получаем верхнетреугольную матрицу r
          if i == n - 2:
              r = multiply(E, a)

      a = multiply(r, h)

      # считаем корень из суммы квадратов поддиагональных элементов
      sum = 0
      for i in range(n-1):
          for j in range(i+1, n):
              end[i] += a[j][i]**2
          sum += end[i]
      sum = math.sqrt(sum)
      # если сумма меньше точности, то выходим
      if sum < epsilon:
          break

      # проверяем, есть ли комплексные собственные значения
      if precheckComplex(a) == 1:

          indexes = checkComplex(a)
          for i in range(n-1):
              flag = 1
              if indexes[i] != -1:
                  res_d, res_x1, res_x2, res_y1, res_y2 = getRoots(a, i)
                  flag = 1
                  if (prev_x1 - res_x1 < epsilon and
                      prev_x2 - res_x2 < epsilon and
                      prev_y1 - res_y1 < epsilon and
                      prev_y2 - res_y2 < epsilon):
                      flag = 0

                  prev_x1 = res_x1
                  prev_x2 = res_x2
                  prev_y1 = res_y1
                  prev_y2 = res_y2

          summ = 0
          for i in range(n-1):
              if indexes[i] != -1:
                  summ += flag
          #  выходим, если разница между комплексными корнями двух
          #  соседних решений меньше заданной точности
          if summ == 0:
              break

      #  обнуляем матрицу Хаусхолдера
      h = multiply(E, E)
  return a, res_x1, res_x2, res_y1, res_y2, flag


# ОПРЕДЕЛЕНИЕ ЗНАКА
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


# ВЫВОД МАТРИЦЫ
def show(a, n):
    for i in range(0, n):
        for j in range(0, n):
            print("\t", a[i][j], " ", end='')
        print("\n")


# 
def precheckComplex(a):
    for j in range(n-2):
        if abs(a[n - 1][j]) > epsilon:
            return 0
    return 1


# ТОЧНОСТЬ
def checkComplex(a):
    indexes_of_nonzero_subdiag = np.zeros(n-1)
    for i in range(n-1):
        indexes_of_nonzero_subdiag[i] = -1
        if abs(a[i + 1][i]) > epsilon:
            indexes_of_nonzero_subdiag[i] = i
    return indexes_of_nonzero_subdiag


# КОРНИ
def getRoots(a, i):
    res_d = 0
    a22 = a[i][i]
    a23 = a[i][i + 1]
    a32 = a[i + 1][i]
    a33 = a[i + 1][i + 1]
    d = (a22 + a33)**2 + 4 * (a23 * a32 - a22 * a33)
    if d < 0:
        d *= -1
        res_d = -1
    else:
        res_d = 1
        
    res_x1 = (a22 + a33) / 2
    res_x2 = (a22 + a33) / 2
    res_y1 = math.sqrt(d) / 2
    res_y2 = -math.sqrt(d) / 2
    res_flag = 0

    return res_d, res_x1, res_x2, res_y1, res_y2


# УМНОЖЕНИЕ МАТРИЦ
def multiply(m1, m2):
    sum = 0  # сумма
    tmp = []  # временная матрица
    ans = []  # конечная матрица
    row1 = len(m1)  # количество строк в первой матрице
    col1 = len(m1[0])  # Количество столбцов в 1
    row2 = col1  # и строк во 2ой матрице
    col2 = len(m2[0])  # количество столбцов во 2ой матрице
    for k in range(0, row1):
        for j in range(0, col2):
            for i in range(0, col1):
                sum = sum + m1[k][i] * m2[i][j]
            tmp.append(sum)
            sum = 0
        ans.append(tmp)
        tmp = []
    return ans


#  функция для получения второго слагаемого формулы
#  для получения матрицы Хаусходера
def multiplyQR(a):
    pr = 0
    ab = np.zeros((n, n))
    for i in range(n):
        pr += a[i] * a[i]
        for j in range(n):
            ab[i][j] = 0
            ab[i][j] = a[i] * a[j]
    pr /= 2
    for i in range(n):
        for j in range(n):
            ab[i][j] /= pr
    return ab


#  НОРМА СТОЛБЦОВ МАТРИЦЫ
def get_norm_of_row(a, row):
    sum = 0
    for i in range(row, n):
        sum += a[i][row]**2
    return math.sqrt(sum)


n = 3
epsilon = 0.0001

a = [ [ -6, 1, -4 ], [ -6, 8, -2 ], [ 2, -9, 5] ]

a, res_x1, res_x2, res_y1, res_y2, flag = QR(a)

print("matrix a---------\n")
show(a, n)
print("SZ: \n")
for i in range(n):
    if i < n - 1:
        if flag == 0:
            if res_d == -1:
                print(f"L{i + 1} = {res_x1} + i({res_y1})\nL{i + 2} = {res_x2} + i({res_y2})\n")
            else:
                print(f"L{i + 1} = {res_x1 + res_y1}\nL{i + 2} = {res_x2 + res_y2}\n")

            i = i + 1
        else:
            print(f"L{i + 1} = {a[i][i]}\n")
    else:
        print(f"L{i + 1} = {a[i][i]}\n")

end = np.zeros(n-1)
a = [ [ -6, 1, -4 ], [ -6, 8, -2 ], [ 2, -9, 5] ]
a_ = a
print("Проверка с помощью linalg:")
x, u = np.linalg.eig(a_)
print('x:\n', x)
print('u:\n')
show(u, len(u))
