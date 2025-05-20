import sys
from scanner import Scanner
from parser import Parser

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo>")
        exit(1)

    scanner = Scanner(sys.argv[1])
    try:
        tokens = scanner.tokenizar()
        parser = Parser(tokens)
        parser.programa()
        print("Compilacao concluida com sucesso.")
    except Exception as e:
        print(f"Erro na compilacao: {e}")
