# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:57:11 2016

@author: Bruno
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

medias_todas = pd.read_csv('TAB-desempenhos.csv',encoding =  'utf8')
#Plotando!
#fonte para embelezar: http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
#Primeiro- deixando os gráficos bonitos!
# These are the "Tableau 20" colors as RGB.    
fig, ax = plt.subplots()
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)   

ax.spines["top"].set_visible(False)    
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False)   
ax.get_xaxis().tick_bottom()    
ax.get_yaxis().tick_left()    
# You typically want your plot to be ~1.33x wider than tall. This plot is a rare    
# exception because of the number of lines being plotted on it.    
# Common sizes: (10, 7.5) and (12, 9)    
plt.figure(figsize=(48, 36))    
ax.axis([0,5,60,90])
#agora pra fazer o gráfico mesmo
#receita da fonte: http://matplotlib.org/examples/api/barchart_demo.html
medias = [x[1] for x in medias_todas.values]
desvios = [x[2] for x in medias_todas.values]
nomes = (x[0] for x in medias_todas.values)
N = 63
width = 0.35   
ind = np.arange(N)
rects1 = ax.bar(ind, medias, width,color=tableau20[6],yerr = desvios)
#rects2 = ax.bar(ind + width, mediasH, width,color=tableau20[19], yerr=desviosH)
ax.set_ylabel('% de acertos')
ax.set_title('Desempenho dos Modelos')
ax.set_xticks(ind + width)
#ax.set_xticklabels(nomes)
ax.legend((rects1), ('% de Acertos',), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.show()
plt.savefig("desempenhoN-gramas.pdf") 
