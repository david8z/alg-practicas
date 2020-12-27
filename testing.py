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
    res = init_matriz(term, ref)

    for i in range(1, len(term) + 1):
        print(res)
        lower_y = max(1, i - threshold)
        upper_y = min(len(ref) + 1, i + threshold)

        for j in range(lower_y, upper_y): # cond 1
            res[i,j] =min(
                    mat[i-1,j-1] + res[i-1,j-1],
                    1 + res[i-1,j],
                    1 + res[i,j-1]
                )
            print(res)

        if min(res[:,j]) > threshold : return threshold + 1 # cond 2

    return res[len(term),len(ref)]

print(dp_levenshtein_backwards_threshold('cansa', 'casa',1))