# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:55:38 2017

@author: Bruno

Nova versão do NBC com as especificações do Paulo
"""
import pandas,re,numpy,nltk,sys
from scipy import spatial
from nltk.stem import RSLPStemmer
from sklearn import cross_validation
from collections import defaultdict
stopwords = nltk.corpus.stopwords.words('portuguese')
stemmer = RSLPStemmer()


def limpa_texto(texto):
    lixo = r"""[\!\.\,\:\;\]\[\}\{\/\?\\\|\@\#\$\%\&\*\(\)\_\-\+\=\'\"\ª\º\§\°\“1234567890]"""
    return re.sub(lixo,' ',texto.lower())

def palavras (texto):#palavras stemizadas de um texto
    texto_limpo = limpa_texto(texto)
    return [x for x in texto_limpo.split()]

def lista_tipos_palavras (texto):#palavras de um texto sem repetição
    return set(palavras(texto))

def trata_texto(texto):#palavras de conteudo de um texto com repeticao
    return [x for x in palavras(texto) if x not in stopwords]


def vocabulario(texto):#palavras de conteúdo de um texto sem repeticao
    return set([x for x in lista_tipos_palavras(texto) if x not in stopwords])





prob(termo) = (alfa,beta)

prob (classe) = (m,n)
def atualiza (texto, label):
    trata =