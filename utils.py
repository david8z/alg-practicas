import numpy as np

def distance(str1, str2):
  d=dict()
  for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
  return d[len(str1)][len(str2)]

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