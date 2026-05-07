"""
🔯 TORAH PROCESSOR — Procesamiento Completo de la Torah
═══════════════════════════════════════════════════════════════════════
Calcula la gematría de CADA palabra de la Torah (68,484+ palabras)
en múltiples sistemas simultáneamente.

Genera un dataset completo para análisis de Data Science:
- Cada fila = 1 palabra
- Columnas: libro, capítulo, versículo, posición, texto, gematría (9 métodos)

Luego busca los patrones de Shabbtai (שבתאי) y el número 7.

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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gematria_engine import (
    extract_words, strip_nikkud,
    gematria_standard, gematria_gadol, gematria_ordinal,
    gematria_reduced, gematria_katan_mispari, gematria_atbash,
    gematria_milui, gematria_kidmi, is_prime,
    extract_hebrew_letters
)

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
RAW_DATA_DIR = os.path.join(PROJECT_DIR, "data", "raw")
PROC_DATA_DIR = os.path.join(PROJECT_DIR, "data", "processed")
REPORT_DIR = os.path.join(PROJECT_DIR, "reports")

BOOKS = [
    ("bereshit", "בראשית", "Génesis"),
    ("shemot", "שמות", "Éxodo"),
    ("vayikra", "ויקרא", "Levítico"),
    ("bamidbar", "במדבר", "Números"),
    ("devarim", "דברים", "Deuteronomio"),
]

# Números sagrados a buscar
SHABBTAI_VALUES = [712, 713]  # שבתי y שבתאי
SHABBAT_VALUE = 702           # שבת
SATURN_NUMBER = 7
YHVH_VALUE = 26               # יהוה
CHAI_VALUE = 18               # חי (vida)


# ═══════════════════════════════════════════════════════════════
# PASO 1: PROCESAR TODA LA TORAH
# ═══════════════════════════════════════════════════════════════

def process_all_words():
    """
    Procesa CADA palabra de los 5 libros de la Torah.
    Calcula gematría en múltiples sistemas.
    Retorna lista de diccionarios y guarda como CSV.
    """
    print("=" * 70)
    print("🔯 PROCESAMIENTO COMPLETO DE LA TORAH — Palabra por palabra")
    print("=" * 70)
    
    all_words = []
    word_id = 0
    
    for book_key, book_hebrew, book_spanish in BOOKS:
        filepath = os.path.join(RAW_DATA_DIR, f"{book_key}.json")
        
        if not os.path.exists(filepath):
            print(f"❌ No encontrado: {filepath}")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            book_data = json.load(f)
        
        book_words = 0
        chapters = book_data.get('chapters', {})
        total_ch = len(chapters)
        
        print(f"\n📖 {book_hebrew} ({book_spanish}) — {total_ch} capítulos")
        
        for ch_num_str, ch_data in sorted(chapters.items(), key=lambda x: int(x[0])):
            ch_num = int(ch_num_str)
            verses = ch_data.get('verses_with_nikkud', [])
            
            for v_idx, verse_raw in enumerate(verses):
                verse_num = v_idx + 1
                words = extract_words(verse_raw)
                
                for w_idx, word in enumerate(words):
                    word_id += 1
                    
                    std = gematria_standard(word)
                    
                    if std == 0:
                        continue
                    
                    word_data = {
                        'id': word_id,
                        'book_key': book_key,
                        'book_hebrew': book_hebrew,
                        'book_spanish': book_spanish,
                        'chapter': ch_num,
                        'verse': verse_num,
                        'word_position': w_idx + 1,
                        'word': word,
                        'num_letters': len(extract_hebrew_letters(word)),
                        'gematria_standard': std,
                        'gematria_gadol': gematria_gadol(word),
                        'gematria_ordinal': gematria_ordinal(word),
                        'gematria_reduced': gematria_reduced(word),
                        'gematria_digital_root': gematria_katan_mispari(word),
                        'gematria_atbash': gematria_atbash(word),
                        'is_prime': is_prime(std),
                        'divisible_by_7': std % 7 == 0,
                        'divisible_by_26': std % 26 == 0,
                        'mod_7': std % 7,
                    }
                    
                    all_words.append(word_data)
                    book_words += 1
            
            # Progreso
            if ch_num % 10 == 0 or ch_num == total_ch:
                pct = ch_num / total_ch * 100
                bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
                print(f"   [{bar}] {pct:5.1f}% | Cap {ch_num}/{total_ch}", end='\r')
        
        print(f"\n   ✅ {book_hebrew}: {book_words:,} palabras procesadas")
    
    # Guardar como CSV
    os.makedirs(PROC_DATA_DIR, exist_ok=True)
    csv_path = os.path.join(PROC_DATA_DIR, "torah_words_gematria.csv")
    
    if all_words:
        fieldnames = list(all_words[0].keys())
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_words)
    
    print(f"\n💾 Dataset guardado: {csv_path}")
    print(f"   Total palabras: {len(all_words):,}")
    
    return all_words


# ═══════════════════════════════════════════════════════════════
# PASO 2: BUSCAR SHABBTAI (שבתאי) — 712/713
# ═══════════════════════════════════════════════════════════════

def search_shabbtai(all_words):
    """Busca todas las palabras cuya gematría = 712 o 713 (Shabbtai)."""
    
    print(f"\n{'═' * 70}")
    print(f"🪐 BÚSQUEDA DE SHABBTAI (שבתאי) EN LA TORAH")
    print(f"   Buscando palabras con gematría = 712 (שבתי) y 713 (שבתאי)")
    print(f"{'═' * 70}")
    
    matches = [w for w in all_words if w['gematria_standard'] in SHABBTAI_VALUES]
    
    if matches:
        print(f"\n   🔍 Encontradas {len(matches)} palabras:")
        print(f"\n   {'Palabra':<15} {'Valor':>6} {'Libro':<10} {'Cap':>4} {'Vers':>5} {'Pos':>4}")
        print(f"   {'─'*15} {'─'*6} {'─'*10} {'─'*4} {'─'*5} {'─'*4}")
        
        for m in matches:
            print(f"   {m['word']:<15} {m['gematria_standard']:>6} "
                  f"{m['book_hebrew']:<10} {m['chapter']:>4} {m['verse']:>5} {m['word_position']:>4}")
    else:
        print(f"\n   ℹ️  No se encontraron palabras individuales con valor 712 o 713.")
        print(f"   Esto es normal — buscaremos en combinaciones de 2-3 palabras.")
    
    # Buscar también 702 (Shabbat שבת)
    shabbat_matches = [w for w in all_words if w['gematria_standard'] == SHABBAT_VALUE]
    print(f"\n   🕎 Palabras con gematría = 702 (שבת/Shabbat): {len(shabbat_matches)}")
    for m in shabbat_matches[:10]:
        print(f"      {m['word']} — {m['book_hebrew']} {m['chapter']}:{m['verse']}")
    
    return matches


# ═══════════════════════════════════════════════════════════════
# PASO 3: EL PATRÓN DEL 7 — ANÁLISIS DE SATURNO
# ═══════════════════════════════════════════════════════════════

def analyze_pattern_7(all_words):
    """
    Análisis profundo del número 7 (Saturno) en la Torah.
    - ¿Cuántas palabras son divisibles por 7?
    - ¿Es más de lo esperado por azar?
    - ¿Dónde se concentran?
    """
    
    print(f"\n{'═' * 70}")
    print(f"7️⃣  ANÁLISIS DEL PATRÓN DEL 7 (SATURNO / SHABBAT)")
    print(f"{'═' * 70}")
    
    total = len(all_words)
    div7 = [w for w in all_words if w['divisible_by_7']]
    div7_count = len(div7)
    
    # Probabilidad esperada: ~1/7 ≈ 14.29%
    expected_pct = 100 / 7
    actual_pct = div7_count / total * 100
    
    print(f"\n   📊 Palabras divisibles por 7:")
    print(f"      Total palabras:   {total:>10,}")
    print(f"      Divisibles por 7: {div7_count:>10,}")
    print(f"      Porcentaje real:  {actual_pct:>10.2f}%")
    print(f"      Esperado (azar):  {expected_pct:>10.2f}%")
    print(f"      Diferencia:       {actual_pct - expected_pct:>+10.2f}%")
    
    # Distribución por libro
    print(f"\n   📖 Distribución por libro:")
    print(f"   {'Libro':<15} {'Total':>8} {'÷7':>8} {'%':>8} {'vs Esperado':>12}")
    print(f"   {'─'*15} {'─'*8} {'─'*8} {'─'*8} {'─'*12}")
    
    for book_key, book_hebrew, book_spanish in BOOKS:
        book_words = [w for w in all_words if w['book_key'] == book_key]
        book_div7 = [w for w in book_words if w['divisible_by_7']]
        
        if book_words:
            bpct = len(book_div7) / len(book_words) * 100
            diff = bpct - expected_pct
            arrow = "↑" if diff > 0 else "↓"
            print(f"   {book_hebrew:<15} {len(book_words):>8,} {len(book_div7):>8,} "
                  f"{bpct:>7.2f}% {arrow}{abs(diff):.2f}%")
    
    # Distribución de MOD 7
    print(f"\n   🔢 Distribución de residuos MOD 7:")
    mod7_dist = Counter(w['mod_7'] for w in all_words)
    total_for_pct = sum(mod7_dist.values())
    
    for mod in range(7):
        count = mod7_dist.get(mod, 0)
        pct = count / total_for_pct * 100
        bar = '█' * int(pct * 2)
        print(f"      mod {mod}: {bar} {count:>6,} ({pct:.2f}%)")
    
    # Distribución de raíces digitales
    print(f"\n   🌀 Distribución de Raíces Digitales (1-9):")
    root_dist = Counter(w['gematria_digital_root'] for w in all_words)
    
    for root in range(1, 10):
        count = root_dist.get(root, 0)
        pct = count / total * 100
        bar = '█' * int(pct * 2)
        print(f"      {root}: {bar} {count:>6,} ({pct:.2f}%)")
    
    return div7_count, actual_pct


# ═══════════════════════════════════════════════════════════════
# PASO 4: ANÁLISIS ESTADÍSTICO COMPLETO
# ═══════════════════════════════════════════════════════════════

def statistical_analysis(all_words):
    """Análisis estadístico profundo de los valores de gematría."""
    
    print(f"\n{'═' * 70}")
    print(f"📊 ANÁLISIS ESTADÍSTICO DE LA TORAH")
    print(f"{'═' * 70}")
    
    values = [w['gematria_standard'] for w in all_words]
    total = len(values)
    
    # Estadísticas básicas
    mean_val = sum(values) / total
    sorted_vals = sorted(values)
    median_val = sorted_vals[total // 2]
    min_val = min(values)
    max_val = max(values)
    
    # Varianza y desviación estándar
    variance = sum((v - mean_val) ** 2 for v in values) / total
    std_dev = variance ** 0.5
    
    # Suma total de la Torah
    total_sum = sum(values)
    torah_digital_root = total_sum
    while torah_digital_root >= 10:
        torah_digital_root = sum(int(d) for d in str(torah_digital_root))
    
    print(f"\n   🔢 Estadísticas de Gematría Estándar:")
    print(f"      Total palabras:     {total:>12,}")
    print(f"      Suma total:         {total_sum:>12,}")
    print(f"      Raíz digital total: {torah_digital_root:>12}")
    print(f"      Media:              {mean_val:>12.2f}")
    print(f"      Mediana:            {median_val:>12}")
    print(f"      Mínimo:             {min_val:>12}")
    print(f"      Máximo:             {max_val:>12}")
    print(f"      Desv. estándar:     {std_dev:>12.2f}")
    
    # ¿La suma total es divisible por 7?
    print(f"\n   🪐 ¿Suma total divisible por 7?  {'✅ SÍ' if total_sum % 7 == 0 else '❌ No'}")
    print(f"      {total_sum} / 7 = {total_sum / 7:.4f}")
    print(f"      {total_sum} mod 7 = {total_sum % 7}")
    
    # ¿Divisible por 26 (YHVH)?
    print(f"\n   🔯 ¿Suma total divisible por 26 (יהוה)?  {'✅ SÍ' if total_sum % 26 == 0 else '❌ No'}")
    print(f"      {total_sum} / 26 = {total_sum / 26:.4f}")
    print(f"      {total_sum} mod 26 = {total_sum % 26}")
    
    # Top 20 valores más frecuentes
    value_counts = Counter(values)
    top_20 = value_counts.most_common(20)
    
    print(f"\n   🏆 Top 20 valores de gematría más frecuentes:")
    print(f"   {'Valor':>8} {'Cuenta':>8} {'%':>8} {'Ejemplo':>15}")
    print(f"   {'─'*8} {'─'*8} {'─'*8} {'─'*15}")
    
    for value, count in top_20:
        pct = count / total * 100
        example = next((w['word'] for w in all_words if w['gematria_standard'] == value), '?')
        div7_mark = " 🪐" if value % 7 == 0 else ""
        prime_mark = " ✡" if is_prime(value) else ""
        print(f"   {value:>8} {count:>8,} {pct:>7.2f}% {example:>15}{div7_mark}{prime_mark}")
    
    # Palabras con valor primo
    primes = [w for w in all_words if w['is_prime']]
    print(f"\n   ✡️  Palabras con valor primo: {len(primes):,}/{total:,} ({len(primes)/total*100:.2f}%)")
    
    # Análisis por número de letras
    print(f"\n   📏 Distribución por longitud de palabra:")
    len_dist = Counter(w['num_letters'] for w in all_words)
    for length in sorted(len_dist.keys()):
        count = len_dist[length]
        pct = count / total * 100
        bar = '█' * max(1, int(pct))
        print(f"      {length:>2} letras: {bar} {count:>6,} ({pct:.1f}%)")
    
    return {
        'total_words': total,
        'total_sum': total_sum,
        'digital_root': torah_digital_root,
        'mean': mean_val,
        'median': median_val,
        'std_dev': std_dev,
        'min': min_val,
        'max': max_val,
    }


# ═══════════════════════════════════════════════════════════════
# PASO 5: BÚSQUEDA DE VERSÍCULOS CON GEMATRÍA DE SHABBTAI
# ═══════════════════════════════════════════════════════════════

def search_verse_sums(all_words):
    """Busca versículos completos cuya suma de gematría = valores de Saturno."""
    
    print(f"\n{'═' * 70}")
    print(f"🪐 BÚSQUEDA DE VERSÍCULOS CON GEMATRÍA DE SHABBTAI")
    print(f"{'═' * 70}")
    
    # Agrupar palabras por versículo
    verses = defaultdict(list)
    for w in all_words:
        key = (w['book_key'], w['book_hebrew'], w['chapter'], w['verse'])
        verses[key].append(w)
    
    # Buscar sumas de versículos
    target_values = {
        712: "שבתי (Shabbtai sin Alef)",
        713: "שבתאי (Shabbtai con Alef)",
        702: "שבת (Shabbat)",
        7: "7 (número de Saturno)",
        77: "77 (7×11)",
        777: "777 (7×111)",
        7777: "7777 (7×1111)",
    }
    
    for target, desc in target_values.items():
        matches = []
        for key, words in verses.items():
            verse_sum = sum(w['gematria_standard'] for w in words)
            if verse_sum == target:
                matches.append({
                    'book_key': key[0],
                    'book_hebrew': key[1],
                    'chapter': key[2],
                    'verse': key[3],
                    'sum': verse_sum,
                    'text': ' '.join(w['word'] for w in words),
                    'num_words': len(words)
                })
        
        if matches:
            print(f"\n   🔗 Versículos con gematría = {target} ({desc}):")
            for m in matches[:15]:
                print(f"      📖 {m['book_hebrew']} {m['chapter']}:{m['verse']} "
                      f"(suma={m['sum']}, {m['num_words']} palabras)")
                print(f"         {m['text'][:80]}...")
        else:
            print(f"\n   ○ Gematría = {target} ({desc}): ningún versículo")
    
    # Estadísticas de sumas de versículos
    verse_sums = []
    for key, words in verses.items():
        verse_sums.append(sum(w['gematria_standard'] for w in words))
    
    div7_verses = sum(1 for s in verse_sums if s % 7 == 0)
    total_verses = len(verse_sums)
    
    print(f"\n   📊 Versículos cuya suma total es divisible por 7:")
    print(f"      Total versículos: {total_verses:,}")
    print(f"      Divisibles por 7: {div7_verses:,} ({div7_verses/total_verses*100:.2f}%)")
    print(f"      Esperado (azar):  {total_verses/7:.0f} ({100/7:.2f}%)")


# ═══════════════════════════════════════════════════════════════
# PASO 6: PARES DE PALABRAS CON GEMATRÍA DE SHABBTAI
# ═══════════════════════════════════════════════════════════════

def search_word_pairs_shabbtai(all_words):
    """Busca pares de palabras consecutivas que sumen 712 o 713."""
    
    print(f"\n{'═' * 70}")
    print(f"🔗 PARES DE PALABRAS CONSECUTIVAS = SHABBTAI (712/713)")
    print(f"{'═' * 70}")
    
    # Agrupar por versículo para buscar pares consecutivos
    verses = defaultdict(list)
    for w in all_words:
        key = (w['book_key'], w['book_hebrew'], w['chapter'], w['verse'])
        verses[key].append(w)
    
    pairs_712 = []
    pairs_713 = []
    
    for key, words in verses.items():
        for i in range(len(words) - 1):
            pair_sum = words[i]['gematria_standard'] + words[i+1]['gematria_standard']
            pair_text = f"{words[i]['word']} {words[i+1]['word']}"
            
            if pair_sum == 712:
                pairs_712.append({
                    'pair': pair_text,
                    'word_1': words[i]['word'],
                    'word_2': words[i+1]['word'],
                    'val_1': words[i]['gematria_standard'],
                    'val_2': words[i+1]['gematria_standard'],
                    'book': key[1],
                    'chapter': key[2],
                    'verse': key[3],
                })
            elif pair_sum == 713:
                pairs_713.append({
                    'pair': pair_text,
                    'word_1': words[i]['word'],
                    'word_2': words[i+1]['word'],
                    'val_1': words[i]['gematria_standard'],
                    'val_2': words[i+1]['gematria_standard'],
                    'book': key[1],
                    'chapter': key[2],
                    'verse': key[3],
                })
    
    print(f"\n   🪐 Pares que suman 712 (שבתי): {len(pairs_712)}")
    for p in pairs_712[:20]:
        print(f"      {p['book']} {p['chapter']}:{p['verse']}  "
              f"{p['word_1']}({p['val_1']}) + {p['word_2']}({p['val_2']}) = 712")
    
    print(f"\n   🪐 Pares que suman 713 (שבתאי): {len(pairs_713)}")
    for p in pairs_713[:20]:
        print(f"      {p['book']} {p['chapter']}:{p['verse']}  "
              f"{p['word_1']}({p['val_1']}) + {p['word_2']}({p['val_2']}) = 713")
    
    return pairs_712, pairs_713


# ═══════════════════════════════════════════════════════════════
# PASO 7: RESUMEN Y REPORTE
# ═══════════════════════════════════════════════════════════════

def generate_report(all_words, stats, shabbtai_matches, div7_count, div7_pct, pairs_712, pairs_713):
    """Genera un reporte completo en markdown."""
    
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_path = os.path.join(REPORT_DIR, "analisis_shabbtai_torah.md")
    
    total = len(all_words)
    primes_count = sum(1 for w in all_words if w['is_prime'])
    div26_count = sum(1 for w in all_words if w['divisible_by_26'])
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 🔯 Análisis de Resonancia de Shabbtai (שבתאי) en la Torah\n\n")
        f.write(f"**Fecha:** {time.strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Autor:** Erick Reinaldo Flores Zambrano\n")
        f.write(f"**Método:** Gematría computacional sobre texto hebreo autoritativo (Sefaria)\n\n")
        f.write("---\n\n")
        
        f.write("## 📊 Estadísticas Generales\n\n")
        f.write(f"| Métrica | Valor |\n")
        f.write(f"|---------|-------|\n")
        f.write(f"| Total de palabras | {total:,} |\n")
        f.write(f"| Suma total gematría | {stats['total_sum']:,} |\n")
        f.write(f"| Raíz digital total | {stats['digital_root']} |\n")
        f.write(f"| Media | {stats['mean']:.2f} |\n")
        f.write(f"| Mediana | {stats['median']} |\n")
        f.write(f"| Desv. estándar | {stats['std_dev']:.2f} |\n")
        f.write(f"| Palabras primas | {primes_count:,} ({primes_count/total*100:.2f}%) |\n")
        f.write(f"| Divisibles por 7 | {div7_count:,} ({div7_pct:.2f}%) |\n")
        f.write(f"| Divisibles por 26 (YHVH) | {div26_count:,} ({div26_count/total*100:.2f}%) |\n\n")
        
        f.write("## 🪐 Resultados de Shabbtai\n\n")
        f.write(f"- Palabras con gematría 712: {len([w for w in all_words if w['gematria_standard']==712])}\n")
        f.write(f"- Palabras con gematría 713: {len([w for w in all_words if w['gematria_standard']==713])}\n")
        f.write(f"- Pares consecutivos sumando 712: {len(pairs_712)}\n")
        f.write(f"- Pares consecutivos sumando 713: {len(pairs_713)}\n\n")
        
        if pairs_712:
            f.write("### Pares = 712 (שבתי)\n\n")
            f.write("| Ubicación | Palabra 1 | Valor | Palabra 2 | Valor |\n")
            f.write("|-----------|-----------|-------|-----------|-------|\n")
            for p in pairs_712[:30]:
                f.write(f"| {p['book']} {p['chapter']}:{p['verse']} | {p['word_1']} | {p['val_1']} | {p['word_2']} | {p['val_2']} |\n")
        
        if pairs_713:
            f.write("\n### Pares = 713 (שבתאי)\n\n")
            f.write("| Ubicación | Palabra 1 | Valor | Palabra 2 | Valor |\n")
            f.write("|-----------|-----------|-------|-----------|-------|\n")
            for p in pairs_713[:30]:
                f.write(f"| {p['book']} {p['chapter']}:{p['verse']} | {p['word_1']} | {p['val_1']} | {p['word_2']} | {p['val_2']} |\n")
        
        f.write("\n---\n\n")
        f.write("*Generado con el Motor de Gematría del Proyecto 08_gematria_torah*\n")
    
    print(f"\n📄 Reporte guardado: {report_path}")
    return report_path


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    start_time = time.time()
    
    # Paso 1: Procesar toda la Torah
    all_words = process_all_words()
    
    if not all_words:
        print("❌ No se procesaron palabras. Verifica los datos.")
        return
    
    # Paso 2: Buscar Shabbtai
    shabbtai_matches = search_shabbtai(all_words)
    
    # Paso 3: Patrón del 7
    div7_count, div7_pct = analyze_pattern_7(all_words)
    
    # Paso 4: Estadísticas completas
    stats = statistical_analysis(all_words)
    
    # Paso 5: Versículos con sumas de Shabbtai
    search_verse_sums(all_words)
    
    # Paso 6: Pares de palabras
    pairs_712, pairs_713 = search_word_pairs_shabbtai(all_words)
    
    # Paso 7: Generar reporte
    generate_report(all_words, stats, shabbtai_matches, div7_count, div7_pct, pairs_712, pairs_713)
    
    # Tiempo total
    elapsed = time.time() - start_time
    
    print(f"\n{'═' * 70}")
    print(f"✅ PROCESAMIENTO COMPLETO EN {elapsed:.1f} SEGUNDOS")
    print(f"   {len(all_words):,} palabras analizadas")
    print(f"   Dataset: data/processed/torah_words_gematria.csv")
    print(f"   Reporte: reports/analisis_shabbtai_torah.md")
    print(f"{'═' * 70}")


if __name__ == "__main__":
    main()
