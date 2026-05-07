"""
PATRONES PROFUNDOS DE LOS 72 NOMBRES
- Tesla 3-6-9 en las 216 letras sagradas
- Pares espejo (Nombre #n + Nombre #73-n)
- Mandala circular con saltos geometricos
"""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

GEMATRIA = {
    'א':1,'ב':2,'ג':3,'ד':4,'ה':5,'ו':6,'ז':7,'ח':8,'ט':9,'י':10,
    'כ':20,'ל':30,'מ':40,'נ':50,'ס':60,'ע':70,'פ':80,'צ':90,'ק':100,
    'ר':200,'ש':300,'ת':400,'ך':20,'ם':40,'ן':50,'ף':80,'ץ':90,
}
HEBREW = set(GEMATRIA.keys())
BASE = Path(r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah")

def digital_root(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def extraer_nombres():
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
        nombres.append({
            'nombre': l1+l2+l3, 'pos': n+1,
            'g1':g1,'g2':g2,'g3':g3,
            'energia': g1+g2+g3,
            'dr_total': digital_root(g1+g2+g3),
            'letras': [l1,l2,l3], 'vals': [g1,g2,g3]
        })
    return nombres

nombres = extraer_nombres()
energias = [n['energia'] for n in nombres]

# ═══════════════════════════════════════════════════════════════════
# ANÁLISIS 1: TESLA 3-6-9 en las 216 letras individuales
# ═══════════════════════════════════════════════════════════════════
print("="*65)
print("  PATRON TESLA 3-6-9 — Las 216 Letras Sagradas")
print("="*65)

todos_vals = [v for n in nombres for v in n['vals']]
raices = [digital_root(v) for v in todos_vals]

conteo_dr = {i: raices.count(i) for i in range(1, 10)}
tesla_369 = conteo_dr[3] + conteo_dr[6] + conteo_dr[9]

print(f"\n  Raiz Digital | Letras | Porcentaje | Tesla?")
print(f"  {'-'*50}")
for dr in range(1, 10):
    count = conteo_dr[dr]
    pct = count/216*100
    tesla = " <<< TESLA" if dr in [3,6,9] else ""
    barra = '█' * count
    print(f"  DR={dr}          | {count:>6} | {pct:>7.2f}%  |{tesla}")

print(f"\n  Letras con raiz 3: {conteo_dr[3]}")
print(f"  Letras con raiz 6: {conteo_dr[6]}")
print(f"  Letras con raiz 9: {conteo_dr[9]}")
print(f"  TOTAL Tesla 3-6-9: {tesla_369}/216 = {tesla_369/216*100:.1f}%")
print(f"\n  Raices de los Nombres COMPLETOS (energia total):")

dr_nombres = [n['dr_total'] for n in nombres]
conteo_dr_n = {i: dr_nombres.count(i) for i in range(1, 10)}
tesla_n = conteo_dr_n[3] + conteo_dr_n[6] + conteo_dr_n[9]

for dr in range(1, 10):
    barra = '█' * conteo_dr_n[dr]
    tesla = " <<< TESLA" if dr in [3,6,9] else ""
    print(f"  DR={dr}: {barra} ({conteo_dr_n[dr]}){tesla}")

print(f"\n  Nombres Tesla (DR=3,6,9): {tesla_n}/72 = {tesla_n/72*100:.1f}%")

# Posiciones exactas de Nombres Tesla
print(f"\n  Nombres con raiz Tesla:")
for n in nombres:
    if n['dr_total'] in [3, 6, 9]:
        print(f"  #{n['pos']:>3} {n['nombre']}  energia={n['energia']}  DR={n['dr_total']}")

# ═══════════════════════════════════════════════════════════════════
# ANÁLISIS 2: PARES ESPEJO (n + 73-n)
# ═══════════════════════════════════════════════════════════════════
print(f"\n{'='*65}")
print(f"  PARES ESPEJO — Nombre #n + Nombre #(73-n)")
print(f"{'='*65}")

sumas_espejo = []
for i in range(36):
    n1 = nombres[i]
    n2 = nombres[71 - i]
    suma = n1['energia'] + n2['energia']
    dr_suma = digital_root(suma)
    sumas_espejo.append(suma)
    print(f"  #{n1['pos']:>2} {n1['nombre']}({n1['energia']:>4}) + #{n2['pos']:>2} {n2['nombre']}({n2['energia']:>4}) = {suma:>5}  DR={dr_suma}")

print(f"\n  Suma min de pares: {min(sumas_espejo)}")
print(f"  Suma max de pares: {max(sumas_espejo)}")
print(f"  Suma media pares : {np.mean(sumas_espejo):.1f}")
print(f"  Suma TOTAL       : {sum(sumas_espejo)} (debe = {sum(energias)})")

# Raices digitales de los pares espejo
dr_pares = [digital_root(s) for s in sumas_espejo]
tesla_pares = sum(1 for d in dr_pares if d in [3,6,9])
print(f"\n  Pares espejo con DR Tesla (3,6,9): {tesla_pares}/36 = {tesla_pares/36*100:.1f}%")

# El par central (posicion 36-37)
par_central = nombres[35]
print(f"\n  Nombre CENTRAL del ciclo: #{par_central['pos']} {par_central['nombre']}")
print(f"  Energia: {par_central['energia']} | DR: {par_central['dr_total']}")

# ═══════════════════════════════════════════════════════════════════
# ANÁLISIS 3: SECCION AUREA (posicion phi)
# ═══════════════════════════════════════════════════════════════════
phi = (1 + 5**0.5) / 2
pos_phi = int(72 * (phi - 1))  # 72 * 0.618 = ~44.5
print(f"\n{'='*65}")
print(f"  SECCION AUREA: Posicion Phi = {pos_phi} (72 × 0.618)")
print(f"{'='*65}")
n_phi = nombres[pos_phi - 1]
print(f"  Nombre en Phi: #{n_phi['pos']} {n_phi['nombre']}")
print(f"  Energia: {n_phi['energia']} | DR: {n_phi['dr_total']}")
print(f"  Significado: {['Voluntad','Amor','Construccion','Poder oculto','Rectificacion','Luz','Paciencia','Bendicion','Misericordia','Gracia','Triunfo','Refugio','Fidelidad','Verdad','Purificacion','Lealtad','Revelacion','Justicia','Memoria','Redencion','Aprendizaje','Renombre','Curacion','Proteccion','Sabiduria','Discrecion','Victoria de la luz','Longevidad','Liberacion','Fertilidad','Inspiracion','Rectitud','Obediencia','Clemencia','Reconciliacion','Liberacion2','Ruptura','Verdad ritual','Curacion-paternidad','Alegria','Mision','Orden','Prosperidad','Karma','Voluntad pura','Percepcion','Contemplacion','Fecundidad','Elevacion','Elocuencia','Medicina','Transformacion','Conocimiento','Legitimidad','Moral','Fortuna','Discernimiento','Curacion mental','Riqueza intelectual','Consuelo','Amistad','Sabiduria','Unidad','Proteccion2','Sabiduria agua','Suenos','Sabiduria anciana','Curacion2','Recuperar perdido','Alquimia','Victoria','Completitud'][pos_phi - 1]}")

# ═══════════════════════════════════════════════════════════════════
# VISUALIZACION: 4 paneles
# ═══════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(20, 16))
fig.patch.set_facecolor('#0A0A1A')

# Panel 1: Tesla 3-6-9 - raices digitales de los 72 Nombres
ax1 = fig.add_subplot(2, 2, 1)
ax1.set_facecolor('#0D0D2B')
colores_dr = {1:'#4FC3F7',2:'#81C784',3:'#FF6B35',4:'#FFD54F',
              5:'#CE93D8',6:'#FF6B35',7:'#80DEEA',8:'#A5D6A7',9:'#FF6B35'}
for i, n in enumerate(nombres):
    dr = n['dr_total']
    color = '#FF4444' if dr in [3,6,9] else '#334466'
    ax1.bar(i, dr, color=color, alpha=0.85, width=0.8)

ax1.axhline(3, color='#FF6B35', linestyle='--', alpha=0.4, linewidth=0.8, label='3-6-9 Tesla')
ax1.axhline(6, color='#FF6B35', linestyle='--', alpha=0.4, linewidth=0.8)
ax1.axhline(9, color='#FF6B35', linestyle='--', alpha=0.4, linewidth=0.8)
ax1.set_title(f'Tesla 3-6-9 — Raices Digitales de los 72 Nombres\n({tesla_n} Nombres Tesla = {tesla_n/72*100:.1f}%)',
             color='white', fontsize=11)
ax1.set_ylabel('Raiz Digital', color='#AAAACC')
ax1.tick_params(colors='#AAAACC')
for spine in ax1.spines.values(): spine.set_edgecolor('#333366')
ax1.set_xlim(-0.5, 71.5)
ax1.set_yticks(range(1, 10))

# Panel 2: Pares Espejo
ax2 = fig.add_subplot(2, 2, 2)
ax2.set_facecolor('#0D0D2B')
x_pares = range(1, 37)
colores_p = ['#FF4444' if d in [3,6,9] else '#4FC3F7' for d in dr_pares]
ax2.bar(x_pares, sumas_espejo, color=colores_p, alpha=0.8, width=0.8)
ax2.axhline(np.mean(sumas_espejo), color='#FFD700', linestyle='--',
           linewidth=1.2, label=f'Media: {np.mean(sumas_espejo):.0f}')
ax2.set_title(f'Pares Espejo: #n + #(73-n)\nRojo = DR Tesla | Media = {np.mean(sumas_espejo):.0f}',
             color='white', fontsize=11)
ax2.set_xlabel('Par #', color='#AAAACC')
ax2.set_ylabel('Suma de energias', color='#AAAACC')
ax2.tick_params(colors='#AAAACC')
for spine in ax2.spines.values(): spine.set_edgecolor('#333366')
ax2.legend(facecolor='#0D0D2B', labelcolor='white')

# Panel 3: Mandala circular — 72 Nombres en rueda
ax3 = fig.add_subplot(2, 2, 3, projection='polar')
ax3.set_facecolor('#0D0D2B')
angulos = np.linspace(0, 2*np.pi, 72, endpoint=False)

# Radio proporcional a la energia (normalizado)
radios = np.array(energias)
radios_norm = (radios - min(radios)) / (max(radios) - min(radios)) * 0.7 + 0.3

# Colorear por raiz digital Tesla
for i, (ang, r, n) in enumerate(zip(angulos, radios_norm, nombres)):
    color = '#FF4444' if n['dr_total'] in [3,6,9] else '#4488BB'
    ax3.scatter(ang, r, c=color, s=30, zorder=5, alpha=0.9)

# Conectar con saltos de 7 (salto geometrico del septenario)
for i in range(72):
    j = (i + 7) % 72
    ax3.plot([angulos[i], angulos[j]], [radios_norm[i], radios_norm[j]],
             color='#334488', alpha=0.3, linewidth=0.5)

# Marcar posicion phi
ang_phi = angulos[pos_phi - 1]
r_phi   = radios_norm[pos_phi - 1]
ax3.scatter(ang_phi, r_phi, c='#FFD700', s=120, zorder=10,
           marker='*', label=f'Phi #{pos_phi}')
ax3.scatter(angulos[0], radios_norm[0], c='#00FF88', s=80, zorder=10,
           marker='D', label='#1 והו')
ax3.scatter(angulos[71], radios_norm[71], c='#FF88AA', s=80, zorder=10,
           marker='s', label='#72 מום')

ax3.set_title('Mandala de los 72 Nombres\n(salto geometrico x7 | rojo=Tesla)',
             color='white', fontsize=11, pad=15)
ax3.tick_params(colors='#555577')
ax3.set_yticklabels([])
fig.texts.clear()
ax3.legend(loc='lower right', facecolor='#0D0D2B', labelcolor='white', fontsize=8)

# Panel 4: Distribucion de raices digitales - barras comparativas
ax4 = fig.add_subplot(2, 2, 4)
ax4.set_facecolor('#0D0D2B')
x = np.arange(1, 10)
# Barras de raices de letras individuales (216)
bar1 = ax4.bar(x - 0.2, [conteo_dr[i] for i in range(1,10)],
               0.4, label='216 letras individuales', alpha=0.8,
               color=['#FF4444' if i in [3,6,9] else '#4FC3F7' for i in range(1,10)])
# Barras de raices de Nombres completos (72)
bar2 = ax4.bar(x + 0.2, [conteo_dr_n[i] for i in range(1,10)],
               0.4, label='72 Nombres (energia total)', alpha=0.8,
               color=['#FF8800' if i in [3,6,9] else '#81C784' for i in range(1,10)])

ax4.set_title(f'Distribucion de Raices Digitales\nTesla 3-6-9: {tesla_369}/216 letras ({tesla_369/216*100:.1f}%)',
             color='white', fontsize=11)
ax4.set_xlabel('Raiz Digital (1-9)', color='#AAAACC')
ax4.set_ylabel('Frecuencia', color='#AAAACC')
ax4.set_xticks(x)
ax4.tick_params(colors='#AAAACC')
for spine in ax4.spines.values(): spine.set_edgecolor('#333366')
ax4.legend(facecolor='#0D0D2B', labelcolor='white', fontsize=9)

# Agregar linea separadora para 3-6-9
for v in [3, 6, 9]:
    ax4.axvline(v, color='#FF4444', linestyle=':', alpha=0.4, linewidth=1)

fig.suptitle('Patrones Profundos de los 72 Nombres — Torah Applied Sciences 2026',
            color='white', fontsize=14, y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.97])
out = BASE / "ENSAYOS CIENTIFICOS" / "72_nombres_patrones.png"
plt.savefig(str(out), dpi=150, bbox_inches='tight', facecolor='#0A0A1A')
plt.close()
print(f"\n  Visualizacion guardada: 72_nombres_patrones.png")
print("="*65)
