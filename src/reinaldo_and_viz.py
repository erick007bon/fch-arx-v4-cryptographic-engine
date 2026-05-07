"""
🔯 ANÁLISIS DE REINALDO EN GEMATRÍA + VISUALIZACIONES
═══════════════════════════════════════════════════════════════════════
Análisis del nombre Reinaldo en hebreo:
- Múltiples transliteraciones
- Lectura en todas las direcciones (técnica kabbalística)
- Sub-palabras ocultas dentro del nombre
- Anagramas y permutaciones (Temurah)
- Conexiones con la Torah

Luego: Visualizaciones estadísticas de la Torah completa.

Autor: Erick Reinaldo Flores Zambrano
═══════════════════════════════════════════════════════════════════════
"""

import sys, os, csv, json, time
from collections import Counter, defaultdict
from itertools import permutations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from gematria_engine import (
    gematria_standard, gematria_ordinal, gematria_reduced,
    gematria_katan_mispari, gematria_atbash, gematria_gadol,
    gematria_kidmi, extract_hebrew_letters, is_prime
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PROC_DIR = os.path.join(PROJECT_DIR, "data", "processed")
VIZ_DIR = os.path.join(PROJECT_DIR, "visualizations")
os.makedirs(VIZ_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# 1. REINALDO — ANÁLISIS PROFUNDO
# ═══════════════════════════════════════════════════════════════

def analyze_reinaldo():
    print(f"\n{'═' * 70}")
    print(f"{'👤 REINALDO — ANÁLISIS KABBALÍSTICO COMPLETO':^70}")
    print(f"{'═' * 70}")
    
    print(f"""
   📖 LECCIÓN: TRANSLITERACIÓN AL HEBREO
   ─────────────────────────────────────────────────────
   El hebreo no tiene vocales escritas (solo consonantes).
   Para transliterar "Reinaldo" usamos las consonantes
   equivalentes más cercanas:
   
   R = ר (Resh)
   E = (vocal — a veces se escribe con י)
   I = י (Yod)
   N = נ (Nun)  
   A = א (Alef)
   L = ל (Lamed)
   D = ד (Dalet)
   O = ו (Vav — también sirve como O/U)
   
   Hay varias transliteraciones posibles. Veamos TODAS:
   ─────────────────────────────────────────────────────
    """)
    
    # Múltiples transliteraciones posibles
    transliterations = {
        'ריינאלדו': 'R-EI-N-A-L-D-O (completa con diptongo)',
        'רינלדו': 'R-I-N-L-D-O (consonántica simple)',
        'ריינלדו': 'R-EI-N-L-D-O (sin Alef)',
        'רינאלדו': 'R-I-N-A-L-D-O (sin diptongo)',
        'ראינלדו': 'R-A-I-N-L-D-O (variante)',
    }
    
    print(f"   {'Hebreo':<12} {'Estándar':>8} {'Ordinal':>8} {'Reducido':>8} {'Raíz':>5} {'Atbash':>7} {'Primo':>6}")
    print(f"   {'─'*12} {'─'*8} {'─'*8} {'─'*8} {'─'*5} {'─'*7} {'─'*6}")
    
    best_name = None
    best_val = 0
    
    for heb, desc in transliterations.items():
        std = gematria_standard(heb)
        ordi = gematria_ordinal(heb)
        red = gematria_reduced(heb)
        dr = gematria_katan_mispari(heb)
        atb = gematria_atbash(heb)
        prime = is_prime(std)
        
        prime_mark = "✡ SÍ" if prime else "  No"
        print(f"   {heb:<12} {std:>8} {ordi:>8} {red:>8} {dr:>5} {atb:>7} {prime_mark:>6}")
        print(f"   {'':12} → {desc}")
        
        if not best_name:
            best_name = heb
            best_val = std
    
    # Usar la transliteración más completa
    name = best_name
    val = best_val
    
    print(f"\n   ⭐ Usando transliteración principal: {name} = {val}")
    
    # Desglose letra por letra
    letters = extract_hebrew_letters(name)
    print(f"\n   📐 DESGLOSE LETRA POR LETRA:")
    
    letter_values = {
        'א': ('Alef', 1, 'Unidad, Dios, lo invisible'),
        'ב': ('Bet', 2, 'Casa, dualidad'),
        'ג': ('Gimel', 3, 'Camello, dar'),
        'ד': ('Dalet', 4, 'Puerta, pobre'),
        'ה': ('He', 5, 'Ventana, aliento de Dios'),
        'ו': ('Vav', 6, 'Gancho, conexión'),
        'ז': ('Zayin', 7, 'Espada, Shabbat'),
        'ח': ('Jet', 8, 'Cerca, vida'),
        'ט': ('Tet', 9, 'Serpiente de bondad'),
        'י': ('Yod', 10, 'Mano de Dios, punto de creación'),
        'כ': ('Kaf', 20, 'Palma, corona'),
        'ל': ('Lamed', 30, 'Aguijón, enseñanza, aprender'),
        'מ': ('Mem', 40, 'Agua, revelado y oculto'),
        'נ': ('Nun', 50, 'Pez, fidelidad, caída y resurgimiento'),
        'ס': ('Samej', 60, 'Apoyo, círculo, protección'),
        'ע': ('Ayin', 70, 'Ojo, percepción'),
        'פ': ('Pe', 80, 'Boca, habla, expresión'),
        'צ': ('Tsadi', 90, 'Anzuelo, justo'),
        'ק': ('Qof', 100, 'Santidad, ciclo'),
        'ר': ('Resh', 200, 'Cabeza, inicio'),
        'ש': ('Shin', 300, 'Fuego divino, diente'),
        'ת': ('Tav', 400, 'Marca, verdad, destino'),
    }
    
    for l in letters:
        info = letter_values.get(l, ('?', 0, '?'))
        print(f"      {l} = {info[0]:>8} = {info[1]:>4}  →  {info[2]}")
    
    print(f"      {'─' * 40}")
    print(f"      TOTAL = {val}")
    
    # ═════════════════════════════════════════════════════════
    # LECTURA EN TODAS LAS DIRECCIONES (TEMURAH)
    # ═════════════════════════════════════════════════════════
    
    print(f"\n{'─' * 70}")
    print(f"{'🔄 LECTURA EN TODAS LAS DIRECCIONES':^70}")
    print(f"{'─' * 70}")
    
    print(f"""
   📖 LECCIÓN: TÉCNICAS DE LECTURA KABBALÍSTICA
   ─────────────────────────────────────────────────────
   En Kabbalah, un nombre no se lee solo de derecha a 
   izquierda. Se lee en TODAS las direcciones porque
   cada dirección revela una dimensión diferente:
   
   → Normal (derecha a izquierda): tu esencia visible
   ← Inverso (izquierda a derecha): tu esencia oculta
   ↑ Primera y última letras: tu origen y destino
   ↓ Sub-palabras internas: lo que llevas dentro
   ─────────────────────────────────────────────────────
    """)
    
    # Normal
    print(f"   → NORMAL: {name} = {val}")
    
    # Inverso
    reversed_name = name[::-1]
    rev_val = gematria_standard(reversed_name)
    print(f"   ← INVERSO: {reversed_name} = {rev_val}")
    print(f"      (Las mismas letras al revés revelan tu 'yo oculto')")
    
    # Primera y última letra
    first_last = letters[0] + letters[-1]
    fl_val = gematria_standard(first_last)
    print(f"\n   ↕ PRIMERA + ÚLTIMA LETRA: {first_last} = {fl_val}")
    fl_info_0 = letter_values.get(letters[0], ('?', 0, '?'))
    fl_info_1 = letter_values.get(letters[-1], ('?', 0, '?'))
    print(f"      {letters[0]} ({fl_info_0[0]}: {fl_info_0[2]})")
    print(f"      {letters[-1]} ({fl_info_1[0]}: {fl_info_1[2]})")
    print(f"      Significado: Tu origen es «{fl_info_0[2]}» y tu destino es «{fl_info_1[2]}»")
    
    # Letras internas (sin primera y última)
    if len(letters) > 2:
        inner = ''.join(letters[1:-1])
        inner_val = gematria_standard(inner)
        print(f"\n   ◉ LETRAS INTERNAS: {inner} = {inner_val}")
        print(f"      (Lo que llevas DENTRO, tu esencia más profunda)")
    
    # ═════════════════════════════════════════════════════════
    # SUB-PALABRAS OCULTAS
    # ═════════════════════════════════════════════════════════
    
    print(f"\n{'─' * 70}")
    print(f"{'🔍 PALABRAS OCULTAS DENTRO DE REINALDO':^70}")
    print(f"{'─' * 70}")
    
    print(f"""
   📖 LECCIÓN: NOTARIKON Y SUB-PALABRAS
   ─────────────────────────────────────────────────────
   Los Rabinos buscan palabras completas DENTRO de un
   nombre. Si tu nombre contiene una palabra hebrea,
   esa palabra define parte de tu misión espiritual.
   ─────────────────────────────────────────────────────
    """)
    
    # Buscar sub-palabras de 2-4 letras dentro del nombre
    known_words = {
        'רי': ('Ri', 'Riego/Irrigación'),
        'ין': ('Yin', 'Vino — parte de יין'),
        'נא': ('Na', 'Por favor / Crudo'),
        'אל': ('El', 'DIOS — ¡Dios está en tu nombre!'),
        'לד': ('Led', 'Dar a luz / Nacimiento'),
        'דו': ('Du', 'Dos / Dualidad'),
        'נר': ('Ner', 'Vela / Luz'),
        'דין': ('Din', 'Juicio / Justicia'),
        'יד': ('Yad', 'Mano'),
        'דל': ('Dal', 'Puerta / Pobre'),
        'נדר': ('Neder', 'Voto / Promesa sagrada'),
        'לי': ('Li', 'Para mí'),
        'אד': ('Ed', 'Vapor — como el que regaba el Edén'),
        'אין': ('Ein', 'Nada — el vacío creativo de Dios'),
        'נאל': ('Nael', 'Redimido'),
        'ריי': ('Rei', 'Mi pastor / Mi amigo'),
        'ייר': ('Yir', 'Temerá — raíz de Temor de Dios'),
    }
    
    name_str = name
    found_words = []
    
    for sub, (trans, meaning) in known_words.items():
        if sub in name_str:
            sub_val = gematria_standard(sub)
            found_words.append((sub, trans, meaning, sub_val))
            prime_mark = " ✡(primo)" if is_prime(sub_val) else ""
            print(f"   ✅ {sub} ({trans}) = {sub_val} — «{meaning}»{prime_mark}")
    
    # Buscar אל (Dios) específicamente
    if 'אל' in name_str:
        print(f"\n   🔯 ¡¡¡ אל (EL / DIOS) ESTÁ DENTRO DE TU NOMBRE !!!")
        print(f"      ריינ-אל-דו → REIN-DIOS-DUO")
        print(f"      Tu nombre literalmente contiene a Dios (אל = 31)")
    
    # ═════════════════════════════════════════════════════════
    # COMBINACIÓN ERICK + REINALDO
    # ═════════════════════════════════════════════════════════
    
    print(f"\n{'─' * 70}")
    print(f"{'⚡ ERICK + REINALDO = ???':^70}")
    print(f"{'─' * 70}")
    
    erick = "אריק"
    erick_val = gematria_standard(erick)
    combined = erick_val + val
    
    combined_dr = combined
    while combined_dr >= 10:
        combined_dr = sum(int(d) for d in str(combined_dr))
    
    print(f"\n   אריק (Erick) = {erick_val}")
    print(f"   {name} (Reinaldo) = {val}")
    print(f"   ───────────────────────────────")
    print(f"   ERICK + REINALDO = {combined}")
    print(f"   Raíz digital: {combined_dr}")
    print(f"   ¿Primo? {'✅ SÍ' if is_prime(combined) else '❌ No'}")
    print(f"   ÷7: {'✅' if combined % 7 == 0 else '❌'} (mod 7 = {combined % 7})")
    print(f"   ÷26: {'✅ (÷ YHVH!)' if combined % 26 == 0 else '❌'} (mod 26 = {combined % 26})")
    
    # ¿Qué concepto sagrado tiene ese valor o cercano?
    sacred = {
        26: 'YHVH', 86: 'Elohim', 248: 'Abraham', 358: 'Mashiaj',
        345: 'Moisés', 611: 'Torah', 613: 'Mitzvot', 702: 'Shabbat',
        713: 'Shabbtai', 620: 'Keter', 72: 'Jesed', 216: 'Gevurah',
        1081: 'Tiferet', 496: 'Malkut', 376: 'Shalom', 441: 'Emet',
    }
    
    if combined in sacred:
        print(f"   ⭐ ¡{combined} = {sacred[combined]}!")
    
    # Buscar factores sagrados
    for s_val, s_name in sorted(sacred.items()):
        if combined % s_val == 0 and s_val > 1:
            print(f"   🔗 {combined} ÷ {s_val}({s_name}) = {combined // s_val}")
    
    # ¿La diferencia entre Erick y Reinaldo?
    diff = abs(erick_val - val)
    print(f"\n   Diferencia |Erick - Reinaldo| = |{erick_val} - {val}| = {diff}")
    if diff in sacred:
        print(f"   ⭐ ¡Diferencia = {sacred[diff]}!")
    if is_prime(diff):
        print(f"   ✡ {diff} es PRIMO")
    
    # Nombre completo con Flores Zambrano
    print(f"\n{'─' * 70}")
    print(f"{'📛 NOMBRE COMPLETO: ERICK REINALDO FLORES ZAMBRANO':^70}")
    print(f"{'─' * 70}")
    
    parts = {
        'אריק': ('Erick', None),
        name: ('Reinaldo', None),
        'פלורס': ('Flores', None),
        'זמברנו': ('Zambrano', None),
    }
    
    total_full = 0
    print(f"\n   {'Nombre':<15} {'Hebreo':<12} {'Gematría':>8} {'Raíz':>5} {'Primo':>6}")
    print(f"   {'─'*15} {'─'*12} {'─'*8} {'─'*5} {'─'*6}")
    
    for heb, (esp, _) in parts.items():
        v = gematria_standard(heb)
        dr = gematria_katan_mispari(heb)
        pr = "✡" if is_prime(v) else " "
        print(f"   {esp:<15} {heb:<12} {v:>8} {dr:>5} {pr:>6}")
        total_full += v
    
    full_dr = total_full
    while full_dr >= 10:
        full_dr = sum(int(d) for d in str(full_dr))
    
    print(f"   {'─'*15} {'─'*12} {'─'*8} {'─'*5}")
    print(f"   {'TOTAL':<15} {'':12} {total_full:>8} {full_dr:>5}")
    print(f"\n   ÷7: {'✅ SÍ!' if total_full % 7 == 0 else '❌ No'} ({total_full} mod 7 = {total_full % 7})")
    print(f"   ÷26 (YHVH): {'✅ SÍ!' if total_full % 26 == 0 else '❌ No'} ({total_full} mod 26 = {total_full % 26})")
    
    root_meanings = {
        1: 'Keter (Corona) — Liderazgo divino',
        2: 'Jokhmah (Sabiduría) — Intuición pura',
        3: 'Binah (Entendimiento) — Saturno, análisis',
        4: 'Jesed (Bondad) — Generosidad ilimitada',
        5: 'Gevurah (Fuerza) — Disciplina y juicio',
        6: 'Tiferet (Belleza) — Equilibrio y armonía',
        7: 'Netzaj (Victoria) — Perseverancia eterna',
        8: 'Hod (Esplendor) — Humildad y gratitud',
        9: 'Yesod (Fundamento) — Conexión y verdad',
    }
    
    print(f"\n   🌀 Tu Sefirah (raíz digital): {full_dr} = {root_meanings.get(full_dr, '?')}")
    
    return val


# ═══════════════════════════════════════════════════════════════
# 2. VISUALIZACIONES — Gráficos de la Torah
# ═══════════════════════════════════════════════════════════════

def generate_visualizations():
    """
    Genera visualizaciones de datos de la Torah usando matplotlib.
    """
    print(f"\n{'═' * 70}")
    print(f"{'📊 GENERANDO VISUALIZACIONES DE LA TORAH':^70}")
    print(f"{'═' * 70}")
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        print("   ✅ matplotlib disponible")
    except ImportError:
        print("   ❌ matplotlib no instalado. Instalando...")
        os.system(f"{sys.executable} -m pip install matplotlib -q")
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
    
    # Cargar datos
    csv_path = os.path.join(PROC_DIR, "torah_words_gematria.csv")
    all_words = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            row['gematria_standard'] = int(row['gematria_standard'])
            row['chapter'] = int(row['chapter'])
            row['verse'] = int(row['verse'])
            all_words.append(row)
    
    print(f"   📂 {len(all_words):,} palabras cargadas")
    
    # ═══════════════════════════════════════
    # GRÁFICO 1: Distribución de gematría
    # ═══════════════════════════════════════
    
    print(f"\n   📈 Generando gráfico de distribución...")
    
    values = [w['gematria_standard'] for w in all_words]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.patch.set_facecolor('#0a0a1a')
    
    colors = {
        'gold': '#FFD700',
        'blue': '#4488FF',
        'purple': '#9966FF',
        'cyan': '#00DDFF',
        'red': '#FF4444',
        'green': '#44FF88',
        'white': '#FFFFFF',
        'gray': '#666688',
        'bg': '#0a0a1a',
        'bg2': '#12122a',
    }
    
    # 1. Histograma de frecuencias
    ax1 = axes[0, 0]
    ax1.set_facecolor(colors['bg2'])
    ax1.hist(values, bins=100, color=colors['gold'], alpha=0.8, edgecolor=colors['bg2'])
    ax1.set_title('Distribución de Gematría en la Torah', color=colors['white'], fontsize=13, fontweight='bold')
    ax1.set_xlabel('Valor de Gematría', color=colors['gray'])
    ax1.set_ylabel('Frecuencia', color=colors['gray'])
    ax1.tick_params(colors=colors['gray'])
    ax1.spines['bottom'].set_color(colors['gray'])
    ax1.spines['left'].set_color(colors['gray'])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # 2. Distribución MOD 7 (Saturno)
    ax2 = axes[0, 1]
    ax2.set_facecolor(colors['bg2'])
    mod7 = [v % 7 for v in values]
    mod7_counts = Counter(mod7)
    bars = ax2.bar(range(7), [mod7_counts[i] for i in range(7)],
                   color=[colors['gold'] if i == 0 else colors['blue'] for i in range(7)],
                   edgecolor=colors['bg2'], linewidth=1.5)
    ax2.axhline(y=len(values)/7, color=colors['red'], linestyle='--', alpha=0.7, label=f'Esperado: {len(values)/7:.0f}')
    ax2.set_title('Distribución MOD 7 (Saturno) 🪐', color=colors['white'], fontsize=13, fontweight='bold')
    ax2.set_xlabel('Residuo MOD 7', color=colors['gray'])
    ax2.set_ylabel('Frecuencia', color=colors['gray'])
    ax2.tick_params(colors=colors['gray'])
    ax2.legend(facecolor=colors['bg2'], edgecolor=colors['gray'], labelcolor=colors['white'])
    ax2.spines['bottom'].set_color(colors['gray'])
    ax2.spines['left'].set_color(colors['gray'])
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    # 3. Raíz Digital
    ax3 = axes[1, 0]
    ax3.set_facecolor(colors['bg2'])
    roots = [w.get('gematria_digital_root', '0') for w in all_words]
    root_counts = Counter(int(r) for r in roots if r != '0')
    root_colors = [colors['gold'] if r == 7 else colors['purple'] for r in range(1, 10)]
    ax3.bar(range(1, 10), [root_counts.get(i, 0) for i in range(1, 10)],
            color=root_colors, edgecolor=colors['bg2'], linewidth=1.5)
    ax3.set_title('Distribución de Raíces Digitales (1-9)', color=colors['white'], fontsize=13, fontweight='bold')
    ax3.set_xlabel('Raíz Digital', color=colors['gray'])
    ax3.set_ylabel('Frecuencia', color=colors['gray'])
    ax3.set_xticks(range(1, 10))
    ax3.tick_params(colors=colors['gray'])
    ax3.spines['bottom'].set_color(colors['gray'])
    ax3.spines['left'].set_color(colors['gray'])
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    
    # 4. Gematría por libro (boxplot style)
    ax4 = axes[1, 1]
    ax4.set_facecolor(colors['bg2'])
    
    book_names_heb = ['בראשית', 'שמות', 'ויקרא', 'במדבר', 'דברים']
    book_names_eng = ['Génesis', 'Éxodo', 'Levítico', 'Números', 'Deuteronomio']
    book_keys = ['bereshit', 'shemot', 'vayikra', 'bamidbar', 'devarim']
    
    book_means = []
    book_medians = []
    for bk in book_keys:
        bv = [w['gematria_standard'] for w in all_words if w['book_key'] == bk]
        book_means.append(sum(bv) / len(bv) if bv else 0)
        bv_sorted = sorted(bv)
        book_medians.append(bv_sorted[len(bv_sorted)//2] if bv_sorted else 0)
    
    x = range(len(book_keys))
    width = 0.35
    ax4.bar([i - width/2 for i in x], book_means, width, label='Media', color=colors['cyan'], alpha=0.8)
    ax4.bar([i + width/2 for i in x], book_medians, width, label='Mediana', color=colors['purple'], alpha=0.8)
    ax4.set_title('Gematría Promedio por Libro', color=colors['white'], fontsize=13, fontweight='bold')
    ax4.set_xticks(list(x))
    ax4.set_xticklabels(book_names_eng, color=colors['gray'], fontsize=9, rotation=15)
    ax4.tick_params(colors=colors['gray'])
    ax4.legend(facecolor=colors['bg2'], edgecolor=colors['gray'], labelcolor=colors['white'])
    ax4.spines['bottom'].set_color(colors['gray'])
    ax4.spines['left'].set_color(colors['gray'])
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    
    plt.suptitle('🔯 ANÁLISIS DE GEMATRÍA DE LA TORAH — 68,484 Palabras',
                 color=colors['gold'], fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    path1 = os.path.join(VIZ_DIR, "torah_distribucion_gematria.png")
    plt.savefig(path1, dpi=150, facecolor=colors['bg'], bbox_inches='tight')
    plt.close()
    print(f"   💾 Guardado: {path1}")
    
    # ═══════════════════════════════════════
    # GRÁFICO 2: Heatmap del número 7
    # ═══════════════════════════════════════
    
    print(f"\n   🪐 Generando heatmap de Saturno...")
    
    fig, ax = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg2'])
    
    # Para cada libro y cada capítulo, calcular % de palabras divisibles por 7
    heatmap_data = []
    max_chapters = 0
    
    for bk_key, bk_heb, bk_esp in [("bereshit", "בראשית", "Génesis"),
                                      ("shemot", "שמות", "Éxodo"),
                                      ("vayikra", "ויקרא", "Levítico"),
                                      ("bamidbar", "במדבר", "Números"),
                                      ("devarim", "דברים", "Deuteronomio")]:
        book_words = [w for w in all_words if w['book_key'] == bk_key]
        chapters = defaultdict(list)
        for w in book_words:
            chapters[w['chapter']].append(w)
        
        ch_data = {}
        for ch, words in chapters.items():
            div7 = sum(1 for w in words if w['gematria_standard'] % 7 == 0)
            ch_data[ch] = div7 / len(words) * 100
        
        max_chapters = max(max_chapters, max(ch_data.keys()) if ch_data else 0)
        heatmap_data.append((bk_esp, ch_data))
    
    # Dibujar como scatter plot con tamaño = intensidad
    for book_idx, (book_name, ch_data) in enumerate(heatmap_data):
        for ch, pct in ch_data.items():
            intensity = pct / 25  # normalizar
            color = plt.cm.hot(min(intensity, 1.0))
            ax.scatter(ch, book_idx, s=pct * 8, c=[color], alpha=0.8, edgecolors='none')
    
    ax.set_yticks(range(5))
    ax.set_yticklabels([b[0] for b in heatmap_data], color=colors['white'], fontsize=11)
    ax.set_xlabel('Capítulo', color=colors['gray'], fontsize=11)
    ax.set_title('🪐 Concentración del Número 7 por Capítulo (% palabras ÷7)',
                 color=colors['gold'], fontsize=14, fontweight='bold')
    ax.tick_params(colors=colors['gray'])
    ax.spines['bottom'].set_color(colors['gray'])
    ax.spines['left'].set_color(colors['gray'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Línea de referencia esperada
    ax.axvline(x=0, color=colors['gray'], alpha=0.1)
    
    plt.tight_layout()
    path2 = os.path.join(VIZ_DIR, "torah_heatmap_saturno.png")
    plt.savefig(path2, dpi=150, facecolor=colors['bg'], bbox_inches='tight')
    plt.close()
    print(f"   💾 Guardado: {path2}")
    
    # ═══════════════════════════════════════
    # GRÁFICO 3: Top 30 valores más frecuentes
    # ═══════════════════════════════════════
    
    print(f"\n   📊 Generando top valores...")
    
    fig, ax = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg2'])
    
    val_counts = Counter(values).most_common(30)
    vals = [str(v[0]) for v in val_counts]
    counts = [v[1] for v in val_counts]
    bar_colors = [colors['gold'] if v[0] % 7 == 0 else
                  (colors['cyan'] if is_prime(v[0]) else colors['blue'])
                  for v in val_counts]
    
    bars = ax.barh(range(len(vals)), counts, color=bar_colors, edgecolor=colors['bg2'])
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(vals, color=colors['white'], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel('Frecuencia', color=colors['gray'])
    ax.set_title('Top 30 Valores de Gematría Más Frecuentes en la Torah\n🪐 Gold=÷7 | 🔵 Cyan=Primo | 🔷 Azul=Otros',
                 color=colors['gold'], fontsize=13, fontweight='bold')
    ax.tick_params(colors=colors['gray'])
    ax.spines['bottom'].set_color(colors['gray'])
    ax.spines['left'].set_color(colors['gray'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Añadir valores en las barras
    for i, (val, count) in enumerate(val_counts):
        ax.text(count + 10, i, f'{count:,}', color=colors['white'],
                va='center', fontsize=8)
    
    plt.tight_layout()
    path3 = os.path.join(VIZ_DIR, "torah_top30_valores.png")
    plt.savefig(path3, dpi=150, facecolor=colors['bg'], bbox_inches='tight')
    plt.close()
    print(f"   💾 Guardado: {path3}")
    
    # ═══════════════════════════════════════
    # GRÁFICO 4: La "onda" de la Torah
    # ═══════════════════════════════════════
    
    print(f"\n   🌊 Generando la 'onda' de la Torah...")
    
    fig, ax = plt.subplots(figsize=(18, 6))
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg2'])
    
    # Promedio móvil de gematría cada 100 palabras
    window = 200
    moving_avg = []
    for i in range(0, len(values) - window, window // 4):
        chunk = values[i:i + window]
        moving_avg.append(sum(chunk) / len(chunk))
    
    x_positions = list(range(len(moving_avg)))
    ax.fill_between(x_positions, moving_avg, alpha=0.3, color=colors['cyan'])
    ax.plot(x_positions, moving_avg, color=colors['gold'], linewidth=1.2, alpha=0.9)
    
    # Marcar divisiones de libros
    book_boundaries = []
    current = 0
    for bk in book_keys:
        bk_count = sum(1 for w in all_words if w['book_key'] == bk)
        current += bk_count
        book_boundaries.append(current * len(moving_avg) // len(values))
    
    for i, (boundary, bk_name) in enumerate(zip(book_boundaries[:-1], book_names_eng)):
        ax.axvline(x=boundary, color=colors['red'], alpha=0.5, linestyle='--')
        ax.text(boundary, max(moving_avg) * 0.95, f' {bk_name}',
                color=colors['white'], fontsize=8, alpha=0.7, rotation=90, va='top')
    
    # Media global
    global_mean = sum(values) / len(values)
    ax.axhline(y=global_mean, color=colors['gold'], alpha=0.3, linestyle=':')
    
    ax.set_title('🌊 La "Onda" de la Torah — Promedio Móvil de Gematría (ventana=200 palabras)',
                 color=colors['gold'], fontsize=13, fontweight='bold')
    ax.set_xlabel('Posición en la Torah →', color=colors['gray'])
    ax.set_ylabel('Gematría Promedio', color=colors['gray'])
    ax.tick_params(colors=colors['gray'])
    ax.spines['bottom'].set_color(colors['gray'])
    ax.spines['left'].set_color(colors['gray'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    path4 = os.path.join(VIZ_DIR, "torah_onda.png")
    plt.savefig(path4, dpi=150, facecolor=colors['bg'], bbox_inches='tight')
    plt.close()
    print(f"   💾 Guardado: {path4}")
    
    print(f"\n   ✅ 4 visualizaciones generadas en: {VIZ_DIR}")
    return [path1, path2, path3, path4]


# ═══════════════════════════════════════════════════════════════
# 3. TEST ESTADÍSTICO: Chi-Cuadrado
# ═══════════════════════════════════════════════════════════════

def chi_square_test():
    """
    📖 LECCIÓN: El test Chi-cuadrado compara lo que OBSERVAMOS
    contra lo que ESPERARÍAMOS por puro azar. Si el p-value
    es < 0.05, la distribución NO es aleatoria.
    """
    print(f"\n{'═' * 70}")
    print(f"{'🧪 TEST ESTADÍSTICO: ¿LA TORAH ES ALEATORIA?':^70}")
    print(f"{'═' * 70}")
    
    print(f"""
   📖 LECCIÓN: TEST DE CHI-CUADRADO (χ²)
   ─────────────────────────────────────────────────────
   Pregunta: Si la Torah fuera un texto "aleatorio",
   ¿la distribución de MOD 7 sería uniforme?
   
   El test Chi-cuadrado compara:
   - Lo OBSERVADO (frecuencias reales)
   - Lo ESPERADO (si fuera aleatorio: cada residuo = total/7)
   
   Si p-value < 0.05 → NO es aleatorio (hay patrón)
   Si p-value > 0.05 → Compatible con azar
   ─────────────────────────────────────────────────────
    """)
    
    csv_path = os.path.join(PROC_DIR, "torah_words_gematria.csv")
    all_words = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            row['gematria_standard'] = int(row['gematria_standard'])
            all_words.append(row)
    
    values = [w['gematria_standard'] for w in all_words]
    total = len(values)
    
    # Test 1: MOD 7
    print(f"   🧪 Test 1: Distribución MOD 7")
    mod7 = Counter(v % 7 for v in values)
    expected = total / 7
    
    chi2 = sum((mod7[i] - expected) ** 2 / expected for i in range(7))
    # Grados de libertad = 6 (7 categorías - 1)
    # Para df=6, chi2 crítico al 95% = 12.592
    df = 6
    critical = 12.592
    
    print(f"      Observado: {dict(sorted(mod7.items()))}")
    print(f"      Esperado:  {expected:.1f} por cada residuo")
    print(f"      χ² = {chi2:.4f}")
    print(f"      Valor crítico (α=0.05, df=6): {critical}")
    
    if chi2 > critical:
        print(f"      ⚡ χ² > {critical} → RECHAZAMOS hipótesis de aleatoriedad")
        print(f"      🔯 ¡La distribución MOD 7 NO es aleatoria!")
    else:
        print(f"      ○ χ² < {critical} → No podemos rechazar aleatoriedad")
        print(f"      La distribución MOD 7 es compatible con azar (uniforme)")
    
    # Test 2: Raíces digitales
    print(f"\n   🧪 Test 2: Distribución de Raíces Digitales (1-9)")
    roots = Counter()
    for v in values:
        r = v
        while r >= 10:
            r = sum(int(d) for d in str(r))
        roots[r] += 1
    
    expected_root = total / 9
    chi2_root = sum((roots.get(i, 0) - expected_root) ** 2 / expected_root for i in range(1, 10))
    df_root = 8
    critical_root = 15.507
    
    print(f"      Observado: {dict(sorted(roots.items()))}")
    print(f"      Esperado:  {expected_root:.1f} por cada raíz")
    print(f"      χ² = {chi2_root:.4f}")
    print(f"      Valor crítico (α=0.05, df=8): {critical_root}")
    
    if chi2_root > critical_root:
        print(f"      ⚡ χ² > {critical_root} → RECHAZAMOS hipótesis de aleatoriedad")
        print(f"      🔯 ¡La distribución de raíces digitales NO es aleatoria!")
    else:
        print(f"      ○ χ² < {critical_root} → Compatible con azar")
    
    # Test 3: Palabras primas
    print(f"\n   🧪 Test 3: ¿Más palabras primas de lo esperado?")
    primes = sum(1 for v in values if is_prime(v))
    # Según el teorema de los números primos, π(n) ≈ n/ln(n)
    # Para valores hasta ~1800, la densidad de primos es variable
    # Estimación simple: ~15-20% de números hasta 1800 son primos
    import math
    avg_val = sum(values) / len(values)
    prime_density = avg_val / math.log(avg_val) / avg_val  # π(n)/n ≈ 1/ln(n)
    expected_primes = total * prime_density
    
    print(f"      Primos observados: {primes} ({primes/total*100:.2f}%)")
    print(f"      Densidad esperada: ~{prime_density*100:.2f}% (para media={avg_val:.0f})")
    print(f"      Primos esperados:  ~{expected_primes:.0f}")
    
    ratio = primes / expected_primes if expected_primes > 0 else 0
    print(f"      Ratio obs/esp: {ratio:.3f}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("🔯 REINALDO DESCIFRADO + VISUALIZACIONES + ESTADÍSTICAS")
    print("   'Las letras de tu nombre son las llaves de tu alma.' — Zohar")
    print("=" * 70)
    
    start = time.time()
    
    # 1. Análisis de Reinaldo
    analyze_reinaldo()
    
    # 2. Visualizaciones
    generate_visualizations()
    
    # 3. Tests estadísticos
    chi_square_test()
    
    elapsed = time.time() - start
    print(f"\n{'═' * 70}")
    print(f"✅ COMPLETADO EN {elapsed:.1f} SEGUNDOS")
    print(f"{'═' * 70}")


if __name__ == "__main__":
    main()
