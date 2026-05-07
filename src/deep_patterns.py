"""
🔯 DEEP PATTERN FINDER — Buscador de Patrones Profundos en la Torah
═══════════════════════════════════════════════════════════════════════
"Cuando dos palabras comparten el mismo valor de gematría, 
 comparten la misma raíz en el Árbol de la Vida." — Zohar

Este script busca:
1. EQUIVALENCIAS: Palabras que comparten el mismo valor
2. ECUACIONES: A + B = C (la suma de dos palabras = otra palabra)
3. RELACIONES TEOLÓGICAS: Nombres de Dios, patriarcas, conceptos
4. PATRONES OCULTOS: Secuencias, repeticiones, simetrías

Autor: Erick Reinaldo Flores Zambrano
Proyecto: 08_gematria_torah
═══════════════════════════════════════════════════════════════════════
"""

import json
import os
import csv
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gematria_engine import (
    extract_words, strip_nikkud, extract_hebrew_letters,
    gematria_standard, gematria_ordinal, gematria_reduced,
    gematria_katan_mispari, gematria_atbash, is_prime
)

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PROC_DATA_DIR = os.path.join(PROJECT_DIR, "data", "processed")
REPORT_DIR = os.path.join(PROJECT_DIR, "reports")


# ═══════════════════════════════════════════════════════════════
# DICCIONARIO DE CONCEPTOS SAGRADOS
# Estas son las palabras clave que todo Rabino conoce
# ═══════════════════════════════════════════════════════════════

SACRED_CONCEPTS = {
    # Nombres de Dios
    'יהוה': ('YHVH', 'El Tetragramatón — Nombre inefable'),
    'אלהים': ('Elohim', 'Dios como Juez/Creador'),
    'אל': ('El', 'Dios — forma corta'),
    'אדני': ('Adonai', 'Mi Señor'),
    'שדי': ('Shaddai', 'Todopoderoso'),
    'צבאות': ('Tzevaot', 'Dios de los ejércitos'),
    'אהיה': ('Ehyeh', 'Yo Soy — Éxodo 3:14'),
    
    # Sefirot
    'כתר': ('Keter', 'Corona — 1ra Sefirah'),
    'חכמה': ('Jokhmah', 'Sabiduría — 2da Sefirah'),
    'בינה': ('Binah', 'Entendimiento — 3ra (Saturno)'),
    'חסד': ('Jesed', 'Bondad — 4ta Sefirah'),
    'גבורה': ('Gevurah', 'Fuerza/Juicio — 5ta Sefirah'),
    'תפארת': ('Tiferet', 'Belleza — 6ta Sefirah'),
    'נצח': ('Netzaj', 'Victoria — 7ma Sefirah'),
    'הוד': ('Hod', 'Esplendor — 8va Sefirah'),
    'יסוד': ('Yesod', 'Fundamento — 9na Sefirah'),
    'מלכות': ('Malkut', 'Reino — 10ma Sefirah'),
    
    # Patriarcas y Matriarcas
    'אברהם': ('Abraham', 'Padre de multitudes'),
    'יצחק': ('Itzjak', 'Isaac — risa'),
    'יעקב': ('Yaakov', 'Jacob — suplantador'),
    'שרה': ('Sarah', 'Princesa'),
    'רבקה': ('Rivkah', 'Rebeca'),
    'רחל': ('Rajel', 'Raquel — oveja'),
    'לאה': ('Leah', 'Lea — cansada'),
    'משה': ('Moshé', 'Moisés — sacado del agua'),
    'אהרן': ('Aharon', 'Aarón'),
    'דוד': ('David', 'David — amado'),
    
    # Conceptos fundamentales
    'תורה': ('Torah', 'Enseñanza/Ley'),
    'אמת': ('Emet', 'Verdad'),
    'שלום': ('Shalom', 'Paz'),
    'אהבה': ('Ahavá', 'Amor'),
    'אחד': ('Ejad', 'Uno'),
    'חיים': ('Jaim', 'Vida'),
    'מות': ('Mavet', 'Muerte'),
    'נשמה': ('Neshamá', 'Alma'),
    'רוח': ('Ruaj', 'Espíritu/Viento'),
    'נפש': ('Nefesh', 'Alma vital'),
    'אור': ('Or', 'Luz'),
    'חשך': ('Joshek', 'Oscuridad'),
    'שמים': ('Shamaim', 'Cielos'),
    'ארץ': ('Eretz', 'Tierra'),
    'מים': ('Maim', 'Agua'),
    'אש': ('Esh', 'Fuego'),
    'רוח': ('Ruaj', 'Aire/Espíritu'),
    'עץ': ('Etz', 'Árbol'),
    'גן': ('Gan', 'Jardín'),
    'עדן': ('Eden', 'Edén — placer'),
    'נחש': ('Najash', 'Serpiente'),
    'משיח': ('Mashiaj', 'Mesías — ungido'),
    'גאולה': ('Geulah', 'Redención'),
    'תשובה': ('Teshuvá', 'Arrepentimiento/Retorno'),
    'ברית': ('Brit', 'Pacto/Alianza'),
    'קדוש': ('Kadosh', 'Santo'),
    'שבת': ('Shabbat', 'Sábado/Descanso'),
    'שבתאי': ('Shabbtai', 'Saturno'),
    'שבתי': ('Shabbtai', 'Saturno (variante)'),
    
    # Elementos de la creación
    'בראשית': ('Bereshit', 'En el principio'),
    'אדם': ('Adam', 'Hombre/Humanidad'),
    'חוה': ('Javá', 'Eva — vida'),
    
    # Números sagrados como palabras
    'חי': ('Jai', 'Vivo/18'),
    'טוב': ('Tov', 'Bueno'),
    'רע': ('Ra', 'Malo'),
}


# ═══════════════════════════════════════════════════════════════
# CARGAR DATOS
# ═══════════════════════════════════════════════════════════════

def load_torah_data():
    """Carga el CSV procesado de la Torah."""
    csv_path = os.path.join(PROC_DATA_DIR, "torah_words_gematria.csv")
    
    if not os.path.exists(csv_path):
        print("❌ No encontrado torah_words_gematria.csv. Ejecuta torah_processor.py primero.")
        return None
    
    words = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['gematria_standard'] = int(row['gematria_standard'])
            row['chapter'] = int(row['chapter'])
            row['verse'] = int(row['verse'])
            words.append(row)
    
    return words


def build_value_index(all_words):
    """Construye un índice invertido: valor → lista de palabras únicas."""
    index = defaultdict(set)
    for w in all_words:
        index[w['gematria_standard']].add(w['word'])
    return index


# ═══════════════════════════════════════════════════════════════
# 1. EQUIVALENCIAS SAGRADAS
# ═══════════════════════════════════════════════════════════════

def find_sacred_equivalences():
    """
    Calcula la gematría de todos los conceptos sagrados
    y encuentra cuáles comparten el mismo valor.
    
    "Cuando dos palabras tienen la misma gematría, están
     unidas por una raíz invisible en el mundo espiritual."
    """
    print(f"\n{'═' * 70}")
    print(f"{'🔯 EQUIVALENCIAS SAGRADAS DE GEMATRÍA':^70}")
    print(f"{'═' * 70}")
    
    # Calcular gematría de cada concepto
    concept_values = {}
    for word, (name, desc) in SACRED_CONCEPTS.items():
        val = gematria_standard(word)
        concept_values[word] = {
            'name': name,
            'description': desc,
            'standard': val,
            'ordinal': gematria_ordinal(word),
            'reduced': gematria_reduced(word),
            'atbash': gematria_atbash(word),
            'digital_root': gematria_katan_mispari(word),
        }
    
    # Agrupar por valor
    by_value = defaultdict(list)
    for word, data in concept_values.items():
        by_value[data['standard']].append((word, data['name'], data['description']))
    
    # Mostrar equivalencias (donde 2+ conceptos comparten valor)
    equivalences = {v: words for v, words in by_value.items() if len(words) >= 2}
    
    print(f"\n   Encontradas {len(equivalences)} familias de equivalencias:\n")
    
    for value in sorted(equivalences.keys()):
        words = equivalences[value]
        prime_mark = " ✡(primo)" if is_prime(value) else ""
        div7_mark = " 🪐(÷7)" if value % 7 == 0 else ""
        
        print(f"   ┌─ Gematría = {value}{prime_mark}{div7_mark}")
        for word, name, desc in words:
            print(f"   │  {word} = {name} — {desc}")
        print(f"   └─────────────────────────────")
    
    # Tabla completa de conceptos sagrados
    print(f"\n{'─' * 70}")
    print(f"📋 TABLA COMPLETA DE CONCEPTOS SAGRADOS")
    print(f"{'─' * 70}")
    print(f"   {'Hebreo':<12} {'Nombre':<15} {'Std':>5} {'Ord':>5} {'Red':>4} {'Raíz':>4} {'Atbash':>6}")
    print(f"   {'─'*12} {'─'*15} {'─'*5} {'─'*5} {'─'*4} {'─'*4} {'─'*6}")
    
    for word in sorted(concept_values.keys(), key=lambda w: concept_values[w]['standard']):
        d = concept_values[word]
        print(f"   {word:<12} {d['name']:<15} {d['standard']:>5} {d['ordinal']:>5} "
              f"{d['reduced']:>4} {d['digital_root']:>4} {d['atbash']:>6}")
    
    return concept_values, equivalences


# ═══════════════════════════════════════════════════════════════
# 2. ECUACIONES DE GEMATRÍA: A + B = C
# ═══════════════════════════════════════════════════════════════

def find_equations(concept_values):
    """
    Busca ecuaciones donde la suma de dos conceptos sagrados
    es igual al valor de un tercer concepto.
    
    Ejemplo clásico: אהבה (Amor=13) + אחד (Uno=13) = יהוה (YHVH=26)
    "El amor y la unidad juntos forman el Nombre de Dios."
    """
    print(f"\n{'═' * 70}")
    print(f"{'⚡ ECUACIONES DE GEMATRÍA: A + B = C':^70}")
    print(f"{'(Cuando la suma de dos conceptos revela un tercero)':^70}")
    print(f"{'═' * 70}")
    
    # Crear lookups
    value_to_concepts = defaultdict(list)
    for word, data in concept_values.items():
        value_to_concepts[data['standard']].append((word, data['name']))
    
    concept_list = list(concept_values.items())
    equations = []
    
    # Buscar A + B = C
    for i, (word_a, data_a) in enumerate(concept_list):
        for j, (word_b, data_b) in enumerate(concept_list):
            if j <= i:
                continue
            
            sum_ab = data_a['standard'] + data_b['standard']
            
            if sum_ab in value_to_concepts:
                for word_c, name_c in value_to_concepts[sum_ab]:
                    if word_c != word_a and word_c != word_b:
                        equations.append({
                            'word_a': word_a, 'name_a': data_a['name'], 'val_a': data_a['standard'],
                            'word_b': word_b, 'name_b': data_b['name'], 'val_b': data_b['standard'],
                            'word_c': word_c, 'name_c': name_c, 'val_c': sum_ab,
                        })
    
    # También buscar A + B donde la suma = un valor especial
    special_values = {
        26: 'YHVH (יהוה)',
        86: 'Elohim (אלהים)',
        358: 'Mashiaj (משיח)',
        345: 'Moshé (משה)',
        248: 'Abraham (אברהם)',
        713: 'Shabbtai (שבתאי)',
        712: 'Shabbtai (שבתי)',
        7: 'Saturno',
        18: 'Jai (חי)',
        613: 'Mitzvot',
    }
    
    print(f"\n   Encontradas {len(equations)} ecuaciones:\n")
    
    # Mostrar ecuaciones más significativas
    shown = set()
    for eq in sorted(equations, key=lambda e: e['val_c']):
        key = f"{eq['word_a']}+{eq['word_b']}"
        if key in shown:
            continue
        shown.add(key)
        
        special = ""
        if eq['val_c'] in special_values:
            special = f" ⭐ = {special_values[eq['val_c']]}"
        
        print(f"   {eq['word_a']}({eq['val_a']}) + {eq['word_b']}({eq['val_b']}) "
              f"= {eq['val_c']} = {eq['word_c']} ({eq['name_c']}){special}")
    
    # Buscar sumas que dan valores especiales
    print(f"\n{'─' * 70}")
    print(f"⭐ ECUACIONES QUE REVELAN VALORES ESPECIALES")
    print(f"{'─' * 70}")
    
    for target_val, target_name in special_values.items():
        target_equations = []
        for i, (word_a, data_a) in enumerate(concept_list):
            for j, (word_b, data_b) in enumerate(concept_list):
                if j <= i:
                    continue
                if data_a['standard'] + data_b['standard'] == target_val:
                    target_equations.append((word_a, data_a, word_b, data_b))
        
        if target_equations:
            print(f"\n   🔗 ¿Qué suma {target_val} ({target_name})?")
            for word_a, data_a, word_b, data_b in target_equations:
                print(f"      {word_a} ({data_a['name']}={data_a['standard']}) + "
                      f"{word_b} ({data_b['name']}={data_b['standard']}) = {target_val}")
    
    return equations


# ═══════════════════════════════════════════════════════════════
# 3. BÚSQUEDA EN LA TORAH REAL: Palabras que comparten valor
# ═══════════════════════════════════════════════════════════════

def find_torah_families(all_words, value_index):
    """
    Encuentra las familias de palabras más grandes en la Torah
    (palabras diferentes que comparten el mismo valor de gematría).
    """
    print(f"\n{'═' * 70}")
    print(f"{'👨‍👩‍👧‍👦 FAMILIAS DE PALABRAS EN LA TORAH':^70}")
    print(f"{'(Palabras diferentes con el mismo valor de gematría)':^70}")
    print(f"{'═' * 70}")
    
    # Encontrar las familias más grandes
    families = [(val, words) for val, words in value_index.items() if len(words) >= 5]
    families.sort(key=lambda x: len(x[1]), reverse=True)
    
    print(f"\n   Top 25 familias más grandes:\n")
    print(f"   {'Valor':>6} {'Miembros':>9} {'÷7':>4} {'Palabras (primeras 8)'}")
    print(f"   {'─'*6} {'─'*9} {'─'*4} {'─'*50}")
    
    for val, words in families[:25]:
        div7 = "🪐" if val % 7 == 0 else "  "
        word_list = sorted(words)[:8]
        words_str = ', '.join(word_list)
        if len(words) > 8:
            words_str += f" ... (+{len(words)-8})"
        print(f"   {val:>6} {len(words):>9} {div7:>4} {words_str}")
    
    return families


# ═══════════════════════════════════════════════════════════════
# 4. PATRONES DE BERESHIT (GÉNESIS 1) — EL CÓDIGO DE LA CREACIÓN
# ═══════════════════════════════════════════════════════════════

def analyze_creation_code(all_words):
    """
    Análisis profundo de Génesis 1 — Los 7 días de la Creación.
    Busca patrones numéricos en el relato de la creación.
    """
    print(f"\n{'═' * 70}")
    print(f"{'🌍 EL CÓDIGO DE LA CREACIÓN — BERESHIT CAPÍTULO 1':^70}")
    print(f"{'═' * 70}")
    
    # Filtrar solo Génesis capítulo 1
    gen1 = [w for w in all_words if w['book_key'] == 'bereshit' and w['chapter'] == 1]
    
    if not gen1:
        print("❌ No se encontraron datos de Génesis 1")
        return
    
    # Agrupar por versículo
    verses = defaultdict(list)
    for w in gen1:
        verses[w['verse']].append(w)
    
    total_sum = sum(w['gematria_standard'] for w in gen1)
    dr = total_sum
    while dr >= 10:
        dr = sum(int(d) for d in str(dr))
    
    print(f"\n   📊 Estadísticas de Génesis 1:")
    print(f"      Versículos: {len(verses)}")
    print(f"      Palabras: {len(gen1)}")
    print(f"      Suma total gematría: {total_sum:,}")
    print(f"      Raíz digital: {dr}")
    print(f"      ÷7: {'✅ SÍ' if total_sum % 7 == 0 else '❌ No'} (mod 7 = {total_sum % 7})")
    
    # Análisis versículo por versículo
    print(f"\n   📖 Análisis por versículo:")
    print(f"   {'Vers':>4} {'Palabras':>8} {'Suma':>8} {'÷7':>4} {'Raíz':>5} {'Primera palabra':>20}")
    print(f"   {'─'*4} {'─'*8} {'─'*8} {'─'*4} {'─'*5} {'─'*20}")
    
    for v_num in sorted(verses.keys()):
        v_words = verses[v_num]
        v_sum = sum(w['gematria_standard'] for w in v_words)
        v_dr = v_sum
        while v_dr >= 10:
            v_dr = sum(int(d) for d in str(v_dr))
        div7 = "🪐" if v_sum % 7 == 0 else "  "
        first_word = v_words[0]['word'] if v_words else ''
        
        print(f"   {v_num:>4} {len(v_words):>8} {v_sum:>8,} {div7:>4} {v_dr:>5} {first_word:>20}")
    
    # Primera palabra de la Torah
    first_word = gen1[0]['word']  # בראשית
    fw_val = gen1[0]['gematria_standard']
    
    print(f"\n   🔯 Primera palabra de la Torah:")
    print(f"      {first_word} (Bereshit) = {fw_val}")
    print(f"      913 es primo: {'✅' if is_prime(913) else '❌'}")
    print(f"      913 = 11 × 83")
    print(f"      Raíz digital: {gematria_katan_mispari(first_word)}")
    
    # Primer versículo completo
    v1_words = verses[1]
    v1_text = ' '.join(w['word'] for w in v1_words)
    v1_sum = sum(w['gematria_standard'] for w in v1_words)
    
    print(f"\n   🔯 Primer versículo completo:")
    print(f"      {v1_text}")
    print(f"      Gematría total: {v1_sum}")
    print(f"      {v1_sum} ÷ 7 = {v1_sum / 7:.4f}")
    print(f"      Número de palabras: {len(v1_words)}")
    print(f"      Número de letras: {sum(len(extract_hebrew_letters(w['word'])) for w in v1_words)}")
    
    # Las 7 palabras del primer versículo
    print(f"\n   📐 Las {len(v1_words)} palabras de Bereshit 1:1:")
    for i, w in enumerate(v1_words):
        letters = extract_hebrew_letters(w['word'])
        print(f"      {i+1}. {w['word']:<12} = {w['gematria_standard']:>5} "
              f"({len(letters)} letras) "
              f"{'🪐' if w['gematria_standard'] % 7 == 0 else ''}")
    
    # ¿Cuántas de las 7 palabras del primer versículo son divisibles por 7?
    div7_first = sum(1 for w in v1_words if int(w['gematria_standard']) % 7 == 0)
    print(f"\n      Palabras divisibles por 7: {div7_first}/{len(v1_words)}")
    
    # Análisis de los 7 días
    print(f"\n{'─' * 70}")
    print(f"🌅 LOS 7 DÍAS DE LA CREACIÓN")
    print(f"{'─' * 70}")
    
    # Los 7 días: Día 1 = v1-5, Día 2 = v6-8, etc.
    days = {
        1: (1, 5, "Luz y oscuridad"),
        2: (6, 8, "Firmamento/Cielos"),
        3: (9, 13, "Tierra seca y vegetación"),
        4: (14, 19, "Sol, Luna y estrellas"),
        5: (20, 23, "Peces y aves"),
        6: (24, 31, "Animales y Hombre"),
        7: (0, 0, "Shabbat — Génesis 2:1-3"),
    }
    
    print(f"\n   {'Día':>4} {'Versículos':>12} {'Palabras':>9} {'Suma':>10} {'÷7':>4} {'Raíz':>5} {'Descripción'}")
    print(f"   {'─'*4} {'─'*12} {'─'*9} {'─'*10} {'─'*4} {'─'*5} {'─'*25}")
    
    for day, (v_start, v_end, desc) in days.items():
        if day == 7:
            print(f"   {day:>4} {'2:1-3':>12} {'—':>9} {'—':>10} {'🪐':>4} {'—':>5} {desc}")
            continue
        
        day_words = [w for w in gen1 if v_start <= w['verse'] <= v_end]
        day_sum = sum(w['gematria_standard'] for w in day_words)
        day_dr = day_sum
        while day_dr >= 10:
            day_dr = sum(int(d) for d in str(day_dr))
        div7 = "🪐" if day_sum % 7 == 0 else "  "
        
        print(f"   {day:>4} {f'{v_start}-{v_end}':>12} {len(day_words):>9} "
              f"{day_sum:>10,} {div7:>4} {day_dr:>5} {desc}")


# ═══════════════════════════════════════════════════════════════
# 5. RELACIONES CRUZADAS — LA RED OCULTA
# ═══════════════════════════════════════════════════════════════

def find_cross_relationships(concept_values):
    """
    Busca relaciones numerológicas profundas entre conceptos:
    - A × 2 = B (duplicación)
    - A = Atbash(B) (espejo)
    - Digital root compartida
    """
    print(f"\n{'═' * 70}")
    print(f"{'🕸️ RED DE RELACIONES CRUZADAS':^70}")
    print(f"{'═' * 70}")
    
    # Relaciones de multiplicación
    print(f"\n   📐 Relaciones de multiplicación (A × n = B):")
    
    items = list(concept_values.items())
    for i, (word_a, data_a) in enumerate(items):
        for j, (word_b, data_b) in enumerate(items):
            if i == j:
                continue
            val_a = data_a['standard']
            val_b = data_b['standard']
            
            if val_a == 0:
                continue
            
            if val_b % val_a == 0 and 2 <= val_b // val_a <= 10:
                factor = val_b // val_a
                print(f"      {word_a}({val_a}) × {factor} = {word_b}({val_b}) "
                      f"[{data_a['name']} × {factor} = {data_b['name']}]")
    
    # Relaciones Atbash (espejo)
    print(f"\n   🪞 Relaciones Atbash (espejo):")
    print(f"      (Cuando el valor estándar de A = valor Atbash de B)")
    
    for word_a, data_a in items:
        for word_b, data_b in items:
            if word_a == word_b:
                continue
            if data_a['standard'] == data_b['atbash']:
                print(f"      {word_a}({data_a['standard']}) ↔ Atbash({word_b}) = {data_b['atbash']} "
                      f"[{data_a['name']} ↔ espejo de {data_b['name']}]")
    
    # Raíz digital compartida
    print(f"\n   🌀 Grupos por Raíz Digital:")
    root_groups = defaultdict(list)
    for word, data in concept_values.items():
        root_groups[data['digital_root']].append((word, data['name'], data['standard']))
    
    for root in sorted(root_groups.keys()):
        group = root_groups[root]
        if len(group) >= 3:
            print(f"\n      Raíz {root}: ({len(group)} conceptos)")
            for word, name, val in sorted(group, key=lambda x: x[2]):
                print(f"         {word:<12} {name:<15} = {val}")


# ═══════════════════════════════════════════════════════════════
# 6. RESUMEN DE DESCUBRIMIENTOS
# ═══════════════════════════════════════════════════════════════

def generate_discoveries_report(concept_values, equations, all_words):
    """Genera reporte de descubrimientos profundos."""
    
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_path = os.path.join(REPORT_DIR, "descubrimientos_profundos.md")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 🔯 Descubrimientos Profundos de Gematría en la Torah\n\n")
        f.write(f"**Fecha:** {time.strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Autor:** Erick Reinaldo Flores Zambrano\n\n")
        f.write("---\n\n")
        
        f.write("## ⚡ Ecuaciones Reveladas\n\n")
        f.write("| Concepto A | Valor | + | Concepto B | Valor | = | Resultado | Valor |\n")
        f.write("|-----------|-------|---|-----------|-------|---|----------|-------|\n")
        
        shown = set()
        for eq in sorted(equations, key=lambda e: e['val_c']):
            key = f"{eq['word_a']}+{eq['word_b']}"
            if key in shown:
                continue
            shown.add(key)
            f.write(f"| {eq['word_a']} ({eq['name_a']}) | {eq['val_a']} | + | "
                    f"{eq['word_b']} ({eq['name_b']}) | {eq['val_b']} | = | "
                    f"{eq['word_c']} ({eq['name_c']}) | {eq['val_c']} |\n")
        
        f.write("\n---\n\n")
        f.write("*Generado computacionalmente a partir del texto hebreo autoritativo de la Torah*\n")
    
    print(f"\n📄 Reporte de descubrimientos: {report_path}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("🔯 DEEP PATTERN FINDER — Buscador de Patrones Profundos")
    print("   'La Torah fue escrita con fuego negro sobre fuego blanco' — Zohar")
    print("=" * 70)
    
    start_time = time.time()
    
    # Cargar datos
    print("\n📂 Cargando datos de la Torah...")
    all_words = load_torah_data()
    if not all_words:
        return
    print(f"   ✅ {len(all_words):,} palabras cargadas")
    
    # Construir índice
    value_index = build_value_index(all_words)
    print(f"   📊 {len(value_index):,} valores únicos de gematría")
    
    # 1. Equivalencias sagradas
    concept_values, equivalences = find_sacred_equivalences()
    
    # 2. Ecuaciones A + B = C
    equations = find_equations(concept_values)
    
    # 3. Familias en la Torah
    find_torah_families(all_words, value_index)
    
    # 4. El código de la Creación
    analyze_creation_code(all_words)
    
    # 5. Relaciones cruzadas
    find_cross_relationships(concept_values)
    
    # 6. Generar reporte
    generate_discoveries_report(concept_values, equations, all_words)
    
    elapsed = time.time() - start_time
    print(f"\n{'═' * 70}")
    print(f"✅ ANÁLISIS PROFUNDO COMPLETADO EN {elapsed:.1f} SEGUNDOS")
    print(f"{'═' * 70}")


if __name__ == "__main__":
    main()
