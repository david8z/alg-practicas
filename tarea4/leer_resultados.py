# -*- coding: utf-8 -*-
import re

import sys

from trie_spell_suggest import TrieSpellSuggester
from tqdm import tqdm

reg = re.compile(r"(?P<term>\w+)\t(?P<threshold>\d+)\t(?P<numresul>\d+)\t(?P<dict>[^\n]*)")
entry = re.compile(r"(?P<dist>\d+):(?P<term>\w+)")

def syntax():
    #  distance si se quiere ejecutar una distancia en especifíco
    # -nv si se quiere evitar la verbosidad útil a la hora de testear todo
    print("python %s [ distance ]  [ -nv | not verbose ]" % sys.argv[0])
    print(sys.argv)
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) > 3:
        syntax()

    trieSpellSuggester = TrieSpellSuggester("../corpus/quijote.txt")

    # Comprobamos que los parametros son correctos
    if len(sys.argv) >= 2 and sys.argv[1] not in trieSpellSuggester.get_implemented_distances() + ["-nv"]:
        print("DISTANCE NOT SUPPORTED IN TREE:")
        print(sys.argv[1] + " not in " + str(trieSpellSuggester.get_implemented_distances()))
        sys.exit()

    distances_list = [sys.argv[1], ] if len(sys.argv) != 1 and sys.argv[1] != "-nv" else trieSpellSuggester.get_implemented_distances()
    verbose = False if "-nv" in sys.argv else True

    # Recorremos todas las distancias comprobando si el output gernerado por nuestro Suggester es igual al output
    # del archivo de los resultados del profesor
    for distance in distances_list:
        if verbose:
            print("TRIE " + distance.upper())
        fichero = f'../result_profesor/result_{distance}_quijote.txt'
        num_lines = sum(1 for line in open(fichero, "r"))
        with open(fichero, "r", encoding='utf-8') as fr:
            for i, line  in tqdm(enumerate(fr), total=num_lines, disable=not verbose):
                matchline = reg.match(line)
                term = matchline.group('term')
                threshold = int(matchline.group('threshold'))
                numresul = int(matchline.group('numresul'))
                resul_profesor = { g.group('term'):int(g.group('dist'))
                    for g in entry.finditer(matchline.group('dict')) }
                assert(numresul == len(resul_profesor))
                resul = trieSpellSuggester.suggest(term,distance=distance,threshold=threshold)

                assert(resul == resul_profesor)
