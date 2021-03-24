from pyfiglet import Figlet
from termcolor import colored


def beautifulPrint(text, color='white'):
    font = Figlet(font='slant')
    print((colored(font.renderText(text), color=color)))


def printLine(amount=35):
    print(color('AZUL') + '--'*amount)


def header():
    printLine()
    beautifulPrint("APP Loterias", 'green')
    print(textLine("Seja bem-vindo ao App Loterias. O que deseja fazer?"))


def footer():
    printLine()
    beautifulPrint("VOLTE SEMPRE", 'green')
    printLine()


def color(color='BRANCO'):
   """
   Função que simplifica o código Ansi para cores no terminal do python.
   :param color: Recebe a cor de forma nominal.
   :return: Retorna o código \033[-;-;m correspondente a cor.
   """""
   colors = {'PADRÃO':'\033[m', 'BRANCO': "\033[1;30m", 'VERMELHO': "\033[1;31m", 'VERDE': "\033[1;32m", 'AMARELO': "\033[1;33m", 'AZUL': "\033[1;34m", 'MAGENTA': "\033[1;35m", 'CIANO': "\033[1;36m", 'CINZA': '\033[1;37m', 'TITULO':'\033[1;31;107m'}
   for k, v in colors.items():
       if color.strip().upper() == k:
           return v


def textLine(msg, cor='BRANCO',):
    """
    Função que retorna um heading estilístico.
    Ex.:   -=-=-=-=-=-=
              PYTHON
           -=-=-=-=-=-=
    :param msg: Recebe a string a ser formatada.(OBRIGATÓRIO)
    :param cor: Recebe uma cor nominal segundo a função ansi_colors.(OPCIONAL: O default é o padrão da função ansi_colors)
    :return: Retorna o heading formatado com a string e sua respectiva cor.
    """
    n = color(cor)
    msg = str(msg)
    return n + msg + color()


def menuOptions(file_msg, item_color, text_color):
    with open(file_msg, 'r', encoding="utf-8") as f:
        printLine()
        for line in f.readlines():
            line = line.replace('\n', '')
            if (d:='->') in line:
                line = line.split('->')
                print(color(item_color) + line[0] + d + color(text_color) + line[1])
                continue
            print(line)
        printLine()
        f.close()

