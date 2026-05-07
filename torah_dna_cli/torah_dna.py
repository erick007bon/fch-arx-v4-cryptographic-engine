import os
import sys
import random
import argparse

"""
=============================================================================
TORAH-DNA STORAGE FRAMEWORK V1.0
Corporation/IP Edition
=============================================================================
Motor robusto de Sanación de Datos (Archivos / Binarios).
Mecánica: Utiliza el sistema 'Omer' de la Torah (7 Semanas x 7 Días = 49).
Construye una malla gravitacional (Matriz 7x7) donde cada bloque de 36 bytes de 
información original es rodeado vertical y horizontalmente por Nodos de Saturno (Base-7).

Si la radiación cósmica corrompe 1 Byte, la malla halla la coordenada (X,Y) 
exacta por la intersección de anomalías en los Nodos de Saturno y resucita 
el Byte original matemáticamente.

(Propiedad Intelectual Protegida).
=============================================================================
"""

def char_to_int(b):
    return b

def get_saturn_node(byte_list):
    """
    Checksum de Saturno: 
    Asegura que la sumatoria total del puente sea módulo 256.
    """
    total = sum(byte_list)
    # Complemento a 256 para que total + node = n * 256
    rem = total % 256
    return (256 - rem) % 256 

def build_7x7_matrix(data_36_bytes):
    """
    Inserta 36 bytes en una matriz de 6x6.
    Añade Filas de Paridad (Nodos Saturno X).
    Añade Columnas de Paridad (Nodos Saturno Y).
    Total = Matriz 7x7 (49 bytes).
    """
    # Llenar ceros si la data es menor a 36
    while len(data_36_bytes) < 36:
        data_36_bytes.append(0)
        
    matrix = []
    idx = 0
    # Construir el 6x6 y añadir el Nodo 7 Columna (Derecha)
    for i in range(6):
        row = data_36_bytes[idx:idx+6]
        row_saturn = get_saturn_node(row)
        row.append(row_saturn)
        matrix.append(row)
        idx += 6
        
    # Construir la Fila 7 (Fila de Nodos Saturno para cada columna vertical)
    bottom_row = []
    for col_idx in range(7): # 7 columnas ahora
        col_data = [matrix[row_idx][col_idx] for row_idx in range(6)]
        col_saturn = get_saturn_node(col_data)
        bottom_row.append(col_saturn)
    
    matrix.append(bottom_row)
    
    # Aplanar la matriz 7x7 a 49 bytes
    flat_block = []
    for r in matrix:
        flat_block.extend(r)
    
    return flat_block

def extract_and_heal_7x7_matrix(block_49_bytes):
    """
    Analiza la matriz 7x7. Detecta colisiones de radiación.
    Encuentra la intersección (X, Y) y cura el Byte dañado.
    """
    matrix = [list(block_49_bytes[r:r+7]) for r in range(0, 49, 7)]
    
    # 1. Escanear Filas (Eje X)
    broken_row_idx = -1
    row_difference = 0
    for i in range(6):
        row_data = matrix[i][:6]
        expected_saturn = get_saturn_node(row_data)
        if expected_saturn != matrix[i][6]:
            broken_row_idx = i
            # Cuánto fue el daño:
            actual_sum = sum(row_data) % 256
            stored_saturn = matrix[i][6]
            # stored_saturn era (256 - original_sum%256)%256
            # -> original_sum%256 = (256 - stored_saturn)%256
            original_sum = (256 - stored_saturn) % 256
            # diferencia
            row_difference = (original_sum - actual_sum) % 256

    # 2. Escanear Columnas (Eje Y)
    broken_col_idx = -1
    for j in range(6):
        col_data = [matrix[i][j] for i in range(6)]
        expected_saturn = get_saturn_node(col_data)
        if expected_saturn != matrix[6][j]:
            broken_col_idx = j
            break
            
    healed = False
    coords = None
    # 3. Intersección y Sanación
    if broken_row_idx != -1 and broken_col_idx != -1:
        # ¡Corrupción Fuerte Localizada! Geometría en acción.
        coords = (broken_row_idx, broken_col_idx)
        mutated_val = matrix[broken_row_idx][broken_col_idx]
        
        # El valor original es el valor mutado + el diferendo de la radiación
        original_val = (mutated_val + row_difference) % 256
        matrix[broken_row_idx][broken_col_idx] = original_val
        healed = True

    # Extraer data real sanada (36 bytes del 6x6 base)
    real_data = []
    for i in range(6):
        real_data.extend(matrix[i][:6])
        
    return real_data, healed, coords

def encode(file_path):
    print(f"[ENCODE] Empaquetando archivo '{file_path}' en Matriz Torah-Omer 7x7...")
    with open(file_path, "rb") as f:
        data = bytearray(f.read())
        
    encoded_bytes = bytearray()
    
    # Procesar bloques de 36 bytes
    for i in range(0, len(data), 36):
        block = list(data[i:i+36])
        secure_49 = build_7x7_matrix(block)
        encoded_bytes.extend(secure_49)
        
    out_name = file_path + ".tora_dna"
    with open(out_name, "wb") as f:
        f.write(encoded_bytes)
        
    print(f"EXITO. Generado archivo seguro: {out_name}")
    print(f"   Volumen subió de {len(data)} a {len(encoded_bytes)} bytes (Nodos Saturno inyectados).")
    return out_name

def irradiate(encoded_file_path):
    """ Rompe bytes aleatorios dentro del archivo (Sin dañar el tamaño total) """
    print(f"[MUTACION COSMICA] Atacando el archivo '{encoded_file_path}'...")
    with open(encoded_file_path, "rb") as f:
        data = bytearray(f.read())
        
    # Número de bloques
    blocks = len(data) // 49
    corrupted_count = 0
    
    # Destruiremos 1 celda en el 30% de los bloques para probar fuerte
    for i in range(blocks):
        if random.random() < 0.30: # 30% prob
            # Escoger un átomo dentro de la matriz 6x6 a destruir (excluimos la periferia Saturno
            # solo para la demostración cruda del file_body, aunque la red cura la periferia también).
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            flat_idx = (i * 49) + (x * 7) + y
            
            # Radiación destruye
            data[flat_idx] = random.randint(0, 255)
            corrupted_count += 1
            
    out_name = encoded_file_path + ".mutated"
    with open(out_name, "wb") as f:
        f.write(data)
        
    print(f"RADIACTIVIDAD INYECTADA. Se han destruido {corrupted_count} atomos.")
    print(f"   Archivo dañado guardado como: {out_name}")
    return out_name

def heal(corrupted_path, output_original_name):
    print(f"[TORAH SCANNER] Desplegando Geometria de Resurreccion en '{corrupted_path}'...")
    with open(corrupted_path, "rb") as f:
        data = bytearray(f.read())
        
    healed_data = bytearray()
    healed_blocks = 0
    
    for i in range(0, len(data), 49):
        block = list(data[i:i+49])
        real_data_block, healed, coords = extract_and_heal_7x7_matrix(block)
        
        if healed:
            healed_blocks += 1
            print(f"   Tumor localizado en Malla X:{coords[0]}, Y:{coords[1]}. Entropia revertida.")
            
        healed_data.extend(real_data_block)
        
    # Quitar los ceros de relleno agregados al final
    # (Para ser rigurosos, un sistema real guarda el largo del archivo en un header, 
    # pero aquí hacemos un rstrip de bytes 0 puro asumiendo texto crudo).
    while healed_data and healed_data[-1] == 0:
        healed_data.pop()
        
    with open(output_original_name, "wb") as f:
        f.write(healed_data)
        
    print(f"ESCANER FINALIZADO. {healed_blocks} bloques reparados desde la destruccion.")
    print(f"   Archivo resucitado guardado como: {output_original_name}")

def main():
    parser = argparse.ArgumentParser(description="Torah-DNA Storage - Zero Entropy Engine")
    parser.add_argument("--encode", type=str, help="Inyecta Geometría Base-7 a un archivo físico")
    parser.add_argument("--irradiate", type=str, help="Destruye y pudre partes del archivo protegido (Ataque)")
    parser.add_argument("--heal", type=str, help="Lee un archivo corrupto y resucita los datos robados")
    parser.add_argument("--out", type=str, default="RESURRECTED_FILE", help="Nombre del archivo resucitado final")
    
    args = parser.parse_args()
    
    if args.encode:
        encode(args.encode)
    elif args.irradiate:
        irradiate(args.irradiate)
    elif args.heal:
        heal(args.heal, args.out)
    else:
        print("Usa --help para ver los comandos. Toráh-DNA Engine Listo.")


if __name__ == "__main__":
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    main()
