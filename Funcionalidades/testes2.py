'''Referenciando os Módulos usados e as funções/métodos importados'''
from random import randint, seed
from math import comb
import time

def num_reset(num, fix, nfix):
    """'''Criando a função que reseta a lista dos números sorteados em cada jogo.

    :param num: Recebe a lista com um jogo feito para ser resetada
    :param fix: É a quantia de números fixados pelo usuário
    :param nfix: Contém os número fixados
    :return: Retorna a lista num resetada
    """
    num = []                                # Reseta a lista de números
    for i in range(0, fix):
        num.append(nfix[i])                 # Preenche com os fixados e novamente zera até o limite do sorteio (15 números para lotofácil)
        if (i == (fix - 1)):
            for j in range(fix, 15):
                num.append(0)
            return num                     # Retorna a lista num inicial pronta para o próximo jogo.


'''Referenciando as variáveis globais'''
excld = []      # Armazena os números retirados do sorteio.
nfix = []       # Armazena os números fixados no sorteio.
num = []        # Armazena jogo a jogo criado e, após a verificação, a lista jogos o recebe e chama a função para resetá-la.
jogos = []      # Armazena os n-jogos pedidos pelo usuário.


'''Iniciando o programa'''
print(f"\033[m\033[1;31;107m{'SORTEADOR LOTOFÁCIL':=^185}\033[m")



erro = int(input("Quantos números você deseja retirar do sorteio?"))      # Pede a quantia de números a serem retirados do sorteio.
for i in range(0, erro):
    excld.append(int(input(f"\033[1;32mDigite o número {i+1}: ")))           # Pede os números a serem retirados.

fix = int(input("\n\033[1;30mQuantos números você deseja fixar?"))      # Pede a quantia de números a serem fixados no sorteio.
for i in range(0, fix):
    x = int(input(f"\033[1;32mDigite o número {i+1}: "))                # Pede os números a serem fixados.
    num.append(x)
    nfix.append(x)
    if i == (fix - 1):
        for j in range(fix, 15):     # Completa o jogo com zeros, respeitando os números fixados.
            num.append(0)

'''Mostrando as n-possibilidades derivadas das opções do usuário'''
ncomb = comb((25 - erro - fix), (15 - fix))                                 # Calcula, por combinação simples, o número de jogos possíveis
print("\n\033[1;30mO número de combinações possíveis são:", ncomb)          # de serem criados com as entradas registrads (erro, fix).

njogos = int(input("\033[1;30m\nQuantos jogos você deseja criar?"))                  # Pede o usuário o número de jogos desejados(Talvez eu mude para depois da combinação)

for i in range(0, njogos):
    jogos.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])         # Cria n listas nulas de acordo com njogos. Cada uma será substituída por um jogo.


'''Gerador de jogos randômicos sem repetição que respeita as n-possibilidades derivadas das opções do usuário'''
x, y = fix, 0
while y < njogos:                                       # Executa o loop até completar o número de jogos pedidos pelo usuário.
    seed()                                              # Cria a semente randômica, que muda sempre que chamada.
    while x < 15:                                       # Executa o loop até completar os números permitidos por cartão no sorteio simples.
        n = randint(1, 25)                              # Sugere um número entre 1 e 25
        for j in range(0, erro):                        # Loop da verificação de erro:
            if (excld[j] != n):                         ### Verifica se o número sugerido está entre os retirados.
                if (j < (erro - 1)):                    # Verifica se todos os números de excld foram verificados.
                    continue                            # Se não, incrementa j e repete a verificação.
                if (j == (erro - 1)):                   # Confirma que todos os números de excld foram verificados, já que j está no valor máximo
                    for k in range(0, 15):              # Loop da verificação de repetição 1.0:
                        if (num[k] != n):               #### Verifica se o número sugerido é repetido.
                            if (k < 14):                # Verifica se toda lista num já foi varrida.
                                continue                # Se não, incrementa k e repete a verificação
                            if (k == 14):               # Confirma que todos os números de num[] foram verificados, já que k está no valor máximo
                                num[x] = n              # Adiciona o número sugerido, após evitar erros e repetições.
                                x += 1                  # Incrementa o contador de números jogados por cartão.
                        else:                           #### O número sugerido é repetido.
                            break                       # Interrompe o loop k e, consequentemente, inicia o loop x novamente, recebendo outra sugestão de número.
            else:                                       ### O número sugerido está entre os retirados.
                break                                   # Interrompe o loop j e, consequentemente, inicia o loop x novamente, recebendo outra sugestão de número,
    num.sort()                                          # Se tudo está verificado, ordena os números sorteados (sorteados + fixos + zeros até x=13).
    for i in range(0, len(jogos)):                      # Loop da verificação de repetição 2.0:
        if num != jogos[i]:                             ## Verifica se o jogo criado já existe na lista de jogos.
            if (i < len(jogos) - 1):                    # Verifica se todos os jogos foram comparados com num.
                continue                                # Se não, invrementa i e repete a verificação.
            if (i == len(jogos) - 1):                   # Confirma que todos os jogos de jogos[] foram verificados, já que i está no valor máximo
                jogos[y] = num                          # Como tudo está verificado, adiociona o jogo à lista de jogos.
                y += 1                                  # Incrementa y, que representa o número de jogos a serem criados.
                x = fix                                 # Reseta x para iniciar o novo jogo logo após os números fixados.
                num = num_reset(num, fix, nfix)         # Chama a função que reseta num e retorna num = [].
        else:                                           ## O jogo sugerido é repetido.
            x = fix                                     # Reseta x para criar outro jogo logo após os números fixados.
            num = num_reset(num, fix, nfix)             # Chama a função que reseta num e retorna num = [].
            break                                       # Interrompe o loop i e, consequentemente, inicia o loop x novamente, recebendo outra sugestão de número.




print(f"\033[1;31;107m{'PROGRAMA FINALIZADO':=^70}\033[m")
print(time.process_time(), "ns")