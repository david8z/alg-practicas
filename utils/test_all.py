# -*- coding: utf-8 -*-
import re
import os
from multiprocessing import Process
from multiprocessing import Pool

import sys

sys.path.append('../')


def execute( tarea, distance):
    os.system( "python3 ../%s/leer_resultados.py %s -nv" % (tarea, distance))


if __name__ == "__main__":
    """
        Encargado de hacer los test de las tareas 3 y 4 de forma concurrente si el funcionamiento es correcto se ejecuta
        sin devolver nada.
    """
    tareas = ["tarea3", "tarea4"]
    distancias = ["levenshtein", "restricted", "intermediate"]

    for tarea in tareas:
        for distancia in distancias:
            Process(target=execute, args=(tarea, distancia)).start()