# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from tarea3.spellsuggest import SpellSuggester

import filecmp

def compare_files():
    files = [f'result_{distance}_quijote.txt' for distance in ['levenshtein','restricted','intermediate']]
    return filecmp.cmpfiles('', 'result_profesor', files)


if __name__ == "__main__":

    spellsuggester = SpellSuggester("quijote.txt")
    for distance in ['levenshtein','restricted','intermediate']:
        destiny =  f'result_{distance}_quijote.txt'
        with open(destiny, "w", encoding='utf-8') as fw:
            for palabra in ("casa", "senor", "jabón", "constitución", "ancho", "savaedra", "vicios", "quixot", "s3afg4ew"):
                for threshold in range(1, 6):
                    resul = spellsuggester.suggest(palabra,distance=distance,threshold=threshold)
                    numresul = len(resul)
                    resul = " ".join(sorted(f'{int(v)}:{k}' for k,v in resul.items()))
                    fw.write(f'{palabra}\t{threshold}\t{numresul}\t{resul}\n')

    print(compare_files())


