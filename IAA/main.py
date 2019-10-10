#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import script
import sys

from script import *
from collections import Counter

def prepararSalida(fichero):
    """ Preparamos el fichero de salida escribiendo los headers. """
    f= open(fichero,"w+")
    f.write("texto; disc. token (%); disc. split (%); disc. etiquetas (%); numero de tokens para %;numero de tokens anotador 1; numero de tokens anotador 2; numero de split para %; numero de split anotador 1; numero de split anotador 2; POS disc. anotador1; POS disc. anotador2; pares discrepantes (POS anotador1 : POS anotador2);discrepancias POS (POS1 - token1 : POS2 - token2);")
    f.write("\n")



""" Codigo del script """
#salida = input("Introduce el nombre del fichero de salida:")
#carpeta1 = input("Introduce el nombre de la carpeta con los textos del autor A:")
#carpeta2 = input("Introduce el nombre de la carpeta con los textos del autor B:")
#aux=""
#while aux!='y' and aux!='n':
#    aux = input("Introduce si quieres que se muestren en terminal los datos [Y/n]:").lower()
#    if aux=='y' or not aux:
#        aux = 'y'
#        verbose = True
#    elif aux == 'n':
#        verbose = False
salida = sys.argv[1]
carpeta1 = sys.argv[2]
carpeta2 = sys.argv[3]
verbose = False


if verbose:
    print("----------------------------------------------------------------")


prepararSalida(salida)
errores_S, numero_S, errores_POS, errores_T, numero_T, errores_S_aux, numero_S_aux, errores_POS_aux, errores_T_aux, numero_T_aux = [0]*10
etiquetas1=Counter()
etiquetas_aux1=Counter()
etiquetas2=Counter()
etiquetas_aux2=Counter()
etiquetas3=Counter()
etiquetas_aux3=Counter()

for f in os.listdir(carpeta1):
    print(f)
    if os.path.isfile(carpeta2 + "/" + f) == False:
        print("[ERROR] El fichero %s de la carpeta %s no tiene equivalente en la carpeta %s" % (f, carpeta1, carpeta2))
    else:
        try:
            errores_S_aux, numero_S_aux, errores_POS_aux, errores_T_aux, numero_T_aux, etiquetas_aux1, etiquetas_aux2, etiquetas_aux3 = compararTextos(carpeta1 + "/" + f, carpeta2 + "/" + f, salida, verbose)
            errores_S += errores_S_aux
            numero_S += numero_S_aux
            errores_POS += errores_POS_aux
            errores_T += errores_T_aux
            numero_T += numero_T_aux
            etiquetas1 = etiquetas1+etiquetas_aux1
            etiquetas2 = etiquetas2+etiquetas_aux2
            etiquetas3 = etiquetas3+etiquetas_aux3
        except Exception as e:
            print("[ERROR] Fallo al analizar los textos %s" % f)
            print(e)
        if verbose:
            print("----------------------------------------------------------------")

for f in os.listdir(carpeta2):
    if os.path.isfile(carpeta1 + "/" + f) == False:
        print("[ERROR] El fichero %s de la carpeta %s no tiene equivalente en la carpeta %s" % (f, carpeta2, carpeta1))

d = str("%.3f" % (float(errores_T)/float(numero_T) * 100))
d1 = d.replace('.', ',')
d = str("%.3f" % (float(errores_S)/float(numero_S) * 100))
d2 = d.replace('.', ',')
d = str("%.3f" % (float(errores_POS)/float(numero_T) * 100))
d3 = d.replace('.', ',')
linea = "Total:;%s;%s;%s;;;;;;;%s;%s;%s" % (d1, d2, d3, etiquetas1.most_common(), etiquetas2.most_common(), etiquetas3.most_common())
f = open(salida, "a")
f.write(linea)
f.close()
