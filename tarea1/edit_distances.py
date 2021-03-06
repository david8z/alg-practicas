import numpy as np

from utils.utils import matriz, init_matriz

TEST_MODULE_FLAG = True

def dp_levenshtein_backwards(x, y):
    """
    Calcula la distancia de Levenshtein entre las cadenas x e y.
    """
    mat = matriz(x, y)
    res = np.zeros(shape=(len(x)+1,len(y)+1))
    for i in range(0,len(x)+1):
        for j in range(0,len(y)+1):
                if i==0 or j==0:
                    res[i,j] = res[i,j] + i + j
                else:
                    res[i,j] = min(
                        mat[i-1,j-1] + res[i-1,j-1],
                        1 + res[i-1,j],
                        1 + res[i,j-1]
                    )

    return res[len(x),len(y)]

def dp_restricted_damerau_backwards(x, y):
    """
    Calcula la distancia de Damerau Levenshtein Restringida entre las cadenas x e y.
    Únicamente añade la función de trasposición de caracteres con coste 1.
    """
    # Simula el infinito
    INF = len(x) + len(y)

    mat = matriz(x, y)
    res = np.zeros(shape=(len(x)+1,len(y)+1))

    for i in range(0,len(x)+1):
        for j in range(0,len(y)+1):
                if i==0 or j==0:
                    res[i,j] = res[i,j] + i + j
                elif i == 1 or j == 1:
                    res[i,j] = min(
                        mat[i-1,j-1] + res[i-1,j-1],
                        1 + res[i-1,j],
                        1 + res[i,j-1],
                    )
                else:
                    res[i,j] = min(
                        mat[i-1,j-1] + res[i-1,j-1],
                        1 + res[i-1,j],
                        1 + res[i,j-1],
                        1 + res[i-2,j-2] + (mat[i-2,j-1] + mat[i-1,j-2]) * INF
                    )
    return res[len(x),len(y)]


def dp_intermediate_damerau_backwards(x, y):
    """
    Calcula la distancia de Damerau Levenshtein no restringida entre las cadenas x e y, con cota de malla.
    """

    M = init_matriz(x, y)

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):

            if x[i - 1] == y[j - 1]:
                initActual = min(M[i-1, j] + 1, M[i, j-1] + 1, M[i-1][j-1])
            else:
                initActual = min(M[i-1, j] + 1, M[i, j-1] + 1, M[i-1][j-1] + 1)

            if j > 1 and i > 1 and x[i - 2] == y[j - 1] and x[i - 1] == y[j - 2]:
                M[i,j] = min(initActual, M[i-2][j-2] + 1)
            elif j > 2 and i > 1 and x[i-2] == y[j-1] and x[i-1] == y[j-3]:
                M[i,j] = min(initActual, M[i-2][j-3] + 2)
            elif i > 2 and j > 1 and x[i - 3] == y[j-1] and x[i-1] == y[j-2]:
                M[i,j] = min(initActual, M[i-3][j-2] + 2)
            else:
                M[i,j] = initActual

    return M[len(x), len(y)]

# TEST MODULE
if TEST_MODULE_FLAG:

    tests = [("algoritmo","algortimo",2.0,1.0,1.0),
            ("algoritmo","algortximo",3.0,3.0,2.0),
            ("algoritmo","lagortimo",4.0,2.0,2.0),
            ("algoritmo","agaloritom",5.0,4.0,3.0),
            ("algoritmo","algormio",3.0,3.0,2.0),
            ("acb","ba",3.0,3.0,2.0)]

    for x,y,sol1,sol2,sol3 in tests:

        try:
            assert dp_levenshtein_backwards(x,y) == sol1
        except AssertionError:
            print('Levenshtein failed in x -> ',x,' , y -> ',y)
            print('Output: ',dp_levenshtein_backwards(x,y))
            print('Expected: ', sol1)

        try:
            assert dp_restricted_damerau_backwards(x,y) == sol2
        except AssertionError:
            print('Restricted levenshtein failed in x -> ',x,' , y -> ',y)
            print('Output: ',dp_restricted_damerau_backwards(x,y))
            print('Expected: ', sol2)

        try:
            assert dp_intermediate_damerau_backwards(x,y) == sol3
        except AssertionError:
            print('Intermediate levenshtein failed in x -> ', x,' , y -> ',y)
            print('Output: ',dp_intermediate_damerau_backwards(x,y))
            print('Expected: ', sol3)
