import argparse

import sys
sys.path.append('../')

import pandas as pd

from tqdm import tqdm

import nltk
print('Downloading required nltk files...')
nltk.download(['stopwords','udhr'])
print('--- done')

from tarea3.spell_suggest import SpellSuggester
from tarea4.trie_spell_suggest import TrieSpellSuggester

import time

from nltk.corpus import stopwords, udhr

import random

STATIC_THRESHOLD = 10
MAX_PERTURBACIONES = 4

RESULT_PATH = 'times.csv'

COLUMNS = ['lang','talla_dict','talla_consultas','SpellSuggester_type','alg','iter','elapsed']


def get_word_set(lang,talla):

    stop_words = set(stopwords.words(lang))
    print('\n Stopwords: ',len(stop_words))

    words = udhr.words(lang+'-Latin1')
    words = [w.lower() for w in words if not w in stop_words and w.isalpha()]
    fdist  = nltk.FreqDist(words)
    words = fdist.most_common(talla)
    return words

def perturbar(word):

    word = list(word)

    n_ops = random.randint(0, min(len(word)-1,MAX_PERTURBACIONES))

    for _ in range(0,n_ops):

        op = random.randint(0, 3)

        if op == 0: # borrar
            idx = random.randint(0,len(word)-1)
            word = word[:idx] + word[(idx+1):]
        elif op == 1: # cambiar
            idx = random.randint(0,len(word)-1)
            char = chr(random.randint(ord('a'),ord('z')+1))
            word[idx] = char
        elif op == 2: # trasposicion
            idx = random.randint(0,len(word)-2)
            tmp = word[idx]
            word[idx] = word[idx+1]
            word[idx+1] = tmp

    return "".join(word)


def get_consultas(word_set,talla):
    consultas = []
    words = list(word_set)
    for _ in tqdm(range(0,talla)):
        w = words[random.randint(0, len(words)-1)]
        consultas.append(perturbar(w))
    return consultas

def main(args):

    results = []

    for lang in tqdm(args.languages,total=len(args.languages),leave=False,desc='Language: ',position=0):
        print('\n'+lang)

        for t_d in tqdm(args.talla_dict,total=len(args.talla_dict),leave=False,desc='Talla del diccionario: ',position=1):

            word_set = get_word_set(lang,t_d)
            print('\n Talla del diccionario ',len(word_set))
            iss = SpellSuggester(word_set)
            tss = TrieSpellSuggester(word_set)

            for t_c in tqdm(args.talla_consultas,total=len(args.talla_consultas),leave=False,desc='Talla de las consultas: ',position=2):

                consultas = get_consultas(word_set,t_c)

                print('\n Spell Suggester Iterativo')
                for alg in iss.get_implemented_distances():

                    print('\n Algoritmo: ',alg)

                    for rep in tqdm(range(0,args.repeat),total=args.repeat,leave=False,desc='Iteracion de repeticion: ',position=3):

                        start = time.time()

                        for consulta in tqdm(consultas,total=len(consultas),leave=True,desc='Consultas: '):
                            _ = iss.suggest(consulta,distance=alg,threshold=STATIC_THRESHOLD)

                        end = time.time()
                        elapsed = end - start

                        results.append({
                            'lang':lang,
                            'talla_dict':t_d,
                            'talla_consultas': t_c,
                            'SpellSuggester_type':'Iterative',
                            'alg':alg,
                            'iter':rep,
                            'elapsed':elapsed
                        })

                print('Spell Suggester Trie')
                for alg in tss.get_implemented_distances():

                    print('\n Algoritmo: ',alg)

                    for rep in tqdm(range(0,args.repeat),total=args.repeat,leave=True,desc='Iteracion de repeticion: '):

                        start = time.time()

                        for consulta in tqdm(consultas,total=len(consultas),leave=True,desc='Consultas: '):
                            _ = tss.suggest(consulta,distance=alg,threshold=STATIC_THRESHOLD)

                        end = time.time()
                        elapsed = end - start

                        results.append({
                            'lang':lang,
                            'talla_dict':t_d,
                            'talla_consultas': t_c,
                            'SpellSuggester_type':'Trie',
                            'alg':alg,
                            'iter':rep,
                            'elapsed':elapsed
                        })


    df = pd.DataFrame(results, columns=COLUMNS)
    print(df.head(df.shape[0]))

    df.to_csv(RESULT_PATH)

    print('\n ---- END PROGRAM')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--talla_dict",nargs='+', default=[20,100,500,2500],type=int)
    parser.add_argument("--languages",nargs='+', default=['Spanish','English'],type=str,choices=['English','Spanish'])
    parser.add_argument("--algorithms",default=['all'],nargs='+',choices=[
        'all',
    ]) # No implementado, siempre con todos
    parser.add_argument('--repeat',type=int,default=3)
    parser.add_argument('--talla_consultas',nargs='+', default=[10,50,250,500,2500],type=int)

    args = parser.parse_args()

    main(args)
