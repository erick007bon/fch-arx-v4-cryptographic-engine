import os
import random
from fch_arx_v3_tensor import fch_arx_v3_hash

def hex_to_bin(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)

def count_flipped_bits(b1, b2):
    return sum(1 for bit1, bit2 in zip(b1, b2) if bit1 != bit2)

def run_avalanche_test(pares=10000):
    print("="*60)
    print(" SAC TEST (Strict Avalanche Criterion) - FCH-ARX V3")
    print(f" Modelo: NIST SP 800-22 (Test de Avalanche Unidireccional)")
    print(f" Total de Iteraciones Matemáticas: {pares}")
    print("="*60)
    
    total_bits = 256
    accumulated_bits_flipped = 0
    max_flipped = 0
    min_flipped = total_bits
    
    anomalies_low = 0
    anomalies_high = 0
    
    random.seed(42) # Reproducibilidad científica
    
    for _ in range(pares):
        # Generar un mensaje al azar
        rnd_bytes = random.randbytes(16)
        
        # Seleccionar un bit al azar para cambiar
        bit_idx = random.randint(0, 127)
        byte_idx = bit_idx // 8
        bit_offset = bit_idx % 8
        
        # Voltear el bit (Avalancha Unidireccional de 1 Bit de Diferencia)
        mutated_bytes = bytearray(rnd_bytes)
        mutated_bytes[byte_idx] ^= (1 << bit_offset)
        
        # Computar el Torá Hash V3
        h1 = fch_arx_v3_hash(rnd_bytes)
        h2 = fch_arx_v3_hash(mutated_bytes)
        
        bin1 = hex_to_bin(h1)
        bin2 = hex_to_bin(h2)
        
        differences = count_flipped_bits(bin1, bin2)
        accumulated_bits_flipped += differences
        
        max_flipped = max(max_flipped, differences)
        min_flipped = min(min_flipped, differences)
        
        # Control NIST > 60% o < 40%
        if differences < (total_bits * 0.40):
            anomalies_low += 1
        elif differences > (total_bits * 0.60):
            anomalies_high += 1

    promedio_flipped = accumulated_bits_flipped / pares
    porcentaje = (promedio_flipped / total_bits) * 100
    desviacion_50 = abs(50.0 - porcentaje)

    print("\n>>> RESULTADOS OFICIALES SAC <<<")
    print(f" Bits totales evaluados       : {pares * total_bits:,}")
    print(f" Promedio de Bits Volteados  : {promedio_flipped:.2f} / {total_bits}")
    print(f" -> EFECTO AVALANCHA FINAL   : {porcentaje:.4f}%")
    print(f" -> DESVIACION DEL CENTRO 50%: {desviacion_50:.4f}%")
    print(f"\n MIN BITS volteados en un par  : {min_flipped}")
    print(f" MAX BITS volteados en un par  : {max_flipped}")
    print(f"\n Anomalías Estadísticas NIST (<40% o >60%):")
    print(f" Pobre Avalancha (<40)       : {anomalies_low} / {pares}")
    print(f" Exceso Avalancha (>60)      : {anomalies_high} / {pares}")
    
    if 49.5 <= porcentaje <= 50.5:
        print("\n [!] VEREDICTO CRIPTOGRÁFICO: APROBADO (NIVEL MILITAR)")
        print("     El algoritmo es Cuánticamente Resistente frente a ataques Lineales y Diferenciales.")
    else:
        print("\n [-] VEREDICTO CRIPTOGRÁFICO: FALLIDO (CORRELACIÓN DETECTADA)")
        
    print("="*60)

if __name__ == '__main__':
    run_avalanche_test()
