import pandas as pd
import requests
from requests.exceptions import RequestException
import json
import os

#os.chdir(r"../")


class Sorteio(object):

    def __init__(self, Loterias):
        """ Classe Sorteio

        :param Loterias: Tipo de Loteria
        """
        self.loteria = Loterias
        self.resultado = self.readConfig()
        self.metadata = {}
        self.url_mapper = {"lotofacil": 'https://cutt.ly/LfnJrGv',
                           "diadesorte": "https://cutt.ly/BzX3Grq"}

    def __str__(self):
        return "Classe Sorteio:" \
               "    -> Recebe um tipo de Loteria e busca e atualiza resultados a cada sorteio " \


    def requestLastResult(self):
        """Faz uma busca na API de resultados da Caixa

        :return: None. Atualiza a database de resultados da Loteria dada
        """
        url = self.url_mapper[f"{self.loteria.nome}"]
        try:
            resp = requests.get(url)
        except RequestException:
            print("O resultado do concurso atual não está disponível")
        else:
            self.metadata = resp.json()
            self.writeConfig()
            if self.loteria.nome == "lotofacil":
                self.resultado = self.metadata["listaDezenas"]
            elif self.loteria.nome == "diadesorte":
                self.resultado = self.metadata["listaDezenas"] + [self.metadata["nomeTimeCoracaoMesSorte"]]
            self.loteria.updateResults(self.metadata)
            print('O último resultado encontrado foi:')
            print(self.resultado)

    def writeConfig(self):
        """ Salva os dados do último resultado

        :return: None
        """
        with open(os.path.join(os.getcwd(), f"settings\\{self.loteria.nome}\\resultadosconfig.json"), 'w+') as f:
            json.dump(self.metadata, f, indent=4)

    def readConfig(self):
        """ Lê os dados do último resultado

        :return: None
        """
        with open(os.path.join(os.getcwd(), f"settings\\{self.loteria.nome}\\resultadosconfig.json"), 'r') as f:
            return json.load(f)

    def info(self):
        """ Mostra os metadados do sorteio atual

        :return: None
        """
        for k, v in self.metadata.items():
            if k == "tipoJogo":
                print(f"Loteria: {v.capitalize()}")
            elif k == "numero":
                print(f"Concurso: {v}")
            elif k == "dataApuracao":
                print(f"Data: {v}")
            elif k == "acumulado":
                if v:
                    print(f"Valor acumulado para o concurso {self.metadata['numero']+1} dia "
                          f"{self.metadata['dataProximoConcurso']}: "
                          f"{self.metadata['valorAcumuladoProximoConcurso']}")
            elif k == "listaDezenas":
                print(f"Dezenas sorteadas: ")
                for i in v:
                    print(i, end= " ")
                print('\n')
            elif k == self.metadata["nomeTimeCoracaoMesSorte"] and k not in ['', None, 0]:
                print(f"{v}")
            elif k == "listaRateioPremio":
                for i in self.metadata["listaRateioPremio"]:
                    print(f"{i['descricaoFaixa']}")
                    print(f' -> Prêmio: {i["valorPremio"]}')
                    print(f' -> Número de ganhadores: {i["numeroDeGanhadores"]}')


