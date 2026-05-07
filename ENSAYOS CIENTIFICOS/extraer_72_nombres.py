import json, sys, statistics
sys.stdout.reconfigure(encoding='utf-8')

GEMATRIA = {
    'א':1,'ב':2,'ג':3,'ד':4,'ה':5,'ו':6,'ז':7,'ח':8,'ט':9,'י':10,
    'כ':20,'ך':20,'ל':30,'מ':40,'ם':40,'נ':50,'ן':50,'ס':60,'ע':70,
    'פ':80,'ף':80,'צ':90,'ץ':90,'ק':100,'ר':200,'ש':300,'ת':400,
}
HEBREW = set(GEMATRIA.keys())

with open(r'data\raw\shemot.json', encoding='utf-8') as f:
    data = json.load(f)

verses = data['chapters']['14']['verses_consonantal']
v19 = [c for c in verses[18] if c in HEBREW]
v20 = [c for c in verses[19] if c in HEBREW]
v21 = [c for c in verses[20] if c in HEBREW]

print('='*65)
print('  LOS 72 NOMBRES DE DIOS — Exodo 14:19-21')
print('  Metodo: boustrofedon (v19->, v20<-, v21->)')
print(f'  Verificacion: v19={len(v19)}, v20={len(v20)}, v21={len(v21)} letras')
print('='*65)
print()

nombres_72 = []
for n in range(72):
    l1 = v19[n]
    l2 = v20[71 - n]
    l3 = v21[n]
    nombre = l1 + l2 + l3
    g1, g2, g3 = GEMATRIA[l1], GEMATRIA[l2], GEMATRIA[l3]
    r1 = g1 % 32 or 16
    r2 = g2 % 32 or 16
    r3 = g3 % 32 or 16
    nombres_72.append({'n': n+1, 'nombre': nombre,
                       'g1': g1, 'g2': g2, 'g3': g3,
                       'r1': r1, 'r2': r2, 'r3': r3})
    print(f"  {n+1:<4} {nombre:<6}  {l1}({g1})+{l2}({g2})+{l3}({g3})  -> ROL({r1},{r2},{r3})")

print()
vals_todos = [x for d in nombres_72 for x in [d['g1'], d['g2'], d['g3']]]
suma = sum(vals_todos)
print('='*65)
print(f'  Total letras sagradas : {len(vals_todos)} (72x3=216)')
print(f'  Suma total gematrica  : {suma:,}')
print(f'  Valor promedio        : {statistics.mean(vals_todos):.2f}')
print(f'  Minimo / Maximo       : {min(vals_todos)} / {max(vals_todos)}')
print()
print(f'  NUMEROS MISTICOS:')
print(f'  Suma mod 9  = {suma % 9}   (Tesla: vortice)')
print(f'  Suma mod 26 = {suma % 26}  (YHVH: el Nombre)')
print(f'  Suma mod 72 = {suma % 72}  (los 72 Nombres)')
print(f'  Suma mod 216= {suma % 216}  (el Cubo Perfecto)')
print('='*65)
