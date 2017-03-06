# -*- coding: utf-8 -*-
"""
Created on Fri May 27 22:08:44 2016
Script que pega o corpus e adiciona uma linha no final, que é o peso silábico 
da penúltima sílaba da palavra
@author: Bruno
"""

#Abrindo o corpus 

arquivo = open('corpus_transcrito.csv', 'r', encoding = 'utf8')


corpus = arquivo.read().split('\n')
corpus_total = []
for item in corpus:
    corpus_total.append(item.split(','))

arquivo.close()
copia = []
for item in corpus_total:
    try:
        if item[0][-1] == 's':
            pass
        else:
            copia.append(item)
    except:
        if item == ['']:
            pass
        else:
            print ('HRURH')
corpus_total = copia
#definindo as grupos de sons relevantes
vogais = '14579!$ae3io0u'
vogais_nasais = 'AEIOU268#%'

consoantes = u'bdDfghjklLmnNprStTvxz'
glides = u'JW'


corpus_total[0].append('PESOPENULT')

for item in corpus_total[1:]:
    transcrita = item[4]
    #se eu inverter a palavra, preciso pegar a primeira letra depois do
    #primeiro '-'
    transcrita = transcrita[::-1]
    alvo = ''
    index = 0
    flag = True
    while flag:
        try:        
            letra = transcrita[index]
            if letra == '-':
                flag = False
                alvo = transcrita[index+1]
            else:
                index += 1
        except:
            flag = False
            alvo = 'blank'
    if alvo in vogais:
        item.append('leve')
    elif alvo == 'blank':
        item.append('blank')
    else:
        item.append('pesado')
        
destino = open('corpus_transcritoPenult.csv', 'w',encoding = 'utf8')

for item in corpus_total:
    string = ''
    for subitem in item:
        string += subitem + ','
    string = string[:-1] + '\n'
    destino.write(string)
    
destino.close()