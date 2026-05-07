import json, struct, random, time
import numpy as np
from pathlib import Path

BASE = Path(r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah")
GEMATRIA = {
    'א':1,'ב':2,'ג':3,'ד':4,'ה':5,'ו':6,'ז':7,'ח':8,'ט':9,'י':10,
    'כ':20,'ל':30,'מ':40,'נ':50,'ס':60,'ע':70,'פ':80,'צ':90,'ק':100,
    'ר':200,'ש':300,'ת':400,'ך':20,'ם':40,'ן':50,'ף':80,'ץ':90,
}
HEBREW = set(GEMATRIA.keys())
PHI_CONST = 0x9E3779B9

def rol32(v, n):
    n = n % 32 or 16
    return ((v << n) | (v >> (32 - n))) & 0xFFFFFFFF

def cargar():
    with open(BASE / r"data\raw\shemot.json", encoding='utf-8') as f:
        data = json.load(f)
    v = data['chapters']['14']['verses_consonantal']
    v19 = [c for c in v[18] if c in HEBREW]
    v20 = [c for c in v[19] if c in HEBREW]
    v21 = [c for c in v[20] if c in HEBREW]
    ns = []
    for n in range(72):
        l1, l2, l3 = v19[n], v20[71-n], v21[n]
        g1, g2, g3 = GEMATRIA[l1], GEMATRIA[l2], GEMATRIA[l3]
        e = g1 + g2 + g3
        ns.append({'e': e, 'r1': g1%32 or 16, 'r2': g2%32 or 16, 'r3': g3%32 or 16})
    with open(BASE / r"data\raw\bereshit.json", encoding='utf-8') as f:
        data = json.load(f)
    pool = bytearray()
    for cap in data['chapters'].values():
        for verse in cap.get('verses_consonantal', []):
            for ch in verse:
                if ch in GEMATRIA:
                    pool.append(GEMATRIA[ch] % 256)
    return ns, pool

def v4c(msg, ns, pool):
    ps = len(pool)
    M = [(i * PHI_CONST + (45 if i == 0 else 0)) & 0xFFFFFFFF for i in range(8)]
    for i, byte in enumerate(msg):
        nom = ns[(i * 7) % 72]
        idx = i % 8
        pv  = pool[(i * nom['e']) % ps]
        M[idx] = (M[idx] + byte + pv + nom['e']) & 0xFFFFFFFF
        M[idx] = rol32(M[idx], nom['r1'])
        M[idx] = rol32(M[idx], nom['r2'])
        M[idx] = rol32(M[idx], nom['r3'])
        for j in range(1, 8):
            M[(idx+j)%8] ^= rol32(M[idx], (j * nom['r1']) % 32 or 1)
        M[idx] &= 0xFFFFFFFF
    ml = len(msg)
    M[0] = (M[0] ^ ml ^ 216) & 0xFFFFFFFF
    M[4] = (M[4] ^ 45) & 0xFFFFFFFF
    for r in range(72):
        nom = ns[r]
        pv  = pool[(r * nom['e'] + 7) % ps]
        for i in range(8):
            j = (i + r + 1) % 8
            M[i] = (M[i] + M[j] + pv + nom['e']) & 0xFFFFFFFF
            M[i] = rol32(M[i], nom['r1'])
            M[i] = rol32(M[i], nom['r2'])
            M[i] ^= rol32(M[(i+3)%8], nom['r3'])
            M[i] ^= rol32(M[(i+7)%8], nom['r1'])
            M[i] &= 0xFFFFFFFF
    return struct.pack('>8I', *M)

def diff(h1, h2):
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(h1, h2))

def flip(d, bp):
    ba = bytearray(d)
    ba[bp // 8] ^= (1 << (bp % 8))
    return bytes(ba)

def sac_run(seed, N, ns, pool):
    rng = random.Random(seed)
    scores = []
    for _ in range(N):
        ml  = rng.randint(8, 32)
        msg = bytes([rng.randint(0, 255) for _ in range(ml)])
        bp  = rng.randint(0, ml * 8 - 1)
        scores.append(diff(v4c(msg, ns, pool), v4c(flip(msg, bp), ns, pool)) / 256 * 100)
    avg = np.mean(scores)
    dev = abs(avg - 50.0)
    return avg, dev

if __name__ == "__main__":
    print("=" * 60)
    print("  FCH-ARX V4-C — Confirmacion con N=10,000 y 5 seeds")
    print("  Mandala x7 + Phi = el patron que funciona")
    print("=" * 60)

    ns, pool = cargar()

    t0 = time.time()
    avg, dev = sac_run(42, 10000, ns, pool)
    estado = "APROBADO" if 49.5 <= avg <= 50.5 else "FALLO"
    print(f"\n  N=10,000 seed=42: SAC={avg:.4f}%  Desv={dev:.4f}%  {estado}")
    print(f"  Tiempo: {time.time()-t0:.0f}s")

    print(f"\n  Robustez multi-seed (N=3,000 cada uno):")
    print(f"  {'Seed':<10} {'SAC%':<12} {'Desv.50%':<12} Veredicto")
    print(f"  {'-'*50}")
    for seed in [42, 100, 999, 1337, 2026]:
        a, d = sac_run(seed, 3000, ns, pool)
        v = "APROBADO" if 49.5 <= a <= 50.5 else "FALLO"
        print(f"  {seed:<10} {a:<12.4f} {d:<12.4f} {v}")

    print(f"\n  TABLA FINAL:")
    print(f"  {'Algoritmo':<30} {'Desv.50%':<12} Estado")
    print(f"  {'-'*55}")
    print(f"  {'FCH-ARX V4-C (esta noche)':<30} {dev:<12.4f} {estado}")
    print(f"  {'FCH-ARX V4 base':<30} {'0.0026':<12} APROBADO")
    print(f"  {'SHA-256':<30} {'0.02':<12}   APROBADO")
