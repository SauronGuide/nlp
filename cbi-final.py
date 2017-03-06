"""
Created on Wed Jul  6 21:07:42 2016

@author: Bruno Ferrari Guide

Script final - classificador bayesiano ingenuo
Esse script monta os modelos definidos no capitulo 4
e depois os testa, devolvendo no fim uma lista com os modelos testados
organizada de acordo com a % de acertos de cada um
"""

#bibliotecas para organizar os dados
import numpy as np
import pandas as pd
#biblioteca para implementar rapido a cross validation
from sklearn import cross_validation
#from collections import defaultdict as dft


corpus = pd.read_csv('corpus_transcritoPenult.csv',sep=',',error_bad_lines=False)

def divide_corpus (corpus):
    treino, teste = cross_validation.train_test_split(corpus,test_size=0.2,
                                                 train_size = 0.8)
    return treino, teste    

treino, teste = divide_corpus(corpus)

def treina_modelo(corpus_treino):
    #input e um dataframe, retorna as listas com os valores
    #Dependente - categorias acentuais
    catAc = [x[6] for x in corpus_treino.values]
    #independentes
    #Categoria Morfossintatica
    catMorf = [x[1] for x in corpus_treino.values]
    #Peso silabico da ultima silaba
    pesoFinal = [x[11] for x in corpus_treino.values]
    #Nivel de frequencia da palavra
    nivelFreq = [x[12] for x in corpus_treino.values]
    #Estrutura Silabica
    estSilabica = [x[5] for x in corpus_treino.values]
    #segmento final
    segFinal = [x[10] for x in corpus_treino.values]
    #peso penultima silaba
    penultSil = [x[13] for x in corpus_treino.values]
    return catAc,catMorf,pesoFinal,nivelFreq,estSilabica,segFinal,penultSil

catAc, catMorf, pesoFinal, nivelFreq, estSilabica,\
        segFinal,penultSil = treina_modelo(treino)

def extrai_priors (lista_de_valores):
    #Funcao que pega uma lista de valores e retorna um histograma em forma
    #de dicionario. a chave e o nome da classe e o valor e a frequencia dela
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

##CRIANDO VARIAVEIS PARA GUARDAR OS MEUS PRIORS
priorOx = histCatAc['oxítona']
priorPar = histCatAc['paroxítona']
priorPro = histCatAc['proparoxítona']

#calcular as probabilidades de cada um dos
#valores das features de acordo com cada uma das catAcentuais
#depois gerar para cada palavra teste 3 vetores, que sao 
#as infos que ja estao no corpus so que mudando a catAc pras
#3 possiveis. 

#sera criada entao dicionarios que estao no formato
# dic_feature = {'valor': [probOx,probPar,probPro], 'valor2'... }
#entao pra cada caracteristica eu preciso fazer um dicionario
# cujas chaves sao o set dos features e os valores sao uma lista com 3 itens 
def zipa (lista1,lista2):    
    zipada = []
    i = 0
    for item in lista1:
        dupla = (item,lista2[i])
        i += 1
        zipada.append(dupla)
    return zipada
    

def faz_histograma2(lista_de_tuplas):
    #calcula o histograma de duas variaveis de cada vez
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

#categoria morfossintatica
tuplMorfAc = zipa(catMorf,catAc)
histMorfAc = faz_histograma2(tuplMorfAc)
#estrutura silabica
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
#Peso penultima silaba
tuplPenultSilAc = zipa(segFinal, catAc)
histPenultSilAc = faz_histograma2(tuplPenultSilAc)

#Agora que eu ja tenho os dicionarios que associam os valores das variaveis
#aos tracos, preciso receber uma palavra, transformar ela em vetor
#fazer o calculo da probabilidade dela diante de cada catAcentual e escolher
#a candidata mais provavel.

def NaiveBayesProb(vetor_palavra,categoria,sextupla):
    '''essa funcao pega um vetor de palavra e uma categoria acentual
    e retorna a probabilidade desse vetor corresponder aquela categoria.
    A sextupla e uma variavel booleana que regula qual feature do corpus esta
    sendo utilizado na atribuicao de probabilidade'''
    
    #extraindo os features da palavra    
    catmorf = vetor_palavra[1]
    freq = vetor_palavra[12]
    sil = vetor_palavra[5]
    pesoFinal = vetor_palavra[11]
    segFinal = vetor_palavra[10]
    penultSil = vetor_palavra[13]
    #a probabilidade sera dada pelo produto da probabilidade de todos os 
    #valores dos features dada a categoria em questao vezes o prior da cat.
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
    #vetor de palavra tal como esta no corpus
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
            total += 1
            log_erros.append((palavra[0],categoria_certa,categoria_classificador))
    

    percent_acertos = acertos/total * 100
    
    return percent_acertos, log_erros


   
ACERTOS, LOG = avalia_class(teste.values, '010000')
#Lista com todas as possibilidades das booleanas
# isso vai alimentar o modelo p/ testar as 63 versoes
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
        ##CRIANDO VARIAVEIS PARA GUARDAR OS MEUS PRIORS
        priorOx = histCatAc['oxítona']
        priorPar = histCatAc['paroxítona']
        priorPro = histCatAc['proparoxítona']
        nome_modelo = ''
        if sextupla[0] == '1':
        #categoria morfossintatica
            tuplMorfAc = zipa(catMorf,catAc)
            histMorfAc = faz_histograma2(tuplMorfAc)
            nome_modelo += 'C'
        if sextupla[1] == '1':
        #estrutura silabica
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
        #Peso penultima silaba
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


    
desempenhos_todos = []
for item in valores_bool:
    desempenhos_todos.append(roda_modelo(item))

ranking = {}

for item in desempenhos_todos:
    nome = item[0]
    media = item[1]
    desvio = item[2]
    ranking[nome]=[media,desvio]
    

ranquear = []

for x,y in ranking.items():
    ranquear.append((y,x))
    

ranquear = sorted(ranquear,reverse=True)
