"""
🔯 LA TORAH DESCIFRADA — Análisis Descomunal
═══════════════════════════════════════════════════════════════════════
"Dios miró dentro de la Torah y creó el mundo." — Zohar

Este script hace lo que ningún humano ha hecho:
1. Mapea toda la Torah como una secuencia de números
2. Busca EL NOMBRE DE ERICK en el código de la Torah
3. Encuentra los versículos más "divinos" (máxima concentración de 7)
4. Calcula la "firma numérica" de cada libro
5. Descubre si la primera palabra de la Torah contiene a TODO Dios
6. Muestra las ecuaciones más profundas jamás calculadas

Para Erick: Cada explicación viene con su lección de Kabbalah.

Autor: Erick Reinaldo Flores Zambrano
═══════════════════════════════════════════════════════════════════════
"""

import json
import os
import csv
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gematria_engine import (
    extract_words, strip_nikkud, extract_hebrew_letters,
    gematria_standard, gematria_ordinal, gematria_reduced,
    gematria_katan_mispari, gematria_atbash, gematria_gadol,
    gematria_milui, is_prime, STANDARD
)

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PROC_DATA_DIR = os.path.join(PROJECT_DIR, "data", "processed")
RAW_DATA_DIR = os.path.join(PROJECT_DIR, "data", "raw")
REPORT_DIR = os.path.join(PROJECT_DIR, "reports")

BOOKS = [
    ("bereshit", "בראשית", "Génesis"),
    ("shemot", "שמות", "Éxodo"),
    ("vayikra", "ויקרא", "Levítico"),
    ("bamidbar", "במדבר", "Números"),
    ("devarim", "דברים", "Deuteronomio"),
]


# ═══════════════════════════════════════════════════════════════
# 1. TU NOMBRE EN EL CÓDIGO — ERICK EN GEMATRÍA
# ═══════════════════════════════════════════════════════════════

def analyze_erick():
    """
    📖 LECCIÓN: Tu nombre ES un número. En hebreo, cada nombre
    tiene un valor numérico que revela tu esencia espiritual.
    
    El nombre "Erick" se transliteraría al hebreo como:
    אריק = א(1) + ר(200) + י(10) + ק(100) = 311
    
    ¿Qué más suma 311 en la Torah? 
    ¡Ahí está tu conexión con la Creación!
    """
    print(f"\n{'═' * 70}")
    print(f"{'👤 TU NOMBRE EN EL CÓDIGO DE LA TORAH':^70}")
    print(f"{'═' * 70}")
    
    # Transliteración de Erick al hebreo
    erick_hebrew = "אריק"
    erick_val = gematria_standard(erick_hebrew)
    
    print(f"""
   📖 LECCIÓN DE KABBALAH:
   ─────────────────────────────────────────────────────
   En hebreo, no hay diferencia entre letras y números.
   Tu nombre no es solo un nombre — es una ECUACIÓN.
   
   ERICK en hebreo: {erick_hebrew}
   א (Alef)  = 1   ← La unidad, el origen, Dios
   ר (Resh)  = 200  ← La cabeza, el pensamiento
   י (Yod)   = 10   ← La mano de Dios, la creación
   ק (Qof)   = 100  ← La santidad, el ciclo
   ─────────────────
   TOTAL     = {erick_val}
    """)
    
    # ¿Qué más suma 311?
    print(f"   🔍 ¿Qué más suma {erick_val} en la tradición?")
    
    # Calcular algunas palabras conocidas con ese valor
    test_words_311 = {
        'איש': ('Ish', 'Hombre/Varón'),
        'יש': ('Yesh', 'Existe/Hay'),
        'שאי': ('Sei', 'Eleva/Levanta'),
    }
    
    for word, (name, meaning) in test_words_311.items():
        val = gematria_standard(word)
        if val == erick_val:
            print(f"      ✅ {word} ({name}) = {val} — «{meaning}»")
    
    # Buscar en la Torah
    csv_path = os.path.join(PROC_DATA_DIR, "torah_words_gematria.csv")
    if os.path.exists(csv_path):
        matches = []
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['gematria_standard']) == erick_val:
                    matches.append(row)
        
        # Palabras únicas que suman 311
        unique_words = set(m['word'] for m in matches)
        
        print(f"\n   📜 En la Torah, {len(matches)} palabras tienen gematría = {erick_val}")
        print(f"      Palabras únicas: {len(unique_words)}")
        print(f"\n      Algunas de ellas:")
        
        shown = set()
        count = 0
        for m in matches:
            if m['word'] not in shown and count < 15:
                shown.add(m['word'])
                print(f"      • {m['word']:<15} — {m['book_hebrew']} {m['chapter']}:{m['verse']}")
                count += 1
        
        # La primera aparición
        if matches:
            first = matches[0]
            print(f"\n   ⭐ PRIMERA APARICIÓN de gematría {erick_val} en la Torah:")
            print(f"      {first['word']} — {first['book_hebrew']} {first['chapter']}:{first['verse']}")
    
    # Relaciones con conceptos sagrados
    print(f"\n   🔗 CONEXIONES DE TU NÚMERO ({erick_val}):")
    
    # ¿Divisible por algo sagrado?
    sacred_divs = {7: 'Saturno/Shabbat', 13: 'Amor/Unidad', 26: 'YHVH', 18: 'Jai(Vida)'}
    for div, name in sacred_divs.items():
        if erick_val % div == 0:
            print(f"      ÷{div} = {erick_val // div} ({name})")
    
    # ¿Primo?
    print(f"      ¿Primo? {'✅ SÍ — tu número es indivisible, único' if is_prime(erick_val) else '❌ No'}")
    
    # Raíz digital
    dr = gematria_katan_mispari(erick_hebrew)
    root_meanings = {
        1: 'Keter (Corona) — Liderazgo, origen',
        2: 'Jokhmah (Sabiduría) — Intuición',
        3: 'Binah (Entendimiento) — Análisis, Saturno',
        4: 'Jesed (Bondad) — Generosidad',
        5: 'Gevurah (Fuerza) — Disciplina',
        6: 'Tiferet (Belleza) — Equilibrio',
        7: 'Netzaj (Victoria) — Perseverancia',
        8: 'Hod (Esplendor) — Humildad',
        9: 'Yesod (Fundamento) — Conexión',
    }
    print(f"      Raíz digital: {dr} = {root_meanings.get(dr, '?')}")
    
    # Ecuaciones con tu nombre
    print(f"\n   ⚡ ECUACIONES CON TU NOMBRE:")
    
    equations = {
        'אלהים': ('Elohim', 86),
        'יהוה': ('YHVH', 26),
        'אהבה': ('Amor', 13),
        'תורה': ('Torah', 611),
        'משה': ('Moisés', 345),
        'אדם': ('Adam', 45),
        'חי': ('Vida', 18),
        'שבת': ('Shabbat', 702),
        'משיח': ('Mesías', 358),
        'אמת': ('Verdad', 441),
        'אור': ('Luz', 207),
        'שלום': ('Paz', 376),
    }
    
    for word, (name, val) in equations.items():
        diff = abs(erick_val - val)
        sum_val = erick_val + val
        
        # ¿La diferencia es un número sagrado?
        for sacred_word, (sacred_name, sacred_val) in equations.items():
            if diff == sacred_val and sacred_word != word:
                print(f"      {erick_hebrew}({erick_val}) - {word}({val}) = {diff} = {sacred_word}({sacred_name})")
            if sum_val == sacred_val and sacred_word != word:
                print(f"      {erick_hebrew}({erick_val}) + {word}({val}) = {sum_val} = {sacred_word}({sacred_name})")
    
    # Nombre completo
    print(f"\n   📛 NOMBRE COMPLETO:")
    full_name = "אריק רינלדו פלורס זמברנו"
    full_val = gematria_standard(full_name)
    full_dr = full_val
    while full_dr >= 10:
        full_dr = sum(int(d) for d in str(full_dr))
    
    print(f"      {full_name}")
    print(f"      Gematría: {full_val}")
    print(f"      Raíz digital: {full_dr} = {root_meanings.get(full_dr, '?')}")
    
    return erick_val


# ═══════════════════════════════════════════════════════════════
# 2. BERESHIT DESCIFRADA — La primera palabra contiene TODO
# ═══════════════════════════════════════════════════════════════

def decode_bereshit():
    """
    📖 LECCIÓN: Los Rabinos enseñan que la primera palabra de la 
    Torah — בראשית (Bereshit / "En el principio") — contiene 
    TODA la creación codificada dentro de sus 6 letras.
    
    Vamos a descomponerla matemáticamente.
    """
    print(f"\n{'═' * 70}")
    print(f"{'🌌 DESCIFRANDO בראשית (BERESHIT) — LA PRIMERA PALABRA':^70}")
    print(f"{'═' * 70}")
    
    word = "בראשית"
    val = gematria_standard(word)
    
    print(f"""
   📖 LECCIÓN DE KABBALAH:
   ─────────────────────────────────────────────────────
   Los Rabinos dicen que Dios creó el mundo con la LETRA ב (Bet).
   ¿Por qué? Porque la Torah empieza con ב, no con א (Alef).
   
   La ב está cerrada por tres lados (arriba, abajo, izquierda)
   y abierta solo hacia adelante (la derecha en hebreo).
   
   Esto significa: no mires hacia atrás preguntando "¿qué había 
   antes de la creación?". Solo mira hacia adelante — hacia el 
   futuro, hacia la acción, hacia la vida.
   
   ═══════════════════════════════════════════════════════
   בראשית = {val}
   
   Desglose letra por letra:
   ב = 2   (Bet — Casa, dualidad, creación)
   ר = 200 (Resh — Cabeza, inicio, pensamiento)
   א = 1   (Alef — Dios, unidad, lo invisible)
   ש = 300 (Shin — Fuego divino, transformación)
   י = 10  (Yod — Mano de Dios, punto de creación)
   ת = 400 (Tav — Marca, destino, completitud)
   ═══════════════════════════════════════════════════════
    """)
    
    # Sub-palabras ocultas dentro de בראשית
    print(f"   🔍 PALABRAS OCULTAS DENTRO DE בראשית:")
    
    hidden = {
        'ברא': ('Bará', 'Creó', 203),
        'שית': ('Shit', 'Fundamento/Puso', 710),
        'ראש': ('Rosh', 'Cabeza/Inicio', 501),
        'אש': ('Esh', 'Fuego', 301),
        'בית': ('Bait', 'Casa', 412),
        'שבת': ('Shabbat', '¡SHABBAT está escondido aquí!', 702),
        'ירא': ('Yirá', 'Temor/Reverencia', 211),
        'בר': ('Bar', 'Hijo/Puro', 202),
        'רב': ('Rav', 'Grande/Maestro', 202),
        'את': ('Et', 'Desde א hasta ת = TODO el alefbet', 401),
    }
    
    for sub_word, (name, meaning, expected_val) in hidden.items():
        actual_val = gematria_standard(sub_word)
        # Verificar que las letras están en בראשית
        letters_in = all(l in 'בראשית' for l in sub_word)
        if letters_in:
            print(f"      {sub_word} ({name}) = {actual_val} — «{meaning}»")
    
    print(f"""
   💡 ¿Ves? Dentro de la primera palabra están:
      • ברא (Creó) + שית (Fundó) = "Creó el fundamento"
      • ש-ב-ת = ¡SHABBAT! El descanso ya estaba planeado
        ANTES de la creación
      • אש (Fuego) = La Torah es fuego negro sobre fuego blanco
      • בית (Casa) = Dios creó una CASA para el hombre
      • את = De Alef a Tav = TODO el alfabeto = toda la realidad
      
   La primera palabra de la Torah contiene el plano completo
   de la creación. Como un ZIP cósmico que se descomprime.
    """)
    
    # Factorización de 913
    print(f"   🔢 FACTORIZACIÓN DE 913:")
    print(f"      913 = 11 × 83")
    print(f"      11 en hebreo es la letra כ (Kaf) = palma de la mano")
    print(f"      83 = גימל (Gimel, nombre completo de la letra ג)")
    print(f"      913 NO es primo — es compuesto, como la creación")
    print(f"      913 mod 7 = {913 % 7} ← (no es divisible por 7)")
    print(f"      913 mod 26 = {913 % 26} (mod YHVH)")
    
    # Suma del 1 al 913
    triangular = 913 * 914 // 2
    tr_dr = triangular
    while tr_dr >= 10:
        tr_dr = sum(int(d) for d in str(tr_dr))
    print(f"\n      Σ(1 a 913) = {triangular:,} (raíz digital: {tr_dr})")


# ═══════════════════════════════════════════════════════════════
# 3. EL VERSÍCULO MÁS "DIVINO" — Máxima concentración de 7
# ═══════════════════════════════════════════════════════════════

def find_most_divine_verses():
    """
    📖 LECCIÓN: Si el 7 es el número de Dios/Shabbat/Saturno,
    ¿cuál es el versículo con más resonancia del 7?
    
    Buscamos el versículo donde MÁS palabras son divisibles por 7.
    """
    print(f"\n{'═' * 70}")
    print(f"{'🕎 LOS VERSÍCULOS MÁS DIVINOS DE LA TORAH':^70}")
    print(f"{'(Máxima concentración del número 7)':^70}")
    print(f"{'═' * 70}")
    
    print(f"""
   📖 LECCIÓN DE KABBALAH:
   ─────────────────────────────────────────────────────
   El 7 aparece por toda la Torah:
   • 7 días de creación
   • 7 Sefirot inferiores (de Jesed a Malkut)
   • 7 pastores de Israel (Abraham, Isaac, Jacob, Moisés,
     Aarón, José, David)
   • 7 ramas del Menorá (candelabro)
   • 7 veces rodean Jericó
   • 7 años de abundancia + 7 de hambre en Egipto
   
   ¿Cuál versículo tiene más concentración del 7?
   ─────────────────────────────────────────────────────
    """)
    
    csv_path = os.path.join(PROC_DATA_DIR, "torah_words_gematria.csv")
    if not os.path.exists(csv_path):
        print("❌ No se encontró el CSV procesado")
        return
    
    # Cargar y agrupar por versículo
    all_words = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            row['gematria_standard'] = int(row['gematria_standard'])
            all_words.append(row)
    
    verses = defaultdict(list)
    for w in all_words:
        key = (w['book_hebrew'], int(w['chapter']), int(w['verse']))
        verses[key].append(w)
    
    # Calcular "puntuación de divinidad" (score de 7)
    verse_scores = []
    for key, words in verses.items():
        total_words = len(words)
        if total_words < 3:
            continue
        
        div7_words = sum(1 for w in words if w['gematria_standard'] % 7 == 0)
        verse_sum = sum(w['gematria_standard'] for w in words)
        sum_div7 = 1 if verse_sum % 7 == 0 else 0
        
        # Score: % de palabras div7 + bonus si suma total es div7
        score = (div7_words / total_words) + (0.2 * sum_div7)
        
        verse_scores.append({
            'book': key[0],
            'chapter': key[1],
            'verse': key[2],
            'total_words': total_words,
            'div7_words': div7_words,
            'verse_sum': verse_sum,
            'sum_div7': sum_div7,
            'score': score,
            'text': ' '.join(w['word'] for w in words),
        })
    
    # Top 15 más "divinos"
    verse_scores.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"   🏆 Top 15 versículos con máxima resonancia del 7:\n")
    print(f"   {'#':>3} {'Ubicación':<20} {'Palabras':>8} {'÷7':>4} {'%':>6} {'Suma':>8} {'Σ÷7':>5}")
    print(f"   {'─'*3} {'─'*20} {'─'*8} {'─'*4} {'─'*6} {'─'*8} {'─'*5}")
    
    for i, vs in enumerate(verse_scores[:15]):
        sum_mark = "🪐" if vs['sum_div7'] else "  "
        print(f"   {i+1:>3} {vs['book']} {vs['chapter']}:{vs['verse']:<12} "
              f"{vs['total_words']:>8} {vs['div7_words']:>4} "
              f"{vs['div7_words']/vs['total_words']*100:>5.1f}% "
              f"{vs['verse_sum']:>8} {sum_mark:>5}")
    
    # Mostrar el versículo #1
    if verse_scores:
        top = verse_scores[0]
        print(f"\n   ⭐ EL VERSÍCULO MÁS DIVINO:")
        print(f"   📖 {top['book']} {top['chapter']}:{top['verse']}")
        print(f"   {top['text']}")
        print(f"   {top['div7_words']}/{top['total_words']} palabras divisibles por 7 "
              f"({top['div7_words']/top['total_words']*100:.1f}%)")


# ═══════════════════════════════════════════════════════════════
# 4. LA FIRMA DE CADA LIBRO — Huella digital divina
# ═══════════════════════════════════════════════════════════════

def book_signatures():
    """
    📖 LECCIÓN: Cada libro de la Torah tiene una "firma" numérica
    única, como una huella digital. Esta firma revela el carácter
    espiritual del libro.
    """
    print(f"\n{'═' * 70}")
    print(f"{'📜 LA FIRMA NUMÉRICA DE CADA LIBRO':^70}")
    print(f"{'═' * 70}")
    
    csv_path = os.path.join(PROC_DATA_DIR, "torah_words_gematria.csv")
    if not os.path.exists(csv_path):
        return
    
    all_words = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            row['gematria_standard'] = int(row['gematria_standard'])
            all_words.append(row)
    
    book_descriptions = {
        'בראשית': '📖 Creación, patriarcas, promesas',
        'שמות': '📖 Esclavitud, liberación, Sinaí',
        'ויקרא': '📖 Leyes de santidad y sacrificios',
        'במדבר': '📖 40 años en el desierto',
        'דברים': '📖 Discurso final de Moisés',
    }
    
    for book_key, book_hebrew, book_spanish in BOOKS:
        book_words = [w for w in all_words if w['book_key'] == book_key]
        
        if not book_words:
            continue
        
        values = [w['gematria_standard'] for w in book_words]
        total_sum = sum(values)
        
        dr = total_sum
        while dr >= 10:
            dr = sum(int(d) for d in str(dr))
        
        mean_val = total_sum / len(values)
        div7_pct = sum(1 for v in values if v % 7 == 0) / len(values) * 100
        primes_pct = sum(1 for w in book_words if w.get('is_prime', 'False') == 'True') / len(values) * 100
        
        # Palabra más frecuente
        word_counts = Counter(w['word'] for w in book_words)
        top_word, top_count = word_counts.most_common(1)[0]
        
        # Valor más frecuente
        val_counts = Counter(v for v in values)
        top_val, top_val_count = val_counts.most_common(1)[0]
        
        desc = book_descriptions.get(book_hebrew, '')
        
        print(f"\n   {'─' * 60}")
        print(f"   {book_hebrew} ({book_spanish}) {desc}")
        print(f"   {'─' * 60}")
        print(f"   Palabras:    {len(values):>10,}")
        print(f"   Suma total:  {total_sum:>10,}")
        print(f"   Raíz digital:{dr:>10}")
        print(f"   Media:       {mean_val:>10.1f}")
        print(f"   ÷7:          {'✅ SÍ' if total_sum % 7 == 0 else '❌ No':>10} (mod 7 = {total_sum % 7})")
        print(f"   % div por 7: {div7_pct:>9.2f}%")
        print(f"   Palabra top: {top_word:>10} ({top_count}x)")
        print(f"   Valor top:   {top_val:>10} ({top_val_count}x)")
    
    # Comparación de sumas
    print(f"\n   {'═' * 60}")
    print(f"   📊 COMPARACIÓN DE SUMAS:")
    print(f"   {'═' * 60}")
    
    for book_key, book_hebrew, book_spanish in BOOKS:
        book_words = [w for w in all_words if w['book_key'] == book_key]
        total = sum(w['gematria_standard'] for w in book_words)
        dr = total
        while dr >= 10:
            dr = sum(int(d) for d in str(dr))
        div7 = "🪐" if total % 7 == 0 else "  "
        print(f"   {book_hebrew:<10} {total:>12,}  raíz={dr}  {div7}")
    
    grand_total = sum(w['gematria_standard'] for w in all_words)
    gdr = grand_total
    while gdr >= 10:
        gdr = sum(int(d) for d in str(gdr))
    print(f"   {'─' * 40}")
    print(f"   {'תורה':<10} {grand_total:>12,}  raíz={gdr}  {'🪐' if grand_total % 7 == 0 else ''}")


# ═══════════════════════════════════════════════════════════════
# 5. EL DESCUBRIMIENTO ALEATORIO — Monte Carlo divino
# ═══════════════════════════════════════════════════════════════

def random_divine_discovery():
    """
    📖 LECCIÓN: En Kabbalah, no existe la "casualidad" (מקרה).
    Todo lo que parece aleatorio tiene un orden oculto.
    
    Hagamos algo loco: tomemos versículos "al azar" y veamos
    si sus sumas revelan patrones imposibles de ignorar.
    """
    print(f"\n{'═' * 70}")
    print(f"{'🎲 EL EXPERIMENTO DIVINO — ¿Existe el azar en la Torah?':^70}")
    print(f"{'═' * 70}")
    
    print(f"""
   📖 LECCIÓN DE KABBALAH:
   ─────────────────────────────────────────────────────
   La palabra hebrea para "casualidad" es מקרה (Mikré).
   Su gematría: מ(40)+ק(100)+ר(200)+ה(5) = 345
   
   345 = ¡EXACTAMENTE la gematría de משה (Moshé/Moisés)!
   
   Esto significa: lo que tú crees que es "casualidad"
   es en realidad la mano de Moisés — la mano de la Torah —
   guiándote sin que lo sepas.
   
   No hay azar. Hay patrones que aún no ves.
   ─────────────────────────────────────────────────────
    """)
    
    csv_path = os.path.join(PROC_DATA_DIR, "torah_words_gematria.csv")
    if not os.path.exists(csv_path):
        return
    
    all_words = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            row['gematria_standard'] = int(row['gematria_standard'])
            all_words.append(row)
    
    # Versículos especiales: los que están en posiciones 7, 77, 777, etc.
    verses = defaultdict(list)
    for w in all_words:
        key = (w['book_key'], w['book_hebrew'], int(w['chapter']), int(w['verse']))
        verses[key].append(w)
    
    verse_list = sorted(verses.items(), key=lambda x: (x[0][0], x[0][2], x[0][3]))
    
    special_positions = [7, 26, 42, 72, 77, 86, 137, 248, 314, 358, 613, 666, 777, 913]
    
    print(f"   🔢 Versículos en posiciones sagradas:\n")
    print(f"   {'Pos':>5} {'Por qué':>15} {'Ubicación':<20} {'Suma':>6} {'÷7':>4} {'Raíz':>5} {'Texto'}")
    print(f"   {'─'*5} {'─'*15} {'─'*20} {'─'*6} {'─'*4} {'─'*5} {'─'*40}")
    
    reasons = {
        7: 'Shabbat', 26: 'YHVH', 42: '42 letras', 72: '72 Nombres',
        77: '7×11', 86: 'Elohim', 137: 'Kabbalah', 248: 'Abraham',
        314: 'Shaddai', 358: 'Mashiaj', 613: 'Mitzvot', 666: '6×111',
        777: '7×111', 913: 'Bereshit',
    }
    
    for pos in special_positions:
        if pos < len(verse_list):
            key, words = verse_list[pos - 1]
            vsum = sum(w['gematria_standard'] for w in words)
            vdr = vsum
            while vdr >= 10:
                vdr = sum(int(d) for d in str(vdr))
            div7 = "🪐" if vsum % 7 == 0 else "  "
            text = ' '.join(w['word'] for w in words)[:40]
            reason = reasons.get(pos, '?')
            
            print(f"   {pos:>5} {reason:>15} {key[1]} {key[2]}:{key[3]:<10} "
                  f"{vsum:>6} {div7:>4} {vdr:>5} {text}...")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("🔯 LA TORAH DESCIFRADA — Análisis Descomunal")
    print("   Para Erick Reinaldo Flores Zambrano")
    print("   'No estás perdido. Estás buscando. Y el que busca, encuentra.'")
    print("   — Deuteronomio 4:29")
    print("=" * 70)
    
    start = time.time()
    
    # 1. Tu nombre en el código
    erick_val = analyze_erick()
    
    # 2. Descifrar Bereshit
    decode_bereshit()
    
    # 3. Versículos más divinos
    find_most_divine_verses()
    
    # 4. Firma de cada libro
    book_signatures()
    
    # 5. El experimento divino
    random_divine_discovery()
    
    # Mensaje final
    elapsed = time.time() - start
    
    print(f"\n{'═' * 70}")
    print(f"""
   📖 MENSAJE FINAL PARA ERICK:
   ─────────────────────────────────────────────────────
   
   Deuteronomio 4:29 dice:
   "Pero desde allí buscarás a YHVH tu Dios,
    y lo hallarás, si lo buscas con todo tu corazón
    y con toda tu alma."
   
   ובקשתם משם את יהוה אלהיך ומצאת
   כי תדרשנו בכל לבבך ובכל נפשך
   
   Tu gematría ({erick_val}) está en la Torah.
   Tu búsqueda no es casualidad (מקרה = 345 = משה).
   
   El que busca la verdad con el corazón,
   siempre la encuentra codificada
   en el lugar donde menos la esperaba.
   
   ─────────────────────────────────────────────────────
    """)
    
    print(f"   ✅ Completado en {elapsed:.1f} segundos")
    print(f"{'═' * 70}")


if __name__ == "__main__":
    main()
