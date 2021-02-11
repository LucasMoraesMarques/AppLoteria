import numpy as np
import math
n_possibles = 25
n_played = 15
removed = int(input("Você deseja remover quantos números? "))
fixed = int(input("Você deseja fixar quantos números"))

if removed > 0:
    print("Digite os números a serem excluídos.")
    removedNumbers = np.zeros(removed)
    for i in range(0, removed):
        removedNumbers[i] = int(input(f"Digite o número {i+1}:"))

if fixed > 0:
    print("Digite os números a serem fixados:")
    fixedNumbers = np.zeros(fixed)
    for i in range(0, fixed):
        fixedNumbers[i] = int(input(f"Digite o número {i+1}:"))

ncomb = math.comb((n_possibles - removed - fixed), (n_played - fixed))                                 # Calcula, por combinação simples, o número de jogos possíveis
print("\n\033[1;30mO número de combinações possíveis são:", ncomb)

nJogos = int(input("Quantos jogos você deseja criar"))

jogos = np.zeros(nJogos, dtype="object")
numbersAllowed = np.array(np.setdiff1d(np.array(range(1, n_possibles + 1)), removedNumbers))
numbersAllowed = np.setdiff1d(numbersAllowed, fixedNumbers)

cont = 0
print(numbersAllowed)
while cont < nJogos:
    np.random.RandomState(cont)
    a = np.random.choice(numbersAllowed, n_played-fixed)
    print(a)
    jogo = np.union1d(a, fixedNumbers)
    print(jogo)
    if jogo not in jogos:
        jogos[cont] = jogo
        cont += 1

print(jogos)

