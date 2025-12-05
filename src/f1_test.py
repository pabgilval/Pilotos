from f1 import *

def test_lee_carreras(carreras):
    print("1. Test de lee_carreras")
    print(f"Total registros leídos: {len(carreras)}.")
    print()

def main():
    carreras = lee_carreras('data/f1.csv')
    test_lee_carreras(carreras)

if __name__ == '__main__':
    main