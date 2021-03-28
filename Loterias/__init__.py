import pandas as pd
import numpy as np
import os
import requests
import json
from Librarie import funcs

metadata = {
    "lotofacil": {'nAcertos': 15, 'nPossiveis': range(1, 26), 'nRange': range(15, 21), 'nFaixas': 4},
    "diadesorte": {'nAcertos': 7, 'nPossiveis': range(1, 32), 'nRange': range(7, 16), 'nFaixas': 5},
    "megasena": {'nAcertos': 6, 'nPossiveis': range(1, 61), 'nRange': range(6, 16), 'nFaixas': 3}
}

url_mapper = {
    "lotofacil": r'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/',
    "megasena": r'http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbwMPI0sDBxNXAOMwrzCjA0sjIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wNnUwNHfxcnSwBgIDUyhCvA5EawAjxsKckMjDDI9FQE-F4ca/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K8DBC0QPVN93KQ10G1/res/id=historicoHTML/c=cacheLevelPage/=/',
    "diadesorte": r'http://loterias.caixa.gov.br/wps/portal/loterias/landing/diadesorte/!ut/p/a1/jc5BDsIgFATQs3gCptICXdKSfpA2ujFWNoaVIdHqwnh-sXFr9c_qJ2-SYYGNLEzxmc7xkW5TvLz_IE6WvCoUwZPwArpTnZWD4SCewTGDlrQtZQ-gVGs401gj6wFw4r8-vpzGr_6BhZmIoocFYUO7toLemqYGz0H1AUsTZ7Cw4X7dj0hu9QIyUWUw/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0KGAB50QMU0UQ6S1004/res/id=historicoHTML/c=cacheLevelPage/=/'
}


class Loterias(object):

    def __init__(self, nome):
        """ Classe Loterias

        :param nome: Tipo de Loteria
        """
        self.nome = nome
        self.file = os.path.join(os.getcwd(), f"data\\loterias\\{nome}\\resultados.xlsx")
        self.resultados = pd.read_excel(self.file,
                                        header=0,
                                        index_col=0)
        self.allJogosStandard = 0
        self.metadata = metadata[nome]
        self.cAtual = self.getCurrentConc()
        self.upgraded = False
        self.filtered = False
        self.checkUpgrade()

    def __str__(self):
        return """Classe Loterias\n
    -> Possui todos os jogos possíveis\n
    -> Possui todos os resultados \n
    -> Aplica filtros na database de resultados\n"""

    def checkUpgrade(self):
        """Verifica se o user baixou o upgrade com todas as combinações possíveis

        :return: None
        """
        try:
            dt = pd.read_pickle(os.path.join(os.getcwd(), f"data\\loterias\\{self.nome}\\todasCombsFiltradas.csv"))
        except FileNotFoundError:
            pass
        else:
            self.upgraded = True
            self.allJogosStandard = dt

    def getCurrentConc(self):
        """ Busca o número do último concurso

        :return: Último concurso
        """
        with open(os.path.join(os.getcwd(), f"data\\loterias\\{self.nome}\\resultadosconfig.json"), 'r') as f:
            lastConc = json.load(f)
        return lastConc["numero"]

    def updateResults(self):
        """Atualiza database de resultados

        :return: None
        """
        while True:
            try:
                resp = requests.get(url_mapper[self.nome])
                if resp.status_code != 200:
                    raise requests.exceptions.RequestException
            except requests.exceptions.RequestException:
                continue
            else:
                dt = pd.read_html(resp.text, decimal=',', thousands='.')[0]
                if self.nome == 'megasena':
                    columns = ['Concurso', 'Local', 'Data do Sorteio', 'Bola 1', 'Bola 2', 'Bola 3', 'Bola 4',
                               'Bola 5', 'Bola 6', 'Ganhadores 6 acertos', 'Ganhadores 5 acertos', 'Ganhadores 4 acertos',
                               'Rateio 6 acertos', 'Rateio 5 acertos', 'Rateio 4 acertos', 'Cidade', 'Valor Arrecadado',
                               'Estimativa para o próximo concurso', 'Valor Acumulado Próximo Concurso', 'Acumulado',
                               'Sorteio Especial', 'Observação']
                    dt.columns = columns
                    dt = dt.drop('Observação', axis=1)

                elif self.nome == "diadesorte":
                    columns = ['Concurso', 'Local', 'Data do Sorteio', 'Bola 1', 'Bola 2', 'Bola 3', 'Bola 4',
                               'Bola 5', 'Bola 6', 'Bola 7', 'Mês da Sorte', 'Ganhadores 7 acertos', 'Ganhadores 6 acertos',
                               'Ganhadores 5 acertos', 'Ganhadores 4 acertos', 'Ganhadores Mês de Sorte', 'Rateio 7 acertos',
                               'Rateio 6 acertos', 'Rateio 5 acertos', 'Rateio 4 acertos', 'Rateio Mês de Sorte', 'Cidade',
                               'Valor Arrecadado', 'Estimativa para o próximo concurso',
                               'Valor Acumulado Próximo Concurso', 'Acumulado', 'Sorteio Especial', 'Observação']
                    dt.columns = columns
                    dt = dt.drop('Observação', axis=1)
                elif self.nome == "lotofacil":
                    columns = ['Concurso', 'Data do Sorteio', 'Bola 1', 'Bola 2', 'Bola 3', 'Bola 4', 'Bola 5', 'Bola 6',
                               'Bola 7', 'Bola 8', 'Bola 9', 'Bola 10', 'Bola 11', 'Bola 12', 'Bola 13', 'Bola 14',
                               'Bola 15', 'Valor Arrecadado', 'Ganhadores 15 acertos', 'Cidade', 'Ganhadores 14 acertos',
                               'Ganhadores 13 acertos', 'Ganhadores 12 acertos', 'Ganhadores 11 acertos', 'Rateio 15 acertos',
                               'Rateio 14 acertos', 'Rateio 13 acertos', 'Rateio 12 acertos', 'Rateio 11 acertos', 'Acumulado',
                               'Estimativa para o próximo concurso', 'Sorteio Especial']
                    dt.columns = columns
                dt = dt.dropna(how='any', thresh=3)
                dt['Concurso'] = dt['Concurso'].astype("int64")
                dt.set_index('Concurso', inplace=True)
                dt.sort_index(ascending=False, inplace=True)
                dt.to_excel(self.file)
                return dt

    def numberRankingAll(self):
        """Rankeia os números mais sorteados na database de resultados

        :return: Ranking
        """
        n = self.metadata['nRange'][0]
        res = self.resultados.loc[:, [f'Bola {i}' for i in range(1, n+1)]]
        rank = dict()
        for i in self.metadata["nPossiveis"]:
            v = np.where(res == i, True, False).sum()
            rank[f'{i}'] = v
        rankSeries = pd.Series(rank)
        rankSeries.sort_values(ascending=False, inplace=True)
        rankSeries.name = "Ranking Geral"
        self.metadata["Ranking"] = rankSeries
        return self.metadata["Ranking"]

    def queryResultsDatabase(self, filters):
        """Analisa a database de resultados a critério do usuário

        :return: Database filtrada
        """
        dt = self.resultados.copy()
        for filter, value in filters.items():
            if 'min' in filter:
                dt = dt[dt[filter] >= value]
            elif 'max' in filter:
                dt = dt[dt[filter] <= value]
            elif filter in ['isOdd', 'nPrime']:
                dt = dt[dt[filter] == value]
        return dt

    def applyJogoMethodsOnDatabase(self):
        """Gera as colunas de filtro na database de resultados

        :return: None
        """
        if not self.filtered:
            n = self.metadata["nRange"][0]
            sliceDezenas = self.resultados.loc[:, [f'Bola {i}' for i in range(1, n+1)]]
            self.resultados["isOdd"] = sliceDezenas.apply(funcs.isOdd, axis=1)
            self.resultados["maxSeq"] = sliceDezenas.apply(lambda x: funcs.sequences(x), axis=1).apply(
                lambda x: max(x))
            self.resultados["minSeq"] = sliceDezenas.apply(lambda x: funcs.sequences(x), axis=1).apply(lambda x: min(x))
            self.resultados["maxGap"] = sliceDezenas.apply(funcs.gap, axis=1).apply(lambda x: max(x))
            self.resultados["nPrime"] = sliceDezenas.apply(funcs.nPrimeNumbers, axis=1)
            self.filtered = True
