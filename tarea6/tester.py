   # -*- coding: utf-8 -*-
import re

import sys
import os

from tqdm import tqdm


if __name__ == "__main__":

    
    for nombre_fichero in ['2015','2015_01']:
        fichero = f'test_results/test_results_{nombre_fichero}.txt'
        indexfile_name = f'indexfile_{nombre_fichero}'
        num_lines = sum(1 for line in open(fichero, "r"))
        with open(fichero, "r", encoding='utf-8') as fr:
            for i, line  in tqdm(enumerate(fr), total=num_lines):  
                for index, d in enumerate(["levenshtein", "restricted", "intermediate"]):
                    for threshold in [1 ,2, 3]:
                        splited_line = line.split()
                        out = os.popen(f'python SAR_proyecto_Searcher.py --index_file {indexfile_name} --distancia {d} --threshold {threshold} --query {" ".join(splited_line[:-9])}').read()
                        # Devuelve la posicion invertida que ocupa el valor de la d y threshold en la linea
                        posicion = -9 + (3 * index) + threshold - 1
                        try:
                            assert(str(out).strip() == splited_line[posicion])
                        except AssertionError:
                            print(" ".join(splited_line[:-9]), str(out).strip(), "!=", splited_line[-posicion])
