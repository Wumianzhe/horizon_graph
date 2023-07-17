import numpy as np
import numpy.typing as npt

def gauss(A:npt.NDArray):
    '''Преобразование системы методом Гаусса с частичным упорядочиванием по столбцам'''
    K = min(A.shape)
    for k in range(K):
        m = k + np.argmax(np.abs(A[k:,k]),axis=0)
        if m != k:
            A[[k,m],:] = A[[m,k],:]
        if abs(A[k,k]) < 1e-6:
            break
        for i in range(k+1,A.shape[0]):
            A[i,:] -= A[k,:] * A[i,k] / A[k,k]

    return A

def solveBounds(A:npt.NDArray,bounds:list[tuple[int,int]]):
    '''Решение недоопределённой системы при заданных значениях координат'''
    if A.shape[0] != A.shape[1] - len(bounds):
        # Недостаточно координат
        raise Exception
    b = sum([-A[:,ind]*val for (ind,val) in bounds])
    a = np.delete(A,[ind for (ind,_) in bounds],axis=1)
    shortX = np.linalg.solve(a,b)
    for (ind,val) in bounds:
        shortX = np.insert(shortX,ind,val)
    return shortX
