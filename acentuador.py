## -*- coding: utf-8 -*-

##Acentuador - ad hoc

execfile('transcritor.py')

#O acentuador é composto por 4 funções, ele recebe um item lexical(0) no formato [glosa, transcrição *(de acordo com o transcritor)] :
    
    #Estrutura silábica - Recebe o item lexical(0) e retorna ele + estrutura em formato CV-CVG-CVC (item lexical(1))
    #Classe Morfológica - para os próximos capítulos (jspell, treetagger) retorna item lexical(2) + classe de palavra
###CLASSE MORFOLÓGICA JÁ FOI EXTRAÍDA EM OUTRA ETAPA###
    #Extrair posição - Recebe o item lexical(2) e retorna a posição a ser acentuada, de acordo com o paradigma definido (Bisol, Lee)
    #Acentua palavra - Recebe a palavra e a posição, retorna a transcrição acentuada.

#Primeira função extrai a estrutura silábica de uma transcrição.
def estrutura_silabica(item_lex):
    #input dessa função é uma lista tal como ['paçoca','nome', 'paçoca', '&pa-so-ka*',3,3,3]
    #output é uma lista ['paçoca','nome','paçoca', '&pa-s0-ka*', '&CV-CV-CV*',3,3,3]

    
    #definindo as grupos de sons relevantes
    vogais_tonicas = u'12456789!#$%'
    vogais_atonas = u'aAe3EiIo0OuU'
    

    vogais = vogais_atonas + vogais_tonicas
    consoantes = u'bdDfghjklLmnNprStTvxz'
    glides = u'JW'

    #Gerando a estrutura da sílaba

    estrutura_silabica = u''
    index = 0
    for letra in item_lex[3]:
        if letra in vogais:
            estrutura_silabica += u'V'
        elif letra in glides:
            estrutura_silabica += u'G'
        elif letra in consoantes:
            estrutura_silabica += u'C'
        elif letra == u's' and item_lex[3][index + 1] == u'*':
            estrutura_silabica += u'S'
        elif letra == u's':
            estrutura_silabica += u'C'
        else:
            estrutura_silabica += letra
        index += 1
    string = estrutura_silabica
    item_lex.insert(4,string)

    return item_lex



#Função para extrair a posição a ser acentuada a partir da estrutura silábica e da categoria morfológica do item lexical

def extrair_posicao (item_lex):
    #input no formato ['paçoca','nome','paçoca', '&pa-s0-ka*', '&CV-CV-CV*',3,3,3]
    #output no formato 4,3,2 ou 1
    index1 = 0
    for letra in item_lex[3]:#Caso dos nomes e verbos marcados
        if letra in u'12456789!#$%':
            return item_lex[3][index1:].count(u'-') + 1
        
        index1 += 1
        
    if item_lex[1] not in [u'V', u'V+P', u'V+U_d']: #Caso dos não verbos não marcados
        estrutura = item_lex[4].split(u'-')
        silaba = estrutura[-1]
        index = 0
        for letra in silaba:
            if letra in u'VS':
                if silaba[index+1] != u'*':
                    return 1
                else:
                    return 2
            index += 1
        
    else: #Caso dos verbos não marcados [oxítonas e paroxítonas]
            
        verbo = silabas(item_lex[0]).split(u'-')
        silaba_final = verbo[-1]
        terminacoes_tonicas2 = [u'ai',u'iu',u'ia',u'ão',u'eu',u'ei',u'ar',u'er',u'ir',u'is',u'os']
        terminacoes_tonicas1 = [u'i']
        terminacoes_tonicas3 = [u'ais',u'eis',u'ias']
        
        if silaba_final[-1] in terminacoes_tonicas1:
            return 1

        elif silaba_final[-2:] in terminacoes_tonicas2:
            return 1

        elif silaba_final[-3:] in terminacoes_tonicas3:
            return 1
        
        else:
            return 2


#Função para acentuar uma determinada palavra transcrita ('&pa-so-ka*') dada a posição da sílaba desejada

def acentua_palavra (palavra, posicao):
    if posicao > 4:
        return u"Acento em posição não permitida pelo PB"
    vogais = u'aAe3EiIo0OuU'
    tonicas_dic = { u'a' : u'1',
                    u'A' : u'2',
                    u'e' : u'4',
                    u'3' : u'5',
                    u'E' : u'6',
                    u'i' : u'7',
                    u'I' : u'8',
                    u'o' : u'9',
                    u'0' : u'!',
                    u'O' : u'#',
                    u'u' : u'$',
                    u'U' : u'%'}

    postonicas_dic= { u'a': u'@',
                      u'A': u'A',
                      u'e': u'y',
                      u'E': u'E',
                      u'i': u'y',
                      u'I': u'I',
                      u'o': u'w',
                      u'O': u'O',
                      u'u': u'w',
                      u'U': u'U'}

    copia = palavra.split(u'-')
    silaba = copia[0-posicao]
    silaba_tonica = u''
    palavra_acentuada = u''
    flag = False #esse flag é pra identificar se a sílaba sendo transcrita é pos ou pré-tonica
    for letra in silaba:
        if letra in vogais:
            silaba_tonica += tonicas_dic[letra]
        else:
            silaba_tonica += letra
    for item in copia:
        if item == silaba:
            if item[-1] == u'*':
                palavra_acentuada += silaba_tonica
                flag = True
            else:
                palavra_acentuada += silaba_tonica + u'-'
                flag = True
        elif flag == False:
            if item[-1] == u'*':
                palavra_acentuada += item
            else:
                palavra_acentuada += item + u'-'
        else:
            silapos = u''
            for letra in item:
                if letra in vogais:
                    silapos += postonicas_dic[letra]
                else:
                    silapos += letra
            if item[-1] == u'*':
                palavra_acentuada += silapos
            else:
                palavra_acentuada += silapos + u'-'
    return palavra_acentuada



#Acentuador
#O input desse programa é a palavra transcrita e silabificada e classe morfológica,
# com o símbolo de começo e fim de palavra no formato:
    #[palavra,categoria,lema,transcrição,freq_total,freq_oral,freq_escrita]

    # ['paçoca','nome', 'paçoca', '&pa-so-ka*',3,3,3]

# e retorna a lista acrescida da estrutura silábica,  a classe morfossintática, transcrição acentuada e do padrão acentual:

    #[palavra,categoria,lema,transcrição, acentuada, estrutura silábica, padrão acentual ,freq_total,freq_oral,freq_escrita]

    # ['paçoca', 'nome', 'paçoca', '&pa-so-ka*', '&pa-s!-ka', '&CV-CV-CV*', 'paroxítona', 3,3,3]
                
def acentuador(item_lex):
    item_lex2 = estrutura_silabica(item_lex)
    # até aqui estamos assim : ['paçoca','nome','paçoca', '&pa-s0-ka*', '&CV-CV-CV*',3,3,3]
    posicao = extrair_posicao(item_lex2)
    item_lex2.insert(4, acentua_palavra(item_lex2[3],posicao))
    if posicao == 1:
        item_lex2.insert(6, u'oxítona')
    elif posicao == 2:
        item_lex2.insert(6, u'paroxítona')
    elif posicao == 3:
        item_lex2.insert(6, u'proparoxítona')
    return item_lex2
