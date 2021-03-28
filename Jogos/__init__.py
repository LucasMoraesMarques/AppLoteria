import numpy as np
import pandas as pd
import random
import os
from Librarie import funcs, style as st

pd.set_option('display.max_columns', None)


class Jogos(object):

    def __init__(self, loto_type, name="default"):
        """ Classe Jogos

        :param loto_type: Tipo de Loteria
        :param name: Nome do conjunto de jogos
        """
        self.loteria = loto_type
        self.jogos = pd.DataFrame()
        self.nPlayed = self.loteria.metadata["nRange"][0]
        self.jogoname = name + ".xlsx"
        self.metadata = dict()

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
               "        - Funciona bem para números de jogos factíveis\n" \
               "    -> Gerador Complexo:\n" \
               "        - Cria combinações inteligentes levando em conta filtros pré-determinados\n" \
               "        - Usa a database contendo todas as combinações possíveis\n"

    def readJogos(self, name):
        """ Lê os jogos armazenados com o nome dado

        :param name: Nome do conjunto de jogos a ser lido
        :return: None
        """
        self.jogos = pd.read_excel(
            os.path.join(os.getcwd(), f"user_data\\user_games\\{self.loteria.nome}\\games\\{name}"),
            header=0,
            index_col=0)
        self.jogoname = name
        self.jogos.astype('int8')
        self.nPlayed = self.jogos.shape[1]

    def writeJogos(self):
        """ Salva os jogos em um arquivo excel

        :return: None
        """
        self.jogos.index = [f"Jogo {i}" for i in range(1, self.jogos.shape[0]+1)]
        self.jogos.columns = [f"bola {i}" for i in range(1, self.nPlayed + 1)]
        self.jogos.to_excel(
            os.path.join(os.getcwd(), f"user_data\\user_games\\{self.loteria.nome}\\games\\{self.jogoname}"))

    def delete(self):
        """ Deleta o arquivo de um determinado set de jogos

        :return: None
        """
        os.remove(os.path.join(os.getcwd(), f"user_data\\user_games\\{self.loteria.nome}\\games\\{self.jogoname}"),)

    def getExternalJogos(self, manual=False, clipboarb=False, nPlayed=0, nJogos=0, jogoname='', path='', filename=''):
        """ Lê jogos externos entrados pelo user

        :param manual: Especifica se a entrada será por digitação
        :param clipboarb: Especifica se a entrada será por Área de Transferência
        :param nPlayed: Número de marcações por jogo
        :param nJogos: Número de jogos a serem lidos
        :param jogoname: Nome do conjunto de jogos lido
        :param path: Se manual e clipboard são falsos, especifica o caminho do arquivo a ser lido
        :param filename: Nome do arquivo a ser lido no path dado
        :return: None
        """

        self.jogoname = jogoname + ".xlsx"

        if manual:
            jogos = funcs.getExternalJogo(nJogos, nPlayed, nrange=self.loteria.metadata["nPossiveis"])
            self.jogos = pd.DataFrame.from_dict(jogos, orient="index")
            self.nPlayed = nPlayed
            self.writeJogos()

        elif path != '':
            try:
                path += f"/{filename}"
                ext = filename.split(".")[-1]
                if ext in ['txt', 'text', 'csv']:
                    jogos = pd.read_csv(path, header=None, index_col=None, sep=r"\s+|[,]", engine='python')
                elif ext in ["xlsx", 'xls']:
                    jogos = pd.read_excel(path, header=None, index_col=None)
                else:
                    raise FileNotFoundError
                if jogos.shape[1] not in self.loteria.metadata['nRange']:
                    raise ValueError

            except (FileExistsError, FileNotFoundError):
                print(st.textLine("Não foi possível encontrar o arquivo. Tente novamente com um endereço absoluto para "
                                  "o diretório do arquivo.\n", 'vermelho'))
                filename = input(st.textLine("Digite o nome do arquivo com extensão:", 'amarelo'))
                self.getExternalJogos(path=input(st.textLine("Endereço do diretório:", 'amarelo')),
                                      jogoname=self.jogoname, filename=filename)

            except ValueError:
                print(st.textLine("Os jogos carregados não seguem os números de marcações permitidas pelo tipo de "
                                  "loteria.\n", 'vermelho'))
                return
            else:
                self.jogos = jogos
                self.nPlayed = jogos.shape[1]
                self.writeJogos()

        elif clipboarb:
            try:
                jogos = pd.read_clipboard(sep=r"[,]|\s+", header=None)
                if jogos.shape[1] not in self.loteria.metadata['nRange']:
                    raise ValueError
            except pd.errors.EmptyDataError:
                print(st.textLine("Não há nada para ser lido no clipboard", 'vermelho'))
            except ValueError:
                print(st.textLine("Não há jogos com o padrão esperado na Área de Transferência. "
                                  "Leia o menu ajuda.", 'vermelho'))
            else:
                self.jogos = jogos
                self.nPlayed = self.jogos.shape[1]
                self.writeJogos()

    def checkResults(self, sorteio):
        """ Confere os resultados para dado conjunto de jogos

        :param sorteio: Instância da classe Sorteio
        :return: None. Exporta para arquivo.
        """
        filePath = os.path.join(os.getcwd(), f"user_data\\user_games\\{self.loteria.nome}"
                                           f"\\results\\res_{self.loteria.nome}_{sorteio.metadata['numero']}_"
                                             f"{self.jogoname.replace('.xlsx', '')}.txt")

        with open(filePath, "w+") as f:
            f.write(f"Resultado referente ao concurso nº {sorteio.metadata['numero']} "
                f"da {sorteio.metadata['tipoJogo']} "
                f"realizado no dia {sorteio.metadata['dataApuracao']}\n")

        if self.loteria.nome == 'diadesorte':
            res = [int(i) for i in sorteio.resultado[0:7]]
        else:
            res = sorteio.resultado
            res = [int(i) for i in res]

        print(st.textLine(f'Os resultados do jogo {self.jogoname.replace(".xlsx", "")} são:', 'azul'))

        with open(filePath, "a") as f:
            if type(self.jogos) == dict:
                # Pandas retorna um dict para excel com mais de 1 planilha
                for k, v in self.jogos.items():
                    f.write(f"\n{k:=^20}\n")
                    for key, value in funcs.checkScores(v, res).items():
                        f.write(f"{key}: {value} acertos\n")
                        print(st.textLine(f"{key}: ", 'azul') + st.textLine(f"{value} acertos", 'verde'))

            elif type(self.jogos) == pd.core.frame.DataFrame:
                f.write(f"\n{self.jogoname.replace('.xlsx', ''):=^20}\n")
                for k, v in self.jogos.iterrows():
                    scores = funcs.checkScores(v, res)
                    f.write(f"{k}: {scores} acertos\n")
                    print(st.textLine(f"{k}: ", 'azul') + st.textLine(f"{scores} acertos", 'verde'))

        print(st.textLine(f"\nOs resultados podem ser exportados através do arquivo txt no seguinte diretório:",'azul'))
        print(st.textLine(f"\nuser_data\\user_games\\{self.loteria.nome}"
                          f"\\results\\res_{self.loteria.nome}_{sorteio.metadata['numero']}_"
                          f"{self.jogoname.replace('.xlsx', '')}.txt", 'amarelo'))

    def complexGenerator(self, nPlayed, removedNumbers, fixedNumbers, **kwargs):
        """ Gerador inteligente que realiza queries na database de combinações possíveis

        :param nPlayed: Quantidade de números escolhidos por jogo
        :param removedNumbers: Números removidos
        :param fixedNumbers: Números fixados
        :param kwargs: Filtros específicos para a query
        :return: None. Cria n jogos pedidos pelo user dentro dos possíveis
        """

        database = self.loteria.allJogosStandard
        combs = funcs.calcCombs(database, nPlayed, removedNumbers, fixedNumbers, kwargs)
        print("\n\033[1;30mO número de combinações possíveis são:", len(combs))

        if len(combs) != 0:
            nJogos = funcs.leia_int(st.textLine("Quantos jogos deseja?", 'azul'), nrange=range(1, combs.shape[0] + 1))
            index = list(combs.index)
            random.shuffle(index)
            self.jogos = combs.loc[index[:nJogos]]
            self.jogos.index = range(1, nJogos + 1)
            self.applyFiltersOnJogos()
            self.jogos = self.jogos.iloc[:, : nPlayed]
            self.writeJogos()
        else:
            print(st.textLine("Não há combinações com esses filtros", 'vermelho'))

    def simpleGenerator(self, nPlayed, nJogos, removedNumbers, fixedNumbers):
        """ Gerador simples. Sem filtros específicos

        :param nPlayed: Quantidade de números escolhidos por jogo
        :param nJogos: Número de jogos a ser criado
        :param removedNumbers: Números removidos
        :param fixedNumbers: Números fixados
        :return: None. Cria n jogos pedidos pelo user
        """
        nFixed = len(fixedNumbers)
        nPossibles = self.loteria.metadata["nPossiveis"]
        self.nPlayed = nPlayed
        jogos = [0]
        numbersAllowed = np.array(np.setdiff1d(np.array(nPossibles), removedNumbers))
        numbersAllowed = np.setdiff1d(numbersAllowed, fixedNumbers)

        cont = 0
        while cont < nJogos:
            numbersAllowedCopy = list(numbersAllowed)
            random.shuffle(numbersAllowedCopy)
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
        self.writeJogos()

    def applyFiltersOnJogos(self):
        """ Gera metadados dos filtros sobre o conjunto de jogos

        :return: None. Atribui dados ao atributo metadata
        """
        nPos = self.nPlayed
        self.metadata["Jogos Filtrados"] = pd.DataFrame()
        dt = self.metadata["Jogos Filtrados"]
        dt["isOdd"] = self.jogos.iloc[:, : nPos].apply(funcs.isOdd, axis=1)
        dt["maxSeq"] = self.jogos.iloc[:, : nPos].apply(lambda x: funcs.sequences(x), axis=1).\
            apply(lambda x: max(x))
        dt["minSeq"] = self.jogos.iloc[:, : nPos].apply(lambda x: funcs.sequences(x), axis=1).\
            apply(lambda x: min(x))
        dt["maxGap"] = self.jogos.iloc[:, : nPos].apply(funcs.gap, axis=1).apply(lambda x: max(x))
        dt["nPrime"] = self.jogos.iloc[:, : nPos].apply(funcs.nPrimeNumbers, axis=1)

    def showDatabaseMetadata(self):
        """ Imprime metadados sobre a database do set de jogos carregado

        :return: None
        """
        if self.jogos.shape[0] > 200:
            print(st.textLine("Os primeiros 200 jogos são:", 'azul'))
            print(self.jogos.iloc[:200, :].to_string())
        else:
            print(st.textLine("Os jogos carregados são:", 'azul'))
            print(self.jogos.to_string())

        print(st.textLine("\nO ranking dos números é:", 'amarelo'))
        print(st.textLine(self.numberRankingAll().to_string()))
        print(st.textLine("\nAs informações dos filtros são:\n"))

        for col in ['isOdd', 'maxGap', 'maxSeq', 'minSeq', 'nPrime']:
            if col != 'isOdd':
                print(funcs.transFilterNames(col))
                print(st.textLine("Número Repetições", 'amarelo'))
            else:
                print(funcs.transFilterNames(col))
                print(st.textLine("Ímpar Repetições", 'amarelo'))
            print(st.textLine(self.metadata["Jogos Filtrados"][col].value_counts().to_string()))

    def filterDatabase(self, filters):
        """ Realiza queries na database de jogos com os filtros dados

        :param filters: Dicionário com os filtros entrados pelo user
        :return: None
        """
        dt = self.jogos.copy()
        for filter, value in filters.items():
            funcs.transFilterNames(filter)
            if 'min' in filter:
                dt = dt.loc[self.metadata["Jogos Filtrados"][filter] >= value]
            elif 'max' in filter:
                dt = dt.loc[self.metadata["Jogos Filtrados"][filter] <= value]
            elif filter in ['isOdd', 'nPrime']:
                dt = dt.loc[self.metadata["Jogos Filtrados"][filter] == value]

        if dt.shape[0] != 0:
            print(st.textLine(f"A database resultante da aplicação dos filtros é:", 'amarelo'))
            print(st.textLine(dt.to_string()))
            print(st.textLine(f"\nA database filtrada possui {dt.shape[0]} jogos, sendo que a database original"
                              f" tinha {self.jogos.shape[0]}, o que resulta numa redução de "
                              f"{round(100*(1-round(dt.shape[0]/self.jogos.shape[0], 2)), 2)} %", 'amarelo'))
        else:
            print(st.textLine(f"Não há jogos com essas combinações de filtros", 'vermelho'))

    def numberRankingAll(self):
        """Rankeia os números mais sorteados na database de jogos

        :return: Ranking dos números
        """
        print(self.jogos)
        rank = dict()
        for i in self.loteria.metadata["nPossiveis"]:
            v = np.where(self.jogos == i, True, False).sum()
            rank[f'{i}'] = v
        rankSeries = pd.Series(rank)
        rankSeries.sort_values(ascending=False, inplace=True)
        rankSeries.name = "Ranking Geral"
        self.metadata["Ranking"] = rankSeries
        return self.metadata["Ranking"]
