import pandas as pd
import requests
from requests.exceptions import RequestException


class Loterias(object):

    def __init__(self, nome, cAtual, **metadata):
        self.nome = nome
        self.resultados = pd.read_excel(f"../data/loterias/{nome}/resultados.xlsx",
                                        index_col=0,
                                        header=0,
                                        parse_dates=['Data'])
        self.cAtual = cAtual
        self.metadata = metadata

    def __str__(self):
        return f'A loteria criada possui os seguintes atributos:\
                \nNome: {self.nome}\
                \nAcertos para ganhar: {self.metadata["nAcertos"]}\
                \nNúmeros para jogar: {self.metadata["nPossiveis"]} \
                \nApostas disponíveis: {self.metadata["nRange"]} números por jogos'

    def atualiza_resultados(self, sorteio):
        print(sorteio)
        if (concursoatual := float(sorteio['numero'])) != self.cAtual:
            self.cAtual = concursoatual
            sorteioAtual = pd.DataFrame([[sorteio['dataApuracao']] + sorteio['listaDezenas']],
                                        columns=self.resultados.columns,
                                        index=[int(float(sorteio["numero"]))])
            self.resultados = self.resultados.append(sorteioAtual)
            self.resultados.sort_index(inplace=True, ascending=False, axis=0)
            self.resultados.to_excel(f'../data/loterias/{self.nome}/resultados.xlsx')

        else:
            print('O resultado do concurso atual ainda não está disponível')


class Sorteio(object):

    def __init__(self, Loterias, **metadata):
        self.loteria = Loterias
        self.resultado = 0
        self.metadata = metadata
        self.url_mapper = {"lotofacil": 'https://cutt.ly/LfnJrGv',
                           "diadesorte": "http://loterias.caixa.gov.br/wps/"
                                         "portal/loterias/landing/diadesorte/!ut/"
                                         "p/a1/jc5BDsIgFATQs3gCptICXdKSfpA2ujFWN"
                                         "oaVIdHqwnh-sXFr9c_qJ2-SYYGNLEzxmc7xkW5Tv"
                                         "Lz_IE6WvCoUwZPwArpTnZWD4SCewTGDlrQtZQ-gVGs4"
                                         "01gj6wFw4r8-vpzGr_6BhZmIoocFYUO7toLemqYGz0H"
                                         "1AUsTZ7Cw4X7dj0hu9QIyUWUw/dl5/d5/L2dBISEvZ0FB"
                                         "IS9nQSEh/pw/Z7_HGK818G0KO5GE0Q8PTB11800G3/res/i"
                                         "d=buscaResultado/c=cacheLevelPage/?timestampAjax=1614618624001"}

    def __str__(self):
        return f'Os dados do sorteio são:\
                \nConcurso: {self.loteria.cAtual}\
                \nPrêmio: {self.metadata["premio"]}\
                \nResultado: {self.resultado}\
                \nPrêmio: {self.metadata["premio"]}'

    def busca_resultado(self):
        url = self.url_mapper[f"{self.loteria.nome}"]
        try:
            resp = requests.get(url)
        except RequestException:
            print("O resultado do concurso atual não está disponível")
        else:
            self.resultado = resp.json()
            self.loteria.atualiza_resultados(self.resultado)


class Jogos(object):

    def __init__(self, jogosname, Sorteio, **metadata):
        self.jogosname = jogosname
        self.sorteio = Sorteio
        self.type = self.sorteio.loteria.nome
        self.jogos = pd.read_excel(f"../user_data/user_games/{self.type}/{self.jogosname}.xlsx",
                                   sheet_name=None,
                                   header=None,
                                   index_col=0)
        self.acertos = 0
        res = self.sorteio.resultado["listaDezenas"]
        res = [int(i) for i in res]
        self.resultado = res

    def confere_resultados(self):
        f = open(f"../user_data/user_games/{self.type}/resultados_{self.type}_{self.jogosname}.txt", "w+")
        f.write(f"Resultado referente ao concurso nº {self.sorteio.resultado['numero']} "
                f"da {self.sorteio.resultado['tipoJogo']} "
                f"realizado no dia {self.sorteio.resultado['dataApuracao']}\n")

        # Pandas retorna um dict para excel com mais de 1 planilha
        for k, v in self.jogos.items():
            f.write(f"\n{k:=^20}\n")
            for key, value in self.confere_acertos(v).items():
                f.write(f"{key}: {value} acertos\n")

    def confere_acertos(self, jogo):
        scores = dict()
        for name, jogo in jogo.iterrows():
            score = len(set(jogo) & set(self.resultado))
            scores[name] = score
        return scores


class Jogo:
    pass


if __name__ == "__main__":
    Lotofacil = Loterias("lotofacil", 2167, resultados=0, nAcertos=15, nPossiveis=25, nRange=range(15, 21))
    print(Lotofacil)
    sorteioloto = Sorteio(Lotofacil, premio=1500000, ganhadores=2)
    print(sorteioloto)
    sorteioloto.busca_resultado()
    jogos = Jogos("lotofacil", sorteioloto)
    jogos.confere_resultados()
