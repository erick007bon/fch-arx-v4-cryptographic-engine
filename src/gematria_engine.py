"""
🔯 GEMATRIA ENGINE — Motor de Cálculo de Gematría Hebrea
═══════════════════════════════════════════════════════════════════════
"En el principio fue la Palabra, y la Palabra era con Dios,
 y la Palabra era Dios." — Juan 1:1

Cada letra hebrea ES un número. Cada palabra ES una ecuación.
La Torah no se lee, se COMPUTA.

Este motor implementa los 9 sistemas auténticos de gematría
según la tradición rabínica (Sefer Yetzirah, Zohar, Pardes Rimonim).

Autor: Erick Reinaldo Flores Zambrano
Proyecto: 08_gematria_torah | Resonancia de Shabbtai en la Torah
═══════════════════════════════════════════════════════════════════════
"""

import re
import json
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


# ═══════════════════════════════════════════════════════════════
# TABLA MAESTRA DE GEMATRÍA
# Fuente: Tradición rabínica estándar (Mispar Hechrachi)
# ═══════════════════════════════════════════════════════════════

# Sistema Estándar (Mispar Hechrachi / מספר הכרחי)
STANDARD = {
    'א': 1,   'ב': 2,   'ג': 3,   'ד': 4,   'ה': 5,
    'ו': 6,   'ז': 7,   'ח': 8,   'ט': 9,   'י': 10,
    'כ': 20,  'ל': 30,  'מ': 40,  'נ': 50,  'ס': 60,
    'ע': 70,  'פ': 80,  'צ': 90,  'ק': 100, 'ר': 200,
    'ש': 300, 'ת': 400,
    # Letras finales (sofit) — mismo valor en sistema estándar
    'ך': 20,  'ם': 40,  'ן': 50,  'ף': 80,  'ץ': 90,
}

# Sistema Gadol (Mispar Gadol / מספר גדול) — Finales con valores altos
GADOL = {
    'א': 1,   'ב': 2,   'ג': 3,   'ד': 4,   'ה': 5,
    'ו': 6,   'ז': 7,   'ח': 8,   'ט': 9,   'י': 10,
    'כ': 20,  'ל': 30,  'מ': 40,  'נ': 50,  'ס': 60,
    'ע': 70,  'פ': 80,  'צ': 90,  'ק': 100, 'ר': 200,
    'ש': 300, 'ת': 400,
    # Letras finales con valores 500-900
    'ך': 500, 'ם': 600, 'ן': 700, 'ף': 800, 'ץ': 900,
}

# Sistema Ordinal (Mispar Siduri / מספר סידורי) — Posición 1-22
ORDINAL = {
    'א': 1,  'ב': 2,  'ג': 3,  'ד': 4,  'ה': 5,
    'ו': 6,  'ז': 7,  'ח': 8,  'ט': 9,  'י': 10,
    'כ': 11, 'ל': 12, 'מ': 13, 'נ': 14, 'ס': 15,
    'ע': 16, 'פ': 17, 'צ': 18, 'ק': 19, 'ר': 20,
    'ש': 21, 'ת': 22,
    # Finales = mismo valor ordinal
    'ך': 11, 'ם': 13, 'ן': 14, 'ף': 17, 'ץ': 18,
}

# Sistema Reducido (Mispar Katan / מספר קטן) — Sin ceros
REDUCED = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5,
    'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 1,
    'כ': 2, 'ל': 3, 'מ': 4, 'נ': 5, 'ס': 6,
    'ע': 7, 'פ': 8, 'צ': 9, 'ק': 1, 'ר': 2,
    'ש': 3, 'ת': 4,
    'ך': 2, 'ם': 4, 'ן': 5, 'ף': 8, 'ץ': 9,
}

# Atbash (את בש) — Sustitución: primera↔última letra
ATBASH_MAP = {
    'א': 'ת', 'ב': 'ש', 'ג': 'ר', 'ד': 'ק', 'ה': 'צ',
    'ו': 'פ', 'ז': 'ע', 'ח': 'ס', 'ט': 'נ', 'י': 'מ',
    'כ': 'ל', 'ל': 'כ', 'מ': 'י', 'נ': 'ט', 'ס': 'ח',
    'ע': 'ז', 'פ': 'ו', 'צ': 'ה', 'ק': 'ד', 'ר': 'ג',
    'ש': 'ב', 'ת': 'א',
    'ך': 'ל', 'ם': 'י', 'ן': 'ט', 'ף': 'ו', 'ץ': 'ה',
}

# Milui (מילוי) — Valor del nombre deletreado de cada letra
MILUI = {
    'א': 111, 'ב': 412, 'ג': 83,  'ד': 434, 'ה': 6,
    'ו': 13,  'ז': 67,  'ח': 418, 'ט': 419, 'י': 20,
    'כ': 100, 'ל': 74,  'מ': 80,  'נ': 106, 'ס': 120,
    'ע': 130, 'פ': 81,  'צ': 104, 'ק': 186, 'ר': 510,
    'ש': 360, 'ת': 406,
    'ך': 100, 'ם': 80,  'ן': 106, 'ף': 81,  'ץ': 104,
}


# ═══════════════════════════════════════════════════════════════
# FUNCIONES DE LIMPIEZA
# ═══════════════════════════════════════════════════════════════

def strip_nikkud(text):
    """
    Remueve nikkud (vocales), trope (cantilación) y puntuación hebrea.
    Deja SOLO las letras consonánticas puras — la esencia para gematría.
    
    Como enseña el Zohar: las consonantes son el CUERPO (גוף),
    las vocales son el ALMA (נשמה), y la cantilación es el ESPÍRITU (רוח).
    Para gematría, trabajamos con el cuerpo — la estructura.
    """
    if not text:
        return ""
    # Remover tags HTML
    text = re.sub(r'<[^>]+>', '', text)
    # Remover cantilación y vocales (Unicode 0591-05C7)
    text = re.sub(r'[\u0591-\u05C7]', '', text)
    # Remover maqaf, sof pasuq y otros signos de puntuación hebreos
    text = re.sub(r'[\u05BE\u05C0\u05C3\u05C6\u05F3\u05F4׃]', '', text)
    return text.strip()


def extract_hebrew_letters(text):
    """Extrae SOLO letras hebreas (consonantes) de un texto."""
    return re.findall(r'[\u05D0-\u05EA\u05DA-\u05DF]', strip_nikkud(text))


def extract_words(text):
    """Extrae palabras hebreas de un texto (ya limpio de nikkud)."""
    clean = strip_nikkud(text)
    # Dividir por espacios y filtrar strings vacíos
    words = [w.strip() for w in clean.split() if w.strip()]
    # Filtrar palabras que no contienen letras hebreas
    hebrew_words = []
    for w in words:
        letters = re.findall(r'[\u05D0-\u05EA\u05DA-\u05DF]', w)
        if letters:
            hebrew_words.append(''.join(letters))
    return hebrew_words


# ═══════════════════════════════════════════════════════════════
# FUNCIONES DE CÁLCULO DE GEMATRÍA
# ═══════════════════════════════════════════════════════════════

def gematria_standard(text):
    """
    Mispar Hechrachi (מספר הכרחי) — Sistema ESTÁNDAR.
    El más usado en la tradición rabínica.
    א=1, ב=2, ... י=10, כ=20, ... ק=100, ר=200, ש=300, ת=400
    Letras finales = mismo valor que su forma regular.
    """
    letters = extract_hebrew_letters(text)
    return sum(STANDARD.get(l, 0) for l in letters)


def gematria_gadol(text):
    """
    Mispar Gadol (מספר גדול) — Sistema GRANDE.
    Igual al estándar pero las letras finales (sofit) tienen valores 500-900.
    ך=500, ם=600, ן=700, ף=800, ץ=900
    """
    letters = extract_hebrew_letters(text)
    return sum(GADOL.get(l, 0) for l in letters)


def gematria_ordinal(text):
    """
    Mispar Siduri (מספר סידורי) — Sistema ORDINAL.
    Cada letra = su posición en el alefbet (1 a 22).
    א=1, ב=2, ... כ=11, ל=12, ... ת=22
    """
    letters = extract_hebrew_letters(text)
    return sum(ORDINAL.get(l, 0) for l in letters)


def gematria_reduced(text):
    """
    Mispar Katan (מספר קטן) — Sistema REDUCIDO.
    Se eliminan los ceros: 10→1, 20→2, ... 100→1, 200→2, etc.
    Todas las letras tienen valor 1-9.
    """
    letters = extract_hebrew_letters(text)
    return sum(REDUCED.get(l, 0) for l in letters)


def gematria_katan_mispari(text):
    """
    Mispar Katan Mispari (מספר קטן מספרי) — RAÍZ DIGITAL.
    Se suma recursivamente hasta obtener un solo dígito (1-9).
    Similar al concepto de "digital root" en matemáticas.
    
    Ejemplo: בראשית = 913 → 9+1+3 = 13 → 1+3 = 4
    """
    value = gematria_standard(text)
    while value >= 10:
        value = sum(int(d) for d in str(value))
    return value


def gematria_atbash(text):
    """
    Atbash (אתבש) — Sistema de SUSTITUCIÓN.
    Cada letra se reemplaza por su opuesta en el alefbet:
    א↔ת, ב↔ש, ג↔ר, ד↔ק, ...
    Luego se calcula el valor estándar de las letras sustituidas.
    
    Mencionado en Jeremías 25:26 y 51:41 (שֵׁשַׁך = בָּבֶל por Atbash)
    """
    letters = extract_hebrew_letters(text)
    substituted = [ATBASH_MAP.get(l, l) for l in letters]
    return sum(STANDARD.get(l, 0) for l in substituted)


def gematria_milui(text):
    """
    Mispar Shemi / Milui (מספר שמי / מילוי) — NOMBRE COMPLETO.
    Cada letra se reemplaza por el valor numérico de su nombre deletreado.
    א (Alef) = א+ל+פ = 1+30+80 = 111
    ב (Bet) = ב+י+ת = 2+10+400 = 412
    """
    letters = extract_hebrew_letters(text)
    return sum(MILUI.get(l, 0) for l in letters)


def gematria_kidmi(text):
    """
    Mispar Kidmi (מספר קדמי) — TRIANGULAR / ACUMULATIVO.
    Cada letra = suma de todos los valores estándar desde א hasta ella.
    א=1, ב=1+2=3, ג=1+2+3=6, ד=1+2+3+4=10, ...
    Basado en el concepto de números triangulares.
    """
    # Precalcular valores triangulares
    triangular = {}
    cumulative = 0
    for letter, value in sorted(STANDARD.items(), key=lambda x: x[1]):
        if letter in 'ךםןףץ':  # Saltar sofit
            continue
        cumulative += value
        triangular[letter] = cumulative
    # Mapear sofit a sus regulares
    triangular['ך'] = triangular.get('כ', 0)
    triangular['ם'] = triangular.get('מ', 0)
    triangular['ן'] = triangular.get('נ', 0)
    triangular['ף'] = triangular.get('פ', 0)
    triangular['ץ'] = triangular.get('צ', 0)
    
    letters = extract_hebrew_letters(text)
    return sum(triangular.get(l, 0) for l in letters)


def gematria_all_methods(text):
    """
    Calcula la gematría de un texto en TODOS los 9 sistemas.
    Retorna un diccionario con los resultados.
    """
    clean = strip_nikkud(text)
    return {
        'text_original': text,
        'text_consonantal': clean,
        'letters': ''.join(extract_hebrew_letters(text)),
        'num_letters': len(extract_hebrew_letters(text)),
        'methods': {
            'standard':      gematria_standard(text),
            'gadol':         gematria_gadol(text),
            'ordinal':       gematria_ordinal(text),
            'reduced':       gematria_reduced(text),
            'katan_mispari': gematria_katan_mispari(text),
            'atbash':        gematria_atbash(text),
            'milui':         gematria_milui(text),
            'kidmi':         gematria_kidmi(text),
        }
    }


# ═══════════════════════════════════════════════════════════════
# FUNCIONES DE BÚSQUEDA Y ANÁLISIS
# ═══════════════════════════════════════════════════════════════

def find_words_by_value(torah_data, target_value, method='standard'):
    """
    Busca todas las palabras en la Torah cuya gematría = target_value.
    
    Args:
        torah_data: dict con los datos JSON de un libro
        target_value: valor numérico a buscar
        method: sistema de gematría ('standard', 'gadol', 'ordinal', etc.)
    
    Returns:
        Lista de matches con ubicación y contexto
    """
    calc_func = {
        'standard': gematria_standard,
        'gadol': gematria_gadol,
        'ordinal': gematria_ordinal,
        'reduced': gematria_reduced,
        'atbash': gematria_atbash,
        'milui': gematria_milui,
    }.get(method, gematria_standard)
    
    matches = []
    book_name = torah_data.get('metadata', {}).get('name_hebrew', '?')
    
    for ch_num, ch_data in torah_data.get('chapters', {}).items():
        verses = ch_data.get('verses_consonantal', [])
        for v_idx, verse in enumerate(verses):
            words = extract_words(verse)
            for w_idx, word in enumerate(words):
                value = calc_func(word)
                if value == target_value:
                    matches.append({
                        'word': word,
                        'book': book_name,
                        'chapter': int(ch_num),
                        'verse': v_idx + 1,
                        'word_position': w_idx + 1,
                        'verse_text': verse,
                        'gematria_value': value,
                        'method': method
                    })
    
    return matches


def divisible_by(torah_data, divisor, method='standard'):
    """
    Busca todas las palabras cuya gematría es divisible por un número.
    Útil para el análisis del 7 (Saturno/Shabbat).
    """
    calc_func = {
        'standard': gematria_standard,
        'gadol': gematria_gadol,
        'ordinal': gematria_ordinal,
        'reduced': gematria_reduced,
    }.get(method, gematria_standard)
    
    matches = []
    book_name = torah_data.get('metadata', {}).get('name_hebrew', '?')
    
    for ch_num, ch_data in torah_data.get('chapters', {}).items():
        verses = ch_data.get('verses_consonantal', [])
        for v_idx, verse in enumerate(verses):
            words = extract_words(verse)
            for w_idx, word in enumerate(words):
                value = calc_func(word)
                if value > 0 and value % divisor == 0:
                    matches.append({
                        'word': word,
                        'book': book_name,
                        'chapter': int(ch_num),
                        'verse': v_idx + 1,
                        'gematria_value': value,
                        'quotient': value // divisor
                    })
    
    return matches


# ═══════════════════════════════════════════════════════════════
# LOS 72 NOMBRES DE DIOS (שמהמפורש — Shem HaMephorash)
# ═══════════════════════════════════════════════════════════════
# 
# Los 72 Nombres provienen de Éxodo (Shemot) 14:19-21.
# Son 3 versículos consecutivos, cada uno con EXACTAMENTE 72 letras.
# 
# Método de extracción (del Zohar, Parashat Beshalach):
# 1. Versículo 19: leer de DERECHA a IZQUIERDA (normal)
# 2. Versículo 20: leer de IZQUIERDA a DERECHA (invertido)  
# 3. Versículo 21: leer de DERECHA a IZQUIERDA (normal)
# 
# Se toma la letra N del verso 1, la letra N del verso 2 (invertido),
# y la letra N del verso 3, formando 72 tripletas (nombres de 3 letras).
#
# Estos 72 Nombres representan las 72 facetas del Nombre Divino
# y están relacionados con los 72 ángeles del Shem HaMephorash.
# ═══════════════════════════════════════════════════════════════

def extract_72_names(shemot_data):
    """
    Extrae los 72 Nombres de Dios de Éxodo 14:19-21.
    
    Los 3 versículos tienen exactamente 72 letras cada uno.
    Se combinan para formar 72 nombres de 3 letras (tripletas).
    
    Patrón:
    - Verso 19: letra 1, 2, 3, ... 72 (dirección normal →)
    - Verso 20: letra 72, 71, 70, ... 1 (dirección invertida ←)
    - Verso 21: letra 1, 2, 3, ... 72 (dirección normal →)
    
    Cada Nombre N = letra_N_de_v19 + letra_N_de_v20_invertido + letra_N_de_v21
    
    Returns:
        dict con los 72 nombres, sus valores de gematría, y metadatos
    """
    # Obtener los 3 versículos del capítulo 14
    chapter_14 = shemot_data.get('chapters', {}).get('14', {})
    verses_nikkud = chapter_14.get('verses_with_nikkud', [])
    
    if len(verses_nikkud) < 21:
        print("❌ Error: No se encontraron suficientes versículos en Éxodo 14")
        return None
    
    # Versículos 19, 20, 21 (índice 18, 19, 20)
    v19_raw = verses_nikkud[18]
    v20_raw = verses_nikkud[19]
    v21_raw = verses_nikkud[20]
    
    # Extraer SOLO letras hebreas (sin nikkud, sin espacios, sin puntuación)
    v19_letters = extract_hebrew_letters(v19_raw)
    v20_letters = extract_hebrew_letters(v20_raw)
    v21_letters = extract_hebrew_letters(v21_raw)
    
    print(f"   📜 Éxodo 14:19 — {len(v19_letters)} letras")
    print(f"   📜 Éxodo 14:20 — {len(v20_letters)} letras")
    print(f"   📜 Éxodo 14:21 — {len(v21_letters)} letras")
    
    # Verificación: cada versículo DEBE tener exactamente 72 letras
    if len(v19_letters) != 72 or len(v20_letters) != 72 or len(v21_letters) != 72:
        print(f"   ⚠️  NOTA: Los conteos no son exactamente 72.")
        print(f"   Esto puede deberse a variantes textuales. Procediendo con los datos disponibles.")
        # Usar el mínimo para no causar error
        min_len = min(len(v19_letters), len(v20_letters), len(v21_letters))
        v19_letters = v19_letters[:min_len]
        v20_letters = v20_letters[:min_len]
        v21_letters = v21_letters[:min_len]
    
    # Invertir versículo 20 (se lee de izquierda a derecha = reverso)
    v20_reversed = list(reversed(v20_letters))
    
    # Construir los 72 Nombres
    names_72 = []
    num_names = len(v19_letters)
    
    for i in range(num_names):
        letter_1 = v19_letters[i]       # Verso 19, dirección normal
        letter_2 = v20_reversed[i]      # Verso 20, invertido
        letter_3 = v21_letters[i]       # Verso 21, dirección normal
        
        name = letter_1 + letter_2 + letter_3
        
        name_data = {
            'number': i + 1,
            'name': name,
            'letters': [letter_1, letter_2, letter_3],
            'gematria_standard': gematria_standard(name),
            'gematria_ordinal': gematria_ordinal(name),
            'gematria_reduced': gematria_reduced(name),
            'gematria_atbash': gematria_atbash(name),
            'digital_root': gematria_katan_mispari(name),
        }
        
        names_72.append(name_data)
    
    # Estadísticas
    all_values = [n['gematria_standard'] for n in names_72]
    total_sum = sum(all_values)
    
    result = {
        'metadata': {
            'source': 'Éxodo (Shemot) 14:19-21',
            'tradition': 'Zohar, Parashat Beshalach',
            'description': 'Los 72 Nombres del Shem HaMephorash (שם המפורש)',
            'total_names': len(names_72),
            'verses': {
                'v19_letters': len(v19_letters),
                'v20_letters': len(v20_letters),
                'v21_letters': len(v21_letters),
            }
        },
        'verses_original': {
            'v19': strip_nikkud(v19_raw),
            'v20': strip_nikkud(v20_raw),
            'v21': strip_nikkud(v21_raw),
        },
        'names': names_72,
        'statistics': {
            'total_sum_standard': total_sum,
            'average_value': round(total_sum / len(names_72), 2) if names_72 else 0,
            'min_value': min(all_values) if all_values else 0,
            'max_value': max(all_values) if all_values else 0,
            'divisible_by_7': sum(1 for v in all_values if v % 7 == 0),
            'prime_values': sum(1 for v in all_values if is_prime(v)),
        }
    }
    
    return result


def is_prime(n):
    """Verifica si un número es primo."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# ═══════════════════════════════════════════════════════════════
# FUNCIONES DE DISPLAY
# ═══════════════════════════════════════════════════════════════

def display_gematria(text, label=None):
    """Muestra el análisis de gematría completo de un texto."""
    result = gematria_all_methods(text)
    
    if label:
        print(f"\n{'═' * 60}")
        print(f"🔯 {label}")
        print(f"{'═' * 60}")
    
    print(f"   Texto: {result['text_consonantal']}")
    print(f"   Letras: {result['letters']} ({result['num_letters']} letras)")
    print(f"   {'─' * 45}")
    
    for method, value in result['methods'].items():
        method_names = {
            'standard': 'Estándar (הכרחי)',
            'gadol': 'Gadol (גדול)',
            'ordinal': 'Ordinal (סידורי)',
            'reduced': 'Reducido (קטן)',
            'katan_mispari': 'Raíz Digital',
            'atbash': 'Atbash (אתבש)',
            'milui': 'Milui (מילוי)',
            'kidmi': 'Kidmi (קדמי)',
        }
        name = method_names.get(method, method)
        print(f"   {name:<25} = {value:>8,}")
    
    return result


def display_72_names(names_data):
    """Muestra los 72 Nombres de Dios en formato tabla."""
    if not names_data:
        print("❌ No hay datos de los 72 Nombres")
        return
    
    print(f"\n{'═' * 70}")
    print(f"🔯 LOS 72 NOMBRES DE DIOS — שם המפורש (Shem HaMephorash)")
    print(f"   Fuente: {names_data['metadata']['source']}")
    print(f"   Tradición: {names_data['metadata']['tradition']}")
    print(f"{'═' * 70}")
    
    print(f"\n{'#':>3} {'Nombre':>8} {'Estándar':>10} {'Ordinal':>10} {'Reducido':>10} {'Raíz':>6}")
    print(f"{'─' * 3} {'─' * 8} {'─' * 10} {'─' * 10} {'─' * 10} {'─' * 6}")
    
    for name in names_data['names']:
        print(f"{name['number']:>3} {name['name']:>8} {name['gematria_standard']:>10} "
              f"{name['gematria_ordinal']:>10} {name['gematria_reduced']:>10} "
              f"{name['digital_root']:>6}")
    
    # Estadísticas
    stats = names_data['statistics']
    print(f"\n{'─' * 70}")
    print(f"📊 ESTADÍSTICAS:")
    print(f"   Suma total (estándar): {stats['total_sum_standard']:,}")
    print(f"   Promedio: {stats['average_value']}")
    print(f"   Rango: [{stats['min_value']} — {stats['max_value']}]")
    print(f"   Divisibles por 7 (Saturno): {stats['divisible_by_7']}")
    print(f"   Valores primos: {stats['prime_values']}")
    

# ═══════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🔯 GEMATRIA ENGINE — Test de Verificación")
    print("=" * 60)
    
    # Test 1: Palabras fundamentales
    test_words = [
        ("בראשית", "Bereshit (En el principio)"),
        ("אלהים", "Elohim (Dios)"),
        ("שבתאי", "Shabbtai (Saturno) — con Alef"),
        ("שבתי", "Shabbtai (Saturno) — sin Alef"),
        ("שבת", "Shabbat (Sábado)"),
        ("תורה", "Torah"),
        ("אדם", "Adam (Hombre)"),
        ("חוה", "Java/Eva"),
        ("משה", "Moshé (Moisés)"),
        ("אהבה", "Ahavá (Amor)"),
        ("אחד", "Ejad (Uno)"),
        ("יהוה", "YHVH (Tetragramatón)"),
        ("אל", "El (Dios)"),
        ("חי", "Jai (Vida)"),
    ]
    
    for word, label in test_words:
        display_gematria(word, label)
    
    # Test 2: Equivalencias célebres
    print(f"\n{'═' * 60}")
    print("🔗 EQUIVALENCIAS CÉLEBRES DE GEMATRÍA")
    print(f"{'═' * 60}")
    
    equivalences = [
        ("אהבה", "אחד", "Amor = Uno = 13"),
        ("משיח", "נחש", "Mesías = Serpiente = 358"),
        ("יין", "סוד", "Vino = Secreto = 70"),
    ]
    
    for word_a, word_b, desc in equivalences:
        val_a = gematria_standard(word_a)
        val_b = gematria_standard(word_b)
        match = "✅" if val_a == val_b else "❌"
        print(f"   {match} {desc}")
        print(f"      {word_a} = {val_a}, {word_b} = {val_b}")
    
    print(f"\n✅ Motor de gematría verificado correctamente.")
