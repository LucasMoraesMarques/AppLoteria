

class Loterias(object):

    def __init__(self, nome, cAtual, resultados, n_acertos=0, n_possiveis=0,
                 n_apostas=0):
        self.nome = nome
        self.n_acertos = n_acertos
        self.n_possiveis = n_possiveis
        self.n_apostas = n_apostas
        self.resultados = resultados
        self.cAtual = cAtual
        #self.res_atual = self.resultados.iloc[0, 1:16].to_numpy()

    def __str__(self):
        return f'A loteria criada possui os seguintes atributos:\
                \nNome: {self.nome}\
                \nAcertos para ganhar: {self.n_acertos}\
                \nNúmeros para jogar: {self.n_possiveis} \
                \nApostas disponíveis: {list(self.n_apostas)} números por jogos'


class Sorteio(Loterias):

    def __init__(self, conc, premio, nome, cAtual, resultados=0):
        super(Loterias).__init__(nome, cAtual, resultados)
        self.concurso = conc[0]
        self.data = conc[1]
        #self.resultado = Loterias.res_atual
        self.resultados = resultados
        self.premio = premio

    def __str__(self):
        return f'Os dados do sorteio são:\
                \nConcurso: {self.concurso}\
                \nData: {self.data}\
                \nResultado: {self.resultado}\
                \nPrêmio: {self.premio}'


class Jogos():

    def __init__(self, Sorteio, jogos):
        self.jogos = jogos
        self.acertos = 0
        self.resultado= Sorteio.resultado

    def confere_acertos(self):
        x = 0
        acertos = []
        for k, v in self.jogos.items():
            x = len(v & set(self.resultado))
            acertos.append([k, x])
        return acertos

    """@property
    def set_acertos(self):
        self.acertos = len(self.numeros & self.resultado)

    @property
    def get_acertos(self):
        if not self.acertos:
            print('O resultado para este jogo ainda não está disponível')
        else:
            print(f'O jogo teve {self.acertos} acertos no sorteio {self.concurso} da {self.nome}')"""



if __name__ == "__main__":
    Lotofacil = Loterias("Lotofácil", 2152, resultados=0, n_acertos=15, n_possiveis=25, n_apostas=range(15, 21))
    print(Lotofacil)
    sorteioloto = Sorteio(Lotofacil, 2152, 1500000, 54)
    print(sorteioloto)


