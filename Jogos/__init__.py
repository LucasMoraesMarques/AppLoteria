import numpy as np
import pandas as pd
import math
import random
import os
from Jogos import funcs


# os.chdir(r"../")


class Jogos(object):

    def __init__(self, loto_type, name="default"):
        """ Classe Jogos

        :param loto_type: Tipo de Loteria
        """
        self.loteria = loto_type
        self.jogos = pd.DataFrame()
        self.jogoname = name + ".xlsx"
        self.metadata = pd.DataFrame()
        print(self.jogoname)

    def __str__(self):
        return "Classe Jogos:\n" \
               "-> Cria, salva, carrega e confere conjuntos de jogos\n" \
               "-> Atributos:\n" \
               "    -> Tipo de Loteria\n" \
               "    -> Conjunto de Jogos\n" \
               "    -> Nome dos Jogos\n" \
               "    -> Metadados do conjunto de Jogos\n" \
               "-> Possui 2 geradores de jogos:\n" \
               "    -> Gerador Simples: \n" \
               "        - Cria combinações sem filtros inteligentes, com números fixos e excluídos facultativos\n" \
               "        - Funciona bem para até 80% do total de combinações\n" \
               "    -> Gerador Complexo:\n" \
               "        - Cria combinações inteligentes levando em conta filtros pré-determinados\n" \
               "        - Usa a database contendo todas as combinações possíveis\n"

    def readJogos(self, name):
        """ Lê jogos armazenados

        :param name: Nome do conjunto de jogos a ser lido
        :return: None
        """
        self.jogos = pd.read_excel(
            os.path.join(os.getcwd(), f"user_data\\user_games\\{self.loteria.nome}\\games\\{name}"),
            sheet_name=None,
            header=None,
            index_col=0)
        self.jogoname = name

    def writeJogos(self):
        print(os.getcwd())
        print(self.jogos)
        self.jogos.to_excel(
            os.path.join(os.getcwd(), f"user_data\\user_games\\{self.loteria.nome}\\games\\{self.jogoname}"))

    def checkResults(self, sorteio):
        """ Confere os resultados para dado conjunto de jogos

        :return: None. Exporta para arquivo.
        """
        f = open(os.path.join(os.getcwd(), f"user_data\\user_games\\{self.loteria.nome}"
                                           f"\\results\\resultados_{self.loteria.nome}_{self.jogoname.replace('.xlsx', '')}.txt"), "w+")
        f.write(f"Resultado referente ao concurso nº {sorteio.metadata['numero']} "
                f"da {sorteio.metadata['tipoJogo']} "
                f"realizado no dia {sorteio.metadata['dataApuracao']}\n")

        res = sorteio.resultado
        res = [int(i) for i in res]

        # Pandas retorna um dict para excel com mais de 1 planilha
        for k, v in self.jogos.items():
            f.write(f"\n{k:=^20}\n")
            print(f"\n{k:=^20}\n")
            for key, value in funcs.checkScores(v, res).items():
                f.write(f"{key}: {value} acertos\n")
                print(f"{key}: {value} acertos\n")


    def callGenerator(self, nPlayed=0, nRemoved=0, nFixed=0, **kwargs):
        """ Chama o gerador de jogos adequado para os paramêtros dados

        :param nPlayed: Quantidade de números escolhidos por jogo
        :param nRemoved: Quantidade de números removidos do intervalo válido para o tipo de Loteria
        :param nFixed: Quantidade de números fixados do intervalo válido para o tipo de Loteria
        :param kwargs: Filtros inteligentes específicos para o gerador complexo
        :return: None. Chama o gerador.
        """

        removedNumbers, fixedNumbers = funcs.askUserFixedAndRemovedNumbers(nRemoved, nFixed)
        print(kwargs)
        if len(kwargs) == 0 or nPlayed > self.loteria.metadata["nRange"][0]:
            self.simpleGenerator(nPlayed, nRemoved, nFixed, removedNumbers, fixedNumbers)
        else:
            self.complexGenerator(nPlayed, removedNumbers, fixedNumbers, kwargs)

    def complexGenerator(self, nPlayed, removedNumbers, fixedNumbers, kwargs):
        """ Gerador inteligente que realiza queries na database de combinações possíveis

        :param nPlayed: Quantidade de números escolhidos por jogo
        :param removedNumbers: Números removidos
        :param fixedNumbers: Números fixados
        :param kwargs: Filtros específicos para a query
        :return: None. Cria n jogos pedidos pelo user
        """
        database = self.loteria.allJogosStandard
        combs = funcs.calcCombs(database, nPlayed, removedNumbers, fixedNumbers, kwargs)
        print("\n\033[1;30mO número de combinações possíveis são:", len(combs))
        nJogos = int(input("Quantos jogos deseja?"))
        index = list(combs.index)
        random.shuffle(index)
        self.jogos = combs.loc[index[:nJogos]]
        self.info()
        self.jogos = self.jogos.iloc[:, : nPlayed]
        self.writeJogos()

    def simpleGenerator(self, nPlayed, nRemoved, nFixed, removedNumbers, fixedNumbers):
        """ Gerador simples. Sem filtros específicos

        :param nPlayed: Quantidade de números escolhidos por jogo
        :param nRemoved: Quantidade de números removidos do intervalo válido para o tipo de Loteria
        :param nFixed: Quantidade de números fixados do intervalo válido para o tipo de Loteria
        :param removedNumbers: Números removidos
        :param fixedNumbers: Números fixados
        :return: None. Cria n jogos pedidos pelo user
        """

        nPossibles = self.loteria.metadata["nPossiveis"]
        nCombs = math.comb((25 - nRemoved - nFixed), (15 - nFixed))

        print("\n\033[1;30mO número de combinações possíveis são:", nCombs)
        nJogos = int(input("Quantos jogos deseja?"))

        jogos = [0]
        numbersAllowed = np.array(np.setdiff1d(np.array(range(1, nPossibles + 1)), removedNumbers))
        numbersAllowed = np.setdiff1d(numbersAllowed, fixedNumbers)
        numbersAllowedCopy = list(numbersAllowed)
        random.shuffle(numbersAllowedCopy)
        cont = 0
        while cont < nJogos:
            numbersAllowedCopy = list(numbersAllowed)
            np.random.RandomState(cont)
            jogo = np.zeros(nPlayed - nFixed)
            for i in range(0, jogo.size):
                number = np.random.choice(numbersAllowedCopy, 1)
                jogo[i] = number
                numbersAllowedCopy.remove(number)

            jogo = np.union1d(jogo, fixedNumbers).astype("int8")
            jogo = list(jogo)
            if jogo in jogos:
                continue
            else:
                jogos.append(jogo)
                cont += 1

        jogos.pop(0)
        self.jogos = pd.DataFrame(jogos)
        self.info()
        self.jogos = self.jogos.iloc[:, : nPlayed + 1]
        self.writeJogos()

    def info(self):
        """ Gera metadados sobre o conjunto de jogos

        :return: None. Atribui dados ao atributo metadata
        """
        nPos = self.loteria.metadata["nPossiveis"]
        if "isOdd" not in self.jogos.columns:
            self.metadata["isOdd"] = self.jogos.iloc[:, : nPos + 1]. \
                apply(funcs.isOdd, axis=1)
            self.metadata["maxSeq"] = self.jogos.iloc[:, : nPos + 1]. \
                apply(lambda x: funcs.sequences(x), axis=1).apply(
                lambda x: max(x))
            self.metadata["minSeq"] = self.jogos.iloc[:, : nPos + 1]. \
                apply(lambda x: funcs.sequences(x), axis=1).apply(lambda x: min(x))
            self.metadata["maxGap"] = self.jogos.iloc[:, : nPos + 1]. \
                apply(funcs.gap, axis=1).apply(lambda x: max(x))
            self.metadata["PrimeNumbers"] = self.jogos.iloc[:, : nPos + 1]. \
                apply(funcs.nPrimeNumbers, axis=1)
        else:
            self.metadata = self.jogos[["isOdd", "maxSeq", "minSeq", "maxGap", "nPrime"]]
