import pandas as pd
import numpy as np
import os
import json
from Librarie import funcs

#os.chdir(r"../")
#print(os.getcwd())

metadata = {"lotofacil": {'nAcertos': 15, 'nPossiveis': range(1, 26), 'nRange': range(15, 21)},
           "diadesorte": {'nAcertos': 7, 'nPossiveis': range(1, 32), 'nRange': range(7, 16)}}


class Loterias(object):

    def __init__(self, nome):
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
        self.metadata = metadata[nome]
        self.cAtual = self.getCurrentConc()
        self.filtered = False

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

    def numberRankingAll(self):
        """Rankeia os números mais sorteados na database de resultados

        :return: None. Define o metadado Ranking
        """
        n = self.metadata['nRange'][0]
        res = self.resultados.iloc[:, 1:n+1]
        rank = dict()
        for i in self.metadata["nPossiveis"]:
            v = np.where(res == i, True, False).sum()
            rank[f'{i}'] = v
        rankSeries = pd.Series(rank)
        rankSeries.sort_values(ascending=False, inplace=True)
        rankSeries.name = "Ranking Geral"
        self.metadata["Ranking"] = rankSeries
        return self.metadata["Ranking"]

    def queryResultsDatabase(self):
        """Analisa a database de reultados a critério do usuário

        :return:
        """
        pass

    def applyJogoMethodsOnDatabase(self):
        if not self.filtered:
            n = self.metadata["nRange"][0]

            self.resultados["isOdd"] = self.resultados.iloc[:, 1: n + 1].\
                apply(funcs.isOdd, axis=1)
            self.resultados["maxSeq"] = self.resultados.iloc[:, 1: n + 1]. \
                apply(lambda x: funcs.sequences(x), axis=1).apply(
                lambda x: max(x))
            self.resultados["minSeq"] = self.resultados.iloc[:, 1: n + 1]. \
                apply(lambda x: funcs.sequences(x), axis=1).apply(lambda x: min(x))
            self.resultados["maxGap"] = self.resultados.iloc[:, 1: n + 1]. \
                apply(funcs.gap, axis=1).apply(lambda x: max(x))
            self.resultados["nPrime"] = self.resultados.iloc[:, 1: n + 1].\
                apply(funcs.nPrimeNumbers, axis=1)
            self.filtered = True

