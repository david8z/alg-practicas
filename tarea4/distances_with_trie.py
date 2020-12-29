import numpy as np

from utils.utils import init_matriz_trie

TEST_MODULE_FLAG = True

# Si al terminar una etapa el menor valor es >threshold se podría parar
# - El nº filas antes era uno más la longitud de una cadena, ahora es el nº estados del Trie.
# - Cuando miras una dependencia vertical en el grafo de dependencia antes venía de la letra anterior
# [i-1,j], ahora con [trie.get_parent(i),j].
# - Cuando miras una dependencia diagonal en el grafo de dependencia era una sustitución que venía de
# [i-1,j-1] y ahora será de [trie.get_parent(i),j-1]. Para determinar si es sustitución o acierto hay que
# consultar trie.get_label(i).
def dp_levenshtein_backwards_threshold_trie(term_trie, ref, threshold):
    """
    term_trie: Trie of term word
    ref: String
    Calcula la distancia de Levenshtein entre las cadenas term y ref
    con un umbral maximo threshold
    """

    # Res: matriz estructura term_trie.get_num_states x len(ref) + 1
    res = init_matriz_trie(term_trie, ref)

    for i in range(0, term_trie.get_num_states()):
        # Si la distancia de el padre es mayor al threshold evitamos j iteraciones
        if min(res[term_trie.get_parent(i), :]) > threshold:
            continue

        for j in range(1, len(ref) + 1):
            res[i,j] = min(
                    res[term_trie.get_parent(i),j-1] if term_trie.get_label(i) == ref[j-1] else 1 + res[term_trie.get_parent(i),j-1],
                    1 + res[term_trie.get_parent(i),j],
                    1 + res[i, j-1]
                )
    result = [(i, res[i, len(ref)]) for i in range(0, term_trie.get_num_states()) if term_trie.is_final(i) and res[i, len(ref)] <= threshold]
    return result



def dp_restricted_damerau_backwards_threshold_trie(term_trie, ref, threshold):
    """
    Calcula la distancia de Damerau Levenshtein Restringida entre las cadenas ref y term.
    Únicamente añade la función de que si dos carácteres seguidos aparecen al reves estos supone coste 1 en vez de coste 2.
    """
    # Simula el infinito
    INF = term_trie.get_num_states()+ len(ref)

    res = init_matriz_trie(term_trie, ref)


    for i in range(0, term_trie.get_num_states()):
        for j in range(1, len(ref) + 1):
            if term_trie.is_leaf(i):
                continue
            for child_st in term_trie.iter_children(i):
                if j == 1:
                    res[child_st, j] = min(
                        res[i,j-1] if term_trie.get_label(child_st) == ref[j-1] else 1 + res[i,j-1],
                        1 + res[i, j],
                        1 + res[child_st, j-1]
                    )
                else:
                    res[child_st, j] = min(
                        res[i,j-1] if term_trie.get_label(child_st) == ref[j-1] else 1 + res[i,j-1],
                        1 + res[i, j],
                        1 + res[child_st, j-1],
                        1 + res[term_trie.get_parent(i), j-2] if term_trie.get_label(term_trie.get_parent(i)) == ref[j-1] and term_trie.get_label(i) == ref[j-2] else INF
                    )
    result = [(i, res[i, len(ref)]) for i in range(0, term_trie.get_num_states()) if term_trie.is_final(i) and res[i, len(ref)] <= threshold]

    return result
