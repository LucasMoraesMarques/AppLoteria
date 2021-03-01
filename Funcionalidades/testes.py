import pandas as pd
import numpy as np
import time


def isOdd(jogo):
    """Posterior método da Classe Jogos

    :param jogo: Jogo único
    :return: Retorna True se o jogo é predominantemente ímpar. Caso contráriio, retorna False
    """
    bolArray = jogo.map(lambda x: x % 2)
    if jogo.size % 2 != 0:
        return True if bolArray.sum(axis=0) > np.floor(jogo.size/2) else False
    else:
        return True if bolArray.sum(axis=0) > (jogo.size / 2) else False


def gap(jogo):
    g = []
    for i in range(0, len(jogo) - 1):
        g.append(jogo[i+1] - jogo[i])
    return g


def sequences(jogo):
    g = gap(jogo)
    s = 1
    seq = []
    for i in range(0, len(g)):
        if g[i] == 1:
            s += 1
        else:
            seq.append(s)
            s = 1
    else:
        seq.append(s)

    return seq


def hasCol(jogo):
    """Verifica se o jogo possui números em cada coluna
    obs: para um jogo de 15 marcações, o mínimo de colunas e linhas é de pelo menos 3
    :param jogo:
    :return:
    """
    cols = np.array([[1, 6, 11, 16, 21], [2, 7, 12, 17, 22], [3, 8, 13, 18, 23],
                     [4, 9, 14, 19, 24], [5, 10, 15, 20, 25]])
    hasCol = []
    for col in cols:
        hasCol.append(True if (ints:= len(np.intersect1d(col, jogo))) != 0 else False)
    return hasCol


def hasRow(jogo):
    rows = np.array([np.arange(1, 6), np.arange(6, 11), np.arange(11, 16),
                     np.arange(16, 21), np.arange(21, 26)])
    hasRowArr = []
    for row in rows:
        hasRowArr.append(True if (ints:= len(np.intersect1d(row, jogo))) != 0 else False)
    return hasRowArr


def numberRankingAll(resultados):
    arr = resultados.loc[:, "bola 1": "bola 15"].to_numpy()
    rep = np.zeros((25,2)).astype("int8")
    for i in range(1, 26):
        v = np.where(arr == i, True, False).sum()
        rep[i-1] = (i,v)
    df = pd.DataFrame(rep)
    df.columns = ["Número", "Repetições"]
    df.sort_values(by="Repetições", ascending=False, inplace=True)
    df.set_index("Número", inplace=True)
    return df


""" Testa numberRankingAll

dt = pd.read_csv("dt_resultados.csv", index_col=0, header=0)
print(dt.head())
df = numberRankingAll(dt)
print(df)
"""


def updateResultsDatabase(results):
    results["isOdd"] = results.loc[:, "bola 1":"bola 15"].apply(isOdd, axis=1)
    results["maxGap"] = results.loc[:, "bola 1":"bola 15"].apply(gap, axis=1).apply(lambda x: max(x))
    results["maxSeq"] = results.loc[:, "bola 1":"bola 15"].apply(lambda x: sequences(x), axis=1).apply(lambda x: max(x))
    results["minSeq"] = results.loc[:, "bola 1":"bola 15"].apply(lambda x: sequences(x), axis=1).apply(lambda x: min(x))
    results["PrimeNumbers"] = results.loc[:, "bola 1":"bola 15"].apply(nPrimeNumbers, axis=1)
    return results


def nPrimeNumbers(jogo=0, loto_range=range(1, 26)):
    primeNumbers = []
    for i in loto_range:
        s = 0
        for j in range(1, i+1):
            if i % j == 0:
                s += 1
        if s == 2:
            primeNumbers.append(i)
    return np.intersect1d(primeNumbers, jogo).size

dt = pd.read_csv("dt_resultados.csv", index_col=0, header=0)
print(dt)
dt = updateResultsDatabase(dt)
print(dt)

"""dt = pd.read_csv("dt_resultados.csv", index_col=0, header=0)
print(dt)
dt = updateResultsDatabase(dt)
print(dt)
print(dt["isOdd"].value_counts())
print(dt["maxGap"].value_counts())
print(dt["maxSeq"].value_counts())
print(dt["minSeq"].value_counts())
print(dt[dt["maxGap"] < 5])
print(dt[dt["isOdd"] == True])
print(dt[dt["maxSeq"] < 7])
"""
















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

