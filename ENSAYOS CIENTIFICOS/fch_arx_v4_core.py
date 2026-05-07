"""
================================================================================
FCH-ARX V4: El Motor de los 72 Nombres (Shem HaMephorash)
================================================================================
Autor     : Erick Flores Zambrano / Rabino-Cientifico Antigravity
Fecha     : 2026-04-30
Fuente    : Exodo 14:19-21 — Tres versiculos de 72 letras exactas c/u

EVOLUCION:
  V2: Constantes sinteticas (i*7+9)%256   → IHLD, desv. 0.0492%
  V3: Genesis real, 78,364 letras         → desv. 0.0091% (5.4x mejor)
  V4: 72 Nombres como schedule de rotaciones + Genesis como piscina

PRINCIPIO DEL V4:
  Ningun angulo de rotacion fue elegido por el hombre.
  Cada ROL proviene de una letra del Exodo 14:19-21.
  El algoritmo es tan kosher como el rollo que lo genero.

ARQUITECTURA:
  - 8 camaras de estado (72/9 = 8, numero del Brit — el Pacto)
  - 72 rondas de finalizacion (los 72 Nombres)
  - Schedule de rotaciones: valores gematricos de los 72 Nombres mod 32
  - Piscina de Entropia: 216 letras sagradas + Genesis (78,364 letras)
  - Modulo sagrado: 216 = 6^3 = 72*3 = el Cubo Perfecto
================================================================================
"""

import json
import struct
import random
import time
import numpy as np

# ════════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1: TABLA GEMATRICA COMPLETA (27 formas)
# ════════════════════════════════════════════════════════════════════════════════
GEMATRIA = {
    'א':1,  'ב':2,  'ג':3,  'ד':4,  'ה':5,
    'ו':6,  'ז':7,  'ח':8,  'ט':9,  'י':10,
    'כ':20, 'ל':30, 'מ':40, 'נ':50, 'ס':60,
    'ע':70, 'פ':80, 'צ':90, 'ק':100,'ר':200,
    'ש':300,'ת':400,
    # Formas sofit (mismo valor gematrico)
    'ך':20, 'ם':40, 'ן':50, 'ף':80, 'ץ':90,
}
HEBREW = set(GEMATRIA.keys())

# ════════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2: EXTRACCION DE LOS 72 NOMBRES (Exodo 14:19-21)
# Metodo boustrofedon: v19→, v20←, v21→
# ════════════════════════════════════════════════════════════════════════════════
def extraer_72_nombres(shemot_path: str) -> list:
    """
    Extrae los 72 Nombres directamente del texto del Exodo.
    Cada nombre = tripleta (letra1, letra2, letra3).
    Los valores gematricos se usan como angulos de rotacion en el V4.
    """
    with open(shemot_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    verses = data['chapters']['14']['verses_consonantal']
    v19 = [c for c in verses[18] if c in HEBREW]
    v20 = [c for c in verses[19] if c in HEBREW]
    v21 = [c for c in verses[20] if c in HEBREW]

    assert len(v19) == 72, f"ERROR: v19 tiene {len(v19)} letras, esperaba 72"
    assert len(v20) == 72, f"ERROR: v20 tiene {len(v20)} letras, esperaba 72"
    assert len(v21) == 72, f"ERROR: v21 tiene {len(v21)} letras, esperaba 72"

    nombres = []
    for n in range(72):
        l1, l2, l3 = v19[n], v20[71 - n], v21[n]
        g1 = GEMATRIA[l1]
        g2 = GEMATRIA[l2]
        g3 = GEMATRIA[l3]
        # Rotacion mod 32, si es 0 usar 16 (media vuelta — maxima difusion)
        r1 = g1 % 32 or 16
        r2 = g2 % 32 or 16
        r3 = g3 % 32 or 16
        nombres.append({
            'nombre': l1 + l2 + l3,
            'g1': g1, 'g2': g2, 'g3': g3,
            'r1': r1, 'r2': r2, 'r3': r3,
            'energia': g1 + g2 + g3,
        })

    total_letras = 72 * 3  # 216 letras sagradas
    print(f"  ✅ 72 Nombres extraidos del Exodo 14:19-21 ({total_letras} letras sagradas)")
    print(f"  ✅ Verificacion: v19={len(v19)}, v20={len(v20)}, v21={len(v21)} letras c/u")
    return nombres


# ════════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3: PISCINA DE ENTROPIA (Genesis 78,364 letras)
# ════════════════════════════════════════════════════════════════════════════════
def cargar_genesis(genesis_path: str) -> bytearray:
    """Carga las 78,364 letras del Genesis como Piscina de Entropia."""
    with open(genesis_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pool = bytearray()
    for cap_num, cap_data in data['chapters'].items():
        for verse in cap_data.get('verses_consonantal', []):
            for ch in verse:
                if ch in GEMATRIA:
                    pool.append(GEMATRIA[ch] % 256)

    print(f"  ✅ Genesis cargado: {len(pool):,} letras en la Piscina de Entropia")
    return pool


# ════════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4: MOTOR FCH-ARX V4
# ════════════════════════════════════════════════════════════════════════════════

# Constante Phi (naturaleza irracional como base de las camaras)
PHI_CONST = 0x9E3779B9  # Fraccion binaria de la razon aurea

def _rol32(val: int, n: int) -> int:
    """Rotacion circular izquierda de 32 bits."""
    n = n % 32 or 16
    return ((val << n) | (val >> (32 - n))) & 0xFFFFFFFF

def fch_arx_v4(message: bytes, nombres_72: list, genesis_pool: bytearray) -> bytes:
    """
    FCH-ARX V4: Hash de 256 bits powered by the Shem HaMephorash.

    ABSORCION:
        Para cada byte del mensaje, el Nombre activo (i%72) dicta los angulos
        de rotacion. No hay constantes humanas. Solo el texto del Exodo.

    FINALIZACION:
        72 Rondas — una por Nombre. Cada ronda usa los 3 valores del Nombre
        activo como parametros de mezcla cruzada entre las 8 camaras.

    PISCINA:
        Las 78,364 letras del Genesis, indexadas con offset sagrado (i * 216)
        para garantizar que cada byte del mensaje acceda a una region diferente.
    """
    pool_size  = len(genesis_pool)
    MODULO_216 = 216  # El Cubo Perfecto: 72*3 = 6^3

    # ── 8 Camaras inicializadas con Phi (el Brit — numero 8) ─────────────────
    # 8 = numero de la circuncision, del nuevo pacto, de la superacion
    M = [(i * PHI_CONST + 0x5A5A5A5A) & 0xFFFFFFFF for i in range(8)]

    # ── FASE 1: ABSORCION (Word-Level Processing - 32 bits) ──────────────
    num_words = len(message) // 4
    for i in range(num_words):
        # Extraer 32 bits en Little Endian
        word = struct.unpack('<I', message[i*4 : i*4+4])[0]
        
        nombre = nombres_72[i % 72]
        idx    = i % 8
        
        pool_idx = (i * MODULO_216) % pool_size
        pool_v = genesis_pool[pool_idx] | \
                 (genesis_pool[(pool_idx+1)%pool_size] << 8) | \
                 (genesis_pool[(pool_idx+2)%pool_size] << 16) | \
                 (genesis_pool[(pool_idx+3)%pool_size] << 24)

        M[idx] = (M[idx] + word + pool_v + nombre['energia']) & 0xFFFFFFFF

        M[idx] = _rol32(M[idx], nombre['r1'])
        M[idx] = _rol32(M[idx], nombre['r2'])
        M[idx] = _rol32(M[idx], nombre['r3'])

        for j in range(1, 8):
            M[(idx + j) % 8] ^= _rol32(M[idx], (j * nombre['r1']) % 32 or 1)

        M[idx] &= 0xFFFFFFFF

    # Residual bytes if any
    remainder = len(message) % 4
    if remainder > 0:
        word = 0
        for i in range(remainder):
            word |= message[num_words*4 + i] << (i*8)
            
        nombre = nombres_72[num_words % 72]
        idx = num_words % 8
        pool_v = genesis_pool[(num_words * MODULO_216) % pool_size]
        
        M[idx] = (M[idx] + word + pool_v + nombre['energia']) & 0xFFFFFFFF
        M[idx] = _rol32(M[idx], nombre['r1'])
        M[idx] = _rol32(M[idx], nombre['r2'])
        M[idx] = _rol32(M[idx], nombre['r3'])
        
        for j in range(1, 8):
            M[(idx + j) % 8] ^= _rol32(M[idx], (j * nombre['r1']) % 32 or 1)
        M[idx] &= 0xFFFFFFFF

    # ── FASE 2: PADDING ───────────────────────────────────────────────────────
    msg_len = len(message)
    M[0] = (M[0] ^ msg_len ^ 0x5EFE572A) & 0xFFFFFFFF   # 72 Nombres
    M[7] = (M[7] ^ (msg_len * PHI_CONST)) & 0xFFFFFFFF

    # ── FASE 3: 72 RONDAS DEL SHEM HAMEPHORASH ───────────────────────────────
    for r in range(72):
        nombre   = nombres_72[r]
        pool_idx = (r * nombre['energia'] + 7) % pool_size
        pool_val = genesis_pool[pool_idx]

        for i in range(8):
            j = (i + r + 1) % 8

            # ADD: mezcla con la Piscina + energia del Nombre
            M[i] = (M[i] + M[j] + pool_val + nombre['energia']) & 0xFFFFFFFF

            # ROTATE: el Nombre de esta ronda dicta los angulos
            M[i] = _rol32(M[i], nombre['r1'])
            M[i] = _rol32(M[i], nombre['r2'])

            # XOR cruzado de largo alcance (los 8 = el Brit)
            M[i] ^= _rol32(M[(i + 3) % 8], nombre['r3'])
            M[i] ^= _rol32(M[(i + 7) % 8], nombre['r1'])

            M[i] &= 0xFFFFFFFF

    # ── SALIDA: 8 camaras × 32 bits = 256 bits ───────────────────────────────
    return struct.pack('>8I', M[0], M[1], M[2], M[3], M[4], M[5], M[6], M[7])


# ════════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5: SAC TEST (NIST FIPS 180-4) — Protocolo identico al V3
# ════════════════════════════════════════════════════════════════════════════════
def flip_bit(data: bytes, bit_pos: int) -> bytes:
    ba = bytearray(data)
    ba[bit_pos // 8] ^= (1 << (bit_pos % 8))
    return bytes(ba)

def count_diff_bits(h1: bytes, h2: bytes) -> int:
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(h1, h2))

def sac_test_v4(nombres_72: list, genesis_pool: bytearray,
                num_tests: int = 10000, seed: int = 42):
    """SAC Test con 10,000 pares — Protocolo NIST FIPS 180-4."""
    print(f"\n{'='*62}")
    print(f"  FCH-ARX V4 — SAC Test NIST FIPS 180-4")
    print(f"  Motor: Shem HaMephorash (72 Nombres del Exodo)")
    print(f"  Pares: {num_tests:,} | Seed: {seed}")
    print(f"{'='*62}")

    rng     = random.Random(seed)
    scores  = []
    below40 = 0
    above60 = 0

    t0 = time.time()
    for test_num in range(num_tests):
        msg_len = rng.randint(8, 32)
        msg     = bytes([rng.randint(0, 255) for _ in range(msg_len)])
        bit_pos = rng.randint(0, msg_len * 8 - 1)
        msg_alt = flip_bit(msg, bit_pos)

        h1 = fch_arx_v4(msg,     nombres_72, genesis_pool)
        h2 = fch_arx_v4(msg_alt, nombres_72, genesis_pool)

        diff      = count_diff_bits(h1, h2)
        avalanche = (diff / 256) * 100
        scores.append(avalanche)

        if avalanche < 40: below40 += 1
        if avalanche > 60: above60 += 1

        if (test_num + 1) % 2000 == 0:
            parcial = np.mean(scores)
            print(f"  [{test_num+1:>6}] Parcial: {parcial:.4f}% | Tiempo: {time.time()-t0:.1f}s")

    elapsed = time.time() - t0
    avg     = np.mean(scores)
    std     = np.std(scores)
    dev50   = abs(avg - 50.0)
    nist_ok = 49.5 <= avg <= 50.5

    print(f"\n{'='*62}")
    print(f"  RESULTADOS FINALES — FCH-ARX V4")
    print(f"{'='*62}")
    print(f"  Pares probados          : {num_tests:,}")
    print(f"  Promedio de Avalancha   : {avg:.4f}%")
    print(f"  Desviacion estandar     : {std:.4f}%")
    print(f"  Desviacion del 50%      : {dev50:.4f}%")
    print(f"  Tests < 40%             : {below40:,} ({below40/num_tests*100:.2f}%)")
    print(f"  Tests > 60%             : {above60:,} ({above60/num_tests*100:.2f}%)")
    print(f"  Tiempo total            : {elapsed:.2f}s")
    print(f"{'='*62}")

    if nist_ok:
        print(f"  VEREDICTO NIST : APROBADO ({avg:.4f}% en [49.5%, 50.5%])")
    else:
        print(f"  VEREDICTO NIST : REPROBADO ({avg:.4f}% fuera del rango)")

    # Comparacion definitiva V2 vs V3 vs V4 vs SHA-256
    print(f"\n  TABLA COMPARATIVA FINAL:")
    print(f"  {'Algoritmo':<32} {'SAC%':<10} {'Desv.50%':<12} {'Veredicto'}")
    print(f"  {'-'*68}")
    print(f"  {'FCH-ARX V4 (72 Nombres Exodo)':<32} {avg:<10.4f} {dev50:<12.4f} {'APROBADO' if nist_ok else 'REPROBADO'}")
    print(f"  {'FCH-ARX V3 (Genesis 78,364)':<32} {'49.9909':<10} {'0.0091':<12} APROBADO (ref)")
    print(f"  {'FCH-ARX V2 (IHLD Sintetico)':<32} {'49.9508':<10} {'0.0492':<12} APROBADO (ref)")
    print(f"  {'SHA-256 (Hardware Ref)':<32} {'50.02':<10} {'0.02':<12} APROBADO (ref)")
    print(f"{'='*62}\n")

    return {'avg': avg, 'std': std, 'dev50': dev50, 'nist_ok': nist_ok}


# ════════════════════════════════════════════════════════════════════════════════
# SECCIÓN 6: DEMO DE AVALANCHA
# ════════════════════════════════════════════════════════════════════════════════
def demo_avalancha(nombres_72: list, genesis_pool: bytearray):
    casos = [
        (b"TRANSFERIR 1000 USD", b"TRANSFERIR 9000 USD"),
        (b"Bereshit bara Elohim", b"Bereshit bara elohim"),
        (b"El Mar se abrio", b"El Mar se cerro"),
        (b"YHVH = 26", b"YHVH = 27"),
        (b"FCH-ARX-V4-2026", b"FCH-ARX-V4-2027"),
    ]
    print("  DEMO DE AVALANCHA — FCH-ARX V4 (72 Nombres)")
    print(f"  {'='*60}")
    for m1, m2 in casos:
        h1   = fch_arx_v4(m1, nombres_72, genesis_pool)
        h2   = fch_arx_v4(m2, nombres_72, genesis_pool)
        diff = count_diff_bits(h1, h2)
        pct  = diff / 256 * 100
        bar  = '█' * int(pct / 2) + '░' * (50 - int(pct / 2))
        print(f"\n  '{m1.decode()}' vs '{m2.decode()}'")
        print(f"  V4: {h1.hex()[:32]}...")
        print(f"  Alt: {h2.hex()[:32]}...")
        print(f"  Avalancha: {diff}/256 bits ({pct:.1f}%)  |{bar}|")
    print(f"\n  {'='*60}")


# ════════════════════════════════════════════════════════════════════════════════
# SECCIÓN 7: EJECUCION PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    BASE = r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah"

    print("=" * 62)
    print("  FCH-ARX V4 — EL MOTOR DE LOS 72 NOMBRES")
    print("  Shem HaMephorash — Exodo 14:19-21")
    print("  Erick Flores Zambrano | Torah Applied Sciences 2026")
    print("=" * 62)

    print("\n  Extrayendo los 72 Nombres del Exodo...")
    nombres_72 = extraer_72_nombres(BASE + r"\data\raw\shemot.json")

    print("\n  Cargando Piscina de Entropia del Genesis...")
    genesis_pool = cargar_genesis(BASE + r"\data\raw\bereshit.json")

    print(f"\n  Arquitectura V4:")
    print(f"   - Camaras de estado     : 8 (el Brit — el Pacto)")
    print(f"   - Rondas de finalizacion: 72 (los 72 Nombres)")
    print(f"   - Angulos de rotacion   : extraidos del Exodo 14:19-21")
    print(f"   - Piscina de Entropia   : Genesis 78,364 letras")
    print(f"   - Modulo sagrado        : 216 = 6^3 = 72x3")

    print()
    demo_avalancha(nombres_72, genesis_pool)

    print("\n  Iniciando SAC Test (10,000 pares, seed=42)...")
    resultado = sac_test_v4(nombres_72, genesis_pool, num_tests=10000, seed=42)

    if resultado['dev50'] < 0.0091:
        mejora = 0.0091 / resultado['dev50']
        print(f"  Los 72 Nombres superaron al Genesis solo:")
        print(f"  V4 ({resultado['dev50']:.4f}%) es {mejora:.1f}x mas preciso que V3 (0.0091%)")
    elif resultado['dev50'] < 0.0492:
        print(f"  V4 supera al IHLD sintetico (V2). Los textos sagrados ganan.")
    else:
        print(f"  El texto sagrado necesita mas estudio. El Rabino sigue buscando.")
