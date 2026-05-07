# -*- coding: utf-8 -*-
"""
AUDITOR MASORETICO - PROTOCOLO DE PUREZA ABSOLUTA
=================================================
Este script purga un archivo de la Tora y comprueba si 
cumple el conteo matematico divino (Ej: Genesis = 78,064 letras).
"""
import sys, re

# Tabla estandar universal del conteo rabinico asquenazi (Textus Receptus)
CONTEO_EXACTO = {
    '1': ('Genesis (Bereshit)', 78064),
    '2': ('Exodo (Shemot)', 63529),
    '3': ('Levitico (Vayikra)', 44790),
    '4': ('Numeros (Bamidbar)', 63530),
    '5': ('Deuteronomio (Devarim)', 54892),
    'ALL': ('Tora Completa', 304805)
}

def purgar_texto(archivo_entrada):
    """Limpia todo rastro que no sea consontante masoretica pura."""
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            texto = f.read()
    except Exception as e:
        print(f"Error abriendo {archivo_entrada}: {e}")
        return None

    # 1. Los pergaminos no tienen parentesis. Si los hay, son Ketiv/Qere modernos.
    texto = re.sub(r'\\(.*?\\)', '', texto)
    texto = re.sub(r'\\[.*?\\]', '', texto)
    texto = re.sub(r'\\{.*?\\}', '', texto)

    # 2. Eliminar grafias de parashot (Peh y Samek aisladas por espacios)
    texto = re.sub(r'(?<= )ס(?= )', '', texto)
    texto = re.sub(r'(?<= )פ(?= )', '', texto)

    # 3. Conjunto estricto de los 22 alefbat (incluyendo las 5 sofiet/finales)
    ALFABETO = set('אבגדהוזחטיכלמנסעפצקרשתךםןףץ')
    
    # Extraemos solo letras puras
    puro = ''.join(c for c in texto if c in ALFABETO)
    return puro

def auditar_libro(id_libro, archivo_txt):
    if id_libro not in CONTEO_EXACTO:
        print("Id de libro invalido.")
        return

    nombre, objetivo = CONTEO_EXACTO[id_libro]
    print("="*60)
    print(f"  AUDITORIA TRIBUNAL: {nombre.upper()}")
    print("="*60)
    print(f"  Objetivo Exigido  : {objetivo:,} letras")
    
    texto_puro = purgar_texto(archivo_txt)
    if texto_puro is None: return
    
    conteo_real = len(texto_puro)
    print(f"  Letras Detectadas : {conteo_real:,}")
    
    diferencia = conteo_real - objetivo
    print("-" * 60)
    if diferencia == 0:
        print("  [VALIDACION KASHER] BINGO! CONTEO 100% PERFECTO.")
        print("  ESTADO: APROBADO PARA MOTOR CRIPTOGRAFICO V3.")
        
        # Sellar y exportar el material radioactivo
        out = f"KASHER_PURE_{id_libro}_{archivo_txt}"
        with open(out, 'w', encoding='utf-8') as f:
            f.write(texto_puro)
        print(f"  Dataset sellado exportado a: {out}")
    else:
        print(f"  [VALIDACION POSUL] Alerta. Diferencia de: {diferencia:+,} letras.")
        print("  ESTADO: RECHAZADO. Posible spelling 'plene' moderno o error de transcripcion.")
        print("  Consiga version 'Westminster Leningrad Codex' o 'Koren Edition'.")
    print("="*60)

if __name__ == '__main__':
    # Instrucciones de uso
    print("\n[!] CENTINELA ACTIVO. Para auditar ejecuta el script modificando el archivo de entrada abajo.\n")
    # Ejemplo:
    # auditar_libro('1', 'mi_genesis_crítico.txt')
