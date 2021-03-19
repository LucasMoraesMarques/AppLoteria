from my_package import style
from Sorteio import Sorteio
from Loterias import Loterias
from Jogos import Jogos
import os
from requests import RequestException
import pandas as pd

mapping = {"1": 'lotofacil', '2': 'diadesorte'}
msgMenu = "1 -> Cadastrar Jogos\n" \
          "2 -> Criar Jogos\n" \
          "3 -> Carregar Jogos\n" \
          "4 -> Buscar último sorteio\n" \
          "5 -> Estatísticas\n" \
          "Digite -1 para sair"

msgOp3 = "O que você deseja fazer com o jogo carregado? As opções são:\n" \
         "1 -> Conferir resultados\n" \
         "2 -> Filtrar jogos\n" \
         "3 -> Mostrar estatísticas\n" \
         "4 -> Deletar jogos\n" \
         "Digite -1 para voltar ao menu principal"

msgOp3_1 = "Qual sorteio você deseja conferir?\n" \
           "1 -> O último\n" \
           "2 -> Outro qualquer\n" \
           "Digite -2 para voltar ao menu de jogos\n"

msgOp3_2 = "Digite o concurso a ser conferido:"


def leia_int(msg):
    """Função que trata os erros de um input de um número inteiro

    :param msg: Recebe o texto a ser printado para o usuário
    :return: Retorna inteiro digitado sem erros no  programa
    """
    while True:
        try:
            n = int(input(f"{style.ansi_colors('branco')}" + msg))
        except (ValueError, TypeError):
            print(f'{style.ansi_colors("vermelho")}ERRO! Digite um número inteiro válido.')
            continue
        except KeyboardInterrupt:
            print(f'{style.ansi_colors("vermelho")}{"O usuário preferiu não digitar esse número"}{style.ansi_colors("branco")}')
            return 0
        else:
            return n


def getUserInput():
    return leia_int("Opção:")


def getUserFilters(loto):
    msg1 = "\nOs filtros dispovíveis são:\n" \
          "-> Máxima diferença entre dois números consecutivos\n" \
          "-> Máxima e mínima sequência ininterrupta de números\n" \
          "-> Quantidade de números primos\n" \
          "-> Remoção de números\n" \
          "-> Fixação de números\n" \
          "Digite 0 para não usar o filtro."
    print(style.ansi_colors("branco") + msg1)

    filters = {"maxGap": leia_int("Máxima diferença entre dois números consecutivos:"),
               "minSeq": leia_int("Mínima sequência de números:"),
               "maxSeq": leia_int("Máxima sequência de números:"),
               "nPrime": leia_int("Quantidade de números primos:"),
               }

    for k, v in filters.copy().items():
        if v == 0:
            del filters[k]
    print(filters)
    nRemoved = leia_int("Deseja remover quantos números?")
    nFixed = leia_int("Deseja fixar quantos números?")
    msg2 = f"Você pode escolher de {list(loto.metadata['nRange'])} dentre os {loto.metadata['nPossiveis']} possíveis.\n"
    print(style.ansi_colors("branco") + msg2 )
    nPlayed = leia_int("Quantos números deseja em cada jogo?")
    return nPlayed, nRemoved, nFixed, filters

def showOptions(msg):
    style.print_msg_line(msg, cor="branco")


def showLotoOptions():
    msg = "\nAs opções de Loteria disponíveis são:\n" \
          "1 -> Lotofácil\n" \
          "2 -> Dia de Sorte"
    print(style.ansi_colors(color="branco") + msg)


def createLoto():
    showLotoOptions()
    lotoType = getUserInput()
    lotoInstance = Loterias(mapping[f"{lotoType}"], nAcertos=15, nPossiveis=25, nRange=range(15, 21))
    return lotoInstance


def createSorteio(loto):
    sorteio = Sorteio(loto)
    return sorteio


def makeJogos(loto):
    name = input("Qual nome identificará esse jogo?")
    jogo = Jogos(loto, name=name)
    nPlayed, nRemoved, nFixed, filters = getUserFilters(loto)
    print(nPlayed, nRemoved, nFixed)
    jogo.callGenerator(nPlayed, nRemoved, nFixed, **filters)



def loadJogos():
    showLotoOptions()
    lotoType = getUserInput()
    savedJogos = os.listdir(os.path.join(os.getcwd(), f"user_data\\user_games\\{mapping[f'{lotoType}']}\\games"))
    if len(savedJogos) != 0:
        print(style.ansi_colors(color="branco") + "Jogos Disponíveis:")
        for i, j in enumerate(savedJogos):
            print(f" {i + 1} -> {j.replace('.xlsx', '')}")
        choice = getUserInput()
        name = savedJogos[choice-1]
        loto = Loterias(mapping[f'{lotoType}'], nAcertos=15, nPossiveis=25, nRange=range(15, 21))
        jogos = Jogos(loto)
        jogos.readJogos(name)
        return jogos

    else:
        print("Não há nenhum jogo salvo. Tente criar alguns.")

def getLastResult():
    loto = createLoto()
    sorteio = createSorteio(loto)
    try:
        sorteio.requestLastResult()
    except RequestException:
        pass
    else:
        sorteio.readConfig()
        return sorteio.info()

def handleLoadedJogos(userInput, jogos):
    while userInput != -1:
        showOptions(msgOp3)
        userInput = getUserInput()
        if userInput == 1:
            handleSorteioResults(jogos)


def handleSorteioResults(jogos):
    showOptions(msgOp3_1)
    choice = getUserInput()
    loto = jogos.loteria
    sorteio = Sorteio(loto)
    if choice == -2:
        showOptions(msgOp3)
    elif choice == 1:
        sorteio.requestLastResult()
        jogos.checkResults(sorteio)
    elif choice == 2:
        print(style.ansi_colors("branco") + msgOp3_2)




def menu():
    style.headings("APP LOTERIA", cor="azul", l=80)
    style.headings("Seja bem-vindo ao App Loterias. O que deseja fazer?", l=80)
    userInput = 999
    while userInput != -1:
        showOptions(msgMenu)
        userInput = getUserInput()
        if userInput == 1:
            pass
        elif userInput == 2:
            loto = createLoto()
            jogos = makeJogos(loto)
        elif userInput == 3:
            loadedJogos = loadJogos()
            handleLoadedJogos(userInput, loadedJogos)

        elif userInput == 4:
            getLastResult()


