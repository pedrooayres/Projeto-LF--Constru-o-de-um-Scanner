class Token:
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    def __str__(self):
        return f"{self.tipo}('{self.lexema}') @({self.linha},{self.coluna})"