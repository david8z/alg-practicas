# -*- coding: utf-8 -*-
import re
import sys
sys.path.append('../')

import tarea1.edit_distances as distances
import tarea2.distances_with_threshold as distances_with_threshold

from tarea3.trie import Trie

# def hamming_distance(string1, string2):
#     dist_counter = 0
# 	for n in range(len(string1)):
# 		if string1[n] != string2[n]:
# 			dist_counter += 1
# 	return dist_counter

class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self, vocab_file_path):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """

        self.vocabulary  = self.build_vocab(vocab_file_path, tokenizer=re.compile("\W+"))

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

    def suggest(self, term, distance="levenshtein", threshold=None):

        """Método para sugerir palabras similares siguiendo la tarea 3.

        A completar.

        Args:
            term (str): término de búsqueda.
            distance (str): algoritmo de búsqueda a utilizar
                {"levenshtein", "restricted", "intermediate"}.
            threshold (int): threshold para limitar la búsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
        """
        assert distance in ["levenshtein", "restricted", "intermediate"]

        results = {} # diccionario termino:distancia
        length = len(term)
        for word in self.vocabulary:
            # 1. It is at least the difference of the sizes of the two strings.
            # 2. It is at most the length of the longer string.
            # 3. It is zero if and only if the strings are equal.
            # 4. If the strings are the same size, the Hamming distance is an uppr bound on the Levenshtein distance.
            # 5. The Levenshtein distance between two strings is no greater than the sum of their Levenshtein distances from a third string (triangle inequality).



            # Condicion 3
            if term == word:
                # Si las palabras son iguales la distancia es 0
                results[word] = 0

            # Condicion 2 y 4 No usamos cotas pesimistas
            # if len(term) == len(word):
                #upper = min(max(length, len(word)), hamming_distance(term,word))

            elif threshold is not None:

                lower = abs(length - len(word))

                # Condición 1
                if lower > threshold:
                    d = threshold + 1
                else:
                    if distance == 'levenshtein':
                        d = distances_with_threshold.dp_levenshtein_backwards_threshold(term, word, threshold)
                    if distance == 'restricted':
                        d = distances_with_threshold.dp_restricted_damerau_backwards_threshold(term, word, threshold)
                    if distance == 'intermediate':
                        d = distances_with_threshold.dp_intermediate_damerau_backwards_with_threshold(term, word, threshold)

                results[word] = d
            else:
                if distance == 'levenshtein':
                    d = distances.dp_levenshtein_backwards(term, word)
                if distance == 'restricted':
                    d = distances.dp_restricted_damerau_backwards(term, word)
                if distance == 'intermediate':
                    d = distances.dp_intermediate_damerau_backwards(term, word)
                results[word] = d
        return results

class TrieSpellSuggester(SpellSuggester):
    """
    Clase que implementa el método suggest para la búsqueda de términos y añade el trie
    """
    def __init__(self, vocab_file_path):
        super().__init__(vocab_file_path)
        self.trie = Trie(self.vocabulary)

if __name__ == "__main__":
    spellsuggester = TrieSpellSuggester("./corpora/quijote.txt")
    print(spellsuggester.suggest("alábese"))
    # cuidado, la salida es enorme print(suggester.trie)


