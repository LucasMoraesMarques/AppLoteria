from Librarie import style as st
from Librarie import funcs as fc
from Sorteio import Sorteio
from Loterias import Loterias
from Jogos import Jogos
import os
import pandas as pd
from requests import RequestException
from math import comb

pd.set_option('display.max_columns', None)

mapping = {"1": 'lotofacil', '2': 'diadesorte', '3': 'megasena'}
msgMenuInicial = 'Librarie/interface/menumsg/main/menuInicial.txt'
msgMenuIniciar = 'Librarie/interface/menumsg/main/menuIniciar.txt'
msgMenuAjuda = 'Librarie/interface/menumsg/main/menuAjuda/menuAjuda.txt'
msgMenuAjudaOp1 = 'Librarie/interface/menumsg/main/menuAjuda/menuAjudaOp1.txt'
msgMenuAjudaOp1_1 = 'Librarie/interface/menumsg/main/menuAjuda/menuAjudaOp1_1.txt'
msgMenuAjudaOp1_2 = 'Librarie/interface/menumsg/main/menuAjuda/menuAjudaOp1_2.txt'
msgMenuAjudaOp1_3 = 'Librarie/interface/menumsg/main/menuAjuda/menuAjudaOp1_3.txt'
msgMenuAjudaOp2 = 'Librarie/interface/menumsg/main/menuAjuda/menuAjudaOp2.txt'
msgMenuSobre = 'Librarie/interface/menumsg/main/menuSobre.txt'
msgLotoOptions = 'Librarie/interface/menumsg/menuLotoOptions.txt'
msgOp1 = 'Librarie/interface/menumsg/Op1/menuOp1.txt'
msgOp1_1 = 'Librarie/interface/menumsg/Op1/menuOp1_1.txt'
msgOp2 = 'Librarie/interface/menumsg/Op2/menuOp2.txt'
msgOp2_2 = 'Librarie/interface/menumsg/Op2/menuOp2_2.txt'
msgOp3 = 'Librarie/interface/menumsg/Op3/menuOp3.txt'
msgOp3_1 = 'Librarie/interface/menumsg/Op3/menuOp3_1.txt'
msgOp3_2 = 'Librarie/interface/menumsg/Op3/menuOp3_2.txt'
msgOp4 = 'Librarie/interface/menumsg/Op4/menuOp4.txt'
msgOp4_3 = 'Librarie/interface/menumsg/Op4/menuOp4_3.txt'


def getUserInput(nrange=0, allowed=0):
    return fc.leia_int(f"{st.color()}Opção:", nrange, allowed)


def getUserFilters():
    showOptions(msgOp2_2)
    filters = {f"maxGap": fc.leia_int(st.textLine("Máxima diferença entre dois números consecutivos:", 'azul')),
               "minSeq": fc.leia_int(st.textLine("Mínima sequência de números:", 'azul')),
               "maxSeq": fc.leia_int(st.textLine("Máxima sequência de números:", 'azul')),
               "nPrime": fc.leia_int(st.textLine("Quantidade de números primos:", 'azul')),
               "isOdd": fc.leia_int(st.textLine("É ímpar: ", 'azul'))
               }

    for k, v in filters.copy().items():
        if v == -1:
            del filters[k]
    print(filters)

    return filters


def showOptions(file_msg):
    st.menuOptions(file_msg, item_color="VERMELHO", text_color="AMARELO")


def createLoto():
    showOptions(msgLotoOptions)
    lotoType = getUserInput(allowed=list(range(1, 4)))
    lotoInstance = Loterias(mapping[f"{lotoType}"])
    return lotoInstance


def createSorteio(loto):
    sorteio = Sorteio(loto)
    return sorteio


def makeJogos(loto):
    showOptions(msgOp2)
    gerador = getUserInput(range(1, 3))
    name = input(st.textLine("Qual nome identificará esse jogo?"))
    jogo = Jogos(loto, name=name)
    if gerador == 1:
        removedNumbers, fixedNumbers, nPlayed, nJogos = fc.askUserFixedAndRemovedNumbers(loto)
        jogo.simpleGenerator(nPlayed, nJogos, removedNumbers, fixedNumbers)
        print(jogo.jogos.head())
    else:
        removedNumbers, fixedNumbers, nPlayed = fc.askUserFixedAndRemovedNumbers(loto, gen=2)
        filters = getUserFilters()
        jogo.complexGenerator(nPlayed, removedNumbers, fixedNumbers, filters)
        print(jogo.jogos.head())


def loadJogos():
    showOptions(msgLotoOptions)
    lotoType = getUserInput(nrange=range(1, 4))
    savedJogos = os.listdir(os.path.join(os.getcwd(), f"user_data\\user_games\\{mapping[f'{lotoType}']}\\games"))
    if len(savedJogos) != 0:
        print(st.textLine("Jogos Disponíveis:"))
        for i, j in enumerate(savedJogos):
            print(f" {i + 1} -> {j.replace('.xlsx', '')}")
        choice = getUserInput(nrange=range(1, len(savedJogos) + 1))
        name = savedJogos[choice-1]
        loto = Loterias(mapping[f'{lotoType}'])
        jogos = Jogos(loto)
        jogos.readJogos(name)
        print(jogos.jogos.to_string())
        return jogos

    else:
        print(st.textLine("Não há nenhum jogo salvo. Tente criar alguns."))


def getResult(last=True):
    loto = createLoto()
    sorteio = createSorteio(loto)
    if last:
        try:
            sorteio.requestLastResult()
        except RequestException:
            pass
        else:
            sorteio.readConfig()
            return sorteio.info()
    else:
        return loto.resultados.to_string


def handleLoadedJogos(userInput, jogos):
    while userInput != -3:
        showOptions(msgOp3)
        userInput = getUserInput(allowed=[-3] + list(range(1, 5)))
        if userInput == 1:
            handleSorteioResults(jogos)
        elif userInput == 2:
            jogos.applyFiltersOnJogos()
            filters = getUserFilters()
            jogos.filterDatabase(filters)
        elif userInput == 3:
            jogos.applyFiltersOnJogos()
            jogos.showDatabaseMetadata()
        elif userInput == 4:
            print(st.textLine(f"Deseja realmente apagar o jogo {jogos.jogoname.replace('.xlsx', '')}? 1 para sim, 0 para não"))
            userInput = getUserInput(allowed=[0, 1])
            if userInput == 1:
                print(st.textLine(f"O jogo {jogos.jogoname.replace('.xlsx', '')} foi deletado com sucesso"))
                jogos.delete()
                del jogos
                return
            else:
                continue
    return


def handleSorteioResults(jogos):
    showOptions(msgOp3_1)
    choice = getUserInput(allowed=[-4] + list(range(1, 3)))
    loto = jogos.loteria
    sorteio = Sorteio(loto)
    if choice == -4:
        showOptions(msgOp3)
    elif choice == 1:
        sorteio.requestLastResult()
        jogos.checkResults(sorteio)
    elif choice == 2:
        showOptions(msgOp3_2)
        userInput = getUserInput(allowed=loto.resultados.index)


def enterExternalJogos():
    loto = createLoto()
    jogo = Jogos(loto)
    showOptions(msgOp1)
    choice = getUserInput(allowed=[-3] + list(range(1, 4)))
    if choice == -3:
        return 1
    elif choice == 1:
        showOptions(msgOp1_1)
        name = input(st.textLine("Digite um nome identificativo para o jogo: "))
        nJogos = fc.leia_int("Digite a quantidade de jogos a serem carregados: ", nrange=range(1, 1000000))
        nPlayed = fc.leia_int("Digite a quantidade de números por jogos: ", nrange=loto.metadata["nRange"])
        jogo.getExternalJogos(manual=True, nPlayed=nPlayed, nJogos=nJogos, jogoname=name)
    elif choice == 2:
        name = input(st.textLine("Digite um nome identificativo para o jogo:"))
        file = input(st.textLine("Digite o nome do arquivo com extensão:"))
        path = input(st.textLine("Digite o endereço completo do arquivo:"))
        jogo.getExternalJogos(path=path, jogoname=name, filename=file)
    else:
        name = input(st.textLine("Digite um nome identificativo para o jogo:"))
        jogo.getExternalJogos(clipboarb=True, jogoname=name)
    print(jogo.jogos)


def showDatabaseMetadata(loto):
    print(st.textLine("ESSA FUNCIONALIDADE AINDA NÃO ESTÁ DISPONÍVEL PARA A MEGA SENA", 'vermelho'))
    print(st.textLine("\nA database de resultados é:", 'amarelo'))
    print(st.textLine(loto.resultados.to_string()))
    print(st.textLine("\nO ranking dos números é:", 'amarelo'))
    print(st.textLine(loto.numberRankingAll().to_string()))
    print(st.textLine("\nAs informações dos filtros são:"))
    for col in ['isOdd', 'maxGap', 'maxSeq', 'minSeq', 'nPrime']:
        fc.transFilterNames(col)
        if col != 'isOdd':
            print(st.textLine("Número Repetições", 'amarelo'))
        else:
            print(st.textLine("Ímpar Repetições", 'amarelo'))
        print(st.textLine(loto.resultados[col].value_counts().to_string()))


def filterDatabase(loto):
    print(st.textLine("ESSA FUNCIONALIDADE AINDA NÃO ESTÁ DISPONÍVEL PARA A MEGA SENA", 'vermelho'))
    filters = getUserFilters()
    dt = loto.resultados.copy()
    for filter, value in filters.items():
        fc.transFilterNames(filter)
        if 'min' in filter:
            dt = dt[dt[filter] >= value]
        elif 'max' in filter:
            dt = dt[dt[filter] <= value]
        elif filter in ['isOdd', 'nPrime']:
            dt = dt[dt[filter] == value]
    if dt.shape[0] != 0:
        print(st.textLine(f"A database resultante da aplicação dos filtros é:"))
        print(st.textLine(dt.to_string()))
    else:
        print(st.textLine(f"Não há resultados com essas combinações de filtros"))


def rankAllCombs(loto):
    nRange = loto.metadata['nPossiveis'][-1]
    n = fc.leia_int(st.textLine('Escolha dupla(2), trio(3), etc ... para checar as combinações:', 'amarelo'), nrange=loto.metadata['nPossiveis'])
    nTotal = comb(nRange, n)
    print(nTotal)
    nUplas = fc.makeCombinations(n, nRange)
    combs = fc.binaryMapping(nUplas)
    ranking = fc.checkCombinations(combs, loto.resultados[[f'bola {i}' for i in range(1, loto.metadata["nRange"][0] + 1)]])
    print(st.textLine(f"O número de combinações de {nRange} tomadas {n} a {n} é {nTotal}", 'amarelo'))
    if ranking.shape[0] < 200:
        print(st.textLine("As combinações são:", 'amarelo'))
        print(ranking.to_string())
    else:
        print("As primeiras 200 combinações são:")
        print(ranking.iloc[:200].to_string())


def menuIniciar(userInput):
    while userInput != -2:
        showOptions(msgMenuIniciar)
        userInput = getUserInput(allowed=[-2] + list(range(1, 5)))
        if userInput == 1:
            enterExternalJogos()
        elif userInput == 2:
            loto = createLoto()
            makeJogos(loto)
        elif userInput == 3:
            loadedJogos = loadJogos()
            if loadedJogos:
                handleLoadedJogos(userInput, loadedJogos)
        elif userInput == 4:
            while userInput != -3:
                showOptions(msgOp4)
                userInput = getUserInput(allowed=[-3, 1, 2, 3])
                if userInput == 1:
                    getResult()
                elif userInput == 2:
                    print(getResult(last=False))
                elif userInput == 3:
                    while userInput != -4:
                        showOptions(msgOp4_3)
                        userInput = getUserInput(allowed=[-4, 1, 2, 3])
                        if userInput == 1:
                            loto = createLoto()
                            loto.applyJogoMethodsOnDatabase()
                            showDatabaseMetadata(loto)
                        elif userInput == 2:
                            loto = createLoto()
                            loto.applyJogoMethodsOnDatabase()
                            filterDatabase(loto)
                        elif userInput == 3:
                            loto = createLoto()
                            rankAllCombs(loto)
    return -2


def menuAjuda(userInput):
    while userInput != -2:
        showOptions(msgMenuAjuda)
        userInput = getUserInput(allowed=[-2, 1, 2])
        if userInput == 1:
            showOptions(msgMenuAjudaOp1)
            userInput = getUserInput(allowed=[-2, 1, 2, 3])
            if userInput == 1:
                showOptions(msgMenuAjudaOp1_1)
            elif userInput == 2:
                showOptions(msgMenuAjudaOp1_2)
            elif userInput == 3:
                showOptions(msgMenuAjudaOp1_3)
        elif userInput == 2:
            showOptions(msgMenuAjudaOp2)
    return -2


def menu():
    userInput = 999
    while userInput != -1:
        showOptions(msgMenuInicial)
        userInput = getUserInput(allowed=[-1, 1, 2, 3])
        while userInput != -2 and userInput != -1:
            if userInput == 1:
                userInput = menuIniciar(userInput)
            elif userInput == 2:
                userInput = menuAjuda(userInput)
            elif userInput == 3:
                showOptions(msgMenuSobre)
                userInput = -2


