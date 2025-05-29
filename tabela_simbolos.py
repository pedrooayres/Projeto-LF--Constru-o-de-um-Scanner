class Simbolo:
    def __init__(self, lexema, tipo, escopo):
        self.lexema = lexema    
        self.tipo = tipo          # Tipo da variável (int, float, char, etc.)
        self.escopo = escopo      # Nível de escopo em que a variável foi declarada

class TabelaSimbolos:
    def __init__(self):
        self.tabela = []

    def inserir(self, simbolo):
        # Verifica se já existe símbolo com mesmo nome no mesmo escopo
        if any(s.lexema == simbolo.lexema and s.escopo == simbolo.escopo for s in self.tabela):
            raise Exception(f"Variável '{simbolo.lexema}' já declarada neste escopo")
        self.tabela.append(simbolo)

    def buscar(self, lexema):
        # Busca do escopo mais interno para o mais externo
        for simbolo in reversed(self.tabela):
            if simbolo.lexema == lexema:
                return simbolo
        return None

    def remover_escopo(self, escopo):
        # Remove todas as variáveis do escopo atual ao sair de um bloco
        self.tabela = [s for s in self.tabela if s.escopo < escopo]
