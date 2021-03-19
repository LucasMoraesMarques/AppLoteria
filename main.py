import Librarie as lib



def main():
    lib.menu()


"""Lotofacil = Loterias("lotofacil", resultados=0, nAcertos=15, nPossiveis=25, nRange=range(15, 21))
sorteioloto = Sorteio(Lotofacil)
sorteioloto.requestLastResult()
sorteioloto.writeConfig()
print(sorteioloto.readConfig())
jogos = Jogos(Lotofacil)
jogos.readJogos('lotofacil')
jogos.checkResults(sorteioloto)

jogos = Jogos(loto_type=Lotofacil)
jogos.callGenerator(nPlayed=15, nRemoved=2, nFixed=2, maxGap=4, maxSeq=5, isOdd=True, nPrime=4)
print(jogos.jogos)
print(jogos.metadata)

jogos = Jogos(loto_type=Lotofacil)
jogos.callGenerator(nPlayed=15, nRemoved=2, nFixed=2)
print(jogos.jogos)
print(jogos.metadata)"""



main()
