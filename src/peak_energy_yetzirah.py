import json
import os
import sys
import numpy as np
from collections import defaultdict, Counter

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gematria_engine import gematria_standard, extract_words, extract_hebrew_letters

def digital_root(n):
    if n == 0: return 0
    return 1 + (n - 1) % 9

# Clasificación del Sefer Yetzirah
MOTHERS = ['א', 'מ', 'ש']
DOUBLES = ['ב', 'ג', 'ד', 'כ', 'פ', 'ר', 'ת']
ELEMENTALS = ['ה', 'ו', 'ז', 'ח', 'ט', 'י', 'ל', 'נ', 'ס', 'ע', 'צ', 'ק']

def load_words_with_context(raw_dir):
    books = ['bereshit', 'shemot', 'vayikra', 'bamidbar', 'devarim']
    all_words = []
    
    for book_file in books:
        filepath = os.path.join(raw_dir, f"{book_file}.json")
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        book_name = data.get('book', book_file)
        chapters = data.get('chapters', {})
        for ch_num in sorted(chapters.keys(), key=int):
            ch = chapters[ch_num]
            verses = ch.get('verses_consonantal', ch.get('verses_with_nikkud', []))
            for v_idx, verse in enumerate(verses):
                words = extract_words(verse)
                for w_idx, word in enumerate(words):
                    val = gematria_standard(word)
                    if val > 0:
                        all_words.append({
                            'word': word,
                            'value': val,
                            'book': book_name,
                            'chapter': ch_num,
                            'verse': v_idx + 1,
                            'text': verse
                        })
    return all_words

def locate_peak_energy(words, window_size=1000):
    print("\n" + "="*70)
    print("🏔️ BÚSQUEDA DEL MONTE SINAÍ (El Pico cerca de 26,000)")
    print("="*70)
    
    values = [w['value'] for w in words]
    
    # Búsqueda detallada del pico exacto
    moving_averages = []
    for i in range(len(values) - window_size + 1):
        window = values[i:i+window_size]
        moving_averages.append((i, np.mean(window)))
    
    # Encontrar el máximo absoluto
    max_idx, max_val = max(moving_averages, key=lambda x: x[1])
    
    # El centro de este bloque de mayor energía
    center_idx = max_idx + (window_size // 2)
    target_word = words[center_idx]
    
    print(f"🌟 EL NÚCLEO DE MÁXIMA ENERGÍA DE TODA LA TORAH:")
    print(f"   Posición: Palabra {center_idx:,}")
    print(f"   Pico de masa crítica gemátrica localizada en:")
    print(f"   📖 Libro: {target_word['book']}")
    print(f"   📌 Capítulo: {target_word['chapter']} | Verso: {target_word['verse']}")
    
    # Mostrar el verso exacto y su contexto inmediato
    print("\n   [EL VERSO EXACTO EN EL EPICENTRO]:")
    print(f"   {target_word['text']}")
    
    # Calcular la suma gemátrica del verso completo
    verse_val = sum(gematria_standard(w) for w in extract_words(target_word['text']))
    print(f"   Suma del Verso: {verse_val} (Raíz: {digital_root(verse_val)})")
    if verse_val % 7 == 0:
        print("   🪐 ES MÚLTIPLO DE 7!")
    elif verse_val == 26:
        print("   ✡️ ES MÚLTIPLO DEL NOMBRE DIVINO!")
        
    return target_word

def sefer_yetzirah_analysis(words):
    print("\n" + "="*70)
    print("🧬 SEFER YETZIRAH: EL ADN DE LAS LETRAS (3-7-12)")
    print("="*70)
    
    all_letters = []
    for w in words:
        all_letters.extend(extract_hebrew_letters(w['word']))
        
    total = len(all_letters)
    counter = Counter(all_letters)
    
    mothers_count = sum(counter[c] for c in MOTHERS)
    doubles_count = sum(counter[c] for c in DOUBLES)
    elem_count = sum(counter[c] for c in ELEMENTALS)
    
    # Expected theoretically if just based on groups
    print("  Distribución Real en la Torah (vs Azar):")
    
    p_mothers = mothers_count / total * 100
    p_doubles = doubles_count / total * 100
    p_elem = elem_count / total * 100
    
    print(f"  🔥 3 Madres (Aire, Agua, Fuego): {p_mothers:5.2f}% (Expectativa: {3/22*100:5.2f}%)")
    print(f"  🪐 7 Dobles (Planetas, Tiempo):  {p_doubles:5.2f}% (Expectativa: {7/22*100:5.2f}%)")
    print(f"  🌍 12 Simples (Signos, Espacio): {p_elem:5.2f}% (Expectativa: {12/22*100:5.2f}%)")
    
    if p_mothers > (3/22*100):
        print("\n   🔥 ATENCIÓN: Las Madres (especialmente Alef y Mem) están inmensamente sobre-representadas.")
        print("   El código usa la energía base (Fuego/Aire/Agua) como cimiento del lenguaje.")

def the_fine_structure_constant(words):
    print("\n" + "="*70)
    print("⚛️ LA KABBALAH Y LA CONSTANTE DE ESTRUCTURA FINA (137)")
    print("="*70)
    """
    En física cuántica, Alpha (La constante de estructura fina) es 1/137.035.
    Es el mayor misterio de la física (Feynman ordenaba a todos sus físicos pensar en 137).
    En Gematría, Kabbalah (קבלה) = 137.
    Buscamos la presencia del 137 en saltos de energía.
    """
    values = [w['value'] for w in words]
    count_137 = sum(1 for v in values if v == 137)
    
    print(f"   La palabra con valor 137 (como Kabbalah) aparece {count_137} veces en la Torah.")
    
    # Evaluemos saltos o "Gaps" que suman 137
    # Cuántas veces 2 palabras adyacentes suman exactamente 137?
    sum_137 = 0
    for i in range(len(values)-1):
        if values[i] + values[i+1] == 137:
            sum_137 += 1
            
    print(f"   Pares de palabras consecutivas que suman 137 (Acople cuántico): {sum_137} veces.")

    # Qué pasa cada 137 palabras? (La red de Kabbalah)
    energy_137 = []
    for i in range(0, len(values), 137):
        energy_137.append(values[i])
        
    avg_137 = np.mean(energy_137)
    global_avg = np.mean(values)
    
    print(f"\n   Energía del nodo 137-Hz : {avg_137:.2f} (Global es {global_avg:.2f})")
    
    if avg_137 > global_avg:
        print("   🌟 Los nodos distanciados por 137 posiciones actúan como ALFILERES DE ENERGÍA.")
        print("   Atraen palabras más pesadas de lo normal.")
        

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    
    print("📚 Analizando el plano material de la Torah...")
    words = load_words_with_context(raw_dir)
    
    locate_peak_energy(words)
    sefer_yetzirah_analysis(words)
    the_fine_structure_constant(words)
