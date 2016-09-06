# -*- coding: utf-8 -*-
"""
Created on Thu May 12 10:58:44 2016
NAIVE BAYES CLASSIFIER - Implementação
@author: Bruno
"""
import numpy as np
import pandas as pd
from sklearn import cross_validation
#from collections import defaultdict as dft


corpus = pd.read_csv('corpus_transcritoPenult.csv',sep=',',error_bad_lines=False)

def divide_corpus (corpus):
    treino, teste = cross_validation.train_test_split(corpus,test_size=0.2,
                                                 train_size = 0.8)
    return treino, teste    

treino, teste = divide_corpus(corpus)

def treina_modelo(corpus_treino):
    #input é um dataframe, retorna as listas com os valores
    #Dependente - categorias acentuais
    catAc = [x[6] for x in corpus_treino.values]
    #independentes
    #Categoria Morfossintática
    catMorf = [x[1] for x in corpus_treino.values]
    #Peso silábico da última sílaba
    pesoFinal = [x[11] for x in corpus_treino.values]
    #Nível de frequência da palavra
    nivelFreq = [x[12] for x in corpus_treino.values]
    #Estrutura Silábica
    estSilabica = [x[5] for x in corpus_treino.values]
    #segmento final
    segFinal = [x[10] for x in corpus_treino.values]
    #peso penúltima sílaba
    penultSil = [x[13] for x in corpus_treino.values]
    return catAc,catMorf,pesoFinal,nivelFreq,estSilabica,segFinal,penultSil

catAc, catMorf, pesoFinal, nivelFreq, estSilabica,\
        segFinal,penultSil = treina_modelo(treino)

def extrai_priors (lista_de_valores):
    #Função que pega uma lista de valores e retorna um histograma em forma
    #de dicionário. a chave é o nome da classe e o valor é a frequência dela
    histo = {}
    for item in lista_de_valores:
        try:
            histo[item] += 1
        except:
            histo[item] = 1
    histo['Total'] = len(lista_de_valores)
    for item in histo.keys():
        if item == 'Total':
            pass
        else:
            histo[item] = histo[item]/histo['Total']
    return histo


#FREQUENCIAS DAS CATEGORIAS
histCatAc = extrai_priors(catAc)

##CRIANDO VARIÁVEIS PARA GUARDAR OS MEUS PRIORS
priorOx = histCatAc['oxítona']
priorPar = histCatAc['paroxítona']
priorPro = histCatAc['proparoxítona']

#preciso agora calcular as probabilidades de cada um dos
#valores das features de acordo com cada uma das catAcentuais
#depois eu vou gerar para cada palavra teste 3 vetores, que são 
#as infos que já estão no corpus só que mudando a catAc pras
#3 possíveis. 

#preciso criar então dicionarios que estão no formato
# dic_feature = {'valor': [probOx,probPar,probPro], 'valor2'... }
#então pra cada característica eu preciso fazer um dicionario
# cujas chaves são o set dos features e os valores são uma lista com 3 itens
#que são 
def zipa (lista1,lista2):    
    zipada = []
    i = 0
    for item in lista1:
        dupla = (item,lista2[i])
        i += 1
        zipada.append(dupla)
    return zipada
    

def faz_histograma2(lista_de_tuplas):
    #calcula o histograma de duas variáveis de cada vez
    set_chaves1 = set([x[0] for x in lista_de_tuplas])    
    hist_tupla = {}
    for chave in set_chaves1:
        #smoothing laplace
        hist_tupla[chave] = {'oxítona':1,'paroxítona':1,'proparoxítona':1}
    for x,y in lista_de_tuplas:
        try:
            hist_tupla[x][y] += 1
        except:
            hist_tupla[x][y] = 1
        try:
            hist_tupla[x]['Total'] += 1
        except:
            hist_tupla[x]['Total'] = 1
    for chave in hist_tupla.keys():
        for chave2 in hist_tupla[chave].keys():
            if chave2!= 'Total':                
                hist_tupla[chave][chave2] /= hist_tupla[chave]['Total'] 
            else:
                pass
    return hist_tupla

#categoria morfossintática
tuplMorfAc = zipa(catMorf,catAc)
histMorfAc = faz_histograma2(tuplMorfAc)
#estrutura silábica
tuplSilAc = zipa(estSilabica,catAc)
histSilAc = faz_histograma2(tuplSilAc)
#peso final
tuplPesoFinalAc = zipa(pesoFinal,catAc)
histPesoAc = faz_histograma2(tuplPesoFinalAc)
#lvl freq
tuplFreqAc = zipa(nivelFreq, catAc)
histFreqAc = faz_histograma2(tuplFreqAc)
#segmento final
tuplSegFinalAc = zipa(segFinal, catAc)
histSegFinalAc = faz_histograma2(tuplSegFinalAc)
#Peso penúltima sílaba
tuplPenultSilAc = zipa(segFinal, catAc)
histPenultSilAc = faz_histograma2(tuplPenultSilAc)

#Agora que eu já tenho os dicionários que associam os valores das variáveis
#aos traços, preciso receber uma palavra, transformar ela em vetor
#fazer o cálculo da probabilidade dela diante de cada catAcentual e escolher
#a candidata mais provável.

corpinho = [
['você','V','você','&vo-se*','&vo-s4*','&CV-CV*','oxítona','29544','27949','1595','V','leve',1],
['uma','DET','uma','&u-ma*','&$-ma*','&V-CV*','paroxítona','28659','16421','12238','V','leve',1],
['né','V','né','&n3*','&n5*','&CV*','oxítona','25291','25223','68','V','leve',1],
['assim','ADV','assim','&a-sI*','&1-sI*','&V-CV*','oxítona','24666','23749','917','N','pesado',1],
['tem','V','ter','&tEJ*','&t6J*','&CVG*','oxítona','23936','20599','3337','N','pesado',1],
['para','PRP','para','&pa-ra*','&p1-ra*','&CV-CV*','paroxítona','20496','1563','18933','V','leve',1]
]

corpinho2 = [
['maléfico','NOM','maléfico','&ma-l3-fi-ko*','&ma-l5-fe-ko*','&CV-CV-CV-CV*','proparoxítona',1,1,0,'V','leve',5,'leve'],
['cartório','V','cartório','&kar-t0-rJo*','&kar-t!-rJo*','&CVC-CV-CGV*','paroxítona',31,26,5,'V','leve',4,'leve']
]

def NaiveBayesProb(vetor_palavra,categoria,sextupla):
    '''essa função pega um vetor de palavra e uma categoria acentual
    e retorna a probabilidade desse vetor corresponder aquela categoria.'''
    
    #extraindo os features da palavra    
    catmorf = vetor_palavra[1]
    freq = vetor_palavra[12]
    sil = vetor_palavra[5]
    pesoFinal = vetor_palavra[11]
    segFinal = vetor_palavra[10]
    penultSil = vetor_palavra[13]
    #a probabilidade será dada pelo produto da probabilidade de todos os 
    #valores dos features dada a categoria em questão vezes o prior da cat.
    if sextupla[0] == '1':
        try:
            pcatmorf = histMorfAc[catmorf][categoria]
        except:
            pcatmorf = 1/len(catMorf)
    else:
        pcatmorf = 1
    if sextupla[3] == '1':
        try:
            pfreq = histFreqAc[freq][categoria]
        except:
            pfreq = 1/len(nivelFreq)
    else:
        pfreq = 1
    if sextupla[2] == '1':
        try:
            ppesofinal = histPesoAc[pesoFinal][categoria]
        except:
            ppesofinal = 1/len(pesoFinal)
    else:
        ppesofinal = 1
    if sextupla[1] == '1':
        try:
            psil = histSilAc[sil][categoria]
        except:
            psil = 1/len(estSilabica)
    else:
        psil = 1
    if sextupla[4] == '1':
        try:
            psegfinal = histPesoAc[segFinal][categoria]
        except:
            psegfinal = 1/len(segFinal)
    else:
        psegfinal = 1
    if sextupla[5] == '1':
        try:
            ppenultsil = histPenultSilAc[penultSil][categoria]
        except:
            ppenultsil = 1/len(penultSil)
    else:
        ppenultsil = 1
            
    prior = histCatAc[categoria]
    
    prob = psil*prior*ppesofinal*ppenultsil*pfreq*pcatmorf*psegfinal
    return prob

    
def Classificador(palavra,sextupla='111111'):
    #vetor de palavra tal como está no corpus
    categorias = ['oxítona','paroxítona','proparoxítona']
    dic_probs = {}
    for categoria in categorias:
        dic_probs[categoria] = NaiveBayesProb(palavra,categoria,sextupla)
    ranking = []
    for key, value in dic_probs.items():
        ranking.append((value,key))
    ranking = sorted(ranking,reverse=True)
    return ranking[0][1]
    
    
def avalia_class(lista_de_palavras, sextupla = '111111'):
    
    acertos,total = 0,0     
    log_erros = []

    for palavra in lista_de_palavras:
        
        categoria_certa = palavra[6]
        categoria_classificador = Classificador(palavra,sextupla)
        if categoria_certa == categoria_classificador:
            acertos += 1
            total += 1
        else:
#            erros += 1
            total += 1
            log_erros.append((palavra[0],categoria_certa,categoria_classificador))
    
#    percent_erros = erros/total * 100
    percent_acertos = acertos/total * 100
    
    return percent_acertos, log_erros


   
ACERTOS, LOG = avalia_class(teste.values, '010000')
########RETOMAR
#Lista com todas as possibilidades das booleanas
# isso vai alimentar o modelo p/ testar as 64 versões
valores_bool = []
for x in range(2**6):
  valores_bool.append(''.join(str((x>>i)&1) for i in range(6-1,-1,-1)))
valores_bool.pop(0)

def roda_modelo(sextupla):
    hist_acertos = []    
    for _ in range(0,100):
        treino,teste = divide_corpus(corpus)
        catAc, catMorf, pesoFinal, nivelFreq, estSilabica,\
        segFinal,penultSil = treina_modelo(treino)    
        #FREQUENCIAS DAS CATEGORIAS
        histCatAc = extrai_priors(catAc)
        ##CRIANDO VARIÁVEIS PARA GUARDAR OS MEUS PRIORS
        priorOx = histCatAc['oxítona']
        priorPar = histCatAc['paroxítona']
        priorPro = histCatAc['proparoxítona']
        nome_modelo = ''
        if sextupla[0] == '1':
        #categoria morfossintática
            tuplMorfAc = zipa(catMorf,catAc)
            histMorfAc = faz_histograma2(tuplMorfAc)
            nome_modelo += 'C'
        if sextupla[1] == '1':
        #estrutura silábica
            tuplSilAc = zipa(estSilabica,catAc)
            histSilAc = faz_histograma2(tuplSilAc)
            nome_modelo += 'E'
        if sextupla[2] == '1':
        #peso final
            tuplPesoFinalAc = zipa(pesoFinal,catAc)
            histPesoAc = faz_histograma2(tuplPesoFinalAc)
            nome_modelo += 'P'
        if sextupla[3] == '1':
        ##lvl freq
            tuplFreqAc = zipa(nivelFreq, catAc)
            histFreqAc = faz_histograma2(tuplFreqAc)
            nome_modelo += 'N'
        if sextupla[4] == '1':
        ##Segmento Final
            tuplSegFinalAc = zipa(segFinal, catAc)
            histSegFinalAc = faz_histograma2(tuplSegFinalAc)    
            nome_modelo += 'S'
        if sextupla[5] == '1':
        #Peso penúltima sílaba
            tuplPenultSilAc = zipa(segFinal, catAc)
            histPenultSilAc = faz_histograma2(tuplPenultSilAc)
            nome_modelo += 'T'
        #% de acertos
        acertos = avalia_class(teste.values,sextupla)
        hist_acertos.append(acertos)

    hist_acertos = np.array(hist_acertos)
    media = np.average(hist_acertos)
    desvio = np.std(hist_acertos)
    return [nome_modelo, media,desvio]


#    
#desempenhos_todos = []
#for item in valores_bool:
#    desempenhos_todos.append(roda_modelo(item))

#ranking = {}
#
#for item in desempenhos_todos:
#    nome = item[0]
#    media = item[1]
#    desvio = item[2]
#    ranking[nome]=[media,desvio]
#    
#
#ranquear = []
#
#for x,y in ranking.items():
#    ranquear.append((y,x))
#    
#
#ranquear = sorted(ranquear,reverse=True)
