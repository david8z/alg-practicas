import numpy as np

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

def dp_levenshtein_backwards_threshold(term, ref, threshold):
    """
    Calcula la distancia de Levenshtein entre las cadenas term y ref
    con un umbral maximo threshold
    """
    mat = matriz(term, ref)
    res = np.zeros(shape=(len(term)+1,len(ref)+1))
    for i in range(0,len(term)+1):
        for j in range(0,len(ref)+1):
            if i==0 or j==0:
                res[i,j] = res[i,j] + i + j
            else:
                
                res[i,j] =min(
                    mat[i-1,j-1] + res[i-1,j-1],
                    1 + res[i-1,j],
                    1 + res[i,j-1]
                )
                if (res.diagonal() > threshold).any():
                    return None
    return res[len(term),len(ref)]


def levenshtein_active_states(ref,term,threshold):
    mat = matriz(term,ref)
    current = np.zeros((len(term)+1))
    prev = np.arange(0,len(term)+1)
    # prev representa la columna anterior
    for i in range(1,len(ref)+1):
        current[0] = prev[0] + 1
        for j in range(1,len(term) + 1):
            cond = ref[i-1] == term[j-1]
            current[j] = min(
                    cond * 1 + prev[j-1],
                    1 + prev[j],
                    1 + current[j-1]
                )
            if i == j and current[j]>threshold:
                return None
        prev = current
    return current[len(term)]

def dp_intermediate_damerau_backwards_with_threshold(x, y, threshold):
    """
    Calcula la distancia de Damerau Levenshtein no restringida entre las cadenas x y y, con cota de malla

    """
    
    M = init_matriz(x, y)

    for i in range(1, len(x) + 1):
        print(M)

        # Tarea 2 punto 1 - Establecer límites en el recorrido para que solamente 
        # se calculen aquellas partes del grafo de dependencias que tengan sentido para dicho umbral.
        # Por ejemplo: zonas relativamente cercanas a la diagonal principal de la matriz.
        lower_y = max(1, i - threshold)
        upper_y = min(len(y) + 1, i + threshold)

        for j in range(lower_y, upper_y):

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
        if min(M[:,j]) > threshold : return None
    print(M)
    return M[len(x), len(y)]