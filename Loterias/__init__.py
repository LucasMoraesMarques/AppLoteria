import pandas as pd
import numpy as np
import os
import json
import Jogos.funcs

#os.chdir(r"../")
print(os.getcwd())


class Loterias(object):

    def __init__(self, nome, **metadata):
        """ Classe Loterias

        :param nome: Tipo da loteria
        :param metadata: Metadados do tipo
        """
        self.nome = nome
        self.file = os.path.join(os.getcwd(), f"data\\loterias\\{nome}\\resultados.xlsx")
        self.resultados = pd.read_excel(self.file,
                                        index_col=0,
                                        header=0,
                                        parse_dates=['Data'])
        self.allJogosStandard = pd.read_pickle(os.path.join(os.getcwd(), f"data\\loterias\\{self.nome}\\todasCombsFiltradas.csv"))
        self.metadata = metadata
        self.cAtual = self.getCurrentConc()

    def __str__(self):
        return "Classe Loterias" \
               "    -> Possui todos os jogos possíveis" \
               "    -> Possui todos os resultados" \
               "    -> Aplica filtros na database de resultados"

    def getCurrentConc(self):
        """ Busca o número do último concurso

        :return: Último concurso
        """
        with open(os.path.join(os.getcwd(), f"settings\\{self.nome}\\resultadosconfig.json"), 'r') as f:
            lastConc = json.load(f)
        return lastConc["numero"]

    def updateResults(self, sorteio):
        """Atualiza database de resultados

        :param sorteio: Instância de Sorteio que realizará a busca na API de resultados
        :return: None
        """

        if (concursoatual := float(sorteio['numero'])) != self.cAtual:
            self.cAtual = concursoatual
            if self.nome == "lotofacil":
                sorteioAtual = pd.DataFrame([[sorteio['dataApuracao']] + sorteio['listaDezenas']],
                                            columns=self.resultados.columns,
                                            index=[int(float(sorteio["numero"]))],
                                            dtype="int8")

            elif self.nome == "diadesorte":
                sorteioAtual = pd.DataFrame([[sorteio['dataApuracao']] + sorteio['listaDezenas'] + [sorteio["nomeTimeCoracaoMesSorte"]]],
                                            columns=self.resultados.columns,
                                            index=[int(float(sorteio["numero"]))],
                                            dtype="int8")

            self.resultados = self.resultados.append(sorteioAtual)
            self.resultados.sort_index(inplace=True, ascending=False, axis=0)
            self.resultados.to_excel(self.file)

        else:
            print('O resultado do concurso atual ainda não está disponível. O último resultado encontrado foi:')

    def numberRankingAll(self):
        """Rankeia os números mais sorteados na database de resultados

        :return: None. Define o metadado Ranking
        """
        res = self.resultados.iloc[:, 1:]
        rank = dict()
        for i in range(1, self.metadata["nPossiveis"] + 1):
            v = np.where(res == i, True, False).sum()
            rank[f'{i}'] = v
        rankSeries = pd.Series(rank)
        rankSeries.sort_values(ascending=False, inplace=True)
        rankSeries.name = "Ranking Geral"
        self.metadata["Ranking"] = rankSeries

    def queryResultsDatabase(self):
        """Analisa a database de reultados a critério do usuário

        :return:
        """
        pass

    def applyJogoMethodsOnDatabase(self):
        nPos = self.metadata["nPossiveis"]

        self.resultados["isOdd"] = self.resultados.iloc[:, 1: nPos+ 1].\
            apply(funcs.isOdd, axis=1)
        self.resultados["maxSeq"] = self.resultados.iloc[:, 1: nPos+ 1]. \
            apply(lambda x: funcs.sequences(x), axis=1).apply(
            lambda x: max(x))
        self.resultados["minSeq"] = self.resultados.iloc[:, 1: nPos+ 1]. \
            apply(lambda x: funcs.sequences(x), axis=1).apply(lambda x: min(x))
        self.resultados["maxGap"] = self.resultados.iloc[:, 1: nPos+ 1]. \
            apply(funcs.gap, axis=1).apply(lambda x: max(x))
        self.resultados["PrimeNumbers"] = self.resultados.iloc[:, 1: nPos+ 1].\
            apply(funcs.nPrimeNumbers, axis=1)

