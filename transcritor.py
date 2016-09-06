## -*- coding: utf-8 -*-
#PARTE 3

from __future__ import unicode_literals

execfile('sil_ep.py') 

#DEFININDO GRUPOS RELEVANTES PARA A FUNÇÃO
vogais = u'aeiou30AEIOU12456789!#$%'
semiV = u'JW'
liquidas = u'lrL'
consoantes = u'bcdfghjklmnpqrstvxzSDTN'
sonoras = u'bdgjlrmnzvDNL'
surdas = u'ptkshfxST'

tabela_nasais = {
                u'a': u'A',
                u'1': u'2',
                u'e': u'E',
                u'4': u'6',
                u'5': u'6',#também
                u'i': u'I',
                u'7': u'8', #índia  já chega nesse ponto como 7ndia. com a nasalização vira 8ndia
                u'o': u'O',
                u'!': u'#',
                u'9': u'#',
                u'$': u'%',
                u'u': u'U'} #Codificação para nasalisar as vogais

excecao = {
        'aguentar': 'a-gWE-tar',                
        'agroexportador': 'a-gro-es-por-ta-dor',
        'agroexportação': 'a-gro-es-por-ta-sAW',        
        'aproximar': 'a-pro-si-mar',        
        'auxiliar': 'aW-si-li-ar',        
        'axilar': 'a-ksi-lar',        
        'bisexuais': 'bi-se-ksu-aJs',
        'bisexual': 'bi-se-ksu-aW',        
        'coexistir': 'ko-e-zis-tir',     
        'desintoxicador': 'de-sI-to-ksi-ka-dor',
        'desintoxicar': 'de-sI-to-ksi-kar',
        'desoxidar': 'de-so-ksi-dar',
        'exsanguinotransfusão': 'e-sA-gWi-no-trAs-fu-zAW',
        'exsudar': 'e-su-dar',
        'exsudação': 'e-su-da-sAW',        
        'extinguir': 'es-tI-gWir',
        'exultar': 'e-zuW-tar',
        'fixar': 'fi-ksar',
        'flexionar': 'fle-ksi-o-nar',        
        'heterossexuais': 'e-te-ro-ksu-aJs',
        'heterossexual': 'e-te-ro-ksu-aW',
        'hexacampeão': 'e-ksa-kA-pe-AW',
        'hexadecimal': 'e-ksa-de-si-maW',
        'hexagonal': 'e-za-go-naW',
        'homossexuais': 'o-mo-se-ksu-aW',
        'homossexual': 'o-mo-se-ksu-aW',
        'indexar': 'I-de-ksar',        
        'lexicalizar': 'le-ksi-ka-li-zar',
        'lexificador': 'le-ksi-fi-ca-dor',
        'maxilar': 'ma-ksi-lar',
        'maximizar': 'ma-ksi-mi-zar',
        'metrossexual': 'm3-tro-se-ksu-aW',
        'oxidar': 'o-ksi-dar',
        'oxidação': 'o-ksi-da-sAW',
        'prolixidez': 'pro-li-ksi-des',
        'proximal': 'pro-si-maW',
        'reflexionar': 're-fle-ksi-o-nar',
        'sexagesimal': 'se-ksa-ge-zi-maW',
        'sexuais': 'se-ksu-aJs',
        'sexual': 'se-ksu-aW',
        'sexualizar': 'se-ksu-a-li-zar',
        'sexualização': 'se-ki-su-a-li-za-sAW',
        'sexualizações': 'se-ksu-a-li-za-sOEs',
        'subaxilar': 'su-ba-ksi-lar',
        'sufixar': 'su-fi-ksar',
        'sufixação': 'su-fi-ksa-sAW',
        'táxi': 't1-ksi',
        'telexar': 'te-le-ksar',
        'transexual': 'trAs-se-ksu-aW',
        'transfixar': 'trAs-fi-ksar',
        'unissexual': 'u-ni-se-ksu-aW',
        'afixado': 'a-fi-ksa-do',
        'afixo': 'a-fi-kso',
        'afluxo': 'a-flu-kso',
        'agroexportadora': 'a-gro-es-por-ta-do-ra',
        'amplexo': 'A-ple-kso',
        'amplexos': 'A-ple-ksos',
        'anexásseis': 'a-ne-ksa-seJs',
        'anexectomia': 'a-ne-kse0ki-to-mJa',
        'anexo': 'a-ne-kso',
        'anorexia': 'a-no-re-ksJa',
        'anoxia': 'a-no-ksJa',
        'apitoxina': 'a-pi-to-ksi-na',        
        'aproximadamente': 'a-pro-si-ma-da-mE-te',
        'auxiliares': 'aW-si-li-a-res',
        'auxologia': 'aW-kso-lo-jJa',
        'auxílio': 'aW-s7-liW',
        'axila': 'a-ksi-la',
        'axiologia': 'a-ksi-o-lo-jia',
        'axioma': 'a-ksi-o-ma',
        'axolote': 'a-kso-lo-te',
        'barbarolexia': 'bar-ba-ro-le-ksJa',        
        'bissexualidade': 'bi-se-ksu-a-li-da-de',
        'bissexualidades': 'bi-se-ksu-a-li-da-des',
        'bissexualismo': 'bi-se-ksu-a-lis-mo',
        'bissexualismos': 'bi-se-ksu-a-lis-mos',
        'bissexualmente': 'bi-se-ksu-aW-mE-te',
        'cardiotirotoxicose': 'kar-Di-o-Ti-ro-to-ksi-ko-ze',
        'circunflexo': 'sir-kU-fle-kso',
        'citotoxidez': 'si-to-to-ksi-des',
        'citotoxina': 'si-to-to-ksi-na',
        'complexidade': 'kO-ple-ksi-da-de',
        'complexo': 'kO-ple-kso',
        'conexionado': 'ko-ne-ksi-o-na-do',
        'conexivo': 'ko-ne-ksi-vo',
        'conexo': 'ko-ne-kso',
        'convexidade': 'kO-ve-ksi-da-de',
        'convexo': 'kO-ve-kso',
        'crucifixo': 'kru-si-fi-kso',
        'crucifixámos': 'kru-si-fi-ks1-mos',
        'anagotóxico': 'a-na-go-t!-ksi-ko',
        'angueira': 'A-gWeJ-ra',
        'angueiras': 'A-gWeJ-ras',
        'anoréxico': 'a-no-r4-ksi-ko',
        'anoxítono': 'a-no-ks7-to-no',
        'anóxica': 'a-n9-ksi-ka',
        'anóxico': 'a-n9-ksi-ko',
        'araputanguense': 'a-ra-pu-tA-gWE-se',
        'argueiro': 'ar-gWeJ-ro',
        'arguente': 'ar-gWE-te',
        'armengue': 'ar-mE-gWe',
        'axiológico': 'a-ksi-o-l!-ji-ko',
        'fluxo': 'flu-kso',
        'fluxograma': 'flu-kso-gra-ma',
        'fluxos': 'flu-ksos',
        'genuflexo': 'ge-nu-fle-kso',
        'genuflexório': 'ge-nu-fle-x!-rJo',
        'hepatotóxico': 'e-pa-to-t!-ksi-ko',
        'heterodoxo': 'e-te-ro-do-kso',
        'heterossexualidade': 'e-te-ro-se-ksu-a-li-da-de',
        'heterossexualismo': 'e-te-ro-se-ksu-a-lis-mo',
        'heterossexualismos': 'e-te-ro-se-ksu-a-lis-mos',
        'heterossexualmente': 'e-te-so-se-ksu-aW-mE-te',
        'hexaedro': 'e-za-e-dro',
        'hexassílabo': 'e-ksa-s7-la-bo',
        'homossexualidade': 'o-mo-se-ksu-a-li-da-de',
        'homossexualismo': 'o-mo-se-ksu-a-lis-mo',
        'homossexualismos': 'o-mo-se-ksu-a-lis-mos',
        'homossexualmente': 'o-mo-se-ksu-aW-mE-te',
        'indexado': 'I-de-ksa-do',
        'infixo': 'I-fi-kso',
        'infixos': 'I-fi-ksos',
        'inflexibilidade': 'I-fle-ksi-bi-li-da-de',
        'inflexível': 'I-fle-ks7-veW',
        'influxo': 'I-flu-kso',
        'abnóxio': 'a-bi-n9-ksJo',
        'carboxílico': 'kar-bo-ks7-li-ko',
        'daxofone': 'da-kso-fo-ne',
        'desoxidante': 'de-zo-ksi-dA-te',
        'disléxico': 'dis-l5-kso',
        'dióxido': 'di-!-ksi-do',
        'flexionável': 'fle-ksi-o-n1-veW',
        'flexografia': 'fle-kso-gra-fJa',
        'flexível': 'fle-ks7-veW',
        'intoxicado': 'I-to-ksi-ka-do',
        'lexema': 'le-kse-ma',
        'lexicografia': 'le-ksi-ko-gra-fJa',
        'lexicologia': 'le-ksi-ko-lo-gJa',
        'lexicógrafo': 'le-ksi-k9-gra-fo',
        'léxica': 'l5-ksi-ka',
        'léxico': 'l5-ksi-ko',
        'lingueta': 'lI-gWe-ta',
        'maximário': 'ma-ksi-m1-rJo',
        'maxissaia': 'ma-ksi-sa-Ja',
        'micotoxina': 'mi-ko-to-ksi-na',
        'máxima': 'm1-si-ma',
        'máximo': 'm1-si-mo',
        'nefrotoxina': 'ne-fro-to-ksi-na',
        'neurotoxicidade': 'neW-ro-to-ksi-si-da-de',
        'neurotoxina': 'neW-ro-to-ksi-na',
        'neurotóxico': 'neW-ro-t!-ksi-ko',
        'nexo': 'ne-kso',
        'nóxio': 'n!-kso',
        'obnóxio': 'o-bi-n!-kso',
        'ortodoxo': 'or-to-do-kso',
        'oxigênio': 'o-ksi-j4-nJo',
        'oximoro': 'o-ksi-mo-ro',
        'oximoros': 'o-ksi-mo-ros',
        'oxiácido': 'o-ksi-1-si-do',
        'oxígono': 'o-ks7-go-no',
        'oxímoro': 'o-ks7-mo-ro',
        'oxímoros': 'o-ks7-mo-ros',
        'oxítona': 'o-ks7-to-na',
        'oxítono': 'o-ks7-to-no',
        'paradoxo': 'pa-ra-do-kso',
        'paroxítona': 'pa-ra-ks7-to-na',
        'paroxítono': 'pa-ra-ks7-to-no',
        'perplexidade': 'per-ple-ksi-da-de',
        'perplexo': 'per-ple-kso',
        'aluguel': 'a-lu-gWeW',
        

        
        }
#Preencher com lista de exceções do corpus

## novas regras de x:
      	## 1.x em ataque medial == S; [FEITO]
        ## 2. x sendo que [i+1] in vogais, [1-1] == '-' e [1-2] == 'e', como e-xa-me, e-xaus-tor [FEITO]
        ## 3. [Está funcionando já!]creio que a regra de consoante + líquida deve pegar casos como extrair*, &extrapolar*, &extratar*, &extração*, certo? Vc pode testar? [FEITO]
        ## 4. x sendo que [i-1] == 'e' e [i+2] in 'tp'  tem som de 's', como ex-ter-nar, ex-tin-guir, ex-tin-ção, in-ter-tex-tu-al, ex-pe-ri-en-te, ex-pe-di-to [FEITO]
        ## 5. xia e xão - [i+1] == 'i' e [i+2] == 'a', anorexia, ataraxia, galaxia, apoplexia, flexão, conexão [aqui tá dando um bug: 'e' seguido de 'x' seguido de vogal: a regra 2 daqui de cima pega isso! então o transcritor retorn 'anorezia'] [RESOLVIDO - FEITO]

def transcritor (palavra):
        #PRIMEIRO PASSO É CHECAR SE A PALAVRA ESTÁ MARCADA COMO EXCEÇÃO
        if palavra in excecao.keys():
                palavra1 = '&' + excecao[palavra] + '*'
                return palavra1
##TRANSCRITOR --  RECEBE A PALAVRA COM EPENTESE, CODIGO FINAL E INICIAL, SEM DÍGRAFOS E SILABIFICADA
        palavra1 = sil_ep(palavra.lower())
        
 #TABELA ELIMINANDO OS SÍMBOLOS DE ACENTO - O PYTHON LIDA COM CODIFICAÇÃO ASCII E NÃO UTF-8
        palavra1= palavra1.replace("\xe9","5") ## é vira 3 tônico - 5
        palavra1= palavra1.replace("\xea","e") ## ê vira e tônico - 4
        palavra1= palavra1.replace("\xe2","a") ## â vira a
        palavra1= palavra1.replace("\xe1","1") ## á vira a tônico - 1
        palavra1= palavra1.replace("\xe0","a") ## à vira a
        palavra1= palavra1.replace("\xe3","A") ## ã vira a nasal - A
        palavra1= palavra1.replace("\xed","7") ## í vira i tônico - 7
        palavra1= palavra1.replace("\xf5","O") ## õ vira o nasal - O
        palavra1= palavra1.replace("\xf3","!") ## ó vira 0 tônico - !
        palavra1= palavra1.replace("\xf4","o") ## ô vira o tônico - 9
        palavra1= palavra1.replace("\xfa","$") ## ú vira u tonico - $
        
        palavra2 = ''
        i = 0
        for letra in palavra1:
                
                #consoantes não ambíguas são transcritas em primeiro lugar.
                if letra in 'kvfjSNhypb':# kleber, favo, peNa
                        palavra2 +=(letra)
                elif letra == 'L': #Por causa de um bug, separamos o caso não ambíguo do L,  como em piLa
                        palavra2 += letra

                elif letra == 'd':
                        if (palavra1[i+1] == 'i' or palavra1[i+1] == 'y'): #dia -> Dia
                                palavra2 += ('D')
                        else:
                                palavra2 += (letra) #domingo

                elif letra == 't':
                        if (palavra1[i+1] == 'i' or palavra1[i+1] == 'y'): #tia -> Tia
                                palavra2 += ('T')
                        else:
                                palavra2 +=(letra) #tobias

                elif letra == 'g':
                        if (palavra1[i+1] == 'i' or palavra1[i+1] == 'e'): #gelo -> jelo / ginástica -> jinástica
                                palavra2 += ('j')
                        else:
                                palavra2 +=(letra) #galo, gato

                elif letra == 'r':
                        if palavra1[i - 1] == '&': #ralo -> halo
                                palavra2 += 'h'
                        elif palavra1[i-1] == '-': #porta
                            if palavra1[i-2] in 'nm':
                                palavra2 += 'h'
                            else:
                                palavra2 += (letra)
                        else:
                                palavra2 += letra #prato

                elif letra == 'l':
                        if palavra1[i+1] == '*' or palavra1[i+1] == '-': #gol -> goW / polvo -> poWvo
                                palavra2 += ('W')
                        else:
                                palavra2 += (letra) #golaço

                elif letra == 'c':
                        if (palavra1[i+1] == 'i' or palavra1[i+1] == 'e'): #céu -> séu / cinema -> sinema
                                palavra2 += ('s')
                        else:
                                palavra2 +=('k') #calo -> kalo / cuspe -> kuspe
                elif letra == 'q':
                        if (palavra1[i+1] == 'a'): #quadro -> kWadro
                            palavra2 += ('kW')
                        elif (palavra1[i+1] in 'ei'): #quente -> kente / quiabo -> kiabo
                            palavra2 += ('k')            

                elif letra == 's':
                        if (palavra1[i-2] in vogais and palavra1[i+1] in vogais): #casa -> caza
                                palavra2 +=('z')
                        elif (i < len(palavra1) - 2) and (palavra1[i+2] == 'c'): #a-do-les-cen-te
                              pass
                        elif (i < len(palavra1) - 2) and (palavra1[i+2] == 's'): #pássaro -> pásaro
                                pass
                        else:
                                palavra2 += (letra)#cascata

                elif letra == 'z':
                        if palavra1 [i+1] == '*': #feliz -> felis
                                palavra2 +=('s')
                        elif palavra1 [i+2] in surdas:
                            palavra2 += 's'
                        else:
                                palavra2 +=(letra) #zebra

                elif letra == 'x':
                        if palavra1[i+1] == '*': #látex -> látekis
                                palavra2 +=('kis')
                        elif palavra1 [i+2] == 'c' and palavra1[i+3] in vogais: #exceção -> eceção
                                pass
                        elif palavra1 [i+2] in consoantes and palavra1[i+3] in liquidas:#exclamação -> esclamação
                                palavra2 += ('s')
                        elif palavra1 [i-1] == '&':#xadrez -> Sadrez
                                palavra2 += ('S')
                        
                        #AQUI COMEÇAM AS SUB-REGULARIDADES - SERÃO MARCADAS PARA SEREM TRANSCRITAS MANUALMENTE
                        elif palavra1 [i+1] == 'A' and palavra1[i+2] == 'o': #conexão -> coneksAo
                                palavra2 += ('ks')
                        elif palavra1 [i+1] in vogais and palavra1[i-2] == 'e': # exame -> ezame
                                palavra2 += ('z')
                        elif palavra1 [i-1] == 'e' and palavra1[i+2] in 'tp': # extinguir -> estinguir
                                palavra2 += ('s')
                        elif palavra1 [i+1] == 'i' and palavra1[i+3] == 'a': # anorexia -> anoreksia
                                palavra2 += ('ks')
                        elif palavra1 [i-1] == '-':
                                palavra2 += ('S')
        
                        else: 
                                palavra2 += (letra)
                                #AQUI MARCAMOS AS PALAVRAS COM UM X QUE NÃO ESTÁ NA TRANSCRIÇÃO PARA MEXERMOS NELAS DEPOIS
                
                elif letra in vogais:
                        if palavra1[i+1] in 'mn': #Nasalização antes de m ou n
                                palavra2 += (tabela_nasais[letra])# banana -> bAnAna
                                
                        elif letra == 'o' and palavra1[i-1] == 'A': #o til não é silabificado, por isso o index é menor aqui
                                palavra2 += 'W' #coração -> coraçAW
                                
                        elif letra == 'e' and palavra1[i-1] == 'O':
                                palavra2 += 'J' #corações -> coraçOJs
                                
                        elif letra == 'i':
                                if palavra1[i-1] in consoantes and i < (len(palavra1)- 2):
                                        if palavra1[i+2] in 'aeoAEO1234567890!':
                                                palavra2 += 'J' #piada -> pJada
                                        else:
                                                palavra2 += letra #vida
                                elif palavra1[i-2] in vogais:
                                        palavra2 += 'J' #paixão -> paJxão
                                else:
                                        palavra2 += letra #história
                                        
                        elif letra == 'u':
                                if palavra1[i-1] in consoantes and i < (len(palavra1)- 2):
                                        if palavra1[i+2] in 'aoAO126890!': 
                                                palavra2 += 'W' #guaraná - gWaraná
                                        elif palavra1[i+1] == '7' and palavra1[i-1] == 'g':
                                                palavra2 += 'W' #linguística - lingW7stica (Silabificação do 7)
                                        elif palavra1[i+2] in 'eE345':
                                                pass #guerra -> gerra
                                        else: #Publicidade
                                                palavra2 += letra
                                elif palavra1[i-2] in vogais and palavra1[i+1] != 'l':#Morreu
                                        palavra2 += 'W'
                                
                                else:
                                        palavra2 += letra #árdua
                        
                        else:
                                palavra2 += letra #vogais não ambíguas.
                                #aba, porta, pedra
                                


                elif letra == 'm':
                        
                        if palavra1[i-1] == 'a' and palavra1[i+1] == '*':
                                palavra2 += ('W') #comam -> comAW
                        elif palavra1[i-1] == 'e' and palavra1[i+1] == '*':
                                palavra2 += ('J') #homem -> homEJ
                        elif (palavra1[i+1] == '*') or (palavra1[i+1] == '-'):
                                pass #emprego -> eprego
                        elif palavra1[i-1] in '&-':
                                palavra2 +=(letra) #marido / pamela

                elif letra == 'n':

                        if palavra1[i-1] == 'e' and palavra1[i+1] == '*':
                                palavra2 += ('J')#hífen -> hifEJ
                        elif palavra1[i+1] == '*' or palavra1[i+1] == '-':
                                pass #entrada -> etrada
                        elif palavra1[i-1] in '&-':
                                palavra2 += (letra) #nasal / janela

                elif letra == '\xe7':
                        palavra2 += 's'
                          #Codificação do cedilha
                i += 1
                palavra3 = '&' + silabas(palavra2) + '*'
        #print palavra1
        return unicode(palavra3)


        




