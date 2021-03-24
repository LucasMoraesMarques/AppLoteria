import numpy as np
import pandas as pd
from Librarie import style as st
import math
import re

pd.set_option('display.max_columns', None)
pd.set_option('display.column_space', 40)


class ValueNotInRange(Exception):

    def __init__(self, nrange):
        self.nrange = nrange

    def __str__(self):
        return st.textLine(f'ERRO! Digite um número inteiro válido dentro do intervalo {self.nrange[0]} a {self.nrange[-1]}.', "vermelho")


class OptionDoesNotExist(Exception):

    def __init__(self, allowed):
        self.nAllowed = allowed

    def __str__(self):
        return st.textLine('ERRO! Digite uma opção disponível.', "vermelho")


def leia_int(msg, nrange=0, allowed=0):
    """Função que trata os erros de um input de um número inteiro

    :param msg: Recebe o texto a ser printado para o usuário
    :return: Retorna inteiro digitado sem erros no  programa
    """
    while True:
        try:
            n = int(input(msg))
            if nrange and n not in nrange:
                raise ValueNotInRange(nrange)
            elif allowed and n not in allowed:
                raise OptionDoesNotExist(allowed)
        except (ValueError, TypeError):
            print(st.textLine('ERRO! Digite um número inteiro válido.', 'vermelho'))
        except ValueNotInRange as exception:
            print(exception)
        except OptionDoesNotExist as exception:
            print(exception)
        except KeyboardInterrupt:
            print(st.textLine("O usuário preferiu não digitar esse número", 'vermelho'))
            return 0
        else:
            return n


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


def askUserFixedAndRemovedNumbers(loto, gen=1):
    """ Pede o input dos números removidos e fixos

    :param nRemoved: Quantidade de números removidos
    :param nFixed: Quantidade de números fixados
    :return: Retorna o input dos números removidos e fixados
    """
    if gen == 2:
        nPlayed = loto.metadata['nRange'][0]
        print(f"O seu jogo será limitado a {nPlayed} números")

    else:
        nRange = list(loto.metadata['nRange'])
        nPos = list(loto.metadata['nPossiveis'])
        msg2 = f"Você pode escolher de {nRange[0]} a {nRange[-1]} dentre {nPos[0]} a {nPos[-1]}\n"
        print(st.textLine(msg2))
        nPlayed = leia_int("Quantos números deseja em cada jogo?", nrange=loto.metadata["nRange"])
    nRemoved = leia_int("Deseja remover quantos números?", nrange=range(0, nPlayed+1))
    nFixed = leia_int("Deseja fixar quantos números?", nrange=range(0, nPlayed-nRemoved+1))

    if nRemoved > 0:
        print("Digite os números a serem excluídos.")
        removedNumbers = np.zeros(nRemoved)
        j = 0
        while j != nRemoved:
            n = leia_int(f"Digite o número {j+1}:", nrange=loto.metadata['nPossiveis'])
            if n not in removedNumbers:
                removedNumbers[j] = n
                j+=1
            else:
                print("Valor já cadastrado")
    else:
        removedNumbers = []

    if nFixed > 0:
        print("Digite os números a serem fixados:")
        fixedNumbers = np.zeros(nFixed)
        j = 0
        while j != nFixed:
            n = leia_int(f"Digite o número {j+1}:", nrange=loto.metadata['nPossiveis'])
            if (n not in removedNumbers) and (n not in fixedNumbers):
                fixedNumbers[j] = n
                j += 1
            else:
                if n in removedNumbers:
                    print("Valor cadastrado nos excluídos")
                else:
                    print("Valor já cadastrado")

    else:
        fixedNumbers = []

    if gen == 1:
        nCombs = math.comb((nPos[-1] - nRemoved - nFixed), (nPlayed - nFixed))
        print("\n\033[1;30mO número de combinações possíveis são:", nCombs)
        nJogos = leia_int("Quantos jogos deseja?", nrange=range(1, nCombs))
        return removedNumbers, fixedNumbers, nPlayed, nJogos
    else:
        return removedNumbers, fixedNumbers, nPlayed


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
            dt = dt[dt[k] == bool(v)]

    return dt


def checkScores(jogo, res):
    """Confere os acertos de cada jogo em determinado set

    :param jogo: Set de jogos
    :return: Dicionário com os acertos de cada jogo no set
    """
    if type(jogo) == pd.core.frame.DataFrame:
        scores = dict()
        for name, jogo in jogo.iterrows():
            score = len(set(jogo) & set(res))
            scores[name] = score
        return scores
    elif type(jogo) == pd.core.series.Series:
        scores = len(set(jogo) & set(res))
        return scores



def getExternalJogo(nJogos, nPlayed, nrange):
    jogos = dict()
    for i in range(1, nJogos + 1):
        jogos[f"Jogo {i}"] = []
        print(f"Jogo {i}:")
        j = 1
        while j != nPlayed+1:
            n = leia_int(f"Digite o número {j}:", nrange)
            if n not in jogos[f"Jogo {i}"]:
                jogos[f"Jogo {i}"].append(n)
                j += 1
            else:
                print("Valor já cadastrado")

    return jogos


def transFilterNames(col):
    if col == "isOdd":
        print(st.textLine("\nParidade dos Jogos (par ou ímpar):", 'azul'))
    elif col == "maxGap":
        print(st.textLine("\nMáxima diferença entre dois números:", 'azul'))
    elif col == "maxSeq":
        print(st.textLine("\nMáxima sequência ininterrupta de números:", 'azul'))
    elif col == "minSeq":
        print(st.textLine("\nMínima sequência ininterrupta de números:", 'azul'))
    elif col == "nPrime":
        print(st.textLine("\nQuantidade de números primos por jogo:", 'azul'))


def makeCombinations(n, nRange):
    """ Cria todas as combinações dos números de nRange tomados n a n.

    :param n: tamanho da n-upla
    :param nRange: intervalo para combinar (1 a nRange)
    :return: todas as Comb(nRange, n)

    Para cada n, cria-se uma sequência binária:
        n=2 -> 0b11 até 0b110000000 ... nRange-2 zeros
        n=3 -> 0b111 até 0b1110000000 ... nRange-3 zeros
    A regra do início é:
        n=2 -> 0b11 = 3 -> 2**2 - 1
        n=3 -> 0b111 = 7 -> 2**3 - 1
        n       ...         2**n - 1
    A regra do fim é:
        n=2, nRange = 5 -> 0b11000 = 2**nRange-1 + 2**nRange-2
        n, nRange   ...    0b1100000..0 = 2**nRange-1 + 2**nRange-2 +...+ 2**nRange-n
    """
    inicio = 2**n - 1
    fim = 0

    for i in range(1, n+1):
        fim += 2**(nRange-i)

    jogos = []
    for i in range(inicio, fim + 1):
        iCopy = format(i, 'b').zfill(nRange)
        if iCopy.count("1") == n:
            x = re.split(r"([01])", iCopy)
            x = [j for j in x if j not in [""]]
            jogos.append(x)
        else:
            continue

    return jogos


def binaryMapping(nUplas):
    combsMapped = []
    for comb in nUplas:
        a = []
        for i, j in enumerate(comb):
            if j == '1':
                a.append(i+1)
        combsMapped.append(set(a))
    return combsMapped


def checkCombinations(combs, jogos):
    """
    Dado n entrado pelo user, quantificar as n-uplas que mais sairam na amostra de 100 resultados
    contida na lista jogos. As n-uplas seram formadas pelos números do nRange. Por exemplo,

    n=2
    nRange = 5

    As n-uplas ou, nesse caso, duplas possíveis serão

    (1, 2), (1, 3), (1, 4), (1, 5)
    (2, 3), (2, 4), (2, 5)
    (3, 4), (3, 5)
    (4, 5)

    Que totalizam 10 combinações de 2 números, ou seja, Comb(nRange, n).

    Com essas combinações criadas, checar em cada jogo da lista jogos e contabilizar as presentes,
    gerando uma relação das mais frequentes levando em conta toda a amostra.
    """

    dictCombsRanking = {f"{comb}": 0 for comb in combs}

    for index, jogo in jogos.iterrows():
        for comb in combs:
            if comb.issubset(jogo):
                dictCombsRanking[f"{comb}"] += 1

    rankingSeries = pd.Series(dictCombsRanking)
    return rankingSeries.sort_values(ascending=False)



