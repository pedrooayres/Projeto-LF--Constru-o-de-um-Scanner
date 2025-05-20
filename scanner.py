# scanner.py
from token import Token
from lexer_rules import RESERVADAS, OPERADORES_ARIT, OPERADORES_REL, MARCADORES

class Scanner:
    def __init__(self, arquivo):
        with open(arquivo, 'r') as f:
            self.codigo = f.read()
        self.pos = 0
        self.linha = 1
        self.coluna = 1
        self.tokens = []

    def avancar(self):
        if self.pos < len(self.codigo):
            char = self.codigo[self.pos]
            self.pos += 1
            if char == '\n':
                self.linha += 1
                self.coluna = 1
            else:
                self.coluna += 1
            return char
        return None

    def retroceder(self):
        self.pos -= 1
        self.coluna -= 1

    def espiar(self):
        return self.codigo[self.pos] if self.pos < len(self.codigo) else None

    def tokenizar(self):
        while self.pos < len(self.codigo):
            c = self.avancar()

            if c is None or c.isspace():
                continue

            if c == '/':
                proximo = self.espiar()
                if proximo == '/':
                    while c and c != '\n':
                        c = self.avancar()
                    continue
                elif proximo == '*':
                    self.avancar()
                    while True:
                        c = self.avancar()
                        if c is None:
                            raise Exception(f"Erro: Comentário de bloco não encerrado (linha {self.linha})")
                        if c == '*' and self.espiar() == '/':
                            self.avancar()
                            if c == "=":
                                if self.espiar() == "=":
                                    self.avancar()
                                    self.tokens.append(Token('OP_REL','==',self.linha,self.coluna -1))
                                else: 
                                    self.tokens.append(Token('ATRIB', '=', self.linha, self.coluna - 1))                                
                            break
                    continue

            if c.isalpha() or c == '_':
                lexema = c
                while self.espiar() and (self.espiar().isalnum() or self.espiar() == '_'):
                    lexema += self.avancar()
                tipo = 'RESERVADA' if lexema in RESERVADAS else 'IDENT'
                self.tokens.append(Token(tipo, lexema, self.linha, self.coluna - len(lexema)))
                continue

            if c.isdigit():
                lexema = c
                is_float = False
                while self.espiar() and self.espiar().isdigit():
                    lexema += self.avancar()
                if self.espiar() == '.':
                    is_float = True
                    lexema += self.avancar()
                    if not self.espiar() or not self.espiar().isdigit():
                        raise Exception(f"Erro: Float mal formado '{lexema}' (linha {self.linha})")
                    while self.espiar() and self.espiar().isdigit():
                        lexema += self.avancar()
                tipo = 'CONST_REAL' if is_float else 'CONST_INT'
                self.tokens.append(Token(tipo, lexema, self.linha, self.coluna - len(lexema)))
                continue

            if c == "'":
                lexema = c
                ch = self.avancar()
                if ch is None or ch == '\n':
                    raise Exception(f"Erro: Constante de caractere mal formada (linha {self.linha})")
                lexema += ch
                if self.avancar() != "'":
                    raise Exception(f"Erro: Constante de caractere mal formada (linha {self.linha})")
                lexema += "'"
                self.tokens.append(Token('CONST_CHAR', lexema, self.linha, self.coluna - len(lexema)))
                continue

            for op in sorted(OPERADORES_REL, key=len, reverse=True):
                if self.codigo.startswith(op, self.pos - 1):
                    self.tokens.append(Token('OP_REL', op, self.linha, self.coluna - 1))
                    for _ in op[1:]:
                        self.avancar()
                    break
            else:
                if c in OPERADORES_ARIT:
                    self.tokens.append(Token('OP_ARIT', c, self.linha, self.coluna - 1))
                    continue
                if c in MARCADORES:
                    self.tokens.append(Token('MARCADOR', c, self.linha, self.coluna - 1))
                    continue
                if c == '!':
                    if self.espiar() != '=':
                        raise Exception(f"Erro: Exclamação isolada (linha {self.linha})")
                raise Exception(f"Erro: Caractere inválido '{c}' (linha {self.linha})")

        self.tokens.append(Token('EOF', '', self.linha, self.coluna))
        return self.tokens
