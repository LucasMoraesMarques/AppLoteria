import pandas as pd
import numpy as np
import time
import os
from Sorteio import Sorteio
from Loterias import Loterias
from Jogos import Jogos

os.chdir(r"../")


diadesorte = Loterias("diadesorte", nAcertos=7, nPossiveis=31, nRange=range(15, 21))
sorteio = Sorteio(diadesorte)
sorteio.requestLastResult()
sorteio.writeConfig()












""" Cria colunas isOdd e maxGap
dt["isOdd"] = dt.apply(isOdd, axis=1)
dt["maxGap"] = dt.iloc[:, 0:15].apply(gap, axis=1).apply(lambda x: max(x))

dt["hasRow"] = dt.iloc[:, 0:15].apply(lambda x: hasRow(x), axis=1)
dt["hasRow1"] = dt["hasRow"].apply(lambda x: x[0]) ...
dt.drop("hasRow", axis=1, inplace=True)

dt["hasCol"] = dt.iloc[:, 0:15].apply(lambda x: hasCol(x), axis=1)
dt["hasCol1"] = dt["hasCol"].apply(lambda x: x[0]) ...
dt.drop("hasCol", axis=1, inplace=True)

dt["maxSeq"] = dt.iloc[:, 0:15].apply(lambda x: sequences(x), axis=1).apply(lambda x: max(x))
dt["minSeq"] = dt.iloc[:, 0:15].apply(lambda x: sequences(x), axis=1).apply(lambda x: min(x))

dt.to_csv("todos.csv")

dt = pd.read_csv('todos.csv', header=0, index_col=0)

dtcopy = dt.copy()
dtcopy = dtcopy.astype({f'{i}': "int8" for i in range(0, 15)})
dtcopy = dtcopy.astype({'maxGap': "int8", "minSeq": "int8", "maxSeq": "int8"})
"""

"""
dt = pd.read_pickle('todos.csv')
print(dt)
dt.to_pickle("todos.csv")"""
#print(dt.iloc[:, 0:15][~dt.isin([1, 2])].dropna())
#print(dt[dt["isOdd"] == True])"""

"""dt = pd.read_pickle('todos.csv')
print(dt)
print(dt["isOdd"].value_counts())
print(dt["maxGap"].value_counts())
print(dt["maxSeq"].value_counts())
print(dt["minSeq"].value_counts())
dt = dt[dt["maxGap"] == 4]
dt = dt[dt["maxSeq"] < 7]
dt = dt[dt["minSeq"] < 2]
dt = dt[dt["isOdd"] == True]
print(dt)
dt.to_csv("allfiltered.csv")"""

#for _, j in dt.iloc[500000:500200, 0:15].iterrows():
 #   print(j)

