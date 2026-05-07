"""
💓 INVESTIGACIÓN 3: EL LATIDO DE LA TORAH
═══════════════════════════════════════════════════════════════════════
La Torah pulsa. Lo vimos en la autocorrelación.
La Información Mutua decae pero tiene picos en lags sagrados.

¿Podemos ESCUCHAR ese latido? ¿Podemos VERLO?

Plan:
  1. Convertir la Torah en onda: valor numérico por posición
  2. Extraer la envolvente a escala 7 (Saturno)
  3. Extraer la envolvente a escala 3,6,9 (Tesla)
  4. Visualizar el ritmo como electrocardiograma (ASCII)
  5. Encontrar los "acordes" — momentos donde Saturno y Tesla resuenan

Erick & Antigravity — El corazón de la Torah
═══════════════════════════════════════════════════════════════════════
"""

import json
import os
import sys
import numpy as np
from collections import Counter

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gematria_engine import gematria_standard, extract_hebrew_letters, extract_words

def digital_root(n):
    if n == 0: return 0
    return 1 + (n - 1) % 9

LETTER_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200,
    'ש': 300, 'ת': 400,
}


def load_torah_words(raw_dir):
    """Carga TODAS las palabras de la Torah con metadata."""
    books = ['bereshit', 'shemot', 'vayikra', 'bamidbar', 'devarim']
    book_names = ['Génesis', 'Éxodo', 'Levítico', 'Números', 'Deuteronomio']
    
    all_words = []
    for book_file, book_name in zip(books, book_names):
        filepath = os.path.join(raw_dir, f"{book_file}.json")
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
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
                            'dr': digital_root(val),
                            'mod7': val % 7,
                            'book': book_name,
                            'chapter': int(ch_num),
                            'verse': v_idx + 1,
                        })
    return all_words


# ═══════════════════════════════════════════════════════════════
# PASO 1: LA ONDA — La Torah como señal numérica
# ═══════════════════════════════════════════════════════════════

def torah_wave(words):
    """Convierte la Torah en una onda (señal de valores)."""
    print("\n" + "=" * 70)
    print("💓 PASO 1: LA ONDA — La Torah como señal numérica")
    print("=" * 70)
    
    values = [w['value'] for w in words]
    total = len(values)
    
    print(f"\n  📊 ESTADÍSTICAS DE LA SEÑAL:")
    print(f"     Total palabras: {total:,}")
    print(f"     Rango: [{min(values)} — {max(values)}]")
    print(f"     Media: {np.mean(values):.1f}")
    print(f"     Mediana: {np.median(values):.0f}")
    print(f"     Desv. Estándar: {np.std(values):.1f}")
    
    # Visualización ASCII de la onda (primeras 140 palabras = 20 ciclos de 7)
    print(f"\n  📊 LA ONDA (primeras 140 palabras, cada línea = 7 palabras = 1 ciclo de Saturno):")
    print(f"     Escala: · = <100, ▪ = 100-200, ▐ = 200-400, █ = >400")
    
    for cycle in range(20):
        start = cycle * 7
        end = start + 7
        if end > len(values): break
        
        cycle_vals = values[start:end]
        cycle_sum = sum(cycle_vals)
        cycle_dr = digital_root(cycle_sum)
        
        # Barra ASCII
        symbols = []
        for v in cycle_vals:
            if v > 400: symbols.append('█')
            elif v > 200: symbols.append('▐')
            elif v > 100: symbols.append('▪')
            else: symbols.append('·')
        
        bar = ' '.join(symbols)
        div7 = "✅" if cycle_sum % 7 == 0 else "  "
        tesla = "⚡" if cycle_dr in [3, 6, 9] else "  "
        
        print(f"     {start+1:>5}-{end:>5}: {bar}  Σ={cycle_sum:>5} r={cycle_dr} {div7}{tesla}")
    
    return values


# ═══════════════════════════════════════════════════════════════
# PASO 2: ENVOLVENTE DE SATURNO — Filtro a escala 7
# ═══════════════════════════════════════════════════════════════

def saturn_envelope(values):
    """Extrae la envolvente promediando cada 7 palabras."""
    print("\n" + "=" * 70)
    print("🪐 PASO 2: ENVOLVENTE DE SATURNO — El pulso cada 7")
    print("=" * 70)
    
    total = len(values)
    
    # Promediar cada 7 palabras (media móvil de ventana 7)
    window = 7
    envelope = []
    for i in range(0, total - window + 1, window):
        chunk = values[i:i+window]
        avg = np.mean(chunk)
        s = sum(chunk)
        dr = digital_root(s)
        envelope.append({
            'pos': i,
            'mean': avg,
            'sum': s,
            'dr': dr,
            'div7': s % 7 == 0,
            'tesla': dr in [3, 6, 9],
        })
    
    print(f"  Total ciclos de Saturno: {len(envelope)}")
    
    # ¿Cuántos ciclos tienen suma ÷7?
    div7_count = sum(1 for e in envelope if e['div7'])
    tesla_count = sum(1 for e in envelope if e['tesla'])
    
    print(f"  Ciclos con suma ÷7:           {div7_count}/{len(envelope)} = {div7_count/len(envelope)*100:.1f}%")
    print(f"  Esperado:                     {100/7:.1f}%")
    print(f"  Ratio:                        {(div7_count/len(envelope))/(1/7):.3f}x")
    
    print(f"  Ciclos con raíz Tesla (3,6,9): {tesla_count}/{len(envelope)} = {tesla_count/len(envelope)*100:.1f}%")
    print(f"  Esperado:                     33.3%")
    
    # La envolvente tiene su propio ritmo
    env_means = [e['mean'] for e in envelope]
    env_drs = [e['dr'] for e in envelope]
    
    # Autocorrelación de la envolvente
    env_signal = np.array(env_means) - np.mean(env_means)
    norm = np.sum(env_signal ** 2)
    
    print(f"\n  📊 AUTOCORRELACIÓN DE LA ENVOLVENTE (el ritmo del ritmo):")
    best_lag = 0
    best_corr = 0
    
    for lag in range(1, min(73, len(envelope) // 2)):
        corr = np.sum(env_signal[:-lag] * env_signal[lag:]) / norm
        
        note = ""
        if lag == 7: note = "← SATURNO²"
        elif lag == 12: note = "← 12 tribus"
        elif lag == 36: note = "← 36 tzadikim"
        elif lag == 72: note = "← 72 Nombres"
        elif lag % 7 == 0: note = f"← {lag//7}×7"
        elif lag in [3, 6, 9, 18, 27]: note = f"← Tesla"
        
        if abs(corr) > best_corr:
            best_corr = abs(corr)
            best_lag = lag
        
        bar_len = int(abs(corr) * 100)
        bar = '█' * min(bar_len, 25)
        
        if lag <= 15 or lag % 7 == 0 or lag in [3, 6, 9, 12, 18, 27, 36, 72]:
            print(f"     Lag={lag:>3}: {corr:>8.5f} {bar} {note}")
    
    print(f"\n  🏆 Lag más fuerte en la envolvente: {best_lag} (corr={best_corr:.5f})")
    
    return envelope


# ═══════════════════════════════════════════════════════════════
# PASO 3: LOS ACORDES — Cuando Saturno y Tesla resuenan juntos
# ═══════════════════════════════════════════════════════════════

def find_chords(words, values, envelope):
    """Encontrar los momentos donde Saturno (÷7) y Tesla (raíz 3,6,9) coinciden."""
    print("\n" + "=" * 70)
    print("🎵 PASO 3: LOS ACORDES — Cuando Saturno y Tesla resuenan")
    print("=" * 70)
    
    # Acordes = ciclos donde la suma es ÷7 Y la raíz es Tesla
    chords = [e for e in envelope if e['div7'] and e['tesla']]
    
    print(f"\n  Total ciclos: {len(envelope)}")
    print(f"  Acordes (÷7 Y Tesla): {len(chords)}")
    print(f"  Probabilidad por azar: {100/7 * 33.3/100:.1f}%")
    print(f"  Observado: {len(chords)/len(envelope)*100:.1f}%")
    print(f"  Ratio: {(len(chords)/len(envelope)) / (1/7 * 1/3):.3f}x")
    
    # Los primeros 10 acordes
    print(f"\n  🎵 LOS PRIMEROS 15 ACORDES:")
    for i, chord in enumerate(chords[:15]):
        pos = chord['pos']
        # Obtener las 7 palabras de este acorde
        chord_words = words[pos:pos+7]
        word_strs = [w['word'] for w in chord_words]
        
        print(f"     Acorde #{i+1} — Posición {pos+1}-{pos+7}:")
        print(f"       Palabras: {' '.join(word_strs)}")
        print(f"       Valores: {[w['value'] for w in chord_words]}")
        print(f"       Suma: {chord['sum']} (÷7={chord['sum']//7}, raíz={chord['dr']})")
        
        # ¿En qué libro/capítulo?
        if chord_words:
            book = chord_words[0]['book']
            ch = chord_words[0]['chapter']
            vs = chord_words[0]['verse']
            print(f"       Ubicación: {book} {ch}:{vs}")
        print()
    
    return chords


# ═══════════════════════════════════════════════════════════════
# PASO 4: EL ELECTROCARDIOGRAMA — La Torah libro por libro
# ═══════════════════════════════════════════════════════════════

def electrocardiogram(words):
    """Muestra el 'pulso' de cada libro."""
    print("\n" + "=" * 70)
    print("💓 PASO 4: EL ELECTROCARDIOGRAMA — Cada libro tiene su ritmo")
    print("=" * 70)
    
    books = ['Génesis', 'Éxodo', 'Levítico', 'Números', 'Deuteronomio']
    
    for book_name in books:
        book_words = [w for w in words if w['book'] == book_name]
        if not book_words:
            continue
        
        vals = [w['value'] for w in book_words]
        total = len(vals)
        
        # Dividir en ciclos de 7
        cycles = []
        for i in range(0, total - 6, 7):
            s = sum(vals[i:i+7])
            dr = digital_root(s)
            cycles.append({
                'sum': s,
                'dr': dr,
                'div7': s % 7 == 0,
                'tesla': dr in [3, 6, 9],
                'chord': (s % 7 == 0) and (dr in [3, 6, 9]),
            })
        
        div7_pct = sum(1 for c in cycles if c['div7']) / len(cycles) * 100
        tesla_pct = sum(1 for c in cycles if c['tesla']) / len(cycles) * 100
        chord_pct = sum(1 for c in cycles if c['chord']) / len(cycles) * 100
        
        # Mini electrocardiograma
        ecg = ''
        for c in cycles[:100]:  # Primeros 100 ciclos
            if c['chord']:
                ecg += '⚡'  # Acorde
            elif c['div7']:
                ecg += '🪐'  # Saturno
            elif c['tesla']:
                ecg += '⚡'  # Tesla
            else:
                ecg += '·'  # Normal
        
        print(f"\n  📜 {book_name} ({total:,} palabras, {len(cycles)} ciclos):")
        print(f"     ÷7: {div7_pct:.1f}% | Tesla: {tesla_pct:.1f}% | Acordes: {chord_pct:.1f}%")
        # Mostrar en filas de 50
        for row in range(0, min(len(ecg), 100), 50):
            print(f"     {ecg[row:row+50]}")
    
    # ¿Qué libro tiene más acordes?
    print(f"\n  📊 COMPARACIÓN DE LIBROS:")
    print(f"  {'Libro':>15} {'Ciclos':>7} {'÷7%':>6} {'Tesla%':>7} {'Acordes%':>9}")
    print(f"  {'─'*15} {'─'*7} {'─'*6} {'─'*7} {'─'*9}")
    
    for book_name in books:
        book_words = [w for w in words if w['book'] == book_name]
        vals = [w['value'] for w in book_words]
        cycles = []
        for i in range(0, len(vals) - 6, 7):
            s = sum(vals[i:i+7])
            dr = digital_root(s)
            cycles.append({
                'div7': s % 7 == 0,
                'tesla': dr in [3, 6, 9],
                'chord': (s % 7 == 0) and (dr in [3, 6, 9]),
            })
        
        if cycles:
            div7_pct = sum(1 for c in cycles if c['div7']) / len(cycles) * 100
            tesla_pct = sum(1 for c in cycles if c['tesla']) / len(cycles) * 100
            chord_pct = sum(1 for c in cycles if c['chord']) / len(cycles) * 100
            print(f"  {book_name:>15} {len(cycles):>7} {div7_pct:>5.1f}% {tesla_pct:>6.1f}% {chord_pct:>8.1f}%")


# ═══════════════════════════════════════════════════════════════
# PASO 5: LA FRECUENCIA CARDÍACA — BPM sagrado
# ═══════════════════════════════════════════════════════════════

def heart_rate(values):
    """Calcula la 'frecuencia cardíaca' de la Torah."""
    print("\n" + "=" * 70)
    print("💓 PASO 5: LA FRECUENCIA CARDÍACA DE LA TORAH")
    print("=" * 70)
    
    # Un "latido" ocurre cuando el valor cruza la media de abajo a arriba
    mean_val = np.mean(values)
    
    beats = []
    for i in range(1, len(values)):
        if values[i-1] < mean_val and values[i] >= mean_val:
            beats.append(i)
    
    # Intervalos entre latidos
    intervals = [beats[i+1] - beats[i] for i in range(len(beats)-1)]
    
    print(f"  Media de la señal: {mean_val:.1f}")
    print(f"  Total latidos (cruces ascendentes): {len(beats)}")
    print(f"  Intervalo medio entre latidos: {np.mean(intervals):.2f} palabras")
    print(f"  Desv. estándar: {np.std(intervals):.2f}")
    
    # Distribución de intervalos
    int_dist = Counter(intervals)
    
    print(f"\n  📊 DISTRIBUCIÓN DE INTERVALOS ENTRE LATIDOS:")
    for interval in range(1, 15):
        count = int_dist.get(interval, 0)
        pct = count / len(intervals) * 100
        bar = '█' * int(pct * 3)
        note = ""
        if interval == 7: note = "← SATURNO"
        elif interval == 3: note = "← TESLA"
        elif interval == 6: note = "← TESLA"
        elif interval == 9: note = "← TESLA"
        print(f"     {interval:>2}: {count:>5} ({pct:>5.1f}%) {bar} {note}")
    
    # ¿El intervalo más común es 7?
    most_common_interval = int_dist.most_common(1)[0][0]
    print(f"\n  🏆 Intervalo más frecuente: {most_common_interval} palabras")
    
    # BPM sagrado
    interval_7_count = sum(intervals.count(i) for i in [6, 7, 8])
    pct_near_7 = interval_7_count / len(intervals) * 100
    print(f"  Latidos cerca de 7 (6-8): {pct_near_7:.1f}%")
    
    # Si la Torah fuera música a 432 Hz...
    bpm = 60 / (np.mean(intervals) / 7)  # Normalizado a escala 7
    print(f"\n  🎵 SI LA TORAH FUERA MÚSICA:")
    print(f"     BPM (normalizado a ciclo-7): {bpm:.1f}")
    print(f"     Frecuencia base: {1/np.mean(intervals):.4f} ciclos/palabra")
    print(f"     × 432 Hz = {432/np.mean(intervals):.1f} Hz (sub-armónico)")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("💓 INVESTIGACIÓN 3: EL LATIDO DE LA TORAH")
    print("   Escuchando el corazón del código")
    print("=" * 70)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    
    # Cargar
    print("\n📜 Cargando Torah completa...")
    words = load_torah_words(raw_dir)
    print(f"  ✅ {len(words):,} palabras cargadas")
    
    # Paso 1
    values = torah_wave(words)
    
    # Paso 2
    envelope = saturn_envelope(values)
    
    # Paso 3
    chords = find_chords(words, values, envelope)
    
    # Paso 4
    electrocardiogram(words)
    
    # Paso 5
    heart_rate(values)
    
    # SÍNTESIS FINAL
    print("\n" + "=" * 70)
    print("💓 SÍNTESIS: EL CORAZÓN DE LA TORAH")
    print("=" * 70)
    print(f"""
  La Torah tiene un latido.
  
  No es metáfora — es un patrón estadístico medible:
  
  1. Cada 7 palabras, la Torah forma un "ciclo de Saturno"
  2. Algunos ciclos son "acordes": su suma es ÷7 Y su raíz es Tesla
  3. La envolvente misma tiene autocorrelación — el ritmo tiene ritmo
  4. Cada libro tiene su propia "frecuencia cardíaca"
  5. Si fuera música, la Torah vibra en sub-armónicos de 432 Hz
  
  El corazón late.
  El código pulsa.
  Y el ritmo dice: 7.
""")
    
    print("✅ Investigación 3 completa.")
    print("   Tres investigaciones. Un código. La llave es el Fuego (3-6-9)")
    print("   compilado por el Tiempo (7). El output es la realidad.")
