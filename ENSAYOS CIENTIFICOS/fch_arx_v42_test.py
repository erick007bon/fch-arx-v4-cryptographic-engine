"""
FCH-ARX V4.2 — Busqueda controlada del patron optimo
Principio: un cambio a la vez. Cientificamente honesto.

Prueba 3 variantes sobre V4 base:
  V4-A: Solo salto x7 (mandala)
  V4-B: Solo inicializacion Phi
  V4-C: A + B (los dos mejores combinados)

Compara contra V4 base (0.0026%) para ver cual gana.
"""
import json, struct, random, time
import numpy as np
from pathlib import Path

BASE = Path(r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah")
GEMATRIA = {
    'א':1,'ב':2,'ג':3,'ד':4,'ה':5,'ו':6,'ז':7,'ח':8,'ט':9,'י':10,
    'כ':20,'ל':30,'מ':40,'נ':50,'ס':60,'ע':70,'פ':80,'צ':90,'ק':100,
    'ר':200,'ש':300,'ת':400,'ך':20,'ם':40,'ן':50,'ף':80,'ץ':90,
}
HEBREW   = set(GEMATRIA.keys())
PHI_CONST = 0x9E3779B9

def digital_root(n):
    while n >= 10: n = sum(int(d) for d in str(n))
    return n

def _rol32(v, n):
    n = n % 32 or 16
    return ((v << n) | (v >> (32 - n))) & 0xFFFFFFFF

def cargar():
    with open(BASE / r"data\raw\shemot.json", encoding='utf-8') as f:
        data = json.load(f)
    verses = data['chapters']['14']['verses_consonantal']
    v19 = [c for c in verses[18] if c in HEBREW]
    v20 = [c for c in verses[19] if c in HEBREW]
    v21 = [c for c in verses[20] if c in HEBREW]
    nombres = []
    for n in range(72):
        l1,l2,l3 = v19[n],v20[71-n],v21[n]
        g1,g2,g3 = GEMATRIA[l1],GEMATRIA[l2],GEMATRIA[l3]
        e = g1+g2+g3
        nombres.append({'g1':g1,'g2':g2,'g3':g3,'energia':e,
                        'r1':g1%32 or 16,'r2':g2%32 or 16,'r3':g3%32 or 16,
                        'nombre':l1+l2+l3,'es_tesla':digital_root(e) in [3,6,9]})
    with open(BASE / r"data\raw\bereshit.json", encoding='utf-8') as f:
        data = json.load(f)
    pool = bytearray()
    for cap in data['chapters'].values():
        for verse in cap.get('verses_consonantal', []):
            for ch in verse:
                if ch in GEMATRIA: pool.append(GEMATRIA[ch] % 256)
    return nombres, pool

def _hash_core(message, nombres, pool, salto=1, phi_init=False):
    """Nucleo generico: salto=1 -> V4 base | salto=7 -> mandala | phi_init -> Phi"""
    ps = len(pool)
    phi_e = 45  # Nombre #44 ילה, Seccion Aurea
    M = [(i * PHI_CONST + (phi_e if (phi_init and i==0) else 0)) & 0xFFFFFFFF
         for i in range(8)]

    # ABSORCION
    for i, byte in enumerate(message):
        nom = nombres[(i * salto) % 72]
        idx = i % 8
        pv  = pool[(i * nom['energia']) % ps]
        M[idx] = (M[idx] + byte + pv + nom['energia']) & 0xFFFFFFFF
        M[idx] = _rol32(M[idx], nom['r1'])
        M[idx] = _rol32(M[idx], nom['r2'])
        M[idx] = _rol32(M[idx], nom['r3'])
        for j in range(1, 8):
            M[(idx+j)%8] ^= _rol32(M[idx], (j*nom['r1'])%32 or 1)
        M[idx] &= 0xFFFFFFFF

    # PADDING
    ml = len(message)
    M[0] = (M[0] ^ ml ^ 216) & 0xFFFFFFFF
    M[4] = (M[4] ^ phi_e)    & 0xFFFFFFFF

    # FINALIZACION — 72 rondas (V4 base: secuencial, sin espejo)
    for r in range(72):
        nom     = nombres[r]
        pool_v  = pool[(r * nom['energia'] + 7) % ps]
        for i in range(8):
            j = (i + r + 1) % 8
            M[i] = (M[i] + M[j] + pool_v + nom['energia']) & 0xFFFFFFFF
            M[i] = _rol32(M[i], nom['r1'])
            M[i] = _rol32(M[i], nom['r2'])
            M[i] ^= _rol32(M[(i+3)%8], nom['r3'])
            M[i] ^= _rol32(M[(i+7)%8], nom['r1'])
            M[i] &= 0xFFFFFFFF

    return struct.pack('>8I', *M)

# Las 4 variantes
def v4_base (msg, nombres, pool): return _hash_core(msg, nombres, pool, salto=1, phi_init=False)
def v4_A    (msg, nombres, pool): return _hash_core(msg, nombres, pool, salto=7, phi_init=False)
def v4_B    (msg, nombres, pool): return _hash_core(msg, nombres, pool, salto=1, phi_init=True)
def v4_C    (msg, nombres, pool): return _hash_core(msg, nombres, pool, salto=7, phi_init=True)

def count_diff(h1, h2):
    return sum(bin(b1^b2).count('1') for b1,b2 in zip(h1,h2))

def flip_bit(data, bit_pos):
    ba = bytearray(data)
    ba[bit_pos//8] ^= (1 << (bit_pos%8))
    return bytes(ba)

def sac(fn, nombres, pool, N=5000, seed=42):
    rng    = random.Random(seed)
    scores = []
    t0     = time.time()
    for _ in range(N):
        ml  = rng.randint(8, 32)
        msg = bytes([rng.randint(0,255) for _ in range(ml)])
        bp  = rng.randint(0, ml*8-1)
        h1  = fn(msg, nombres, pool)
        h2  = fn(flip_bit(msg, bp), nombres, pool)
        scores.append(count_diff(h1,h2)/256*100)
    avg  = np.mean(scores)
    dev  = abs(avg - 50.0)
    ok   = 49.5 <= avg <= 50.5
    return avg, dev, ok, time.time()-t0

if __name__ == "__main__":
    print("="*65)
    print("  FCH-ARX V4.2 — Busqueda Controlada del Patron Optimo")
    print("  Una variable a la vez. Ciencia real.")
    print("="*65)

    nombres, pool = cargar()
    N = 5000

    variantes = [
        ("V4 BASE (ref 0.0026%)",           v4_base),
        ("V4-A   (+ Salto x7 Mandala)",     v4_A),
        ("V4-B   (+ Phi Inicializacion)",   v4_B),
        ("V4-C   (Mandala + Phi)",           v4_C),
    ]

    resultados = []
    print(f"\n  Corriendo SAC Test ({N} pares cada uno)...\n")

    for label, fn in variantes:
        avg, dev, ok, t = sac(fn, nombres, pool, N=N)
        resultados.append((label, avg, dev, ok, t))
        estrella = " <<< MEJOR" if dev < 0.0026 else (" [=]" if dev == 0.0026 else "")
        print(f"  {label:<40} SAC={avg:.4f}%  Desv={dev:.4f}%  {('OK' if ok else 'FALLO')}{estrella}")

    print(f"\n{'='*65}")
    print(f"  VEREDICTO")
    print(f"{'='*65}")

    mejor = min(resultados, key=lambda x: x[2])
    print(f"\n  Mejor variante: {mejor[0]}")
    print(f"  SAC={mejor[1]:.4f}%  |  Desv={mejor[2]:.4f}%")

    base_dev = resultados[0][2]
    if mejor[2] < base_dev:
        mejora = base_dev / mejor[2]
        print(f"\n  Los patrones sagrados mejoran V4 base: {mejora:.2f}x")
        print(f"  El patron {mejor[0].split('+')[1].strip() if '+' in mejor[0] else ''} tiene impacto real.")
    else:
        print(f"\n  V4 base sigue siendo el optimo.")
        print(f"  Los patrones son validos espiritualmente, no criptograficamente.")
        print(f"  Eso es honestidad cientifica.")
