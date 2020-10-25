import numpy as np
def matriz(term, ref):
    """
    Metodo de las transparencias
    """
    vref = np.array(list(ref))
    return np.vstack([vref != letter for letter in term]) + 0

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