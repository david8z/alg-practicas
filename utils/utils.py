import re
import numpy as np 

def matriz(x, y):
    """
    Metodo dado en el boletin, matriz que contrasta dos palabras indicando con 0 si son
    el mismo caracter o con 1 si son diferentes
    """
    vy = np.array(list(y))
    return np.vstack([vy != letter for letter in x]) + 0

def init_matriz(x, y):
    """
    Inicia la matriz para calculos con Damerau
    """
    matriz = np.ones((len(x) + 1, len(y) + 1)) * np.inf

    matriz[0] = np.arange(len(y)+1)
    matriz[:][:,0] = np.arange(len(x)+1)

    return matriz

def init_matriz_trie(term_trie, y):
    """
    Inicia la matriz para calculos con Tries
    """
    M = np.ones((term_trie.get_num_states(), len(y) + 1)) * np.inf

    M[0] = np.arange(len(y)+1)
    for i in range(1, term_trie.get_num_states()):
        M[i, 0] = M[term_trie.get_parent(i), 0] + 1

    return M


def hamming_distance(x, y):

    dist_counter = 0

    for n in range(len(x)):
        if x[n] != y[n]:
            dist_counter += 1

    return dist_counter

class Suggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self, vocab):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """
        if isinstance(vocab, str):
            self.vocabulary  = self.build_vocab(vocab, tokenizer=re.compile("\W+"))
        elif isinstance(vocab,list):
            # Necesario para el trie
            self.vocabulary = sorted([w for w in vocab])
        else:
            raise Exception("Vocab is wrong type")

    def build_vocab(self, vocab_file_path, tokenizer):
        """Método para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard('') # por si acaso
            return sorted(vocab)