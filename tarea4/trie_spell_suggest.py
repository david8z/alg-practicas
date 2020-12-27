# -*- coding: utf-8 -*-
import re
import sys
sys.path.append('../')

from trie import Trie

from tarea3.spell_suggest import SpellSuggester
from distances_with_trie import dp_levenshtein_backwards_threshold_trie, dp_restricted_damerau_backwards_threshold_trie

class TrieSpellSuggester(SpellSuggester):
    """
    Clase que implementa el método suggest para la búsqueda de términos y añade el trie
    """
    def __init__(self, vocab_file_path):
        super().__init__(vocab_file_path)
        self.trie = Trie(self.vocabulary)


    def suggest(self, term, distance="levenshtein", threshold=None):
        
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

    spellSuggesterTrie = TrieSpellSuggester("../tarea3/quijote.txt")
    for distance in ['restricted',]: #['levenshtein','restricted','intermediate']
        destiny =  f'result_{distance}_quijote.txt'
        with open(destiny, "w", encoding='utf-8') as fw:
            for palabra in ("casa", ):
                for threshold in range(1, 6):
                    result = spellSuggesterTrie.suggest(palabra, distance, threshold)
                    # print(str(i) + ': ' + str(len(result)))
                    # print(result)
                    numresul = len(result)
                    print(str(threshold) + ': ' + str(numresul))
                    resul = " ".join(sorted(f'{int(v)}:{k}' for k,v in result.items()))
                    fw.write(f'{palabra}\t{threshold}\t{numresul}\t{resul}\n')
                    print("-------------")
                    """ Devuelve uno más ya que incluye la cadena vacia."""


