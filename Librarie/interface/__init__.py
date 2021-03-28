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
msgMenuDownload = 'Librarie/interface/menumsg/main/menuDownload.txt'
msgMenuSobre = 'Librarie/interface/menumsg/main/menuSobre.txt'
msgLotoOptions = 'Librarie/interface/menumsg/menuLotoOptions.txt'
msgLotoOptionsCombs = 'Librarie/interface/menumsg/menuLotoOptionsCombs.txt'
msgOp1 = 'Librarie/interface/menumsg/Op1/menuOp1.txt'
msgOp1_1 = 'Librarie/interface/menumsg/Op1/menuOp1_1.txt'
msgOp2 = 'Librarie/interface/menumsg/Op2/menuOp2.txt'
msgOp2_2 = 'Librarie/interface/menumsg/Op2/menuOp2_2.txt'
msgOp3 = 'Librarie/interface/menumsg/Op3/menuOp3.txt'
msgOp3_1 = 'Librarie/interface/menumsg/Op3/menuOp3_1.txt'
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
    if loto.upgraded:
        showOptions(msgOp2)
        gerador = getUserInput(range(1, 3))
        name = input(st.textLine("Qual nome identificará esse jogo?", 'azul'))
        jogo = Jogos(loto, name=name)
        if gerador == 1:
            removedNumbers, fixedNumbers, nPlayed, nJogos = fc.askUserFixedAndRemovedNumbers(loto)
            jogo.simpleGenerator(nPlayed, nJogos, removedNumbers, fixedNumbers)
        else:
            removedNumbers, fixedNumbers, nPlayed = fc.askUserFixedAndRemovedNumbers(loto, gen=2)
            filters = getUserFilters()
            jogo.complexGenerator(nPlayed, removedNumbers, fixedNumbers, **filters)
    else:
        print(st.textLine("Somente o gerador simples está disponível. Com ele você pode"
                          " criar jogos \nrandômicos excluindo e fixando números, sem limites"
                          " de números marcados.", 'azul'))
        name = input(st.textLine("\nQual nome identificará esse jogo?", 'azul'))
        jogo = Jogos(loto, name=name)
        removedNumbers, fixedNumbers, nPlayed, nJogos = fc.askUserFixedAndRemovedNumbers(loto)
        jogo.simpleGenerator(nPlayed, nJogos, removedNumbers, fixedNumbers)

    if jogo.jogos.shape[0] > 200:
        print(st.textLine("\nOs primeiros 200 jogos criados são:"), 'azul')
        print(jogo.jogos.head(200).to_string())
    else:
        print(st.textLine("\nOs  jogos criados são:"), 'azul')
        print(jogo.jogos.to_string())


def loadJogos():
    showOptions(msgLotoOptions)
    lotoType = getUserInput(nrange=range(1, 4))
    savedJogos = os.listdir(os.path.join(os.getcwd(), f"user_data\\user_games\\{mapping[f'{lotoType}']}\\games"))
    if len(savedJogos) != 0:
        print(st.textLine("Jogos Disponíveis:", 'azul'))
        for i, j in enumerate(savedJogos):
            print(st.textLine(f" {i + 1} ->", 'vermelho') + st.textLine(f" {j.replace('.xlsx', '')}", 'amarelo'))
        choice = getUserInput(nrange=range(1, len(savedJogos) + 1))
        name = savedJogos[choice-1]
        loto = Loterias(mapping[f'{lotoType}'])
        jogos = Jogos(loto)
        jogos.readJogos(name)
        if jogos.jogos.shape[0] > 200:
            print(st.textLine("Os primeiros 200 jogos são:", 'azul'))
            print(jogos.jogos.iloc[:200, :].to_string())
        else:
            print(st.textLine("Os jogos carregados são:", 'azul'))
            print(jogos.jogos.to_string())

        return jogos
    else:
        print(st.textLine("Não há nenhum jogo salvo. Tente criar alguns.", 'azul'))




def getResult(last=True):
    loto = createLoto()
    sorteio = createSorteio(loto)
    if last:
        try:
            sorteio.requestLastResult()
        except RequestException:
            pass
        else:
            print('O último resultado encontrado foi:')
            sorteio.readConfig()
            return sorteio.info()
    else:
        return loto.resultados.head(50).to_string()


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
            print(st.textLine(f"Deseja realmente apagar o jogo {jogos.jogoname.replace('.xlsx', '')}? 1 para sim, 0 para não", 'vermelho'))
            userInput = getUserInput(allowed=[0, 1])
            if userInput == 1:
                print(st.textLine(f"O jogo {jogos.jogoname.replace('.xlsx', '')} foi deletado com sucesso", 'verde'))
                jogos.delete()
                del jogos
                return
            else:
                continue
    return


def handleSorteioResults(jogos):
    showOptions(msgOp3_1)
    choice = getUserInput(allowed=[-4, 1, 2])
    loto = jogos.loteria
    sorteio = Sorteio(loto)
    if choice == -4:
        showOptions(msgOp3)
    elif choice == 1:
        sorteio.requestLastResult()
        jogos.checkResults(sorteio)
    elif choice == 2:
        print(st.textLine(f"A {loto.nome.upper()} possui {loto.resultados.shape[0]} concursos. Escolha um: ", 'azul'))
        userInput = getUserInput(allowed=loto.resultados.index.astype('int64').to_list())
        sorteio = Sorteio(loto)
        sorteio.resultado = loto.resultados.loc[userInput, f'Bola 1' : f'Bola {loto.metadata["nRange"][0]}':]
        sorteio.metadata['numero'] = userInput
        sorteio.metadata['tipoJogo'] = loto.nome
        sorteio.metadata['dataApuracao'] = loto.resultados.loc[userInput, 'Data do Sorteio']
        jogos.checkResults(sorteio)


def enterExternalJogos():
    loto = createLoto()
    jogo = Jogos(loto)
    showOptions(msgOp1)
    choice = getUserInput(allowed=[-3] + list(range(1, 4)))
    if choice == -3:
        return 1
    else:
        showOptions(msgOp1_1)
        name = input(st.textLine("Digite um nome identificativo para o jogo: ", 'amarelo'))
        if choice == 1:
            nJogos = fc.leia_int(st.textLine("Digite a quantidade de jogos a serem carregados: ", 'amarelo'), nrange=range(1, 1000000))
            nPlayed = fc.leia_int(st.textLine("Digite a quantidade de números por jogos: ", 'amarelo'), nrange=loto.metadata["nRange"])
            jogo.getExternalJogos(manual=True, nPlayed=nPlayed, nJogos=nJogos, jogoname=name)
        elif choice == 2:
            file = input(st.textLine("Digite o nome do arquivo com extensão:", 'amarelo'))
            path = input(st.textLine("Digite o endereço completo do diretório do arquivo:", 'amarelo'))
            jogo.getExternalJogos(path=path, jogoname=name, filename=file)
        else:
            jogo.getExternalJogos(clipboarb=True, jogoname=name)

    if jogo.jogos.shape[0] > 0:
        print(st.textLine("Os jogos carregados são:\n", 'azul'))
        print(jogo.jogos)


def showDatabaseMetadata(loto):
    print(st.textLine("\nA database de resultados é:", 'amarelo'))
    print(st.textLine(loto.resultados.iloc[:50, :].to_string()))
    print(st.textLine("\nO ranking dos números é:", 'amarelo'))
    print(st.textLine(loto.numberRankingAll().to_string()))
    print(st.textLine("\nAs informações dos filtros são:"))
    for col in ['isOdd', 'maxGap', 'maxSeq', 'minSeq', 'nPrime']:
        print(fc.transFilterNames(col))
        if col != 'isOdd':
            print(st.textLine("Número Repetições", 'amarelo'))
        else:
            print(st.textLine("Ímpar Repetições", 'amarelo'))
        print(st.textLine(loto.resultados[col].value_counts().to_string()))


def filterDatabase(loto):
    filters = getUserFilters()
    dt = loto.queryResultsDatabase(filters)
    if dt.shape[0] != 0:
        print(st.textLine(f"\nA database resultante da aplicação dos filtros é:", 'amarelo'))
        print(st.textLine(dt.to_string()))
        print(st.textLine(f'\nA aplicação dos filtros resulta numa redução de '
                          f'{(1 - round(len(dt)/len(loto.resultados), 2))*100}% na database de resultados', 'amarelo'))
    else:
        print(st.textLine(f"Não há resultados com essas combinações de filtros", 'vermelho'))


def rankAllCombs():
    showOptions(msgLotoOptionsCombs)
    lotoType = getUserInput(allowed=list(range(1, 3)))
    loto = Loterias(mapping[f"{lotoType}"])
    nRange = loto.metadata['nPossiveis'][-1]
    n = fc.leia_int(st.textLine('Escolha dupla(2), trio(3), etc ... para checar as combinações:', 'amarelo'), nrange=loto.metadata['nPossiveis'])
    nTotal = comb(nRange, n)
    print(st.textLine(f"O número de combinações de {nRange} tomadas {n} a {n} é {nTotal}", 'amarelo'))
    print(st.textLine("\nEsse processo pode demorar muito dependendo do total de combinações", 'vermelho'))
    print(st.textLine(f"\nCalculando ...", 'verde'))
    nUplas = fc.makeCombinations(n, nRange)
    combs = fc.binaryMapping(nUplas)
    ranking = fc.checkCombinations(combs, loto.resultados[[f'Bola {i}' for i in range(1, loto.metadata["nRange"][0] + 1)]])
    if ranking.shape[0] < 200:
        print(st.textLine("\nAs combinações são:", 'amarelo'))
        print(ranking.to_string())
    else:
        print(st.textLine("\nAs primeiras 200 combinações são:"))
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
                            rankAllCombs()
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
    return userInput


def menuDownload(userInput):
    while userInput != -2:
        showOptions(msgMenuDownload)
        userInput = getUserInput(allowed=[-2, 1, 2])
        if userInput == 1:
            print(st.textLine(f"O link para download é {'https://drive.google.com/file/d/1sEwHmGXO8H4LTQyPnF21piJ87B5Dl_r2/view?usp=sharing'}", 'azul'))
            print(st.textLine("Coloque o arquivo no seguinte diretório:", 'azul'))
            print(st.textLine('App/data/loterias/diadesorte', 'azul'))
            return -2
        elif userInput == 2:
            print(st.textLine(f"O link para download é {'https://drive.google.com/file/d/1zbczYhLB_m84VdUDPZ_PhZ7yFUpJgVV0/view?usp=sharing'}", 'azul'))
            print(st.textLine("Coloque o arquivo no seguinte diretório:", 'azul'))
            print(st.textLine('App/data/loterias/lotofacil', 'azul'))
            return -2
    return userInput


def menu():
    userInput = 999
    while userInput != -1:
        showOptions(msgMenuInicial)
        userInput = getUserInput(allowed=[-1, 1, 2, 3, 4])
        while userInput != -2 and userInput != -1:
            if userInput == 1:
                userInput = menuIniciar(userInput)
            elif userInput == 2:
                userInput = menuAjuda(userInput)
            elif userInput == 3:
                userInput = menuDownload(userInput)
            elif userInput == 4:
                showOptions(msgMenuSobre)
                userInput = -2

