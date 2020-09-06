import numpy as np
import pandas as pd
import csv
from ProjetosLoteria.App.Sorteio import Sorteio, Loterias, Jogos
import requests
from openpyxl import load_workbook


url = 'https://cutt.ly/LfnJrGv'


def carrega_resultados():
    resultados = pd.read_excel('teste.xlsx', index_col=0, parse_dates=['Data'])
    cAtual = resultados.index[0]
    loto = Loterias('Lotofácil', cAtual, resultados)
    return loto


def busca_resultado(url):
    while True:
        resp = requests.get(url)
        if resp.status_code == 200:
            resultado = resp.json()
            break
        else:
            continue
    return resultado


def atualiza_resultados(dtf, resultado, loto):
    if float(resultado['nu_concurso']) != loto.cAtual:
        res = pd.DataFrame([[resultado['dt_apuracaoStr']] + resultado['resultadoOrdenado'].split('-')], columns=dtf.columns, index=[int(float(resultado["nu_concurso"]))])
        dt = dtf.append(res)
        dt.sort_index(inplace=True, ascending=False, axis=0)
        dt.to_excel('teste.xlsx')
        return dt
    else:
        print('O resultado do concurso atual ainda não está disponível')


def confere_jogos(Loto, conc):
    book = load_workbook('Jogo.xlsx')
    nome_jogos = book.sheetnames
    file = 'resultados.txt'
    f = open(file, 'wt')
    f.write(f'Resultado referente ao Concurso nº{Loto.cAtual}({Loto.resultados.iloc[0, 0]}) da Lotofácil\n')
    for nome in nome_jogos:
        sheet = book[f'{nome}']
        l = sheet.max_row
        jogos = dict()
        for row in sheet.iter_rows(min_row=1, max_row=l, max_col=16):
            for i, cell in enumerate(row):
                if i == 0:
                    name = cell.value
                    jogos[name] = set()
                else:
                    jogos[name].add(int(cell.value))
        jogos = Jogos(conc, jogos)
        acertos = jogos.confere_acertos()
        f.write(f'\n{"-=" * 5} {nome} {"-=" * 5}\n')
        #print(f'\n{"-=" * 5} {nome} {"-=" * 5}\n')
        for j_name, pts in acertos:
        #    print(f'{j_name}: {pts} acertos')
            f.write(f'{j_name}: {pts} acertos\n')

    f.close()


Loto = carrega_resultados()
conc = Sorteio(Loto)
dt = Loto.resultados
resultado = busca_resultado(url)
print(Loto.cAtual)

dt = atualiza_resultados(dt, resultado, Loto)
print(pd.read_excel('teste.xlsx', index_col=0))
print(Loto.res_atual)
confere_jogos(Loto, conc)






