import numpy as np
from linalg import gauss,solveBounds

# "ручной" рассчёт главного модуля платлайна, с алгоритмом произошёл затуп
# газы нормированы в 1000, чтобы у матрицы было всё лучше с обусловленностью
A = np.array([
    [1,0,0,0,0,0,-1] # PtMP
    ,[1,0,0,-2,0,0,0] # AqReg
    ,[-0.11,0,0,0,0,0,0] # PlatRes
    ,[-1,18,0,0,0,0,0] # PlC
    ,[0,3.6,0,0,0,0,0] # AmCl
    ,[0,-16,0,0,0,1,0]# PlatSalt
    ,[0,-4,0,0,4,0,0]# RePt
    ,[0,-3.6,0,0,0,0,0]# PdAm
    ,[0,-9,2,0,0,0,0]# NO2
    ,[0,-9,0,1,0,0,0]# Dil. Sulfuric
    ,[0,0,1,0,0,0,0]# O
    ,[0,0,1,0,0,0,0]# Water
    ,[0,0,-2,1,0,0,0]# Nitric
    ,[0,0,0,0,0,-0.9,1]# RPS
    ,[0,0,0,0,0,0,-0.087]# Chlorine
    ,[0,0,0,0,1,0,0]# Ca 
    ,[0,0,0,0,-2,0,0]# Pt
    ,[0,0,0,0,-3,0,0]# CaCl
])
# нормировка в минуты
A[:,0] *= 60/12.5
A[:,1] *= 60/70
A[:,2] *= 60/16
A[:,3] *= 60/1.5
A[:,4] *= 60/1.5
A[:,5] *= 60/30
A[:,6] *= 60/10

B = np.zeros((18,10))
# inputs
B[0,0] = -1
B[4,1] = -1
B[10,2] = -1
B[11,3] = -1
B[15,4] = -1
# outputs
B[2,5] = 1
B[7,6] = 1
B[14,7] = 1
B[16,8] = 1
B[17,9] = 1

a = np.block([A,B])
new_a = gauss(a)
# non-zero rows of transformed matrix
new_a = new_a[[i for i in range(a.shape[0]) if not np.allclose(new_a[i,:],0)],:]
# no boundary conditions added yet, so b is assumed to be zeroes and will not be transformed

x = solveBounds(new_a,[(1,2)])
# EV reactor for acid + plat, most of things HV
# EV sifter, EV main reactor
weights = np.array([8,2,4,4,4,8,4])
# new_a = magic(a)
# b = np.zeroes(18) - a[bound]*boundval
# x = np.solve(new_a, b)
# значения в x это то, из чего можно выбирать ограничения: первые 7 (A.shape[2]) значений это множители рецептов, следующие 10(9) --- вводы/выводы
# множители рецептов часто будут больше 1, не волнуемся. Чтобы найти реальные значения количества машин, надо делить на оверклок
print(x[:7]/weights)
