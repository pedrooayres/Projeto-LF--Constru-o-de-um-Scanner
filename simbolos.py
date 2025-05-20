class Simbolo:
    def __init__(self, lexema, tipo, escopo):
        self.lexema = lexema
        self.tipo = tipo
        self.escopo = escopo

class TabelaSimbolos:
    def __init__(self):
        self.tabela = []

    def inserir(self, simbolo):
        if any(s.lexema == simbolo.lexema and s.escopo == simbolo.escopo for s in self.tabela):
            raise Exception(f"Variavel '{simbolo.lexema}' ja declarada neste escopo")
        self.tabela.append(simbolo)

    def buscar(self, lexema):
        for simbolo in reversed(self.tabela):
            if simbolo.lexema == lexema:
                return simbolo
        return None

    def remover_escopo(self, escopo):
        self.tabela = [s for s in self.tabela if s.escopo < escopo]
