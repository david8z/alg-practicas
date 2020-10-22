import numpy as np

def matriz(term, ref):
   """
   Metodo dado en el boletin
   """
   vref = np.array(list(ref))
   return np.vstack([vref != letter for letter in term]) + 0


def levenshtein(term, ref):
   """
   Calcula la distancia de Levenshtein entre las cadenas term y ref
   """
   mat = matriz(term, ref)
   res = np.zeros(shape=(len(term)+1,len(ref)+1))
   for i in range(0,len(term)+1):
      for j in range(0,len(ref)+1):
            if i==0 or j==0:
               res[i,j] = res[i,j] + i + j
            else:
               res[i,j] =min(
                  mat[i-1,j-1] + res[i-1,j-1],
                  1 + res[i-1,j],
                  1 + res[i,j-1]
               )
               
   return res[len(term),len(ref)]

def damerau_levenstein_restringida(term, ref):
   """
   Calcula la distancia de Damerau Levenshtein Restringida entre las cadenas term y ref
   """
   # Simula el infinito
   INF = len(term) + len(ref)

   mat = matriz(term, ref)
   res = np.zeros(shape=(len(term)+1,len(ref)+1))

   for i in range(0,len(term)+1):
      for j in range(0,len(ref)+1):
            if i==0 or j==0:
               res[i,j] = res[i,j] + i + j
            elif i == 1 or j == 1:
               res[i,j] =min(
                  mat[i-1,j-1] + res[i-1,j-1],
                  1 + res[i-1,j],
                  1 + res[i,j-1],
               )
            else:
               res[i,j] =min(
                  mat[i-1,j-1] + res[i-1,j-1],
                  1 + res[i-1,j],
                  1 + res[i,j-1],
                  1 + res[i-2,j-2] + (mat[i-2,j-1] + mat[i-1,j-2]) * INF
               )
   return res[len(term),len(ref)]
