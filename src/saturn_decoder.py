"""
🪐 SATURN DECODER — Decodificador de Saturno / Shabbtai
═══════════════════════════════════════════════════════════════════════
"Y Dios descansó el séptimo día" — Génesis 2:2

Saturno (שבתאי / Shabbtai) = El planeta del Shabbat.
En la tradición kabbalística, Saturno gobierna el tiempo, la estructura,
y el código oculto de la creación.

Este script busca el "código madre" de la Torah a través del 7:
1. Análisis fractal — ¿El patrón del 7 se repite en todas las escalas?
2. Extracción de la 7ª letra, 7ª palabra, 7º versículo...
3. Mapa de calor de la distribución MOD 7
4. El "ritmo de Saturno" — cada 7 letras, ¿qué emerge?
5. Análisis multi-escala: letra → palabra → versículo → capítulo → libro

Autor: Erick Reinaldo Flores Zambrano
Proyecto: 08_gematria_torah | El Código Madre
═══════════════════════════════════════════════════════════════════════
"""

import json
import os
import sys
import numpy as np
from collections import Counter, defaultdict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gematria_engine import STANDARD, extract_hebrew_letters, strip_nikkud, gematria_standard, extract_words

# ═══════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════

def digital_root(n):
    if n == 0: return 0
    return 1 + (n - 1) % 9

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True


def load_torah(raw_dir):
    """Carga los 5 libros y retorna letras, palabras, versículos estructurados."""
    books = ['bereshit', 'shemot', 'vayikra', 'bamidbar', 'devarim']
    names = ['Génesis', 'Éxodo', 'Levítico', 'Números', 'Deuteronomio']
    names_heb = ['בראשית', 'שמות', 'ויקרא', 'במדבר', 'דברים']
    
    torah = {
        'letters': [],       # Todas las letras (valores)
        'words': [],         # Todas las palabras (valores gematría)
        'word_texts': [],    # Textos de las palabras
        'verses': [],        # Sumas de versículos
        'chapters': [],      # Sumas de capítulos
        'books': [],         # Sumas de libros
        'structure': [],     # Metadatos por versículo
    }
    
    for book_file, book_name, book_heb in zip(books, names, names_heb):
        filepath = os.path.join(raw_dir, f"{book_file}.json")
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        book_sum = 0
        book_letters = 0
        
        chapters = data.get('chapters', {})
        for ch_num in sorted(chapters.keys(), key=int):
            ch = chapters[ch_num]
            verses = ch.get('verses_consonantal', ch.get('verses_with_nikkud', []))
            chapter_sum = 0
            
            for v_idx, verse in enumerate(verses):
                letters = extract_hebrew_letters(verse)
                words = extract_words(verse)
                
                verse_letter_vals = [STANDARD.get(l, 0) for l in letters if STANDARD.get(l, 0) > 0]
                verse_word_vals = [gematria_standard(w) for w in words]
                verse_sum = sum(verse_letter_vals)
                
                torah['letters'].extend(verse_letter_vals)
                torah['words'].extend(verse_word_vals)
                torah['word_texts'].extend(words)
                torah['verses'].append(verse_sum)
                torah['structure'].append({
                    'book': book_name,
                    'book_heb': book_heb,
                    'chapter': int(ch_num),
                    'verse': v_idx + 1,
                    'sum': verse_sum,
                    'words': len(words),
                    'letters': len(verse_letter_vals),
                })
                
                chapter_sum += verse_sum
                book_sum += verse_sum
                book_letters += len(verse_letter_vals)
            
            torah['chapters'].append(chapter_sum)
        
        torah['books'].append({'name': book_name, 'hebrew': book_heb, 'sum': book_sum, 'letters': book_letters})
        print(f"  📜 {book_name} ({book_heb}): {book_letters:,} letras, suma={book_sum:,}")
    
    print(f"\n  ✅ Total: {len(torah['letters']):,} letras, {len(torah['words']):,} palabras, {len(torah['verses']):,} versículos")
    return torah


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS 1: FRACTAL DEL 7 — ¿El patrón se repite en todas las escalas?
# ═══════════════════════════════════════════════════════════════

def fractal_analysis(torah):
    """
    Analiza la distribución MOD 7 en CADA escala:
    - Letras individuales MOD 7
    - Palabras MOD 7
    - Versículos MOD 7
    - Capítulos MOD 7
    - Libros MOD 7
    
    Si el 7 es el "código madre", el mismo patrón emerge en TODAS las escalas.
    """
    print("\n" + "=" * 70)
    print("🪐 ANÁLISIS FRACTAL DEL 7 — ¿Se repite en todas las escalas?")
    print("=" * 70)
    
    scales = [
        ('Letras', torah['letters']),
        ('Palabras', torah['words']),
        ('Versículos', torah['verses']),
        ('Capítulos', torah['chapters']),
    ]
    
    results = {}
    
    for scale_name, values in scales:
        arr = np.array(values)
        mod7 = arr % 7
        counts = Counter(mod7)
        total = len(mod7)
        expected = total / 7
        
        # Chi-cuadrado
        chi2 = sum((counts.get(i, 0) - expected)**2 / expected for i in range(7))
        
        # Porcentaje de divisibles por 7
        div7_pct = counts.get(0, 0) / total * 100
        expected_pct = 100 / 7  # ~14.29%
        
        # Raíz digital distribution
        dr_counts = Counter(digital_root(int(v)) for v in values if v > 0)
        
        print(f"\n  📊 {scale_name} (N={total:,}):")
        print(f"     MOD 7:  {' '.join(f'{i}:{counts.get(i,0):,}' for i in range(7))}")
        print(f"     Div÷7:  {counts.get(0,0):,} ({div7_pct:.2f}%) — esperado: {expected_pct:.2f}%")
        print(f"     Ratio:  {div7_pct/expected_pct:.3f}x")
        print(f"     χ²:     {chi2:.2f} {'✅ Significativo' if chi2 > 12.59 else '─ No significativo'}")
        
        # Test de consistencia: ¿el residuo 0 es siempre el más frecuente?
        max_residue = max(range(7), key=lambda i: counts.get(i, 0))
        print(f"     Residuo más frecuente: MOD 7 = {max_residue}")
        
        results[scale_name] = {
            'total': total,
            'div7_pct': div7_pct,
            'ratio': div7_pct / expected_pct,
            'chi2': chi2,
            'max_residue': max_residue,
            'distribution': {i: counts.get(i, 0) for i in range(7)}
        }
    
    # FRACTALIDAD: ¿El patrón es consistente?
    print(f"\n  🔯 TEST DE FRACTALIDAD:")
    ratios = [results[s]['ratio'] for s in results]
    all_above = all(r > 1.0 for r in ratios)
    print(f"     Ratios divisibilidad por 7: {', '.join(f'{r:.3f}' for r in ratios)}")
    if all_above:
        print(f"     ✅ EL 7 DOMINA EN TODAS LAS ESCALAS — Patrón fractal confirmado")
    else:
        print(f"     ⚠️  El patrón no es uniforme en todas las escalas")
    
    return results


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS 2: CADA 7ª — Extracción del "Ritmo de Saturno"
# ═══════════════════════════════════════════════════════════════

def saturn_rhythm(torah):
    """
    Extrae cada 7ª letra, cada 7ª palabra, cada 7º versículo.
    ¿Qué mensaje emerge del "ritmo de Saturno"?
    """
    print("\n" + "=" * 70)
    print("🪐 RITMO DE SATURNO — Cada 7ª posición")
    print("=" * 70)
    
    # Cada 7ª letra
    seventh_letters_vals = torah['letters'][6::7]  # Índice 6, 13, 20...
    seventh_sum = sum(seventh_letters_vals)
    
    # Cada 7ª palabra  
    seventh_words = torah['word_texts'][6::7]
    seventh_words_vals = torah['words'][6::7]
    seventh_words_sum = sum(seventh_words_vals)
    
    # Cada 7º versículo
    seventh_verses = [torah['structure'][i] for i in range(6, len(torah['structure']), 7)]
    seventh_verses_sum = sum(v['sum'] for v in seventh_verses)
    
    print(f"\n  📊 Cada 7ª LETRA:")
    print(f"     Total: {len(seventh_letters_vals):,} letras")
    print(f"     Suma: {seventh_sum:,}")
    print(f"     Raíz digital: {digital_root(seventh_sum)}")
    print(f"     MOD 7: {seventh_sum % 7}")
    print(f"     MOD 26: {seventh_sum % 26}")
    print(f"     ¿Divisible por 7? {'✅ SI' if seventh_sum % 7 == 0 else '❌ No'}")
    
    print(f"\n  📊 Cada 7ª PALABRA:")
    print(f"     Total: {len(seventh_words):,} palabras")
    print(f"     Suma: {seventh_words_sum:,}")
    print(f"     Raíz digital: {digital_root(seventh_words_sum)}")
    print(f"     MOD 7: {seventh_words_sum % 7}")
    print(f"     ¿Divisible por 7? {'✅ SI' if seventh_words_sum % 7 == 0 else '❌ No'}")
    
    # Las primeras 7 palabras de la Torah
    first_7_words = torah['word_texts'][:7]
    first_7_vals = torah['words'][:7]
    first_7_sum = sum(first_7_vals)
    
    print(f"\n  📜 LAS PRIMERAS 7 PALABRAS (Génesis 1:1):")
    for i, (w, v) in enumerate(zip(first_7_words, first_7_vals)):
        print(f"     {i+1}. {w} = {v} (raíz: {digital_root(v)}, MOD7: {v%7})")
    print(f"     SUMA: {first_7_sum}")
    print(f"     Raíz digital: {digital_root(first_7_sum)}")
    print(f"     MOD 7: {first_7_sum % 7}")
    print(f"     ¿Divisible por 7? {'✅ SI' if first_7_sum % 7 == 0 else '❌ No'}")
    print(f"     ¿Primo? {'✅ SI' if is_prime(first_7_sum) else '❌ No'}")
    print(f"     Factorización: ", end="")
    n = first_7_sum
    factors = []
    for p in range(2, int(n**0.5) + 1):
        while n % p == 0:
            factors.append(p)
            n //= p
    if n > 1:
        factors.append(n)
    print(" × ".join(str(f) for f in factors))
    
    # Top 10 palabras más frecuentes en posición 7ª
    word_freq = Counter(seventh_words)
    print(f"\n  📊 Palabras más frecuentes en posición 7ª:")
    for word, count in word_freq.most_common(10):
        val = gematria_standard(word)
        print(f"     {word:>8} = {val:>4} × {count} veces (raíz: {digital_root(val)})")
    
    return {
        'seventh_letters_sum': seventh_sum,
        'seventh_words_sum': seventh_words_sum,
        'first_7_sum': first_7_sum,
    }


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS 3: MAPA DE CALOR — Distribución espacial del 7
# ═══════════════════════════════════════════════════════════════

def saturn_heatmap(torah):
    """
    ¿Dónde se concentran los múltiplos de 7 en la Torah?
    ¿Hay zonas "cargadas" de energía de Saturno?
    """
    print("\n" + "=" * 70)
    print("🪐 MAPA DE SATURNO — ¿Dónde se concentra el 7?")
    print("=" * 70)
    
    # Dividir la Torah en 72 bloques (porque 72 Nombres)
    N = len(torah['words'])
    block_size = N // 72
    
    blocks = []
    for i in range(72):
        start = i * block_size
        end = start + block_size if i < 71 else N
        block_words = torah['words'][start:end]
        
        div7_count = sum(1 for w in block_words if w % 7 == 0)
        div7_pct = div7_count / len(block_words) * 100
        block_sum = sum(block_words)
        
        blocks.append({
            'block': i + 1,
            'div7_pct': div7_pct,
            'sum': block_sum,
            'sum_mod7': block_sum % 7,
            'div7_count': div7_count,
            'total_words': len(block_words),
        })
    
    # Los 5 bloques con más concentración de 7
    blocks_sorted = sorted(blocks, key=lambda b: b['div7_pct'], reverse=True)
    
    print(f"\n  📊 Torah dividida en 72 bloques ({block_size} palabras/bloque):")
    print(f"\n  🔝 Top 5 bloques con mayor concentración de '7':")
    for b in blocks_sorted[:5]:
        print(f"     Bloque #{b['block']:>2}: {b['div7_pct']:.1f}% div÷7 ({b['div7_count']}/{b['total_words']}), suma={b['sum']:,} MOD7={b['sum_mod7']}")
    
    print(f"\n  🔻 5 bloques con menor concentración:")
    for b in blocks_sorted[-5:]:
        print(f"     Bloque #{b['block']:>2}: {b['div7_pct']:.1f}% div÷7 ({b['div7_count']}/{b['total_words']})")
    
    # ¿Cuántos bloques tienen suma divisible por 7?
    div7_blocks = sum(1 for b in blocks if b['sum_mod7'] == 0)
    print(f"\n  🔯 Bloques con suma divisible por 7: {div7_blocks}/72 ({div7_blocks/72*100:.1f}%)")
    print(f"     Esperado por azar: {72/7:.1f} = {1/7*100:.1f}%")
    print(f"     Ratio: {(div7_blocks/72)/(1/7):.2f}x")
    
    return blocks


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS 4: EL CÓDIGO MADRE — Búsqueda del patrón generador
# ═══════════════════════════════════════════════════════════════

def mother_code(torah):
    """
    Si la Torah es un programa, ¿cuál es su instrucción fundamental?
    
    Buscamos el patrón que se repite con mayor frecuencia y que
    conecta el 7 con la estructura global del texto.
    
    Hipótesis: El "código madre" es una secuencia de N valores
    que al repetirse genera la distribución observada.
    """
    print("\n" + "=" * 70)
    print("🧬 EL CÓDIGO MADRE — Buscando el algoritmo de la Creación")
    print("=" * 70)
    
    letters = np.array(torah['letters'])
    words = np.array(torah['words'])
    N = len(letters)
    
    # 1. La "firma" de cada libro (media, std, MOD7 dominante)
    print(f"\n  📊 FIRMA NUMÉRICA DE CADA LIBRO:")
    print(f"     {'Libro':>15} {'Media':>8} {'Std':>8} {'MOD7':>5} {'Div÷7%':>7} {'Raíz':>5} {'Primo?':>7}")
    print(f"     {'─'*15} {'─'*8} {'─'*8} {'─'*5} {'─'*7} {'─'*5} {'─'*7}")
    
    idx = 0
    for book in torah['books']:
        book_letters = letters[idx:idx + book['letters']]
        mean = np.mean(book_letters)
        std = np.std(book_letters)
        s = book['sum']
        mod7 = s % 7
        div7 = np.sum(book_letters % 7 == 0) / len(book_letters) * 100
        dr = digital_root(s)
        prime = is_prime(s)
        
        print(f"     {book['name']:>15} {mean:>8.2f} {std:>8.2f} {mod7:>5} {div7:>7.2f} {dr:>5} {'✅' if prime else '❌':>7}")
        idx += book['letters']
    
    # 2. Buscar secuencias recurrentes de raíces digitales
    print(f"\n  🔢 PATRONES DE RAÍZ DIGITAL:")
    dr_sequence = [digital_root(int(v)) for v in torah['words'] if v > 0]
    
    # Buscar patrones de longitud 7
    patterns_7 = Counter()
    for i in range(len(dr_sequence) - 6):
        pattern = tuple(dr_sequence[i:i+7])
        patterns_7[pattern] += 1
    
    print(f"     Patrones de 7 raíces digitales más frecuentes:")
    for pattern, count in patterns_7.most_common(7):
        s = sum(pattern)
        print(f"     {pattern} × {count} veces (suma={s}, MOD7={s%7}, raíz={digital_root(s)})")
    
    # 3. La gran pregunta: ¿La suma parcial cada N palabras es siempre divisible por 7?
    print(f"\n  🔯 TEST DEL CÓDIGO MADRE:")
    print(f"     ¿Existe un N tal que la suma de cada N palabras consecutivas es siempre ÷7?")
    
    best_n = 0
    best_pct = 0
    
    for test_n in [7, 14, 22, 26, 42, 49, 72, 77, 91]:
        blocks = [sum(words[i:i+test_n]) for i in range(0, len(words) - test_n, test_n)]
        div7 = sum(1 for b in blocks if b % 7 == 0)
        pct = div7 / len(blocks) * 100 if blocks else 0
        expected = 100 / 7
        ratio = pct / expected
        sig = "✅" if ratio > 1.5 else ("⚠️" if ratio > 1.2 else "─")
        print(f"     N={test_n:>3}: {div7}/{len(blocks)} bloques div÷7 = {pct:.1f}% (ratio={ratio:.2f}x) {sig}")
        
        if pct > best_pct:
            best_pct = pct
            best_n = test_n
    
    print(f"\n     Mejor N: {best_n} ({best_pct:.1f}%)")
    
    # 4. La "frecuencia de Saturno" — ratio exacto
    total_sum = sum(torah['letters'])
    print(f"\n  🪐 CONSTANTES DE SATURNO:")
    print(f"     Suma total: {total_sum:,}")
    print(f"     Total / 7: {total_sum / 7:,.4f}")
    print(f"     Total / 49: {total_sum / 49:,.4f}")
    print(f"     Total / 7²: {total_sum / 49:,.4f}")
    print(f"     Total MOD 7: {total_sum % 7}")
    print(f"     Total MOD 49: {total_sum % 49}")
    print(f"     Total / 26 (YHVH): {total_sum / 26:,.4f}")
    print(f"     Total / 72 (Nombres): {total_sum / 72:,.4f}")
    
    # ¿La suma es divisible por 7 Y por 26?
    if total_sum % 7 == 0 and total_sum % 26 == 0:
        print(f"     ✅ ¡La suma total es divisible por 7 Y por 26 (YHVH)!")
        print(f"     {total_sum} = 7 × {total_sum // 7}")
        print(f"     {total_sum} = 26 × {total_sum // 26}")
    elif total_sum % 7 == 0:
        print(f"     ✅ ¡La suma total es divisible por 7 (Saturno/Shabbat)!")
        print(f"     {total_sum} = 7 × {total_sum // 7}")
    
    # 5. Entropía — ¿Cuánta información contiene?
    letter_freq = Counter(torah['letters'])
    total_letters = len(torah['letters'])
    probs = np.array([count / total_letters for count in letter_freq.values()])
    entropy = -np.sum(probs * np.log2(probs))
    max_entropy = np.log2(len(letter_freq))  # Si fuera uniforme
    
    print(f"\n  📊 ENTROPÍA DE LA SEÑAL:")
    print(f"     Entropía: {entropy:.4f} bits/letra")
    print(f"     Máxima posible: {max_entropy:.4f} bits/letra")
    print(f"     Eficiencia: {entropy/max_entropy*100:.1f}%")
    print(f"     Redundancia: {(1 - entropy/max_entropy)*100:.1f}%")
    print(f"     → La Torah usa {(1 - entropy/max_entropy)*100:.1f}% MENOS información que un texto aleatorio")
    print(f"     → Esa redundancia ES la estructura oculta")
    
    return {
        'total_sum': total_sum,
        'entropy': entropy,
        'max_entropy': max_entropy,
        'redundancy': 1 - entropy / max_entropy,
    }


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS 5: ELS — Equidistant Letter Sequences (inicio)
# ═══════════════════════════════════════════════════════════════

def els_search(torah, target_word, max_skip=100):
    """
    Busca una palabra como secuencia equidistante de letras (ELS).
    Por cada skip N, busca si las letras target_word aparecen cada N posiciones.
    """
    print(f"\n  🔍 ELS: Buscando '{target_word}' en secuencias equidistantes...")
    
    # Construir mapa de letras: valor -> posiciones
    letter_sequence = []
    for book_file in ['bereshit', 'shemot', 'vayikra', 'bamidbar', 'devarim']:
        filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'raw', f"{book_file}.json")
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        chapters = data.get('chapters', {})
        for ch_num in sorted(chapters.keys(), key=int):
            ch = chapters[ch_num]
            verses = ch.get('verses_consonantal', ch.get('verses_with_nikkud', []))
            for verse in verses:
                letters = extract_hebrew_letters(verse)
                letter_sequence.extend(letters)
    
    target_letters = list(target_word)
    N = len(letter_sequence)
    found = []
    
    for skip in range(1, min(max_skip + 1, N // len(target_letters))):
        for start in range(min(skip * 10, N - skip * len(target_letters))):
            match = True
            for j, target_l in enumerate(target_letters):
                pos = start + j * skip
                if pos >= N or letter_sequence[pos] != target_l:
                    match = False
                    break
            if match:
                found.append({'start': start, 'skip': skip})
    
    if found:
        print(f"     ✅ Encontrado {len(found)} veces:")
        for f in found[:10]:
            print(f"        Inicio={f['start']}, Skip={f['skip']} (cada {f['skip']} letras)")
    else:
        print(f"     ─ No encontrado con skip 1-{max_skip}")
    
    return found


# ═══════════════════════════════════════════════════════════════
# VISUALIZACIÓN
# ═══════════════════════════════════════════════════════════════

def visualize_saturn(torah, output_dir):
    """Genera visualizaciones del análisis de Saturno."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("  ⚠️  matplotlib no disponible")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), facecolor='#0a0a1a')
    
    # 1. Distribución MOD 7 de palabras
    ax = axes[0, 0]
    ax.set_facecolor('#0a0a1a')
    mod7_counts = Counter(w % 7 for w in torah['words'])
    vals = [mod7_counts.get(i, 0) for i in range(7)]
    colors = ['#00E5FF' if i == 0 else '#FFD700' for i in range(7)]
    bars = ax.bar(range(7), vals, color=colors, alpha=0.8, edgecolor='#333')
    ax.axhline(len(torah['words'])/7, color='#FF4444', linestyle='--', alpha=0.5, label='Esperado')
    ax.set_title('Distribución MOD 7 de Palabras', color='#FFD700', fontsize=12, fontweight='bold')
    ax.set_xlabel('Residuo MOD 7', color='#888')
    ax.set_ylabel('Cantidad', color='#888')
    ax.tick_params(colors='#666')
    ax.legend(facecolor='#0a0a1a', edgecolor='#333', labelcolor='#aaa')
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 50, f'{v:,}', ha='center', va='bottom', color='#ddd', fontsize=8)
    
    # 2. Raíz digital de versículos
    ax = axes[0, 1]
    ax.set_facecolor('#0a0a1a')
    dr_counts = Counter(digital_root(v) for v in torah['verses'] if v > 0)
    vals = [dr_counts.get(i, 0) for i in range(1, 10)]
    colors2 = ['#00E5FF' if i == 7 else '#BB86FC' for i in range(1, 10)]
    ax.bar(range(1, 10), vals, color=colors2, alpha=0.8, edgecolor='#333')
    ax.set_title('Raíz Digital de Versículos', color='#BB86FC', fontsize=12, fontweight='bold')
    ax.set_xlabel('Raíz Digital', color='#888')
    ax.set_ylabel('Cantidad', color='#888')
    ax.tick_params(colors='#666')
    
    # 3. Media móvil de la señal con zonas div÷7
    ax = axes[1, 0]
    ax.set_facecolor('#0a0a1a')
    window = 500
    words = np.array(torah['words'][:5000])
    moving_avg = np.convolve(words, np.ones(window)/window, mode='valid')
    ax.plot(moving_avg, color='#FFD700', alpha=0.7, linewidth=0.8)
    # Marcar versículos divisibles por 7
    div7_positions = [i for i in range(len(words)) if words[i] % 7 == 0]
    ax.scatter(div7_positions, [words[i] for i in div7_positions], c='#00E5FF', s=1, alpha=0.3)
    ax.set_title('Primeras 5000 Palabras (azul = div÷7)', color='#00E5FF', fontsize=12, fontweight='bold')
    ax.set_xlabel('Posición', color='#888')
    ax.set_ylabel('Gematría', color='#888')
    ax.tick_params(colors='#666')
    
    # 4. Entropía por libro
    ax = axes[1, 1]
    ax.set_facecolor('#0a0a1a')
    book_names = [b['name'][:3] for b in torah['books']]
    book_sums = [b['sum'] for b in torah['books']]
    book_mod7 = [b['sum'] % 7 for b in torah['books']]
    colors3 = ['#00E5FF' if m == 0 else '#FFD700' for m in book_mod7]
    ax.barh(book_names, book_sums, color=colors3, alpha=0.8, edgecolor='#333')
    for i, (s, m) in enumerate(zip(book_sums, book_mod7)):
        ax.text(s + 5000, i, f'{s:,} (MOD7={m})', color='#ddd', fontsize=9, va='center')
    ax.set_title('Suma Total por Libro (cian = div÷7)', color='#FFD700', fontsize=12, fontweight='bold')
    ax.tick_params(colors='#666')
    
    plt.tight_layout()
    path = os.path.join(output_dir, 'saturn_decoder.png')
    plt.savefig(path, dpi=150, facecolor='#0a0a1a', bbox_inches='tight')
    plt.close()
    print(f"\n  📊 Guardado: {path}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("🪐 SATURN DECODER — El Código Madre de la Torah")
    print("   'Y Dios descansó el séptimo día'")
    print("=" * 70)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    viz_dir = os.path.join(base_dir, 'visualizations')
    
    # Cargar Torah
    print("\n📜 Cargando los 5 libros de la Torah...")
    torah = load_torah(raw_dir)
    
    # Análisis 1: Fractal
    fractal = fractal_analysis(torah)
    
    # Análisis 2: Ritmo de Saturno
    rhythm = saturn_rhythm(torah)
    
    # Análisis 3: Mapa de Saturno
    heatmap = saturn_heatmap(torah)
    
    # Análisis 4: Código Madre
    mother = mother_code(torah)
    
    # Análisis 5: ELS básico
    print("\n" + "=" * 70)
    print("🔍 ELS — Equidistant Letter Sequences")
    print("=" * 70)
    els_search(torah, "תורה", max_skip=50)   # "Torah"
    els_search(torah, "שבת", max_skip=50)     # "Shabbat"
    els_search(torah, "אלהים", max_skip=30)   # "Elohim"
    
    # Visualización
    print("\n🎨 Generando visualizaciones...")
    visualize_saturn(torah, viz_dir)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("🪐 RESUMEN: EL CÓDIGO DE SATURNO")
    print("=" * 70)
    print(f"\n  Suma total de la Torah: {mother['total_sum']:,}")
    print(f"  Divisible por 7: {'✅ SI' if mother['total_sum'] % 7 == 0 else '❌ No'}")
    print(f"  Entropía: {mother['entropy']:.4f} bits (redundancia: {mother['redundancy']*100:.1f}%)")
    print(f"  → {mother['redundancy']*100:.1f}% de la Torah es ESTRUCTURA, no ruido")
    print(f"\n  El 7 domina en:")
    for scale, data in fractal.items():
        if data['ratio'] > 1.0:
            print(f"     ✅ {scale}: {data['ratio']:.3f}x más divisibilidad que azar")
    
    print(f"\n  Primeras 7 palabras (Génesis 1:1): suma = {rhythm['first_7_sum']}")
    
    print("\n✅ Saturn Decoder completo.")
