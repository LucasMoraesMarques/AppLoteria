

class Loterias(object):

    def __init__(self, nome, n_acertos, n_possiveis, n_apostas):
        self.nome = nome
        self.n_acertos = n_acertos
        self.n_possiveis = n_possiveis
        self.n_apostas = n_apostas

    def __str__(self):
        return f'A loteria criada possui os seguintes atributos:\
                \nNome: {self.nome}\
                \nAcertos para ganhar: {self.n_acertos}\
                \nNúmeros para jogar: {self.n_possiveis} \
                \nApostas disponíveis: {list(self.n_apostas)} números por jogos'


class Sorteio(Loterias):

    def __init__(self, concurso, data, resultado, nome, premio=1000000,
                 n_acertos=0, n_possiveis=0, n_apostas=0):
        super().__init__(nome, n_acertos, n_apostas, n_possiveis)
        self.concurso = concurso
        self.data = data
        self.resultado = resultado
        self.premio = premio

    def __str__(self):
        return f'Os dados do sorteio são:\
                \nConcurso: {self.concurso}\
                \nData: {self.data}\
                \nResultado: {self.resultado}\
                \nPrêmio: {self.premio}'


class Jogo(Sorteio):

    def __init__(self, numeros, acertos, resultado):
        super().__init__(resultado)
        self.numeros = numeros
        self.__acertos = False

    @property
    def set_acertos(self):
        self.__acertos = len(self.numeros & self.resultado)

    @property
    def get_acertos(self):
        if not self.__acertos:
            print('O resultado para este jogo ainda não está disponível')
        else:
            print(f'O jogo teve {self.__acertos} acertos no sorteio {self.concurso} da {self.nome}')







