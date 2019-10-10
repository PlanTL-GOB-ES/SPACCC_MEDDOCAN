#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter

def imprimirSalida(archivo,salida, datos, etiquetas, actual, metricas, verbose):

    d = str("%.3f" % (float(metricas['errores_T'])/float(metricas['numero_T']) * 100))
    d1 = d.replace('.', ',')
    d = str("%.3f" % (float(metricas['errores_S'])/float(metricas['numero_S']) * 100))
    d2 = d.replace('.', ',')
    d = str("%.3f" % (float(metricas['errores_POS'])/float(metricas['numero_T']) * 100))
    d3 = d.replace('.', ',')
    
    ## Informacion para mostrar en terminal
    if verbose:
        print("Porcentaje de discrepancias en el token: %s" % (d1) + "%")
        print("Porcentaje de discrepancias en el split: %s" % (d2) + "%")
        print("Porcentaje de discrepancias en la etiqueta: %s" % (d3) + "%")
        print("Numero de tokens: %d" % (metricas['numero_T']))
        print("Numero de splits: %d" % (metricas['numero_S']))
    
    ## Informacion para guardar en csv
    linea = "%s;%s;%s;%s;%d;%d;%d;%d;%d;%d;%s;%s;%s;%s;" % (archivo.split('/')[-1:],d1, d2, d3, metricas['numero_T'], metricas['numero_T_A'][0], metricas['numero_T_A'][1], metricas['numero_S'], metricas['numero_S_A'][0], metricas['numero_S_A'][1],  etiquetas['n_disc_etiquetas1'].most_common(), etiquetas['n_disc_etiquetas2'].most_common(), etiquetas['pares_disc_etiquetas'].most_common(), etiquetas['etiquetas_disc'])
    f = open(salida, "a")
    f.write(linea)
    f.write("\n")
    f.close()
    
def soluciona_tokens(datos,actual,metricas):
    # Tratamos de hacer coincidir de nuevo los tokens, por tanto mientras no sea asi:
    while actual['tokens'][0] != actual['tokens'][1]:
        # Identificamos el token largo y el corto
        largo = 0 if len(actual['tokens'][0])>len(actual['tokens'][1]) else 1
        corto = (largo+1)%2
        # Si el corto es un fallo de split lo contamos
        if actual['tokens'][corto]=='\n':
            metricas['numero_S'] += 1
            metricas['errores_S'] += 1
            metricas['numero_S_A'][corto] += 1
        # En caso contrario cortamos al token largo la longitud del corto y eliminamos '_' al principio
        else:
            actual['tokens'][largo] = actual['tokens'][largo][len(actual['tokens'][corto]):].lstrip('_')
            metricas['numero_T_A'][corto] += 1
        # El token que hemos cortado debe avanzar uno
        actual['lines'][corto] = datos['textos'][corto].readline()
        actual['tokens'][corto] = actual['lines'][corto].split(' ')[0]
    

def discrepancia_POS(etiquetas,actual):
    # Guardamos la discrepancia del POS que ha fallado junto al token de cada anotador
    etiquetas['etiquetas_disc'].append("[ "+actual['POS'][0]+" - "+actual['tokens'][0]+" : "+actual['POS'][1]+" - "+actual['tokens'][1]+" ]")
    # Guardamos discrepancia el anotador 1
    discrepancia_A_1=actual['tokens'][0]+" - "+actual['POS'][0]
    etiquetas['n_disc_etiquetas1'][discrepancia_A_1] += 1
    # Guardamos discrepancia el anotador 2
    discrepancia_A_2=actual['tokens'][1]+" - "+actual['POS'][1]
    etiquetas['n_disc_etiquetas2'][discrepancia_A_2] += 1
    # Guardamos cual ha sido la pareja de POS donde ha habido discrepancia
    discrepancia= "[ "+actual['POS'][0]+" : "+actual['POS'][1]+" ]"
    etiquetas['pares_disc_etiquetas'][discrepancia] += 1


def compararTextos(file1, file2, salida, verbose):

    # Textos anotados
    datos={'textos' : [open(file1),open(file2)]}
    # Discrepancias en etiquetas
    etiquetas={'etiquetas_disc' : [],'n_disc_etiquetas1' : Counter(),'n_disc_etiquetas2' : Counter(),'pares_disc_etiquetas' : Counter()}
    # Valores para el informe
    metricas={'errores_T' : 0,'errores_S' : 0,'errores_POS' : 0,'numero_T' : 0,'numero_T_A' : [0,0],'numero_S' : 0,'numero_S_A' : [0,0]}
    # Linea, token y POS donde se encuentra procesando
    actual={'lines' : ["",""],'tokens' : ["",""],'POS' : ["",""]}

    actual['lines'][0] = datos['textos'][0].readline()
    actual['lines'][1] = datos['textos'][1].readline()
    while actual['lines'][0] and actual['lines'][1]:
        ## Comprobamos errores de split
        if actual['lines'][0] == "\n" or actual['lines'][1] == "\n":
            metricas['numero_S'] += 1
            if actual['lines'][1] != "\n":
                metricas['numero_S_A'][0] += 1
                metricas['errores_S'] += 1
                actual['lines'][0] = datos['textos'][0].readline()
                continue
            if actual['lines'][0] != "\n":
                metricas['numero_S_A'][1] += 1
                metricas['errores_S'] += 1
                actual['lines'][1] = datos['textos'][1].readline()
                continue
            metricas['numero_S_A'][0] += 1
            metricas['numero_S_A'][1] += 1
            actual['lines'][0] = datos['textos'][0].readline()
            actual['lines'][1] = datos['textos'][1].readline()
            continue
        # Comprobamos errores de token
        actual['tokens'][0] = actual['lines'][0].split(' ')[0]
        actual['tokens'][1] = actual['lines'][1].split(' ')[0]
        actual['POS'][0] = actual['lines'][0].split(' ')[2].rstrip('\n')
        actual['POS'][1] = actual['lines'][1].split(' ')[2].rstrip('\n')
        metricas['numero_T'] += 1
        metricas['numero_T_A'][0] += 1
        metricas['numero_T_A'][1] += 1
        if actual['tokens'][0] != actual['tokens'][1]:
            discrepancia_POS(etiquetas,actual)
            metricas['errores_T'] += 1
            metricas['errores_POS'] += 1
            soluciona_tokens(datos,actual,metricas)
        # Comprobamos errores de etiqueta
        elif actual['POS'][0] != actual['POS'][1]:
            discrepancia_POS(etiquetas,actual)
            metricas['errores_POS'] += 1
        actual['lines'][0] = datos['textos'][0].readline()
        actual['lines'][1] = datos['textos'][1].readline()

    datos['textos'][0].close()
    datos['textos'][1].close()

    imprimirSalida(file1, salida, datos, etiquetas, actual, metricas, verbose)
    return metricas['errores_S'], metricas['numero_S'], metricas['errores_POS'], metricas['errores_T'], metricas['numero_T'], etiquetas['n_disc_etiquetas1'], etiquetas['n_disc_etiquetas2'] ,etiquetas['pares_disc_etiquetas']
