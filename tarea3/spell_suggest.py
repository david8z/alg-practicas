import re
import sys
sys.path.append('../')

import tarea1.edit_distances as distances
import tarea2.distances_with_threshold as distances_with_threshold

from utils.utils import SpellSuggester


class IterSpellSuggester(SpellSuggester):

    """
    Clase que implementa el método suggest para la búsqueda de términos de manera iterativa.
    """
    
    def __init__(self,vocab):
        super().__init__(vocab)
        self.IMPLEMENTED_DISTANCES = ["levenshtein", "restricted", "intermediate"]

    def get_implemented_distances(self):
        return self.IMPLEMENTED_DISTANCES

    def suggest(self, term, distance="levenshtein", threshold=None):

        assert distance in self.get_implemented_distances()

        results = {} # diccionario termino:distancia
        length = len(term)
        for word in self.vocabulary:

            # Wikipedia Upper and Lower bounds

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
                    continue
                else:
                    if distance == 'levenshtein':
                        d = distances_with_threshold.dp_levenshtein_backwards_threshold(term, word, threshold)
                    if distance == 'restricted':
                        d = distances_with_threshold.dp_restricted_damerau_backwards_threshold(term, word, threshold)
                    if distance == 'intermediate':
                        d = distances_with_threshold.dp_intermediate_damerau_backwards_with_threshold(term, word, threshold)
                    if d <= threshold:
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


