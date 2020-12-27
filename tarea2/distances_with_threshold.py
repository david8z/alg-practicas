import numpy as np

TEST_MODULE_FLAG = True

def matriz(term, ref):
    """
    Metodo de las transparencias
    """
    vref = np.array(list(ref))
    return np.vstack([vref != letter for letter in term]) + 0

def init_matriz(x, y):
    """
    Inicia la matriz para calculos con Damerau
    """
    M = np.ones((len(x) + 1, len(y) + 1)) * np.inf

    M[0] = np.arange(len(y)+1)
    M[:][:,0] = np.arange(len(x)+1)

    return M


# def levenshtein_active_states(ref,term,threshold):
#     mat = matriz(term,ref)
#     current = np.zeros((len(term)+1))
#     prev = np.arange(0,len(term)+1)
#     # prev representa la columna anterior
#     for i in range(1,len(ref)+1):
#         current[0] = prev[0] + 1
#         for j in range(1,len(term) + 1):
#             cond = ref[i-1] == term[j-1]
#             current[j] = min(
#                     cond * 1 + prev[j-1],
#                     1 + prev[j],
#                     1 + current[j-1]
#                 )
#             if i == j and current[j]>threshold:
#                 return None
#         prev = current
#     return current[len(term)]


# def dp_levenshtein_backwards_threshold(term, ref, threshold):
#     """
#     Calcula la distancia de Levenshtein entre las cadenas term y ref
#     con un umbral maximo threshold
#     """
#     mat = matriz(term, ref)
#     res = np.zeros(shape=(len(term)+1,len(ref)+1))
#     for i in range(0,len(term)+1):
#         for j in range(0,len(ref)+1):
#             if i==0 or j==0:
#                 res[i,j] = res[i,j] + i + j
#             else:

#                 res[i,j] =min(
#                     mat[i-1,j-1] + res[i-1,j-1],
#                     1 + res[i-1,j],
#                     1 + res[i,j-1]
#                 )
#                 if (res.diagonal() > threshold).any():
#                     return None
#     return res[len(term),len(ref)]

def dp_levenshtein_backwards_threshold(term, ref, threshold):
    """
    Calcula la distancia de Levenshtein entre las cadenas term y ref
    con un umbral maximo threshold
    """
    mat = matriz(term, ref)
    res = init_matriz(term, ref)

    for i in range(1, len(term) + 1):

        lower_y = max(1, i - threshold) 
        upper_y = min(len(ref), i + threshold)

        for j in range(lower_y, upper_y + 1):
            res[i,j] =min(
                    mat[i-1,j-1] + res[i-1,j-1],
                    1 + res[i-1,j],
                    1 + res[i,j-1]
                )

        if min(res[i,:]) > threshold : return threshold + 1

    return res[len(term),len(ref)]

def dp_restricted_damerau_backwards_threshold(term, ref, threshold):
    """
    Calcula la distancia de Damerau Levenshtein Restringida entre las cadenas ref e term.
    Únicamente añade la función de que si dos carácteres seguidos aparecen al reves estos supone coste 1 en vez de coste 2.
    """
    # Simula el infinito
    INF = len(term) + len(ref)

    mat = matriz(term, ref)
    res = init_matriz(term, ref)

    for i in range(1,len(term)+1):

        lower_y = max(1, i - threshold)
        upper_y = min(len(ref), i + threshold)

        for j in range(lower_y, upper_y + 1):
            if i == 1 or j == 1:
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
        if min(res[i,:]) > threshold : return threshold + 1

    return res[len(term),len(ref)]

def dp_intermediate_damerau_backwards_with_threshold(x, y, threshold):
    """
    Calcula la distancia de Damerau Levenshtein no restringida entre las cadenas x y y, con cota de malla

    """

    M = init_matriz(x, y)

    for i in range(1, len(x) + 1):
        # Tarea 2 punto 1 - Establecer límites en el recorrido para que solamente
        # se calculen aquellas partes del grafo de dependencias que tengan sentido para dicho umbral.
        # Por ejemplo: zonas relativamente cercanas a la diagonal principal de la matriz.
        lower_y = max(1, i - threshold)
        upper_y = min(len(y), i + threshold)

        for j in range(lower_y, upper_y + 1):

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

        # Tarea 2 punto 2 - Detener el algoritmo si, tras calcular una etapa
        # (fila o columna según sea tu algoritmo) se puede asegurar que el coste superará el umbral.
        if min(M[i,:]) > threshold :
            return threshold + 1

    return M[len(x), len(y)]


def general_damerau_levenshtein(x,y):
    return 0 # reemplazar/completar

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
            assert dp_levenshtein_backwards_threshold(x,y, 100) == sol1
        except AssertionError:
            print('Levenshtein failed in x -> ',x,' , y -> ',y)
            print('Output: ',dp_levenshtein_backwards_threshold(x,y, 100))
            print('Expected: ', sol1)

        try:
            assert dp_restricted_damerau_backwards_threshold(x,y,100) == sol2
        except AssertionError:
            print('Restricted levenshtein failed in x -> ',x,' , y -> ',y)
            print('Output: ',dp_restricted_damerau_backwards_threshold(x,y, 100))
            print('Expected: ', sol2)

        try:
            assert dp_intermediate_damerau_backwards_with_threshold(x,y, 100) == sol3
        except AssertionError:
            print('Intermediate levenshtein failed in x -> ', x,' , y -> ',y)
            print('Output: ',dp_intermediate_damerau_backwards_with_threshold(x,y, 100))
            print('Expected: ', sol3)