
import re
import sys
sys.path.append('../')

from tarea4.trie import Trie

from utils.utils import Suggester

from tarea4.distances_with_trie import dp_levenshtein_backwards_threshold_trie, dp_restricted_damerau_backwards_threshold_trie


class TrieSpellSuggester(Suggester):
    """
    Clase que implementa el método suggest para la búsqueda de términos y añade el trie
    """

    def __init__(self,vocab):
        super().__init__(vocab)
        self.trie = Trie(self.vocabulary)
        self.IMPLEMENTED_DISTANCES = ['levenshtein','restricted']

    def get_implemented_distances(self):
        return self.IMPLEMENTED_DISTANCES

    def suggest(self, term, distance="levenshtein", threshold=None):

        assert distance in self.get_implemented_distances()

        if distance == 'levenshtein':
            words = dp_levenshtein_backwards_threshold_trie(self.trie, term, threshold)
        if distance == 'restricted':
            words = dp_restricted_damerau_backwards_threshold_trie(self.trie, term, threshold)
        # if distance == 'intermediate':
        #     d = distances_with_threshold.dp_intermediate_damerau_backwards_with_threshold(term, word, threshold)
        # if d <= threshold:
        #     results[word] = d


        result = {}
        for w,d in words:
            result[self.trie.get_output(w)] = int(d)
        return result




if __name__ == "__main__":

    spellSuggesterTrie = TrieSpellSuggester("../corpus/quijote.txt")
    for distance in ['restricted',]: #['levenshtein','restricted','intermediate']
        destiny =  f'result_{distance}_quijote.txt'
        with open(destiny, "w", encoding='utf-8') as fw:
            for palabra in ("casa", "senor", "jabón", "constitución", "ancho", "savaedra", "vicios", "quixot", "s3afg4ew"):
                for threshold in range(1, 6):
                    result = spellSuggesterTrie.suggest(palabra, distance, threshold)
                    numresul = len(result)
                    print(str(threshold) + ': ' + str(numresul))
                    resul = " ".join(sorted(f'{int(v)}:{k}' for k,v in result.items()))
                    fw.write(f'{palabra}\t{threshold}\t{numresul}\t{resul}\n')
                    print("-------------")


