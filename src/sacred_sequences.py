"""
🔯 SECUENCIAS SAGRADAS EN LA TORAH — Fibonacci, Triangulares, Perfectos
═══════════════════════════════════════════════════════════════════════
"Dios creó el mundo con números, letras y relatos." — Sefer Yetzirah 1:1

Este script busca las huellas de secuencias matemáticas sagradas
dentro de la Torah: ¿Aparecen los números de Fibonacci más de lo
esperado? ¿Los números triangulares? ¿Los perfectos?

Si la Torah es un texto "normal", estas secuencias aparecerían
por azar. Si hay un patrón, hay una firma.

Autor: Erick Reinaldo Flores Zambrano
═══════════════════════════════════════════════════════════════════════
"""

import sys, os, csv, json, time, math
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from gematria_engine import gematria_standard, is_prime, extract_hebrew_letters

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PROC_DIR = os.path.join(PROJECT_DIR, "data", "processed")
VIZ_DIR = os.path.join(PROJECT_DIR, "visualizations")
REPORT_DIR = os.path.join(PROJECT_DIR, "reports")
os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# GENERADORES DE SECUENCIAS SAGRADAS
# ═══════════════════════════════════════════════════════════════

def fibonacci_set(max_val):
    """Genera números de Fibonacci hasta max_val."""
    fibs = set()
    a, b = 1, 1
    while a <= max_val:
        fibs.add(a)
        a, b = b, a + b
    return fibs

def triangular_set(max_val):
    """Números triangulares: 1, 3, 6, 10, 15, 21, 28..."""
    tri = set()
    n = 1
    while True:
        t = n * (n + 1) // 2
        if t > max_val:
            break
        tri.add(t)
        n += 1
    return tri

def perfect_set(max_val):
    """Números perfectos: 6, 28, 496..."""
    perfects = set()
    for n in [6, 28, 496, 8128]:
        if n <= max_val:
            perfects.add(n)
    return perfects

def square_set(max_val):
    """Cuadrados perfectos: 1, 4, 9, 16, 25..."""
    squares = set()
    n = 1
    while n * n <= max_val:
        squares.add(n * n)
        n += 1
    return squares

def star_of_david_set(max_val):
    """Números estrella de David: 1, 13, 37, 73, 181, 337, 541..."""
    # Fórmula: 6n(n-1) + 1
    stars = set()
    n = 1
    while True:
        s = 6 * n * (n - 1) + 1
        if s > max_val:
            break
        stars.add(s)
        n += 1
    return stars


def load_torah_words():
    """Carga todas las palabras de la Torah procesadas."""
    csv_path = os.path.join(PROC_DIR, "torah_words_gematria.csv")
    words = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            row['gematria_standard'] = int(row['gematria_standard'])
            row['chapter'] = int(row['chapter'])
            row['verse'] = int(row['verse'])
            words.append(row)
    return words


def analyze_sacred_sequences():
    """Análisis principal de secuencias sagradas."""
    
    print(f"\n{'═' * 70}")
    print(f"{'🔯 SECUENCIAS SAGRADAS EN LA TORAH':^70}")
    print(f"{'═' * 70}")
    
    words = load_torah_words()
    values = [w['gematria_standard'] for w in words]
    max_val = max(values)
    total = len(values)
    
    print(f"   📂 {total:,} palabras cargadas (max valor: {max_val})")
    
    # Generar todas las secuencias
    fibs = fibonacci_set(max_val)
    tris = triangular_set(max_val)
    perfs = perfect_set(max_val)
    squares = square_set(max_val)
    stars = star_of_david_set(max_val)
    primes = set(v for v in set(values) if is_prime(v))
    
    sequences = {
        'Fibonacci': fibs,
        'Triangulares': tris,
        'Perfectos': perfs,
        'Cuadrados': squares,
        'Estrella David': stars,
        'Primos': primes,
        'Divisibles ÷7': set(v for v in set(values) if v % 7 == 0),
        'Divisibles ÷26': set(v for v in set(values) if v % 26 == 0),
    }
    
    print(f"""
   📖 LECCIÓN: SECUENCIAS SAGRADAS
   ─────────────────────────────────────────────────────
   Si la Torah fuera un texto cualquiera, los números de
   Fibonacci, triangulares, etc. aparecerían con una
   frecuencia predecible (proporcional a cuántos hay
   en el rango de valores posibles).
   
   Si aparecen MÁS de lo esperado → hay un patrón.
   Si aparecen MENOS → también es significativo.
   
   Vamos a medir esto con rigor estadístico.
   ─────────────────────────────────────────────────────
    """)
    
    # ═════════════════════════════════════════
    # 1. Frecuencia de cada tipo
    # ═════════════════════════════════════════
    
    unique_vals = set(values)
    total_unique = len(unique_vals)
    
    print(f"   {'Secuencia':<18} {'En rango':>8} {'Únicas':>8} {'Palabras':>10} {'% Palabras':>10} {'Esperado%':>10} {'Ratio':>8}")
    print(f"   {'─'*18} {'─'*8} {'─'*8} {'─'*10} {'─'*10} {'─'*10} {'─'*8}")
    
    results = {}
    
    for name, seq in sequences.items():
        # Cuántos de la secuencia están en el rango
        in_range = seq & set(range(1, max_val + 1))
        # Cuántos valores únicos de la Torah están en la secuencia
        hits_unique = unique_vals & seq
        # Cuántas palabras tienen un valor de la secuencia
        hits_count = sum(1 for v in values if v in seq)
        # Porcentaje
        pct = hits_count / total * 100
        # Esperado (si fuera aleatorio: proporción de números en rango que son de la secuencia)
        expected_pct = len(in_range) / max_val * 100 if max_val > 0 else 0
        ratio = pct / expected_pct if expected_pct > 0 else 0
        
        marker = ""
        if ratio > 1.2:
            marker = " ⬆️"
        elif ratio < 0.8:
            marker = " ⬇️"
        
        print(f"   {name:<18} {len(in_range):>8} {len(hits_unique):>8} {hits_count:>10,} {pct:>9.2f}% {expected_pct:>9.2f}% {ratio:>7.3f}{marker}")
        
        results[name] = {
            'in_range': len(in_range),
            'unique_hits': len(hits_unique),
            'word_count': hits_count,
            'percentage': pct,
            'expected_pct': expected_pct,
            'ratio': ratio,
        }
    
    # ═════════════════════════════════════════
    # 2. Fibonacci profundo
    # ═════════════════════════════════════════
    
    print(f"\n{'─' * 70}")
    print(f"{'🌀 FIBONACCI EN LA TORAH':^70}")
    print(f"{'─' * 70}")
    
    print(f"""
   📖 LECCIÓN: LA SECUENCIA DE FIBONACCI
   ─────────────────────────────────────────────────────
   1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987...
   
   Cada número es la suma de los dos anteriores.
   
   Esta secuencia aparece en:
   • Las espirales de los girasoles
   • La proporción áurea (1.618...)
   • Las galaxias espirales
   • La estructura del ADN
   
   ¿Aparece también en la Torah?
   ─────────────────────────────────────────────────────
    """)
    
    fib_list = sorted(fibs)
    print(f"   Números Fibonacci hasta {max_val}: {len(fib_list)}")
    print(f"   {', '.join(str(f) for f in fib_list)}\n")
    
    fib_words = [(w, w['gematria_standard']) for w in words if w['gematria_standard'] in fibs]
    fib_counter = Counter(w[1] for w in fib_words)
    
    print(f"   Total de palabras Fibonacci en la Torah: {len(fib_words):,}")
    print(f"\n   Distribución por valor Fibonacci:")
    for fval, count in sorted(fib_counter.items()):
        bar = '█' * min(count // 5, 50)
        print(f"      {fval:>5}: {count:>5} {bar}")
    
    # Fibonacci 13 = Ahavá (Amor) y Ejad (Uno)
    print(f"\n   🔮 HALLAZGO: Fibonacci y los conceptos sagrados:")
    fib_sacred = {
        1: ('א', 'Alef — la primera letra, la unidad'),
        2: ('ב', 'Bet — la primera letra de la Torah (Bereshit)'),
        3: ('ג', 'Guímel — dar, camello'),
        5: ('ה', 'He — ventana al cielo, aliento de Dios'),
        8: ('ח', 'Jet — vida (חי = 18 = חח)'),
        13: ('אהבה/אחד', 'Amor/Uno — los dos = 13 = Fibonacci!'),
        21: ('אהיה', 'Ehyeh — "Yo Soy" (nombre de Dios en Éxodo 3:14)'),
        34: ('לד', 'Nacimiento — dar a luz'),
        89: ('גולגלתא', 'Cerca del valor de Elohim (86)'),
        144: ('קדם', 'Qedem — Oriente/Antigüedad = 144!'),
        233: ('עץ החיים', 'Cerca de "Árbol" (עץ=160) + "vida"'),
        377: ('שבעה', 'No exacto pero 377 ≈ שלום(376)+1'),
        610: ('ות', 'Cercano a Torah (611) — ¡A 1 de distancia!'),
        987: ('שלחן', 'Mesa — 987 = Fibonacci 16°'),
    }
    
    for fval, (heb, meaning) in fib_sacred.items():
        if fval in fibs:
            count = fib_counter.get(fval, 0)
            print(f"      {fval:>5} = {heb} → {meaning} (aparece {count:,}× en la Torah)")
    
    # ¡610 está a 1 de Torah (611)!
    print(f"\n   ⚡ DESCUBRIMIENTO:")
    print(f"      Fibonacci(15) = 610")
    print(f"      Torah (תורה) = 611")
    print(f"      ¡Diferencia = 1!")
    print(f"      610 + 1(א/Alef/Dios) = 611 = Torah")
    print(f"      → Torah = Fibonacci + Dios")
    
    # ═════════════════════════════════════════
    # 3. Proporción Áurea (Phi) en la Torah
    # ═════════════════════════════════════════
    
    print(f"\n{'─' * 70}")
    print(f"{'φ LA PROPORCIÓN ÁUREA (1.618...) EN LA TORAH':^70}")
    print(f"{'─' * 70}")
    
    PHI = (1 + math.sqrt(5)) / 2  # 1.6180339887...
    
    # ¿Dónde cae el punto áureo de la Torah?
    total_words = len(words)
    golden_point = int(total_words / PHI)
    golden_word = words[golden_point]
    
    print(f"\n   Total de palabras en la Torah: {total_words:,}")
    print(f"   Punto áureo (total ÷ φ): palabra #{golden_point:,}")
    print(f"   📍 La palabra en el punto áureo es:")
    print(f"      {golden_word['word']} = {golden_word['gematria_standard']}")
    print(f"      Ubicación: {golden_word['book_spanish']} {golden_word['chapter']}:{golden_word['verse']}")
    
    # ¿Hay pares consecutivos cuya razón se acerca a Phi?
    phi_pairs = []
    for i in range(len(values) - 1):
        if values[i] > 0 and values[i+1] > 0:
            ratio = max(values[i], values[i+1]) / min(values[i], values[i+1])
            if abs(ratio - PHI) < 0.01:
                phi_pairs.append((i, values[i], values[i+1], ratio))
    
    print(f"\n   Pares consecutivos con razón ≈ φ (±0.01): {len(phi_pairs):,}")
    # Esperado por azar: ~1/100 de pares
    expected_phi = total_words / 100  # rough estimate
    print(f"   Esperado por azar: ~{expected_phi:.0f}")
    ratio_phi = len(phi_pairs) / expected_phi if expected_phi > 0 else 0
    print(f"   Ratio observado/esperado: {ratio_phi:.3f}")
    
    if len(phi_pairs) > 0:
        print(f"\n   Primeros 5 pares φ:")
        for p in phi_pairs[:5]:
            w1 = words[p[0]]
            w2 = words[p[0]+1]
            print(f"      {w1['word']}({p[1]}) · {w2['word']}({p[2]}) → razón = {p[3]:.6f}")
    
    # ═════════════════════════════════════════
    # 4. Números Estrella de David
    # ═════════════════════════════════════════
    
    print(f"\n{'─' * 70}")
    print(f"{'✡ NÚMEROS ESTRELLA DE DAVID EN LA TORAH':^70}")
    print(f"{'─' * 70}")
    
    star_list = sorted(stars)
    print(f"""
   📖 LECCIÓN: NÚMEROS ESTRELLA DE DAVID
   ─────────────────────────────────────────────────────
   Un número estrella tiene la forma 6n(n-1) + 1:
   1, 13, 37, 73, 181, 337, 541, 817, 1177...
   
   Estos números forman hexagramas perfectos
   (la Estrella de David) cuando se representan
   como puntos. Son especialmente sagrados porque
   combinan el 6 (creación) con la unidad (+1).
   
   13 = אהבה (Amor) = Estrella de David #2
   37 = הבל (Abel) = Estrella de David #3
   73 = חכמה (Sabiduría) = Estrella de David #4 !!
   ─────────────────────────────────────────────────────
    """)
    
    star_words = [(w, w['gematria_standard']) for w in words if w['gematria_standard'] in stars]
    star_counter = Counter(w[1] for w in star_words)
    
    print(f"   Total de palabras con valor 'Estrella': {len(star_words):,}")
    for sval, count in sorted(star_counter.items()):
        bar = '█' * min(count // 3, 40)
        print(f"      {sval:>5}: {count:>5} {bar}")
    
    # 37 y 73 son inversos y ambos son Estrella de David Y primos
    print(f"\n   🔮 MISTERIO 37-73:")
    print(f"      37 = Estrella de David #3, PRIMO")
    print(f"      73 = Estrella de David #4, PRIMO")
    print(f"      37 × 73 = {37*73}")
    print(f"      37 es 73 al revés y viceversa")
    print(f"      חכמה (Jokhmah/Sabiduría) = 73")
    print(f"      הבל (Hevel/Abel) = 37")
    print(f"      37 + 73 = {37+73} = {gematria_standard('יד')} (Yad/Mano? No.)")
    print(f"      37 + 73 = 110 = יוסף (Yosef/José) lifespan = 110 años!")
    
    # ═════════════════════════════════════════
    # 5. GRAFO: Encontrar redes de conexión
    # ═════════════════════════════════════════
    
    print(f"\n{'─' * 70}")
    print(f"{'🕸️ RED DE CONEXIONES ENTRE LOS 72 NOMBRES':^70}")
    print(f"{'─' * 70}")
    
    # Cargar los 72 nombres
    names_72 = [
        "והו","ילי","סיט","עלמ","מהש","ללה","אכא","כהת",
        "הזי","אלד","לאו","ההע","יזל","מבה","הרי","הקם",
        "לאו","כלי","לוו","פהל","נלך","ייי","מלה","חהו",
        "נתה","האא","ירת","שאה","ריי","אום","לכב","ושר",
        "יחו","להח","כוק","מנד","אני","חעם","רהע","ייז",
        "ההה","מיכ","וול","ילה","סאל","ערי","עשל","מיה",
        "והו","דני","החש","עמם","ננא","נית","מבה","פוי",
        "נמם","ייל","הרח","מצר","ומב","יהה","ענו","מחי",
        "דמב","מנק","איע","חבו","ראה","יבמ","היי","מום",
    ]
    
    # Construir relaciones: nombres que comparten letras, suman valores sagrados, etc.
    edges = []
    sacred_targets = {26, 72, 86, 7, 13, 182, 248, 358, 345, 376}
    
    for i in range(len(names_72)):
        for j in range(i + 1, len(names_72)):
            vi = gematria_standard(names_72[i])
            vj = gematria_standard(names_72[j])
            sum_ij = vi + vj
            
            # Conexión por valor sagrado
            if sum_ij in sacred_targets:
                edges.append((i, j, f"suma={sum_ij}", 'sacred'))
            
            # Misma gematría
            if vi == vj:
                edges.append((i, j, f"gemelos={vi}", 'twin'))
            
            # Comparten 2+ letras
            li = set(extract_hebrew_letters(names_72[i]))
            lj = set(extract_hebrew_letters(names_72[j]))
            shared = li & lj
            if len(shared) >= 2:
                edges.append((i, j, f"letras={''.join(shared)}", 'letters'))
    
    print(f"\n   Total de conexiones encontradas: {len(edges)}")
    print(f"   Tipos:")
    type_counts = Counter(e[3] for e in edges)
    for t, c in type_counts.items():
        labels = {'sacred': 'Suma sagrada', 'twin': 'Gemelos (= gematría)', 'letters': 'Letras compartidas'}
        print(f"      {labels.get(t, t)}: {c}")
    
    # Nombres más conectados
    conn_count = Counter()
    for e in edges:
        conn_count[e[0]] += 1
        conn_count[e[1]] += 1
    
    print(f"\n   📊 Top 10 nombres más conectados:")
    for idx, count in conn_count.most_common(10):
        n = names_72[idx]
        v = gematria_standard(n)
        print(f"      #{idx+1:>2} {n} = {v:>4} → {count} conexiones")
    
    # Generar grafo como datos JSON para la webapp
    graph_data = {
        'nodes': [
            {'id': i, 'name': names_72[i], 'value': gematria_standard(names_72[i]),
             'connections': conn_count[i]}
            for i in range(72)
        ],
        'edges': [
            {'source': e[0], 'target': e[1], 'label': e[2], 'type': e[3]}
            for e in edges
        ],
    }
    
    graph_path = os.path.join(PROJECT_DIR, "data", "reference", "72_names_graph.json")
    with open(graph_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    print(f"\n   💾 Grafo guardado: {graph_path}")
    
    # ═════════════════════════════════════════
    # 6. Generación de gráficos
    # ═════════════════════════════════════════
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        generate_sequence_charts(values, fibs, tris, stars, words)
    except ImportError:
        os.system(f"{sys.executable} -m pip install matplotlib -q")
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        generate_sequence_charts(values, fibs, tris, stars, words)
    
    return results


def generate_sequence_charts(values, fibs, tris, stars, words):
    """Genera gráficos de secuencias sagradas."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    colors = {
        'gold':'#FFD700','blue':'#4488FF','purple':'#9966FF','cyan':'#00DDFF',
        'red':'#FF4444','green':'#44FF88','white':'#FFFFFF','gray':'#666688',
        'bg':'#0a0a1a','bg2':'#12122a','orange':'#FF9800',
    }
    
    # ═════════════════════════════════════════
    # Gráfico: Fibonacci en la Torah
    # ═════════════════════════════════════════
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor(colors['bg'])
    
    # 1. Fibonacci histogram
    ax = axes[0]
    ax.set_facecolor(colors['bg2'])
    fib_vals = sorted(fibs)
    fib_counts = []
    fib_labels = []
    for f in fib_vals:
        if f <= 1000:
            count = values.count(f)
            if count > 0:
                fib_counts.append(count)
                fib_labels.append(str(f))
    
    bar_colors = [colors['gold'] if is_prime(int(l)) else colors['cyan'] for l in fib_labels]
    ax.barh(range(len(fib_labels)), fib_counts, color=bar_colors, edgecolor=colors['bg2'])
    ax.set_yticks(range(len(fib_labels)))
    ax.set_yticklabels(fib_labels, color=colors['white'], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel('Frecuencia en la Torah', color=colors['gray'])
    ax.set_title('Fibonacci en la Torah\nGold=Primo | Cyan=Compuesto', color=colors['gold'], fontsize=12, fontweight='bold')
    ax.tick_params(colors=colors['gray'])
    for s in ['top','right']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(colors['gray'])
    ax.spines['left'].set_color(colors['gray'])
    
    for i, c in enumerate(fib_counts):
        ax.text(c + 5, i, str(c), color=colors['white'], va='center', fontsize=8)
    
    # 2. Estrella de David
    ax2 = axes[1]
    ax2.set_facecolor(colors['bg2'])
    star_vals = sorted(stars)
    star_counts = []
    star_labels = []
    for s in star_vals:
        if s <= 1500:
            count = values.count(s)
            if count > 0:
                star_counts.append(count)
                star_labels.append(str(s))
    
    ax2.barh(range(len(star_labels)), star_counts, color=colors['purple'], edgecolor=colors['bg2'])
    ax2.set_yticks(range(len(star_labels)))
    ax2.set_yticklabels(star_labels, color=colors['white'], fontsize=9)
    ax2.invert_yaxis()
    ax2.set_xlabel('Frecuencia en la Torah', color=colors['gray'])
    ax2.set_title('Numeros Estrella de David en la Torah', color=colors['purple'], fontsize=12, fontweight='bold')
    ax2.tick_params(colors=colors['gray'])
    for s in ['top','right']: ax2.spines[s].set_visible(False)
    ax2.spines['bottom'].set_color(colors['gray'])
    ax2.spines['left'].set_color(colors['gray'])
    
    for i, c in enumerate(star_counts):
        ax2.text(c + 5, i, str(c), color=colors['white'], va='center', fontsize=8)
    
    plt.suptitle('Secuencias Sagradas en la Torah', color=colors['gold'], fontsize=15, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    path = os.path.join(VIZ_DIR, "torah_secuencias_sagradas.png")
    plt.savefig(path, dpi=150, facecolor=colors['bg'], bbox_inches='tight')
    plt.close()
    print(f"\n   💾 Gráfico: {path}")
    
    # ════════════════════════════════════════
    # Gráfico: La espiral de la Torah
    # ════════════════════════════════════════
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg'])
    
    # Cada uno de los 72 nombres como un punto en espiral
    names_72 = [
        "והו","ילי","סיט","עלמ","מהש","ללה","אכא","כהת",
        "הזי","אלד","לאו","ההע","יזל","מבה","הרי","הקם",
        "לאו","כלי","לוו","פהל","נלך","ייי","מלה","חהו",
        "נתה","האא","ירת","שאה","ריי","אום","לכב","ושר",
        "יחו","להח","כוק","מנד","אני","חעם","רהע","ייז",
        "ההה","מיכ","וול","ילה","סאל","ערי","עשל","מיה",
        "והו","דני","החש","עמם","ננא","נית","מבה","פוי",
        "נמם","ייל","הרח","מצר","ומב","יהה","ענו","מחי",
        "דמב","מנק","איע","חבו","ראה","יבמ","היי","מום",
    ]
    
    import numpy as np
    theta = np.linspace(0, 4 * np.pi, 72)  # 2 vueltas
    r = np.linspace(0.5, 2.5, 72)
    
    gem_vals = [gematria_standard(n) for n in names_72]
    sizes = [max(v * 0.5, 15) for v in gem_vals]
    
    # Color por raíz digital
    dr_vals = []
    for v in gem_vals:
        d = v
        while d >= 10:
            d = sum(int(c) for c in str(d))
        dr_vals.append(d)
    
    scatter = ax.scatter(theta, r, c=dr_vals, s=sizes, cmap='plasma',
                        alpha=0.8, edgecolors='white', linewidths=0.5)
    
    ax.set_title('Los 72 Nombres en Espiral\n(color = raiz digital, tamano = gematria)',
                color=colors['gold'], fontsize=13, fontweight='bold', pad=20)
    ax.tick_params(colors=colors['gray'])
    ax.grid(True, alpha=0.1, color=colors['gray'])
    ax.set_rgrids([0.5, 1, 1.5, 2, 2.5], labels=['', '', '', '', ''], angle=0)
    
    # Label some key names
    for i in [0, 25, 41, 71]:  # #1, #26, #42, #72
        ax.annotate(f"#{i+1} {names_72[i]}",
                    xy=(theta[i], r[i]),
                    xytext=(theta[i] + 0.3, r[i] + 0.3),
                    color=colors['gold'], fontsize=9,
                    fontfamily='sans-serif',
                    arrowprops=dict(arrowstyle='->', color=colors['gold'], lw=0.8))
    
    path2 = os.path.join(VIZ_DIR, "torah_72_espiral.png")
    plt.savefig(path2, dpi=150, facecolor=colors['bg'], bbox_inches='tight')
    plt.close()
    print(f"   💾 Espiral: {path2}")


def main():
    print("=" * 70)
    print("🔯 SECUENCIAS SAGRADAS + FIBONACCI + GRAFOS")
    print('   "La geometría es el lenguaje de Dios." — Galileo')
    print("=" * 70)
    
    start = time.time()
    analyze_sacred_sequences()
    elapsed = time.time() - start
    
    print(f"\n{'═' * 70}")
    print(f"✅ COMPLETADO EN {elapsed:.1f} SEGUNDOS")
    print(f"{'═' * 70}")


if __name__ == "__main__":
    main()
