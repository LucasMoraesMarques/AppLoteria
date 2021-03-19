import numpy as np
import pandas as pd

# Funções auxiliares para a classe Jogos


def isOdd(jogo):
    """Checa se um jogo é par ou ímpar

    :param jogo: Jogo único
    :return: Retorna True se o jogo é predominantemente ímpar. Caso contráriio, retorna False
    """
    bolArray = jogo.map(lambda x: x % 2)
    if jogo.size % 2 != 0:
        return True if bolArray.sum(axis=0) > np.floor(jogo.size / 2) else False
    else:
        return True if bolArray.sum(axis=0) > (jogo.size / 2) else False


def gap(jogo):
    """Checa os espaçamentos entre números consecutivos(extremos inclusive)

    :return: Array com os espaçamentos
    """
    g = []
    for i in range(0, len(jogo) - 1):
        g.append(jogo[i + 1] - jogo[i])
    return g


def sequences(jogo):
    """Checa as sequências presentes e retorna o seu tamanho

    :return: Quantia de números em cada sequência
    """
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
    :param jogo: Jogo único
    :return: Array booleano com as colunas presentes no jogo
    """
    cols = np.array([[1, 6, 11, 16, 21], [2, 7, 12, 17, 22], [3, 8, 13, 18, 23],
                     [4, 9, 14, 19, 24], [5, 10, 15, 20, 25]])
    hasCol = []
    for col in cols:
        hasCol.append(True if (ints := len(np.intersect1d(col, jogo))) != 0 else False)
    return hasCol


def hasRow(jogo):
    """Verifica se o jogo possui números em cada linha
    obs: para um jogo de 15 marcações, o mínimo de colunas e linhas é de pelo menos 3
    :param jogo: Jogo único
    :return: Array booleano com as colunas presentes no jogo
    """
    rows = np.array([np.arange(1, 6), np.arange(6, 11), np.arange(11, 16),
                     np.arange(16, 21), np.arange(21, 26)])
    hasRowArr = []
    for row in rows:
        hasRowArr.append(True if (ints := len(np.intersect1d(row, jogo))) != 0 else False)
    return hasRowArr


def nPrimeNumbers(jogo):
    """Checa a quantia de números primos presentes no jogo

    :param loto_range:
    :return: Retorna o número de primos presentes
    """
    primeNumbers = []
    for i in jogo:
        s = 0
        for j in range(1, i + 1):
            if i % j == 0:
                s += 1
        if s == 2:
            primeNumbers.append(i)
    return np.intersect1d(primeNumbers, jogo).size


def askUserFixedAndRemovedNumbers(nRemoved, nFixed):
    """ Pede o input dos números removidos e fixos

    :param nRemoved: Quantidade de números removidos
    :param nFixed: Quantidade de números fixados
    :return: Retorna o input dos números removidos e fixados
    """
    if nRemoved > 0:
        print("Digite os números a serem excluídos.")
        removedNumbers = np.zeros(nRemoved)
        for i in range(0, nRemoved):
            removedNumbers[i] = int(input(f"Digite o número {i + 1}:"))
    else:
        removedNumbers = []

    if nFixed > 0:
        print("Digite os números a serem fixados:")
        fixedNumbers = np.zeros(nFixed)
        for i in range(0, nFixed):
            fixedNumbers[i] = int(input(f"Digite o número {i + 1}:"))

    else:
        fixedNumbers = []

    return removedNumbers, fixedNumbers


def checkJogo(jogo, maxGap, maxSeq, minSeq, isodd, nPrime):
    """ Testa a validade de um dado jogo com filtros inteligentes

    :param jogo: Jogo único
    :param maxGap: Subtração máxima entre dois números consecutivos
    :param maxSeq: Tamanho máximo de uma sequência de números
    :param minSeq: Tamanho mínimo de uma sequência de números
    :param isodd: Paridade do jogo
    :param nPrime: Quantidade de números primos no jogo
    :return: Boolean Array com os testes
    """
    boolArray = []
    if max(gap(jogo)) > maxGap or max(sequences(jogo)) > maxSeq \
        or min(sequences(jogo)) < minSeq or isOdd(jogo) != isodd\
        or (nPrime != 0 and nPrimeNumbers(jogo) != nPrime):
        boolArray.append(False)
    else:
        boolArray.append(True)
    return boolArray


def calcCombs(database, nPlayed, numbersRemoved, numbersFixed, kwargs):
    """ Calcula todas as combinações com os filtro dados através da database de todos os jogos

    :param database: Todos os jogos possíveis
    :param nPlayed: Quantidade de números escolhidos no jogo
    :param numbersRemoved: Números removidos
    :param numbersFixed: Números fixados
    :param kwargs: Filtros inteligentes
    :return: Todas as combinações válidas
    """
    dt = database
    dtAuxIndexes = dt.loc[:, "0":f"{nPlayed-1}"][~dt.isin(numbersRemoved)].dropna().index
    dtAux1 = dt.loc[dtAuxIndexes, "0": f"{nPlayed-1}"]
    for i in numbersFixed:
        dtAuxIndexes = dtAux1[dtAux1.isin([i])].dropna(how="all").index
        dtAux1 = dtAux1.loc[dtAuxIndexes, :]

    dt = dt.loc[dtAux1.index, :]
    for k, v in kwargs.items():
        if 'max' in k:
            dt = dt[dt[k] <= v]
        elif 'min' in k:
            dt = dt[dt[k] >= v]
        elif k == 'nPrime' and v != 0:
            dt = dt[dt[k] == v]
        elif k == "isOdd":
            dt = dt[dt[k] == v]

    return dt


def checkScores(jogo, res):
    """Confere os acertos de cada jogo em determinado set

    :param jogo: Set de jogos
    :return: Dicionário com os acertos de cada jogo no set
    """
    scores = dict()
    for name, jogo in jogo.iterrows():
        score = len(set(jogo) & set(res))
        scores[name] = score
    return scores



