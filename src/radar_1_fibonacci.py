import time

print("="*70)
print(" [O] RADAR 1: ALGORITMO DE REGENERACION (FIBONACCI VS GENESIS)")
print(" Buscando el Bucle de Tikkun (Reparacion) en la Creacion")
print("="*70)

# Gematría de las primeras 7 palabras del Génesis 1:1
# Bereshit Bara Elohim Et Hashamayim Ve'et Ha'aretz
genesis_words = [913, 203, 86, 401, 395, 407, 296]
word_names = ["Bereshit", "Bara", "Elohim", "Et", "Hashamayim", "Ve'et", "Ha'aretz"]

def digital_root(n):
    if n == 0: return 0
    return 9 if n % 9 == 0 else n % 9

def main():
    print("[*] Generando Secuencia Fibonacci (Primeras 24 iteraciones)...")
    fib = [1, 1]
    for _ in range(22):
        fib.append(fib[-1] + fib[-2])
        
    print("\n[*] Cruzando Gematría del Génesis con Módulo de Fibonacci:")
    print(f"{'Palabra':<12} | {'Valor':<6} | {'Raíz (1-9)':<10} | {'Módulo 26 (YHVH)':<16} | {'Fibonacci Cíclico'}")
    print("-" * 70)
    
    for i in range(7):
        val = genesis_words[i]
        root = digital_root(val)
        mod26 = val % 26
        # Resonancia con el índice de Fibonacci correspondiente
        fib_val = fib[i]
        fib_root = digital_root(fib_val)
        
        print(f"{word_names[i]:<12} | {val:<6} | {root:<10} | {mod26:<16} | Fib({i+1})={fib_val} (Raíz: {fib_root})")

    # Sumatorias Totales
    total_gematria = sum(genesis_words)
    total_root = digital_root(total_gematria)
    
    print("\n" + "="*50)
    print(" HALLAZGOS DEL RADAR 1 (FIBONACCI)")
    print("="*50)
    print(f"Suma Total de la Creación (7 palabras): {total_gematria}")
    print(f"Raíz Digital de la Creación           : {total_root}")
    print(f"Sumatoria % 26 (Frecuencia YHVH)      : {total_gematria % 26}")
    
    # Búsqueda del Patrón Regenerativo
    print("\n[!] DESCUBRIMIENTO GEOMÉTRICO:")
    print("Al extraer las raíces digitales del Génesis, observamos cómo el")
    print("valor total (2701) forma un hexagrama perfecto (Triángulo 73).")
    print(f"El número 2701 = 37 x 73. (Ambos números son primordiales).")
    print(f"73 es la Gematría de Jojmá (Sabiduría) y 37 de Yejidá (El núcleo del Alma).")

if __name__ == "__main__":
    main()
