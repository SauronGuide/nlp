from __future__ import unicode_literals
import codecs
from collections import defaultdict





#1- Variáveis relevantes para a criação das candidatas
#Variável para criar as versões tônicas
tonicas_dic = { 'a' : '1',
                    'A' : '2',
                    'e' : '4',
                    '3' : '5',
                    'E' : '6',
                    'i' : '7',
                    'I' : '8',
                    'o' : '9',
                    '0' : '!',
                    'O' : '#',
                    'u' : '$',
                    'U' : '%'}

#Variáveis para armazenar as frequencias dos ngramas
arq1 = codecs.open('TAB-Uni.csv','r','utf8')
arq2 = codecs.open('TAB-Bi.csv','r','utf8')
arq3 = codecs.open('TAB-Tri.csv','r','utf8')
tabUni,tabBi,tabTri = [],[],[]
for item in arq1:
    tabUni.append(item.strip('\n').split(','))
for item in arq2:
    tabBi.append(item.strip('\n').split(','))
for item in arq3:
    tabTri.append(item.strip('\n').split(','))

arq1.close()
arq2.close()
arq3.close()
dic_freq_uni = defaultdict(lambda: [1.0,1.0])
dic_freq_bi = defaultdict(lambda: [1.0,1.0])
dic_freq_tri = defaultdict(lambda: [1.0,1.0])


for item in tabUni:
    dic_freq_uni[item[0]] = item[1:]
for item in tabBi:
    dic_freq_bi[item[0]] = item[1:]

for item in tabTri:
    dic_freq_tri[item[0]] = item[1:]
#Variável que armazena o indice da frequencia em type e em token

type_index = 0

token_index = 1

#Função de divisão que já inclui um smoothing de laplace, ou seja:
# se o dividendo não existir, ou seja a freq do dividendo for igual a 0, eu mudo essa freq pra 1 pra tolerar alguns casos.

def divisao(dividendo,divisor):
    try:
        return float(dividendo)/float(divisor)
    except:
            return 1.0/float(divisor)
        
#Função que ranqueia 3 opções
def ranqueia(tripla):
    a = tripla[0]
    b = tripla[1]
    c = tripla[2]
    
    if a > b and a > c:
        return ['oxítona',a]
    elif b > a and b > c:
        return ['paroxítona',b]
    elif c > a and c > b:
        return ['proparoxítona',c]
    elif a == b and a == c:
        return ['empateTodas',a]
    elif a == b:
        return ['empateOxPar',a]
    elif a == c:
        return ['empateOxPro',a]
    elif c == b:
        return ['empateParPro',b]

def acentua (cat,pal):
    #recebe a categoria acentual 1 pra oxi, 2 pra par, 3 pra pro e uma palavra, retorna ela na cat
    invert = pal[::-1]
    cop = ''
    flag = False
    for letra in invert:
        if letra in tonicas_dic.keys() and cat == 1:
            if flag == False:
                cop += tonicas_dic[letra]
                flag = True
            else:
                cop += letra
        elif letra in tonicas_dic.keys() and cat > 1:
            cop += letra
            cat -= 1
        else:
            cop += letra
    return cop[::-1]
#Função que pega uma palavra transcrita não acentuada e retorna as três possibilidades de acentuação da mesma
def gera_candidatas(palavra):
    #gerando as candidatas
    oxitona = acentua(1,palavra)
    paroxitona = acentua (2,palavra)
    proparoxitona = acentua(3,palavra)
    return oxitona,paroxitona,proparoxitona

#Função que extrai os n-gramas (uni,bi tri) de uma palavra
def extrai_ngramas(palavra):
    uni = [palavra[i:i+1] for i in range(len(palavra))]
    bi = [palavra[i:i+2] for i in range(len(palavra)-1)]
    tri = [palavra[i:i+3] for i in range(len(palavra)-2)]
   # print uni,bi,tri
    return uni,bi,tri

#Função que calcula a probabilidade de uma cadeia de ngramas

def prob_ngramas(palavra,dicionario_freq_uni,dicionario_freq_bi,dicionario_freq_tri):
    #essa função pega uma palavra e um dicionário com as frequencias em types e tokens
    #de uni,bi e tri-gramas de um corpus, retorna 4 valores da probabilidade da palavra nos modelos bi e tri-gramas
    # usando as frequencias de types e tokens
    if palavra == 'null':
        return [0,0,0,0]
    #extraindo os ngramas da palavra
    uni,bi,tri = extrai_ngramas(palavra)
    token_index = 0
    type_index = 1
    #inicializando as variáveis 
    prob_bi_tok = divisao(dicionario_freq_bi[bi[0]][token_index],dicionario_freq_uni[uni[0]][token_index])
    prob_bi_typ = divisao(dicionario_freq_bi[bi[0]][type_index],dicionario_freq_uni[uni[0]][type_index])
    prob_tri_tok = divisao(dicionario_freq_tri[tri[0]][token_index],dicionario_freq_bi[bi[0]][token_index])
    prob_tri_typ = divisao(dicionario_freq_tri[tri[0]][type_index],dicionario_freq_bi[bi[0]][type_index])
    
    #loop dos bigramas
    index = 1
    while index < len(bi):
        prob_bi_tok *= divisao(dicionario_freq_bi[bi[index]][type_index],dicionario_freq_uni[uni[index]][token_index])
        prob_bi_typ *= divisao(dicionario_freq_bi[bi[index]][type_index],dicionario_freq_uni[uni[index]][type_index])
        index += 1
    #loop dos trigramas
    index = 1
    while index< len(tri):
        prob_tri_tok *= divisao(dicionario_freq_tri[tri[index]][token_index],dicionario_freq_bi[bi[index]][token_index])
        prob_tri_typ *= divisao(dicionario_freq_tri[tri[index]][type_index],dicionario_freq_bi[bi[index]][type_index])
        index += 1
    
    return prob_bi_tok, prob_bi_typ, prob_tri_tok, prob_tri_typ

#Função que atribui as probabilidades pra cada um dos candidatos baseado no modelo de ngramas
def modelo_ngramas(palavra):
    if palavra.count('-') == 0:
        oxi,par,pro =gera_candidatas(palavra)
        par = 'null'
        pro = 'null'
    elif palavra.count('-') == 1:
        oxi,par,pro =gera_candidatas(palavra)
        pro = 'null'
    else:
        oxi,par,pro =gera_candidatas(palavra)
    #print oxi,par,pro
    #variáveis que guardam uma quádrupla - a probabilidade associada a palavra candidata de acordo com cada um dos modelos.
    
    oxi_probs = prob_ngramas(oxi,dic_freq_uni,dic_freq_bi,dic_freq_tri)
    par_probs = prob_ngramas(par,dic_freq_uni,dic_freq_bi,dic_freq_tri)
    pro_probs = prob_ngramas(pro,dic_freq_uni,dic_freq_bi,dic_freq_tri)
    print 'Resultados obtidos no modelo de n-gramas para a palavra ', palavra
    print 'Probabilidades normalizadas dos modelos:'
    probsbitok = [oxi_probs[0],par_probs[0],pro_probs[0]]
    print 'Modelo Bi-gramas Tokens:'
    print 'Oxitona: {0:.2f}'.format(oxi_probs[0]/sum(probsbitok) * 100)
    print 'Paroxitona: {0:.2f}'.format(par_probs[0]/ sum(probsbitok) * 100)
    print 'Proparoxitona: {0:.2f}'.format(pro_probs[0]/ sum(probsbitok) * 100)
    probsbityp = [oxi_probs[1],par_probs[1],pro_probs[1]]
    print '\n'
    print 'Modelo Bi-gramas Types:'
    print 'Oxitona: {0:.2f}'.format(oxi_probs[1]/sum(probsbityp) * 100)
    print 'Paroxitona: {0:.2f}'.format(par_probs[1]/ sum(probsbityp) * 100)
    print 'Proparoxitona: {0:.2f}'.format(pro_probs[1]/ sum(probsbityp) * 100)
    probstritok = [oxi_probs[2],par_probs[2],pro_probs[2]]
    print '\n'
    print 'Modelo Tri-gramas Tokens:'
    print 'Oxitona: {0:.2f}'.format(oxi_probs[2]/sum(probstritok) * 100)
    print 'Paroxitona: {0:.2f}'.format(par_probs[2]/ sum(probstritok) * 100)
    print 'Proparoxitona: {0:.2f}'.format(pro_probs[2]/ sum(probstritok) * 100)
    probstrityp = [oxi_probs[3],par_probs[3],pro_probs[3]]
    print '\n'
    print 'Modelo Tri-gramas Types:'
    print 'Oxitona: {0:.2f}'.format(oxi_probs[3]/sum(probstrityp) * 100)
    print 'Paroxitona: {0:.2f}'.format(par_probs[3]/ sum(probstrityp) * 100)
    print 'Proparoxitona: {0:.2f}'.format(pro_probs[3]/ sum(probstrityp) * 100)
    
                  
    champ_bi_tok = ranqueia([oxi_probs[0],par_probs[0],pro_probs[0]])
    champ_bi_typ = ranqueia([oxi_probs[1],par_probs[1],pro_probs[1]])
    champ_tri_tok = ranqueia([oxi_probs[2],par_probs[2],pro_probs[2]])
    champ_tri_typ = ranqueia([oxi_probs[3],par_probs[3],pro_probs[3]])
    
    champs = [champ_bi_tok,champ_bi_typ,champ_tri_tok,champ_tri_typ]
    print '\n\n'
    print 'As campeãs de cada modelo são: '
    print 'Bi-gramas tokens: ', champs[0]
    print 'Bi-gramas types: ', champs[1]
    print 'Tri-gramas tokens: ', champs[2]
    print 'Tri-gramas types: ', champs[3]
    return champs
