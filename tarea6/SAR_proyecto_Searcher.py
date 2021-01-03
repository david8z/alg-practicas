# -*- coding: utf-8 -*-
##################################################
##                                              ##
##            RECUPERADOR DE NOTICIAS           ##
##                   Version -1                 ##
##                                              ##
##              NO OPTIMIZADO !!                ##
## NO se puede utilizar PARA el proyecto de SAR ##
##                                              ##
##################################################

import pickle
import sys
sys.path.append('../')
from tarea4.trie_spell_suggest import TrieSpellSuggester as suggester
import itertools

import argparse  

def load_object(indexfile):
    with open(indexfile, 'rb') as fh:
        object = pickle.load(fh)
    return object

def buscar_aproximados(index, term, distancia, threshold):
    suggesterObject = suggester(list(index.keys()))
    return list(dict.fromkeys(
        itertools.chain.from_iterable(
        [index[word] for word, _ in suggesterObject.suggest(term, distancia, threshold).items() ]
            )
        ))

def solve_query(index, N, query, aproximada, distancia, threshold):
    """
    FUNCION NO ACEPTABLE PARA EL PROYECTO DE SAR !!!
    """

    spt = query.split()
    i = 0
    if spt[i] == 'not':
        neg, i = True, i + 1
    else:
        neg = False
    term = spt[i]
    try:
        l1 = index[term]
    except KeyError:
        # Buscamos un termino aproximado si 'aproximado == True'
        l1 = buscar_aproximados(index, term, distancia, threshold) if aproximada else  []
    if neg:
        l1 = sorted(set(range(N)).difference(l1))
    i += 1
    while i < len(spt):
        conn = spt[i]
        neg, i = False, i + 1
        if spt[i] == 'not':
            neg, i = True, i + 1
        term = spt[i]
        try:
            l2 = index[term]
        except KeyError:
            # Buscamos un termino aproximado si 'aproximado == True'
            l2 = buscar_aproximados(index, term, distancia, threshold) if aproximada else  []
        if neg:
            l2 = sorted(set(range(N)).difference(l2))
        l1 = solve_conn(conn, l1, l2)
        i += 1
    return l1


def solve_conn(conn, l1, l2):
    """
      FUNCION NO ACEPTABLE PARA EL PROYECTO DE SAR !!!
    """
    r = set(l1)
    if conn == 'and':
        # AND sin negaciones
        r = r.intersection(l2)
    elif conn == 'or':
        # OR sin negaciones
        r = r.union(l1, l2)
    return sorted(r)


def solve_query_list( index, N, fname, aproximada, distancia, threshold):
    with open(fname,encoding='utf-8') as fh:
        ql = fh.read().split('\n')
    # He eliminado el -1 ya que o sino no ejecutaba la última query de la lista de palabras
    # for query in ql[:-1]:
    for query in ql[:]:
        if len(query) > 0:
            r = solve_query(index, N, query.lower(), aproximada, distancia, threshold)
            print("%s\t%d" % (query, len(r)))


def syntax():
    # -a si se quiere activa la busqueda aproximada, vacío si no
    print("python %s indexfile query_list [ distancia ] [threshold]" % sys.argv[0])
    print(sys.argv)
    sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--index_file", default='indexfile_2015',type=str)
    parser.add_argument("--ql_file", default='listapalabras.txt',type=str)
    parser.add_argument("--aproximada", default=True, type=bool)
    # Por defecto, levenshtein porque es el más rápido
    parser.add_argument("--distancia",default='levenshtein',choices=['levenshtein','restricted','intermediate'])
    parser.add_argument('--threshold',type=int, default=2)
    parser.add_argument('--query',type=str, default="",nargs='+')
    
    args = parser.parse_args()

    (index, nnews) = load_object("indexfiles/" + args.index_file)
    if args.query:
        print(len(solve_query(index, nnews, ' '.join(args.query).lower(), args.aproximada, args.distancia, args.threshold)))
        sys.exit()

    solve_query_list(index, nnews, args.ql_file, args.aproximada, args.distancia, args.threshold)

