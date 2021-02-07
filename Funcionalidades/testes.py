import pandas as pd
import numpy as np


def isOdd(jogo):
    """Posterior método da Classe Jogos

    :param jogo: Jogo único
    :return: Retorna True se o jogo é predominantemente ímpar. Caso contráriio, retorna False
    """
    jogo = jogo
    bolArray = jogo.map(lambda x: x % 2)
    if jogo.size % 2 != 0:
        return True if bolArray.sum(axis=0) > np.floor(jogo.size/2) else False
    else:
        return True if bolArray.sum(axis=0) > (jogo.size / 2) else False


def gap(jogo):
    gap = []
    for i in range(0, len(jogo) - 1):
        gap.append(jogo[i+1] - jogo[i])
    return gap
"""

dt = pd.read_csv("dt_resultados.csv", index_col=0, header=0)
print(dt.head())
for _, jogo in dt.iloc[0:5, 1: ].iterrows():
    print(jogo)
    bolArray = jogo.map(lambda x: x % 2)
    print(bolArray.sum(axis=0))
    print(isOdd(jogo))"""

dt = pd.read_csv("dt_resultados.csv", index_col=0, header=0)


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
        hasCol.append([True if (ints:= len(np.intersect1d(col, jogo))) != 0 else False, ints])
    return hasCol


def hasRow(jogo):
    rows = np.array([np.arange(1, 6), np.arange(6, 11), np.arange(11, 16),
                     np.arange(16, 21), np.arange(21, 26)])
    print(rows)
    hasRow = []
    for row in rows:
        hasRow.append([True if (ints:= len(np.intersect1d(row, jogo))) != 0 else False, ints])
    return hasRow

"""for _, jogo in dt.iloc[0:100, 1: ].iterrows():
    j = jogo.array
    print(j)
    print(columnsNumber(j))
    print()"""

# Função para database de resultados


def numberRankingAll(jogos):
    arr = jogos.iloc[:, 1:].to_numpy()
    rep = np.zeros((25,2)).astype("int")
    for i in range(1, 26):
        v = np.where(arr == i, True, False).sum()
        rep[i-1] = (i,v)
    return rep
        # print(f"Número {i}: {v}x")


dt = pd.read_csv("dt_resultados.csv", index_col=0, header=0)

print(dt.head())
print(numberRankingAll(dt))
df = pd.DataFrame(numberRankingAll(dt))
df.columns = ["Número", "Repetições"]
print(df.sort_values(by="Repetições", ascending=False).set_index("Número"))




