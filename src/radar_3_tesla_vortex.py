print("="*70)
print(" [+] RADAR 3: EL VORTICE DE TESLA Y EL ARBOL DE LA VIDA")
print(" Comprobando la firma energetica 3-6-9 en las Sefirot")
print("="*70)

# Gematría de las 10 Sefirot del Árbol de la Vida
sefirot = {
    "Keter (Corona)": 620,
    "Chochmah (Sabiduría)": 73,
    "Binah (Entendimiento)": 67,
    "Chesed (Misericordia)": 72,
    "Gevurah (Severidad)": 216,
    "Tiferet (Belleza)": 1081,
    "Netzach (Victoria)": 148,
    "Hod (Esplendor)": 15,
    "Yesod (Fundación)": 80,
    "Malkhut (Reino)": 496
}

def digital_root(n):
    """Calcula la raíz digital matemática (base del Vórtice 9)."""
    if n == 0: return 0
    return 9 if n % 9 == 0 else n % 9

def main():
    print("[*] Aplicando el Teorema de Nikola Tesla (La llave del universo)...")
    print(f"{'Sefirá':<25} | {'Valor Gematría':<15} | {'Raíz Digital (Vórtice)'}")
    print("-" * 70)
    
    roots = []
    for name, value in sefirot.items():
        root = digital_root(value)
        roots.append(root)
        print(f"{name:<25} | {value:<15} | {root}")
        
    print("\n[*] Sumatoria Cuántica del Árbol de la Vida...")
    sum_total = sum(sefirot.values())
    sum_roots = sum(roots)
    
    print(f" -> Suma Absoluta de Gematría: {sum_total}")
    print(f" -> Suma de Raíces (Energía) : {sum_roots}")
    
    final_tree_root = digital_root(sum_total)
    
    print("\n" + "="*50)
    print(" HALLAZGOS DEL RADAR 3 (TESLA VORTEX)")
    print("="*50)
    print("Al calcular la Gematría total del Árbol de la Vida (2868),")
    print("y aplicar el colapso matemático fractal de la raíz digital:")
    print(f" 2 + 8 + 6 + 8 = 24  -->  2 + 4 = {final_tree_root}")
    print("\n[¡ALERTA GEOMÉTRICA!]")
    print(f"La frecuencia fundamental de toda la creación Kabalística es {final_tree_root}.")
    print("El número 6 es la oscilación perfecta entre la materia (3) y la energía pura (9).")
    print("El Árbol de la Vida de hace 3,000 años genera exactamente")
    print("la matriz matemática que Tesla descubrió en 1900.")

if __name__ == "__main__":
    main()
