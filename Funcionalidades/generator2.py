import pandas as pd
import numpy as np
import re
import time
inicio = 0b111111111111111
fim = 0b1111111111111110000000000
jogos = []
for i in range(inicio, fim+1):
    iCopy = f"{i:025b}"
    if iCopy.count("1") == 15:
        x = re.split(r"([01])", iCopy)
        x = [j for j in x if j not in [""]]
        jogos.append(x)
    else:
        continue


def binaryMapping(jogos):
    jogosMapped = []
    for jogo in jogos:
        a = []
        for i, j in enumerate(jogo):
            if j == '1':
                a.append(i+1)
        jogosMapped.append(a)
    return jogosMapped


jogos = binaryMapping(jogos)
np.savetxt("todosjogosloto.csv", jogos, fmt="%s", delimiter=",")

print(len(jogos))
print(time.process_time())
