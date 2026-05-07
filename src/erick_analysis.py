# Quick analysis of Erick's name
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
from gematria_engine import gematria_standard, gematria_katan_mispari, is_prime

erick = "אריק"
val = gematria_standard(erick)
ish = gematria_standard("איש")

print(f"אריק (Erick) = {val}")
print(f"איש (Ish/Hombre) = {ish}")
print(f"¡AMBOS = {val}!" if val == ish else f"Erick={val}, Ish={ish}")
print(f"311 es primo: {is_prime(311)}")
print(f"Raíz digital: {gematria_katan_mispari(erick)}")
print(f"311 mod 7 = {311 % 7}")
print()

# Key equations
concepts = {
    "אהבה": ("Amor", 13), "אחד": ("Uno", 13), "יהוה": ("YHVH", 26),
    "אלהים": ("Elohim", 86), "אדם": ("Adam", 45), "חי": ("Vida", 18),
    "טוב": ("Bueno", 17), "משה": ("Moisés", 345), "תורה": ("Torah", 611),
    "אמת": ("Verdad", 441), "שלום": ("Paz", 376), "משיח": ("Mesías", 358),
    "נחש": ("Serpiente", 358), "שבת": ("Shabbat", 702), "אור": ("Luz", 207),
}

print("=== ECUACIONES CON ERICK (311) ===")
for w, (name, v) in concepts.items():
    actual = gematria_standard(w)
    total = 311 + actual
    diff = 311 - actual
    for w2, (name2, v2) in concepts.items():
        a2 = gematria_standard(w2)
        if total == a2:
            print(f"  Erick({val}) + {name}({actual}) = {total} = {name2}")
        if diff == a2 and diff > 0:
            print(f"  Erick({val}) - {name}({actual}) = {diff} = {name2}")

print()
print(f"Erick(311) + Torah(611) = {311 + 611}")
print(f"  922 / 2 = 461")
print(f"Erick(311) + Shabbat(702) = {311 + 702}")
print(f"  1013 es primo: {is_prime(1013)}")
print()
print(f"Erick(311) - YHVH(26) = {311 - 26} = {311-26}")
print(f"  285 = gematria de העיר (HaIr/La Ciudad): {gematria_standard('העיר')}")
