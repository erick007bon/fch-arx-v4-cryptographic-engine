import os
from colorama import init, Fore, Style

# Inicializar colores en consola Windows
init(autoreset=True)

def rotl(val, r):
    return ((val << r) & 0xFFFFFFFF) | (val >> (32 - r))

def fch_v2_hash(texto):
    SATURN_SQUARE = [4, 9, 2, 3, 5, 7, 8, 1, 6]
    M = [(s * 0x9E3779B9) & 0xFFFFFFFF for s in SATURN_SQUARE]
    FIB_WHEEL = [1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9]
    TESLA_ROTS = [3, 6, 9]

    for i, char in enumerate(texto):
        val = ord(char)
        W = FIB_WHEEL[i % 24]
        idx = i % 9
        
        # ARX
        M[idx] = (M[idx] + val + (W * (i + 1))) & 0xFFFFFFFF
        M[(idx + 1) % 9] = rotl(M[(idx + 1) % 9], TESLA_ROTS[0])
        M[(idx + 2) % 9] = rotl(M[(idx + 2) % 9], TESLA_ROTS[1])
        M[(idx + 3) % 9] = rotl(M[(idx + 3) % 9], TESLA_ROTS[2])
        M[(idx + 4) % 9] ^= M[idx]
        M[(idx + 5) % 9] ^= M[(idx + 1) % 9]
        M[(idx + 6) % 9] ^= M[(idx + 2) % 9]

    # FINALIZACIÓN PROFUNDA: Sinergia de los 3 Proyectos (El Trinomio)
    # 1. YHVH-26 (Neuro-AI): 26 Rondas de Mezcla
    for i in range(26):
        M[i % 9] = (M[i % 9] + M[(i + 8) % 9] + 26) & 0xFFFFFFFF
        
        # 2. Vórtice de Tesla (Web3 Crypto): Rotaciones en Base 9
        M[(i + 1) % 9] = rotl(M[(i + 1) % 9], 3)
        M[(i + 2) % 9] = rotl(M[(i + 2) % 9], 6)
        M[(i + 3) % 9] = rotl(M[(i + 3) % 9], 9)
        
        # 3. Omer 7x7 (Data Recovery): Desplazamientos Ortogonales
        M[(i + 4) % 9] = rotl(M[(i + 4) % 9], 7) 
        
        # Difusión final combinada
        M[(i + 5) % 9] ^= (M[i % 9] + 7) & 0xFFFFFFFF
        M[(i + 6) % 9] ^= rotl(M[(i + 1) % 9], 26)

    state = [(M[k] ^ M[(k + 1) % 9]) for k in range(8)]
    return "".join(f"{x:08x}" for x in state).upper()

def get_binary(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(256)

print(Fore.CYAN + "="*70)
print(Fore.YELLOW + Style.BRIGHT + "   VISUALIZADOR DEL EFECTO AVALANCHA (FCH-ARX V2)")
print(Fore.CYAN + "="*70)

# TEXTOS
t1 = "TRANSFERIR 1000 USD AL SEÑOR ERICK"
t2 = "TRANSFERIR 9000 USD AL SEÑOR ERICK"

h1 = fch_v2_hash(t1)
h2 = fch_v2_hash(t2)

b1 = get_binary(h1)
b2 = get_binary(h2)

print(Fore.WHITE + "1. Texto A: " + t1)
print(Fore.WHITE + "2. Texto B: " + t2)
print()
print(Fore.GREEN + "Cambiamos 1 solo carácter ('1' por '9'). Mira lo que pasa en los 256 bits:")
print()

# Mostrar diferencias con COLORES
print("H1(1000): " + b1[:64] + "...")
print("H2(9000): ", end="")

diff_count = 0
for bit1, bit2 in zip(b1, b2):
    if bit1 != bit2:
        diff_count += 1

# Mostramos solo los primeros 64 bits para no llenar la pantalla y que lo vea claro
for bit1, bit2 in zip(b1[:64], b2[:64]):
    if bit1 != bit2:
        print(Fore.RED + bit2, end="")
    else:
        print(Fore.GREEN + bit2, end="")

print(Fore.RESET + "...")
print()
print(Fore.RED + "Los bits ROJOS representan los bits destruidos/alterados.")
print(Fore.YELLOW + f"  -> Bits totales volteados: {diff_count} de 256")
pct = (diff_count / 256) * 100
print(Fore.YELLOW + f"  -> Efecto Avalancha: {pct:.2f}% (Se requiere 50%+ para uso militar)")
print(Fore.CYAN + "="*70)

print(Fore.WHITE + "Este es el corazon del muro impenetrable.")
print(Fore.WHITE + "Rotando 3, 6, 9 veces, el caos matematico hace su trabajo perfecto.")
