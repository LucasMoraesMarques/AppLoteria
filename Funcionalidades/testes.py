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



def numberRankingAll(jogos):
    arr = jogos.iloc[:, 1:].to_numpy()
    rep = np.zeros((25,2)).astype("int")
    for i in range(1, 26):
        v = np.where(arr == i, True, False).sum()
        rep[i-1] = (i,v)
    return rep
        # print(f"Número {i}: {v}x")



"""print(dt.head())
print(numberRankingAll(dt))
df = pd.DataFrame(numberRankingAll(dt))
df.columns = ["Número", "Repetições"]
print(df.sort_values(by="Repetições", ascending=False).set_index("Número"))"""

""" Cria colunas isOdd e maxGap
dt["isOdd"] = dt.apply(isOdd, axis=1)
dt["maxGap"] = dt.iloc[:, 0:14].apply(gap, axis=1).apply(lambda x: max(x))
print(dt.head())
dt.to_csv("todos.csv")

dt["hasRow"] = dt.iloc[:, 0:15].apply(lambda x: hasRow(x), axis=1)
dt["hasRow1"] = dt["hasRow"].apply(lambda x: x[0])
dt["hasRow2"] = dt["hasRow"].apply(lambda x: x[1])
dt["hasRow3"] = dt["hasRow"].apply(lambda x: x[2])
dt["hasRow4"] = dt["hasRow"].apply(lambda x: x[3])
dt["hasRow5"] = dt["hasRow"].apply(lambda x: x[4])
dt.drop("hasRow", axis=1, inplace=True)
print(f"1/3 : {time.process_time()}")
dt["hasCol"] = dt.iloc[:, 0:15].apply(lambda x: hasCol(x), axis=1)
dt["hasCol1"] = dt["hasCol"].apply(lambda x: x[0])
dt["hasCol2"] = dt["hasCol"].apply(lambda x: x[1])
dt["hasCol3"] = dt["hasCol"].apply(lambda x: x[2])
dt["hasCol4"] = dt["hasCol"].apply(lambda x: x[3])
dt["hasCol5"] = dt["hasCol"].apply(lambda x: x[4])
dt.drop("hasCol", axis=1, inplace=True)
print(f"2/3 : {time.process_time()}")
dt["maxSeq"] = dt.iloc[:, 0:15].apply(lambda x: sequences(x), axis=1).apply(lambda x: max(x))
dt["minSeq"] = dt.iloc[:, 0:15].apply(lambda x: sequences(x), axis=1).apply(lambda x: min(x))
print(f"3/3 : {time.process_time()}")
dt.to_csv("todos.csv")

dt = pd.read_csv('todos.csv', header=0, index_col=0)

dtcopy = dt.copy()
dtcopy = dtcopy.astype({f'{i}': "int8" for i in range(0, 15)})
dtcopy = dtcopy.astype({'maxGap': "int8", "minSeq": "int8", "maxSeq": "int8"})
"""


#dt = pd.read_pickle('todos.csv')
#print(dt)
#dt.to_pickle("todos.csv")

