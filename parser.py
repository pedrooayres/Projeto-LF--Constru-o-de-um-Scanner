# parser.py
from token import Token
from tabela_simbolos import TabelaSimbolos, Simbolo

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.escopo = 0
        self.ts = TabelaSimbolos()

    def atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token("EOF", "", -1, -1)

    def consumir(self):
        self.pos += 1

    def erro(self, msg):
        t = self.atual()
        raise Exception(f"Erro sintatico: {msg} em {t.lexema} linha {t.linha}, coluna {t.coluna}")

    def programa(self):
        if self.atual().lexema != "int": self.erro("Esperado 'int'")
        self.consumir()
        if self.atual().lexema != "main": self.erro("Esperado 'main'")
        self.consumir()
        if self.atual().lexema != "(": self.erro("Esperado '('")
        self.consumir()
        if self.atual().lexema != ")": self.erro("Esperado ')'")
        self.consumir()
        self.bloco()
        if self.atual().tipo != "EOF": self.erro("Codigo apos fim do main")

    def bloco(self):
        if self.atual().lexema != "{": self.erro("Esperado '{'")
        self.escopo += 1
        self.consumir()

        while self.atual().lexema in {"int", "float", "char"}:
            self.declarar_variaveis()

        while self.atual().lexema in {"if", "while", "do", "for", "printf", "break", "continue"} or self.atual().tipo == "IDENT":
            self.comando()

        if self.atual().lexema != "}": self.erro("Esperado '}'")
        self.escopo -= 1
        self.ts.remover_escopo(self.escopo)
        self.consumir()

    def declarar_variaveis(self):
        tipo = self.atual().lexema
        self.consumir()
        while True:
            if self.atual().tipo != "IDENT": self.erro("Esperado identificador")
            ident = self.atual()
            self.ts.inserir(Simbolo(ident.lexema, tipo, self.escopo))
            self.consumir()
            if self.atual().lexema == ",":
                self.consumir()
            else:
                break
        if self.atual().lexema != ";": self.erro("Esperado ';'")
        self.consumir()

    def comando(self):
        if self.atual().lexema == "if":
            self.consumir()
            if self.atual().lexema != "(": self.erro("Esperado '(' apos if")
            self.consumir()
            self.expressao()
            if self.atual().lexema != ")": self.erro("Esperado ')' apos condicao do if")
            self.consumir()
            self.bloco()
            if self.atual().lexema == "else":
                self.consumir()
                self.bloco()

        elif self.atual().lexema == "while":
            self.consumir()
            if self.atual().lexema != "(": self.erro("Esperado '(' apos while")
            self.consumir()
            self.expressao()
            if self.atual().lexema != ")": self.erro("Esperado ')' apos condicao do while")
            self.consumir()
            self.bloco()

        elif self.atual().lexema == "do":
            self.consumir()
            self.bloco()
            if self.atual().lexema != "while": self.erro("Esperado 'while' apos bloco do")
            self.consumir()
            if self.atual().lexema != "(": self.erro("Esperado '(' apos while")
            self.consumir()
            self.expressao()
            if self.atual().lexema != ")": self.erro("Esperado ')' apos condicao do while")
            self.consumir()
            if self.atual().lexema != ";": self.erro("Esperado ';' apos do-while")
            self.consumir()

        elif self.atual().lexema == "for":
            self.consumir()
            if self.atual().lexema != "(": self.erro("Esperado '(' apos for")
            self.consumir()
            self.comando()
            self.expressao()
            if self.atual().lexema != ";": self.erro("Esperado ';' apos expressao de condicao")
            self.consumir()
            self.comando()
            if self.atual().lexema != ")": self.erro("Esperado ')' apos for")
            self.consumir()
            self.bloco()

        elif self.atual().lexema == "printf":
            self.consumir()
            if self.atual().lexema != "(": self.erro("Esperado '(' apos printf")
            self.consumir()
            self.expressao()
            if self.atual().lexema != ")": self.erro("Esperado ')' apos argumento de printf")
            self.consumir()
            if self.atual().lexema != ";": self.erro("Esperado ';' apos printf")
            self.consumir()

        elif self.atual().lexema == "break" or self.atual().lexema == "continue":
            self.consumir()
            if self.atual().lexema != ";": self.erro("Esperado ';' apos break/continue")
            self.consumir()

        elif self.atual().tipo == "IDENT":
            ident = self.atual()
            if not self.ts.buscar(ident.lexema):
                self.erro(f"Variavel '{ident.lexema}' nao declarada")
            self.consumir()
            if self.atual().lexema != "=": self.erro("Esperado '='")
            self.consumir()
            self.expressao()
            if self.atual().lexema != ";": self.erro("Esperado ';'")
            self.consumir()

        else:
            self.erro("Comando invalido")

    def expressao(self):
        self.termo()
        while self.atual().lexema in {"+", "-", "<", ">", "<=", ">=", "==", "!="}:
            self.consumir()
            self.termo()

    def termo(self):
        self.fator()
        while self.atual().lexema in {"*", "/"}:
            self.consumir()
            self.fator()

    def fator(self):
        if self.atual().tipo in {"CONST_INT", "CONST_REAL", "CONST_CHAR", "CONST_STRING"}:
            self.consumir()
        elif self.atual().tipo == "IDENT":
            if not self.ts.buscar(self.atual().lexema):
                self.erro(f"Variavel '{self.atual().lexema}' nao declarada")
            self.consumir()
        elif self.atual().lexema == "(":
            self.consumir()
            self.expressao()
            if self.atual().lexema != ")": self.erro("Esperado ')'")
            self.consumir()
        else:
            self.erro("Expressao mal formada")
