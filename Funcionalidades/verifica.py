import requests
import pandas as pd
import openpyxl

url = 'https://cutt.ly/LfnJrGv'
file = r"C:\Users\Lucas\PycharmProjects\ProjetosLoteria\App\Funcionalidades\Jogo.xlsx"
file_res = r"C:\Users\Lucas\PycharmProjects\ProjetosLoteria\App\Funcionalidades\resultados.txt"


def busca_resultado(url):
    while True:
        resp = requests.get(url)
        if resp.status_code == 200:
            resultado = resp.json()
            break
        else:
            continue
    return resultado


def busca_jogos(file):
    jogos = pd.read_excel(file, sheet_name=None, header=None, index_col=0)

    return jogos


def confere_resultados(resultado, jogos, file):
    res = resultado["listaDezenas"]
    res = [int(i) for i in res]
    jogos = jogos
    file = file
    f = open(file, "w+")
    f.write(f"Resultado referente ao concurso nº {resultado['numero']} da {resultado['tipoJogo']} "
            f"realizado no dia {resultado['dataApuracao']}\n")
    # Pandas retorna um dict para excel com mais de 1 planilha
    for k, v in jogos.items():
        f.write(f"\n{k:=^20}\n")
        for k, v in acertos(res, v).items():
            f.write(f"{k}: {v} acertos\n")


def acertos(resultados, jogos):
    scores = dict()
    for name, jogo in jogos.iterrows():
        score = len(set(jogo) & set(resultados))
        scores[name] = score
    return scores


if __name__ == "__main__":
    res = busca_resultado(url)
    jogos = busca_jogos(file)
    confere_resultados(res, jogos, file_res)


