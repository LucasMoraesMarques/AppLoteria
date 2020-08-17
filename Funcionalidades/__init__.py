import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
import csv
from ProjetosLoteria.App.Sorteio import Sorteio

url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/'
option = Options()
option.headless = True
driver = webdriver.Firefox(executable_path=r'C:\Users\Lucas\PycharmProjects\ProjetosLoteria\App\app\Lib\site-packages\selenium\webdriver\common\geckodriver.exe', options=option)
file = 'resultados.xlsx'
cAnt = 2011


def carregaResultados(file):
    dt = pd.read_excel(file).astype('object')
    return dt


def armazenaResultado(url, cAnt, file):
    dt = carregaResultados(file)
    col = dt.columns.array
    print(col)
    conc = atualizaResultados(url, cAnt)
    try:
        if conc.resultado.any() != None:
            data = np.concatenate((dt, conc.resultado), axis=0)
            dt = pd.DataFrame(data, columns=col)
            dt.iloc[:, 0] = dt.iloc[:, 0].astype('int')
            dt.iloc[:, 2:16] = dt.iloc[:, 2:16].astype('int')
            dt.sort_values('Concurso', axis=0, ascending=False, inplace=True)
            dt.index = range(2012, 0, -1)
            print(dt)
            return dt
    except AttributeError:
        pass



def atualizaResultados(url, cAnt):
    driver.get(url)
    driver.implicitly_wait(15)
    cAtual = buscaUltimoConcurso(url)
    try:
        if int(cAtual[0]) > cAnt:
            element = driver.find_element_by_xpath('//*[@id="resultados"]/div[2]/div/div/div[1]/table')
            soup = BeautifulSoup(element.text, 'html5lib')
            match = re.findall(r'<body>([0-9\s]+?)</body>', soup.prettify(), flags=re.MULTILINE)
            res = match[0].strip().replace('\n', ' ').split(' ')
            resultado = np.array([list(cAtual) + res]).astype('object')
            driver.close()
            concAtual = Sorteio(cAtual[0], cAtual[1], resultado, 'Lotofácil')
            driver.quit()
        else:
            print('O concurso atual não está disponível')
            return None
    except (ValueError, TypeError):
        print('O Web Scraping não obteve o resultado esperado. Tente novamente')
        return None
    else:
        return concAtual



def buscaUltimoConcurso(url):
    driver.get(url)
    driver.implicitly_wait(15)
    try:
        conc = driver.find_element_by_class_name('ng-binding')
        cAtual = re.search(r'([0-9]{4}).+?(\d\d/\d\d/\d\d\d\d)', str(conc.text)).groups()
    except:
        print('A busca pelo último concurso não foi realizada com sucesso')
    else:
        return cAtual


def criaDataCsv(url, cAnt, file):
    data = armazenaResultado(url, cAnt, file)
    data.to_csv('dt_resultados.csv', index=False)

criaDataCsv(url, cAnt, file)
