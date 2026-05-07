"""
================================================================================
FCH-ARX V4.1: El Motor de los 72 Nombres — MEJORADO CON PATRONES SAGRADOS
================================================================================
Mejoras sobre V4 basadas en los patrones descubiertos esta sesion:

PATRON 1 — Par Espejo #20 = 216 EXACTO
  El par (פהל + נןא) suma exactamente 216 = el Cubo Perfecto.
  El texto se describe a si mismo. Usamos 216 como modulo sagrado primario.

PATRON 2 — Salto Geometrico ×7 del Mandala
  En lugar de acceder a los Nombres secuencialmente (i%72),
  usamos el salto de 7 posiciones que crea el mandala estelar:
  Nombre activo = NOMBRES[(i * 7) % 72]
  Esto garantiza que todos los 72 Nombres se visiten antes de repetir
  Y que el orden no sea predecible linealmente.

PATRON 3 — Tesla Boost (DR=3,6,9)
  Los 19 Nombres con raiz digital Tesla reciben una ronda adicional de XOR.
  Son los nodos de mayor difusion del sistema.

PATRON 4 — Phi en la Inicializacion
  La camara 0 se inicializa con la energia del Nombre #44 (ילה = 45)
  — la posicion de la Seccion Aurea en el ciclo de 72 Nombres.

PATRON 5 — Espejo en la Finalizacion
  Cada ronda r usa simultaneamente Nombre #r y su espejo #(71-r).
  La difusion cruzada entre espejo-pares rompe toda simetria lineal.

RESULTADO ESPERADO: Desviacion del 50% < 0.0026% (mejor que V4 base)
================================================================================
"""

import json
import struct
import random
import time
import numpy as np
from pathlib import Path

BASE = Path(r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah")

GEMATRIA = {
    'א':1,'ב':2,'ג':3,'ד':4,'ה':5,'ו':6,'ז':7,'ח':8,'ט':9,'י':10,
    'כ':20,'ל':30,'מ':40,'נ':50,'ס':60,'ע':70,'פ':80,'צ':90,'ק':100,
    'ר':200,'ש':300,'ת':400,'ך':20,'ם':40,'ן':50,'ף':80,'ץ':90,
}
HEBREW = set(GEMATRIA.keys())

# Constantes sagradas descubiertas esta sesion
MODULO_216   = 216          # El Cubo Perfecto: par espejo #20 suma exactamente 216
SALTO_7      = 7            # Salto geometrico del mandala estelar
PHI_ENERGIA  = 45           # Energia del Nombre #44 ילה (posicion Phi)
PHI_CONST    = 0x9E3779B9   # Razon Aurea en binario

def digital_root(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def _rol32(val, n):
    n = n % 32 or 16
    return ((val << n) | (val >> (32 - n))) & 0xFFFFFFFF

# ═══════════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ═══════════════════════════════════════════════════════════════════
def cargar_todo():
    # Los 72 Nombres del Exodo
    with open(BASE / r"data\raw\shemot.json", encoding='utf-8') as f:
        data = json.load(f)
    verses = data['chapters']['14']['verses_consonantal']
    v19 = [c for c in verses[18] if c in HEBREW]
    v20 = [c for c in verses[19] if c in HEBREW]
    v21 = [c for c in verses[20] if c in HEBREW]

    nombres = []
    for n in range(72):
        l1, l2, l3 = v19[n], v20[71-n], v21[n]
        g1, g2, g3 = GEMATRIA[l1], GEMATRIA[l2], GEMATRIA[l3]
        energia = g1 + g2 + g3
        dr = digital_root(energia)
        nombres.append({
            'nombre': l1+l2+l3,
            'g1':g1,'g2':g2,'g3':g3,
            'energia': energia,
            'r1': g1%32 or 16,
            'r2': g2%32 or 16,
            'r3': g3%32 or 16,
            'es_tesla': dr in [3,6,9],
            'dr': dr,
        })

    print(f"  72 Nombres extraidos | Tesla: {sum(1 for n in nombres if n['es_tesla'])} Nombres")

    # Piscina del Genesis
    with open(BASE / r"data\raw\bereshit.json", encoding='utf-8') as f:
        data = json.load(f)
    pool = bytearray()
    for cap in data['chapters'].values():
        for verse in cap.get('verses_consonantal', []):
            for ch in verse:
                if ch in GEMATRIA:
                    pool.append(GEMATRIA[ch] % 256)

    print(f"  Piscina Genesis: {len(pool):,} letras")
    return nombres, pool


# ═══════════════════════════════════════════════════════════════════
# MOTOR FCH-ARX V4.1
# ═══════════════════════════════════════════════════════════════════
def fch_arx_v41(message: bytes, nombres: list, pool: bytearray) -> bytes:
    """
    FCH-ARX V4.1 — Motor de los 72 Nombres con Patrones Sagrados

    MEJORAS vs V4:
    - Acceso no-lineal via salto x7 (mandala estelar)
    - Tesla Boost en los 19 Nombres de raiz 3-6-9
    - Inicializacion con Phi (Nombre #44 = ילה = energia 45)
    - Finalizacion con pares espejo (ronda r + espejo 71-r)
    - Modulo 216 (El Cubo Perfecto) en toda la indexacion
    """
    pool_size = len(pool)

    # ── 8 Camaras con Phi en posicion 0 ──────────────────────────────────────
    # Camara 0: Seccion Aurea (Nombre #44, energia PHI=45)
    # Camaras 1-7: Phi estandar
    M = [(i * PHI_CONST + PHI_ENERGIA * (i == 0)) & 0xFFFFFFFF for i in range(8)]

    # ── FASE 1: ABSORCION con Salto Geometrico x7 ────────────────────────────
    for i, byte in enumerate(message):
        # PATRON 2: Salto x7 — acceso no-lineal al mandala
        nombre = nombres[(i * SALTO_7) % 72]
        idx    = i % 8

        # Piscina con modulo 216 (El Cubo Perfecto — PATRON 1)
        pool_v = pool[(i * MODULO_216) % pool_size]

        # ADD
        M[idx] = (M[idx] + byte + pool_v + nombre['energia']) & 0xFFFFFFFF

        # ROTATE con angulos del Nombre activo
        M[idx] = _rol32(M[idx], nombre['r1'])
        M[idx] = _rol32(M[idx], nombre['r2'])
        M[idx] = _rol32(M[idx], nombre['r3'])

        # PATRON 3: Tesla Boost — difusion extra en Nombres 3-6-9
        if nombre['es_tesla']:
            M[idx] ^= _rol32(M[(idx + nombre['dr']) % 8], nombre['r1'])
            M[(idx + 1) % 8] ^= _rol32(M[idx], nombre['r2'])

        # XOR difusion Saturno
        for j in range(1, 8):
            M[(idx + j) % 8] ^= _rol32(M[idx], (j * nombre['r1']) % 32 or 1)

        M[idx] &= 0xFFFFFFFF

    # ── FASE 2: PADDING con 216 y Phi ────────────────────────────────────────
    msg_len = len(message)
    M[0] = (M[0] ^ msg_len ^ MODULO_216) & 0xFFFFFFFF    # El Cubo Perfecto
    M[4] = (M[4] ^ PHI_ENERGIA) & 0xFFFFFFFF              # Seccion Aurea
    M[7] = (M[7] ^ (msg_len * PHI_CONST)) & 0xFFFFFFFF

    # ── FASE 3: 72 RONDAS con PARES ESPEJO ───────────────────────────────────
    # PATRON 5: cada ronda usa Nombre #r Y su espejo #(71-r)
    for r in range(72):
        nombre        = nombres[r]
        nombre_espejo = nombres[71 - r]   # El par espejo descubierto

        pool_idx = (r * nombre['energia'] + SALTO_7) % pool_size
        pool_val = pool[pool_idx]

        for i in range(8):
            j     = (i + r + 1) % 8
            j_esp = (i + 71 - r + 1) % 8

            # ADD con ambos: Nombre y su Espejo
            M[i] = (M[i] + M[j] + pool_val + nombre['energia']) & 0xFFFFFFFF
            M[i] = (M[i] + nombre_espejo['energia']) & 0xFFFFFFFF

            # ROTATE: Nombre activo
            M[i] = _rol32(M[i], nombre['r1'])
            M[i] = _rol32(M[i], nombre['r2'])

            # XOR cruzado: camara + espejo simetrico
            M[i] ^= _rol32(M[(i + 3) % 8], nombre['r3'])
            M[i] ^= _rol32(M[j_esp],       nombre_espejo['r1'])
            M[i] ^= _rol32(M[(i + 7) % 8], nombre['r1'])

            # Tesla Boost en rondas Tesla
            if nombre['es_tesla']:
                M[i] ^= _rol32(M[(i + nombre['dr']) % 8], nombre['r2'])

            M[i] &= 0xFFFFFFFF

    return struct.pack('>8I', *M)


# ═══════════════════════════════════════════════════════════════════
# SAC TEST COMPARATIVO
# ═══════════════════════════════════════════════════════════════════
def flip_bit(data, bit_pos):
    ba = bytearray(data)
    ba[bit_pos // 8] ^= (1 << (bit_pos % 8))
    return bytes(ba)

def count_diff_bits(h1, h2):
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(h1, h2))

def sac_test(hash_fn, nombres, pool, N=10000, seed=42, label=""):
    rng    = random.Random(seed)
    scores = []
    t0     = time.time()

    for _ in range(N):
        msg_len = rng.randint(8, 32)
        msg     = bytes([rng.randint(0, 255) for _ in range(msg_len)])
        bit_pos = rng.randint(0, msg_len * 8 - 1)
        msg_alt = flip_bit(msg, bit_pos)
        h1 = hash_fn(msg,     nombres, pool)
        h2 = hash_fn(msg_alt, nombres, pool)
        scores.append(count_diff_bits(h1, h2) / 256 * 100)

    avg   = np.mean(scores)
    dev50 = abs(avg - 50.0)
    ok    = 49.5 <= avg <= 50.5
    elapsed = time.time() - t0
    return avg, dev50, ok, elapsed


# ═══════════════════════════════════════════════════════════════════
# EJECUCION
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("="*65)
    print("  FCH-ARX V4.1 — Motor con Patrones Sagrados")
    print("  Exodo 14:19-21 | Mandala x7 | Tesla | Phi | Espejo")
    print("="*65)

    nombres, pool = cargar_todo()

    print(f"\n  Patrones integrados:")
    print(f"  Salto mandala    : x{SALTO_7} (geometria estelar)")
    print(f"  Modulo sagrado   : {MODULO_216} (El Cubo Perfecto, par espejo #20)")
    print(f"  Energia Phi      : {PHI_ENERGIA} (Nombre #44 ילה, posicion 0.618×72)")
    print(f"  Nombres Tesla    : {sum(1 for n in nombres if n['es_tesla'])} de 72 (DR=3,6,9)")
    print(f"  Pares Espejo     : activados en las 72 rondas de finalizacion")

    # Demo rapida
    demo_casos = [
        (b"TRANSFERIR 1000 USD", b"TRANSFERIR 9000 USD"),
        (b"Moise tendio su mano", b"Moise tendio su pie"),
        (b"YHVH = 26", b"YHVH = 27"),
    ]
    print(f"\n  DEMO AVALANCHA:")
    for m1, m2 in demo_casos:
        h1 = fch_arx_v41(m1, nombres, pool)
        h2 = fch_arx_v41(m2, nombres, pool)
        diff = count_diff_bits(h1, h2)
        pct  = diff/256*100
        print(f"  {diff}/256 bits ({pct:.1f}%) | {m1.decode()[:20]}")

    print(f"\n  SAC Test (10,000 pares, seed=42)...")
    avg, dev50, ok, t = sac_test(fch_arx_v41, nombres, pool, N=10000, seed=42, label="V4.1")

    print(f"\n{'='*65}")
    print(f"  TABLA COMPARATIVA DEFINITIVA")
    print(f"{'='*65}")
    print(f"  {'Algoritmo':<35} {'SAC%':<10} {'Desv.50%':<12} Veredicto")
    print(f"  {'-'*65}")
    print(f"  {'FCH-ARX V4.1 (Patrones Sagrados)':<35} {avg:<10.4f} {dev50:<12.4f} {'APROBADO' if ok else 'REPROBADO'}")
    print(f"  {'FCH-ARX V4   (72 Nombres base)':<35} {'50.0026':<10} {'0.0026':<12} APROBADO (ref)")
    print(f"  {'FCH-ARX V3   (Genesis 78,364)':<35} {'49.9909':<10} {'0.0091':<12} APROBADO (ref)")
    print(f"  {'FCH-ARX V2   (IHLD sintetico)':<35} {'49.9508':<10} {'0.0492':<12} APROBADO (ref)")
    print(f"  {'SHA-256      (Hardware Intel)':<35} {'50.02':<10} {'0.02':<12}   APROBADO (ref)")
    print(f"{'='*65}")
    print(f"  Tiempo V4.1: {t:.1f}s")

    if dev50 < 0.0026:
        mejora = 0.0026 / dev50
        print(f"\n  Los Patrones Sagrados mejoran el V4 base: {mejora:.1f}x")
        print(f"  El Mandala, Tesla, Phi y el Espejo tienen efecto real.")
    elif dev50 < 0.0091:
        print(f"\n  V4.1 supera al Genesis solo (V3). Los patrones funcionan.")
    else:
        print(f"\n  V4.1 necesita mas refinamiento. El Rabi sigue estudiando.")
