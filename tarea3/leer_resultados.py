# -*- coding: utf-8 -*-
import re

import sys

from spell_suggest import SpellSuggester
from tqdm import tqdm

reg = re.compile(r"(?P<term>\w+)\t(?P<threshold>\d+)\t(?P<numresul>\d+)\t(?P<dict>[^\n]*)")
entry = re.compile(r"(?P<dist>\d+):(?P<term>\w+)")

def syntax():
    # -a si se quiere activa la busqueda aproximada, vacío si no
    print("python %s [ distance ] [ -nv | not verbose ]" % sys.argv[0])
    print(sys.argv)
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) > 3:
        syntax()

    spellSuggester = SpellSuggester("../corpus/quijote.txt")

    if len(sys.argv) >= 2 and sys.argv[1] not in spellSuggester.get_implemented_distances() + ["-nv"]:
        print("DISTANCE NOT SUPPORTED IN CADENA:")
        print(sys.argv[1] + " not in " + str(spellSuggester.get_implemented_distances()))
        sys.exit()

    distances_list = [sys.argv[1], ] if len(sys.argv) != 1 and sys.argv[1] != "-nv" else spellSuggester.get_implemented_distances()
    verbose = False if "-nv" in sys.argv else True

    for distance in distances_list:
        if verbose:
            print("CADENA " + distance.upper())
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
                resul = spellSuggester.suggest(term,distance=distance,threshold=threshold)
                assert(resul == resul_profesor)
