import requests
from requests.exceptions import RequestException
import json
import os
from Librarie import style as st


class Sorteio(object):

    def __init__(self, Loterias):
        """ Classe Sorteio

        :param Loterias: Tipo de Loteria
        """
        self.loteria = Loterias
        self.resultado = self.readConfig()
        self.metadata = {}
        self.url_mapper = {"lotofacil": 'https://cutt.ly/LfnJrGv',
                           "diadesorte": "https://cutt.ly/BzX3Grq",
                           "megasena": 'https://cutt.ly/AxGhxYz'
                           }

    def __str__(self):
        return "Classe Sorteio:\n" \
               "    -> Recebe um tipo de Loteria e busca e atualiza resultados a cada sorteio " \


    def requestLastResult(self):
        """Faz uma busca na "API" de resultados da Caixa

        :return: None. Atualiza a database de resultados da Loteria dada
        """
        url = self.url_mapper[f"{self.loteria.nome}"]
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                raise RequestException
        except RequestException:
            print(st.textLine("O resultado do concurso atual não está disponível", 'vermelho'))
        else:
            self.metadata = resp.json()
            if self.metadata['numero'] != self.readConfig()['numero']:
                print(st.textLine('Aguarde um momento! Encontramos um novo resultado e estamos atualizando a '
                                  'database de resultados.', 'azul'))
                self.writeConfig()
                self.loteria.updateResults()

            if self.loteria.nome in ['lotofacil', 'megasena']:
                self.resultado = self.metadata["listaDezenas"]
            elif self.loteria.nome == "diadesorte":
                self.resultado = self.metadata["listaDezenas"] + [self.metadata["nomeTimeCoracaoMesSorte"].strip()]

    def writeConfig(self):
        """ Salva os dados do último resultado

        :return: None
        """
        with open(os.path.join(os.getcwd(), f"data\\loterias\\{self.loteria.nome}\\resultadosconfig.json"), 'w+') as f:
            json.dump(self.metadata, f, indent=4)

    def readConfig(self):
        """ Lê os dados do último resultado

        :return: None
        """
        with open(os.path.join(os.getcwd(), f"data\\loterias\\{self.loteria.nome}\\resultadosconfig.json"), 'r') as f:
            return json.load(f)

    def info(self):
        """ Mostra os metadados do sorteio atual

        :return: None
        """
        for k, v in self.metadata.items():
            if k == "tipoJogo":
                print(st.textLine(f"\nLoteria: ", 'azul') + st.textLine(f"{v.capitalize()}", 'amarelo'))
            elif k == "numero":
                print(st.textLine(f"\nConcurso: ", 'azul') + st.textLine(f"{v}", 'amarelo'))
            elif k == "dataApuracao":
                print(st.textLine(f"\nData: ", 'azul') + st.textLine(f"{v}", 'amarelo'))
            elif k == "acumulado":
                if v:
                    print(st.textLine(f"\nValor acumulado para o concurso {self.metadata['numero']+1} dia "
                          f"{self.metadata['dataProximoConcurso']}: "
                          f"{self.metadata['valorAcumuladoProximoConcurso']}", 'azul'))
            elif k == "listaDezenas":
                print(st.textLine(f"\nDezenas sorteadas: ", 'azul'))
                for i in v:
                    print(st.textLine(i, 'amarelo'), end=" ")
                print('\n')
            elif k == self.metadata["nomeTimeCoracaoMesSorte"] and k not in ['', None, 0]:
                print(f"\n{v}")
            elif k == "listaRateioPremio":
                for i in self.metadata["listaRateioPremio"]:
                    print(st.textLine(f"{i['descricaoFaixa']}", 'azul'))
                    print(st.textLine(f' -> Prêmio: {i["valorPremio"]}', 'azul'))
                    print(st.textLine(f' -> Número de ganhadores: {i["numeroDeGanhadores"]}\n', 'azul'))


