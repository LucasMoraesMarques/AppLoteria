import numpy as np
import math
import random
import time
import pandas as pd
n_possibles = 25
n_played = 15
removed = int(input("Você deseja remover quantos números? "))
fixed = int(input("Você deseja fixar quantos números"))


if removed > 0:
    print("Digite os números a serem excluídos.")
    removedNumbers = np.zeros(removed)
    for i in range(0, removed):
        removedNumbers[i] = int(input(f"Digite o número {i+1}:"))
else:
    removedNumbers = []

if fixed > 0:
    print("Digite os números a serem fixados:")
    fixedNumbers = np.zeros(fixed)
    for i in range(0, fixed):
        fixedNumbers[i] = int(input(f"Digite o número {i+1}:"))

else:
    fixedNumbers = []

ncomb = math.comb((n_possibles - removed - fixed), (n_played - fixed))                                 # Calcula, por combinação simples, o número de jogos possíveis
print("\n\033[1;30mO número de combinações possíveis são:", ncomb)

nJogos = int(input("Quantos jogos você deseja criar"))

jogos = [0]
numbersAllowed = np.array(np.setdiff1d(np.array(range(1, n_possibles + 1)), removedNumbers))
numbersAllowed = np.setdiff1d(numbersAllowed, fixedNumbers)
numbersAllowedCopy = list(numbersAllowed)
random.shuffle(numbersAllowedCopy)
cont = 0
while cont < nJogos:
    numbersAllowedCopy = list(numbersAllowed)
    np.random.RandomState(cont)
    jogo = np.zeros(n_played-fixed)
    for i in range(0, jogo.size):
        number = np.random.choice(numbersAllowedCopy, 1)
        jogo[i] = number
        numbersAllowedCopy.remove(number)

    jogo = np.union1d(jogo, fixedNumbers).astype("int8")
    jogo = list(jogo)
    jogosCopy = jogos.copy()
    if jogo in jogos:
        continue
    else:
        jogos.append(jogo)
        cont += 1

jogos.pop(0)

np.savetxt("todosjogosloto.csv", jogos, fmt="%s", delimiter=",")
print(time.process_time())
