import sys
from scanner import Scanner

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo>")
        exit(1)
    
    scanner = Scanner(sys.argv[1])
    try:
        tokens = scanner.tokenizar()
        for token in tokens:
            print(token)
        print("Compilação concluída com sucesso.")
    except Exception as e:
        print(f"Erro na análise léxica: {e}")
