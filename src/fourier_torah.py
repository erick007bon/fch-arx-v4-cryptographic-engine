"""
🌀 FOURIER TORAH — Análisis de Frecuencias Ocultas en la Torah
═══════════════════════════════════════════════════════════════════════
La Torah como SEÑAL NUMÉRICA.

Si la Torah fuera texto aleatorio, su espectro de Fourier sería ruido blanco.
Si tiene estructura matemática oculta, la FFT revelará frecuencias dominantes:
la "melodía" matemática del texto sagrado.

Método:
1. Convertir cada letra hebrea a su valor de gematría
2. Crear una señal numérica continua (304,805 puntos)
3. Aplicar FFT (Fast Fourier Transform)
4. Identificar picos (frecuencias dominantes)
5. Comparar con texto aleatorio (Monte Carlo)

Autor: Erick Reinaldo Flores Zambrano
Proyecto: 08_gematria_torah
═══════════════════════════════════════════════════════════════════════
"""

import json
import os
import sys
import numpy as np
from collections import Counter
import csv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Import our gematria engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gematria_engine import STANDARD, extract_hebrew_letters, strip_nikkud

# ═══════════════════════════════════════════════════════════════
# PASO 1: CONVERTIR LA TORAH EN UNA SEÑAL NUMÉRICA
# ═══════════════════════════════════════════════════════════════

def torah_to_signal(data_dir):
    """
    Lee los 5 libros de la Torah y convierte CADA LETRA a su valor de gematría.
    Retorna un array numpy con ~304,805 valores (uno por letra).
    """
    books = ['bereshit', 'shemot', 'vayikra', 'bamidbar', 'devarim']
    book_names = ['Génesis', 'Éxodo', 'Levítico', 'Números', 'Deuteronomio']
    
    all_values = []
    book_boundaries = []  # Dónde empieza cada libro
    
    for book_file, book_name in zip(books, book_names):
        filepath = os.path.join(data_dir, f"{book_file}.json")
        if not os.path.exists(filepath):
            print(f"  ⚠️  Archivo no encontrado: {filepath}")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        book_start = len(all_values)
        book_letters = 0
        
        chapters = data.get('chapters', {})
        for ch_num in sorted(chapters.keys(), key=int):
            ch = chapters[ch_num]
            verses = ch.get('verses_consonantal', ch.get('verses_with_nikkud', []))
            for verse in verses:
                letters = extract_hebrew_letters(verse)
                for letter in letters:
                    val = STANDARD.get(letter, 0)
                    if val > 0:
                        all_values.append(val)
                        book_letters += 1
        
        book_boundaries.append({
            'name': book_name,
            'hebrew': book_file,
            'start': book_start,
            'end': len(all_values),
            'letters': book_letters
        })
        print(f"  📜 {book_name}: {book_letters:,} letras")
    
    signal = np.array(all_values, dtype=np.float64)
    print(f"\n  ✅ Señal total: {len(signal):,} puntos (letras)")
    return signal, book_boundaries


def torah_to_word_signal(data_dir):
    """
    Versión por PALABRAS: cada punto = gematría de una palabra completa.
    Retorna ~68,484 valores.
    """
    books = ['bereshit', 'shemot', 'vayikra', 'bamidbar', 'devarim']
    
    all_values = []
    
    for book_file in books:
        filepath = os.path.join(data_dir, f"{book_file}.json")
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chapters = data.get('chapters', {})
        for ch_num in sorted(chapters.keys(), key=int):
            ch = chapters[ch_num]
            verses = ch.get('verses_consonantal', ch.get('verses_with_nikkud', []))
            for verse in verses:
                clean = strip_nikkud(verse)
                words = [w.strip() for w in clean.split() if w.strip()]
                for word in words:
                    letters = extract_hebrew_letters(word)
                    val = sum(STANDARD.get(l, 0) for l in letters)
                    if val > 0:
                        all_values.append(val)
    
    return np.array(all_values, dtype=np.float64)


# ═══════════════════════════════════════════════════════════════
# PASO 2: FFT — FAST FOURIER TRANSFORM
# ═══════════════════════════════════════════════════════════════

def compute_fft(signal, label="Señal"):
    """
    Aplica FFT a la señal y retorna las frecuencias y magnitudes.
    """
    N = len(signal)
    
    # Normalizar (restar media para eliminar componente DC)
    signal_centered = signal - np.mean(signal)
    
    # FFT
    fft_vals = np.fft.rfft(signal_centered)
    magnitudes = np.abs(fft_vals) / N
    frequencies = np.fft.rfftfreq(N)  # Frecuencias normalizadas (0 a 0.5)
    periods = np.zeros_like(frequencies)
    periods[1:] = 1.0 / frequencies[1:]  # Períodos (en # de letras/palabras)
    
    # Encontrar picos dominantes (excluyendo DC, freq=0)
    mag_no_dc = magnitudes[1:].copy()
    freq_no_dc = frequencies[1:]
    period_no_dc = periods[1:]
    
    # Top 20 picos
    top_indices = np.argsort(mag_no_dc)[-20:][::-1]
    
    peaks = []
    for idx in top_indices:
        peaks.append({
            'frequency': float(freq_no_dc[idx]),
            'period': float(period_no_dc[idx]),
            'magnitude': float(mag_no_dc[idx]),
            'rank': len(peaks) + 1
        })
    
    print(f"\n  📊 FFT de {label}:")
    print(f"     Media: {np.mean(signal):.2f}")
    print(f"     Desv. estándar: {np.std(signal):.2f}")
    print(f"     Puntos: {N:,}")
    print(f"\n     🔝 TOP 10 FRECUENCIAS DOMINANTES:")
    print(f"     {'#':>3} {'Frecuencia':>12} {'Período':>12} {'Magnitud':>12}")
    print(f"     {'─'*3} {'─'*12} {'─'*12} {'─'*12}")
    for p in peaks[:10]:
        print(f"     {p['rank']:>3} {p['frequency']:>12.6f} {p['period']:>12.1f} {p['magnitude']:>12.4f}")
    
    return {
        'frequencies': frequencies,
        'magnitudes': magnitudes,
        'periods': periods,
        'peaks': peaks,
        'mean': float(np.mean(signal)),
        'std': float(np.std(signal)),
        'N': N
    }


# ═══════════════════════════════════════════════════════════════
# PASO 3: COMPARAR CON TEXTO ALEATORIO (MONTE CARLO)
# ═══════════════════════════════════════════════════════════════

def monte_carlo_comparison(torah_signal, n_simulations=100):
    """
    Genera n_simulations textos aleatorios con la MISMA distribución de letras
    que la Torah, y compara sus espectros FFT.
    
    Si la Torah tiene estructura, sus picos serán significativamente más altos
    que los de textos aleatorios con la misma distribución.
    """
    N = len(torah_signal)
    
    # Distribución de frecuencias de la Torah
    letter_freq = Counter(torah_signal.astype(int))
    values = list(letter_freq.keys())
    probs = np.array([letter_freq[v] for v in values], dtype=np.float64)
    probs /= probs.sum()
    
    # FFT de la Torah
    torah_centered = torah_signal - np.mean(torah_signal)
    torah_fft = np.abs(np.fft.rfft(torah_centered)) / N
    torah_max_peak = np.max(torah_fft[1:])  # Excluir DC
    
    # Top 5 frecuencias de la Torah
    torah_top_indices = np.argsort(torah_fft[1:])[-5:][::-1] + 1
    
    print(f"\n  🎲 Monte Carlo: {n_simulations} simulaciones de texto aleatorio")
    print(f"     (misma distribución de letras, N={N:,})")
    
    random_max_peaks = []
    random_top_values = [[] for _ in range(5)]  # Para las top 5 frecuencias
    
    for i in range(n_simulations):
        # Generar texto aleatorio con misma distribución
        random_signal = np.random.choice(values, size=N, p=probs).astype(np.float64)
        random_centered = random_signal - np.mean(random_signal)
        random_fft = np.abs(np.fft.rfft(random_centered)) / N
        
        random_max_peaks.append(np.max(random_fft[1:]))
        
        for j, idx in enumerate(torah_top_indices):
            if idx < len(random_fft):
                random_top_values[j].append(random_fft[idx])
        
        if (i + 1) % 20 == 0:
            print(f"     ... {i + 1}/{n_simulations}")
    
    random_max_peaks = np.array(random_max_peaks)
    
    # P-value: ¿cuántas simulaciones tienen pico >= Torah?
    p_value = np.mean(random_max_peaks >= torah_max_peak)
    z_score = (torah_max_peak - np.mean(random_max_peaks)) / np.std(random_max_peaks)
    
    print(f"\n  📊 RESULTADOS MONTE CARLO:")
    print(f"     Pico máximo Torah:    {torah_max_peak:.6f}")
    print(f"     Pico máximo aleatorio: {np.mean(random_max_peaks):.6f} ± {np.std(random_max_peaks):.6f}")
    print(f"     Z-score:              {z_score:.2f}")
    print(f"     P-value:              {p_value:.6f}")
    
    if z_score > 3:
        print(f"     ✅ SIGNIFICATIVO: La Torah tiene estructura NO aleatoria (z={z_score:.1f})")
    elif z_score > 2:
        print(f"     ⚠️  PROBABLEMENTE significativo (z={z_score:.1f})")
    else:
        print(f"     ❌ No significativo (z={z_score:.1f})")
    
    # Análisis por frecuencia
    print(f"\n     📈 Análisis por frecuencia dominante:")
    print(f"     {'Freq':>8} {'Período':>10} {'Torah':>10} {'Random':>10} {'Z-score':>10} {'Significativo':>14}")
    print(f"     {'─'*8} {'─'*10} {'─'*10} {'─'*10} {'─'*10} {'─'*14}")
    
    freq_results = []
    freqs = np.fft.rfftfreq(N)
    for j, idx in enumerate(torah_top_indices):
        if idx < len(freqs):
            rv = np.array(random_top_values[j])
            if len(rv) > 0 and np.std(rv) > 0:
                z = (torah_fft[idx] - np.mean(rv)) / np.std(rv)
                period = 1.0 / freqs[idx] if freqs[idx] > 0 else float('inf')
                sig = "✅ SI" if z > 3 else ("⚠️ Prob." if z > 2 else "❌ No")
                print(f"     {freqs[idx]:>8.6f} {period:>10.1f} {torah_fft[idx]:>10.6f} {np.mean(rv):>10.6f} {z:>10.2f} {sig:>14}")
                freq_results.append({'freq': float(freqs[idx]), 'period': period, 'z_score': float(z)})
    
    return {
        'torah_max_peak': float(torah_max_peak),
        'random_mean_peak': float(np.mean(random_max_peaks)),
        'random_std_peak': float(np.std(random_max_peaks)),
        'z_score': float(z_score),
        'p_value': float(p_value),
        'n_simulations': n_simulations,
        'freq_analysis': freq_results
    }


# ═══════════════════════════════════════════════════════════════
# PASO 4: ANÁLISIS DE PERIODICIDADES SAGRADAS
# ═══════════════════════════════════════════════════════════════

def check_sacred_periodicities(signal, fft_result):
    """
    Verifica si las frecuencias dominantes corresponden a números sagrados:
    7 (Shabbat), 22 (letras), 26 (YHVH), 72 (Nombres), 
    42 (nombre de 42 letras), 50 (Jubileo), 49 (7x7)
    """
    N = len(signal)
    sacred_periods = {
        7: 'Shabbat / 7 días',
        22: '22 letras del alefbet',
        26: 'YHVH (יהוה)',
        42: 'Nombre de 42 letras (Ana Bekoach)',
        49: '7×7 (Sefirot del Omer)',
        50: 'Jubileo (50 años)',
        72: '72 Nombres de Dios',
        248: '248 mandamientos positivos',
        365: '365 mandamientos negativos',
        304805: 'Total de letras en la Torah',
    }
    
    freqs = fft_result['frequencies']
    mags = fft_result['magnitudes']
    
    # Media y desviación de las magnitudes (sin DC)
    mag_no_dc = mags[1:]
    mean_mag = np.mean(mag_no_dc)
    std_mag = np.std(mag_no_dc)
    
    print(f"\n  🔯 PERIODICIDADES SAGRADAS:")
    print(f"     Magnitud media: {mean_mag:.6f}")
    print(f"     Desviación estándar: {std_mag:.6f}")
    print(f"\n     {'Período':>8} {'Significado':>35} {'Magnitud':>10} {'Z-score':>8} {'Estado':>12}")
    print(f"     {'─'*8} {'─'*35} {'─'*10} {'─'*8} {'─'*12}")
    
    results = []
    for period, meaning in sorted(sacred_periods.items()):
        if period <= 1 or period >= N // 2:
            continue
        # Frecuencia correspondiente
        target_freq = 1.0 / period
        # Encontrar el índice más cercano
        freq_idx = np.argmin(np.abs(freqs - target_freq))
        
        if freq_idx > 0 and freq_idx < len(mags):
            mag = mags[freq_idx]
            z = (mag - mean_mag) / std_mag if std_mag > 0 else 0
            
            if z > 5:
                status = "🔥 FUERTE"
            elif z > 3:
                status = "✅ Signif."
            elif z > 2:
                status = "⚠️ Débil"
            else:
                status = "─ Normal"
            
            print(f"     {period:>8} {meaning:>35} {mag:>10.6f} {z:>8.2f} {status:>12}")
            results.append({'period': period, 'meaning': meaning, 'magnitude': float(mag), 'z_score': float(z)})
    
    return results


# ═══════════════════════════════════════════════════════════════
# PASO 5: AUTOCORRELACIÓN
# ═══════════════════════════════════════════════════════════════

def compute_autocorrelation(signal, max_lag=500):
    """
    Calcula la autocorrelación de la señal para diferentes lags.
    Si la Torah tiene periodicidad, habrá picos en la autocorrelación
    en los múltiplos del período.
    """
    N = len(signal)
    signal_centered = signal - np.mean(signal)
    variance = np.var(signal_centered)
    
    if variance == 0:
        return {}
    
    autocorr = []
    for lag in range(1, min(max_lag + 1, N // 2)):
        corr = np.sum(signal_centered[:N-lag] * signal_centered[lag:]) / ((N - lag) * variance)
        autocorr.append({'lag': lag, 'correlation': float(corr)})
    
    # Top 10 autocorrelaciones
    autocorr_sorted = sorted(autocorr, key=lambda x: abs(x['correlation']), reverse=True)
    
    print(f"\n  📈 AUTOCORRELACIÓN (top 10 lags de 1 a {max_lag}):")
    print(f"     {'Lag':>6} {'Correlación':>14} {'Significado (si aplica)':>30}")
    print(f"     {'─'*6} {'─'*14} {'─'*30}")
    
    sacred_lags = {7:'Shabbat', 22:'Alefbet', 26:'YHVH', 42:'Ana Bekoach', 49:'7x7', 50:'Jubileo', 72:'72 Nombres'}
    
    for item in autocorr_sorted[:10]:
        meaning = sacred_lags.get(item['lag'], '')
        star = '⭐' if abs(item['correlation']) > 0.05 else ''
        print(f"     {item['lag']:>6} {item['correlation']:>14.6f} {meaning:>26} {star}")
    
    # Específicamente mirar lags sagrados
    print(f"\n     🔯 Lags en números sagrados:")
    for lag, meaning in sorted(sacred_lags.items()):
        ac_item = next((a for a in autocorr if a['lag'] == lag), None)
        if ac_item:
            r = ac_item['correlation']
            sig = "✅" if abs(r) > 0.01 else "─"
            print(f"     {lag:>6} = {meaning:>15}: r={r:>10.6f} {sig}")
    
    return autocorr


# ═══════════════════════════════════════════════════════════════
# PASO 6: GENERAR VISUALIZACIONES
# ═══════════════════════════════════════════════════════════════

def generate_visualizations(signal, fft_result, book_boundaries, output_dir):
    """Genera gráficas del espectro y la señal."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.rcParams['font.size'] = 10
    except ImportError:
        print("  ⚠️  matplotlib no disponible. Saltando visualizaciones.")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    # === 1. LA SEÑAL (la Torah como onda) ===
    fig, axes = plt.subplots(2, 1, figsize=(16, 8), facecolor='#0a0a1a')
    
    # Señal completa (subsampled para velocidad)
    ax1 = axes[0]
    ax1.set_facecolor('#0a0a1a')
    step = max(1, len(signal) // 5000)
    x = np.arange(0, len(signal), step)
    y = signal[::step]
    ax1.plot(x, y, color='#FFD700', alpha=0.3, linewidth=0.3)
    # Media móvil
    window = 1000
    if len(signal) > window:
        moving_avg = np.convolve(signal, np.ones(window)/window, mode='valid')
        ax1.plot(np.arange(len(moving_avg)), moving_avg, color='#00E5FF', linewidth=1.2, label=f'Media móvil ({window} letras)')
    
    # Marcar límites de libros
    colors_books = ['#FF4444', '#FFD700', '#00E676', '#BB86FC', '#00E5FF']
    for i, bb in enumerate(book_boundaries):
        ax1.axvline(bb['start'], color=colors_books[i], alpha=0.5, linewidth=1, linestyle='--')
        ax1.text(bb['start'] + 1000, np.max(signal)*0.95, bb['name'], color=colors_books[i], fontsize=9, fontweight='bold')
    
    ax1.set_title('La Torah como Señal Numérica (cada punto = valor de gematría de una letra)', color='#FFD700', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Posición (letra #)', color='#888')
    ax1.set_ylabel('Valor de gematría', color='#888')
    ax1.tick_params(colors='#666')
    ax1.legend(facecolor='#0a0a1a', edgecolor='#333', labelcolor='#aaa')
    
    # === 2. ESPECTRO FFT ===
    ax2 = axes[1]
    ax2.set_facecolor('#0a0a1a')
    freqs = fft_result['frequencies'][1:]  # Sin DC
    mags = fft_result['magnitudes'][1:]
    
    # Solo mostrar hasta frecuencia 0.1 (períodos > 10)
    mask = freqs < 0.1
    ax2.plot(freqs[mask], mags[mask], color='#BB86FC', alpha=0.6, linewidth=0.5)
    
    # Marcar picos
    for peak in fft_result['peaks'][:5]:
        ax2.annotate(f"T≈{peak['period']:.0f}", 
                     xy=(peak['frequency'], peak['magnitude']),
                     xytext=(peak['frequency'] + 0.002, peak['magnitude'] + 0.0005),
                     color='#FFD700', fontsize=8, fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color='#FFD700', lw=0.8))
    
    ax2.set_title('Espectro de Fourier — Frecuencias Ocultas de la Torah', color='#BB86FC', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Frecuencia (ciclos / letra)', color='#888')
    ax2.set_ylabel('Magnitud', color='#888')
    ax2.tick_params(colors='#666')
    
    plt.tight_layout()
    path1 = os.path.join(output_dir, 'torah_señal_y_espectro.png')
    plt.savefig(path1, dpi=150, facecolor='#0a0a1a', bbox_inches='tight')
    plt.close()
    print(f"  📊 Guardado: {path1}")
    
    # === 3. PERÍODOS SAGRADOS ===
    fig, ax = plt.subplots(figsize=(14, 6), facecolor='#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    
    # Convertir frecuencias a períodos
    periods = 1.0 / freqs[freqs > 0]
    mags_p = mags[freqs > 0]
    
    # Solo períodos de interés (2 a 500)
    mask = (periods >= 2) & (periods <= 500)
    ax.plot(periods[mask], mags_p[mask], color='#00E5FF', alpha=0.5, linewidth=0.7)
    
    # Marcar períodos sagrados
    sacred = {7: 'Shabbat\n(7)', 22: 'Alefbet\n(22)', 26: 'YHVH\n(26)', 
              42: 'Ana Bekoach\n(42)', 49: '7×7\n(49)', 50: 'Jubileo\n(50)', 72: '72 Nombres\n(72)'}
    for period, label in sacred.items():
        target_freq = 1.0 / period
        idx = np.argmin(np.abs(freqs - target_freq))
        if idx > 0 and idx < len(mags):
            ax.axvline(period, color='#FFD700', alpha=0.4, linewidth=1, linestyle='--')
            ax.annotate(label, xy=(period, mags[idx]),
                       xytext=(period + 5, mags[idx] + 0.0003),
                       color='#FFD700', fontsize=8, fontweight='bold')
    
    ax.set_title('Espectro por Período — ¿Resuenan los Números Sagrados?', color='#FFD700', fontsize=13, fontweight='bold')
    ax.set_xlabel('Período (cada N letras)', color='#888')
    ax.set_ylabel('Magnitud', color='#888')
    ax.tick_params(colors='#666')
    ax.set_xlim(2, 200)
    
    plt.tight_layout()
    path2 = os.path.join(output_dir, 'torah_periodos_sagrados.png')
    plt.savefig(path2, dpi=150, facecolor='#0a0a1a', bbox_inches='tight')
    plt.close()
    print(f"  📊 Guardado: {path2}")
    
    return [path1, path2]


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("🌀 FOURIER TORAH — La Melodía Matemática Oculta")
    print("   Análisis de frecuencias de la Torah como señal numérica")
    print("=" * 70)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    viz_dir = os.path.join(base_dir, 'visualizations')
    
    # === PASO 1: Señal por letras ===
    print("\n📜 PASO 1: Convirtiendo la Torah a señal numérica (por letras)...")
    signal, boundaries = torah_to_signal(raw_dir)
    
    if len(signal) == 0:
        print("❌ No se pudo cargar la Torah. Verifica los archivos JSON.")
        sys.exit(1)
    
    # === PASO 2: FFT ===
    print("\n🔬 PASO 2: Aplicando Transformada de Fourier (FFT)...")
    fft_letters = compute_fft(signal, "Torah (por letras)")
    
    # === PASO 3: Señal por palabras ===
    print("\n📜 PASO 2b: FFT por palabras...")
    word_signal = torah_to_word_signal(raw_dir)
    fft_words = compute_fft(word_signal, "Torah (por palabras)")
    
    # === PASO 4: Periodicidades sagradas ===
    print("\n🔯 PASO 3: Buscando periodicidades sagradas (letras)...")
    sacred_letters = check_sacred_periodicities(signal, fft_letters)
    
    print("\n🔯 PASO 3b: Buscando periodicidades sagradas (palabras)...")
    sacred_words = check_sacred_periodicities(word_signal, fft_words)
    
    # === PASO 5: Autocorrelación ===
    print("\n📈 PASO 4: Autocorrelación...")
    autocorr = compute_autocorrelation(signal, max_lag=100)
    
    # === PASO 6: Monte Carlo ===
    print("\n🎲 PASO 5: Comparación Monte Carlo (50 simulaciones)...")
    mc_result = monte_carlo_comparison(signal, n_simulations=50)
    
    # === PASO 7: Visualizaciones ===
    print("\n🎨 PASO 6: Generando visualizaciones...")
    generate_visualizations(signal, fft_letters, boundaries, viz_dir)
    
    # === RESUMEN FINAL ===
    print("\n" + "=" * 70)
    print("🌀 RESUMEN: LA MELODÍA DE LA TORAH")
    print("=" * 70)
    
    print(f"\n  📏 Señal: {len(signal):,} letras → {len(word_signal):,} palabras")
    print(f"  📊 Media por letra: {np.mean(signal):.2f}")
    print(f"  📊 Media por palabra: {np.mean(word_signal):.2f}")
    
    print(f"\n  🔝 Top 5 períodos dominantes (por letra):")
    for p in fft_letters['peaks'][:5]:
        print(f"     Cada {p['period']:.0f} letras (magnitud: {p['magnitude']:.4f})")
    
    print(f"\n  🔝 Top 5 períodos dominantes (por palabra):")
    for p in fft_words['peaks'][:5]:
        print(f"     Cada {p['period']:.0f} palabras (magnitud: {p['magnitude']:.4f})")
    
    # Hallazgos significativos
    sig_sacred = [s for s in sacred_letters if s['z_score'] > 3]
    if sig_sacred:
        print(f"\n  🔯 PERIODICIDADES SAGRADAS SIGNIFICATIVAS:")
        for s in sig_sacred:
            print(f"     ✅ T={s['period']} ({s['meaning']}): z={s['z_score']:.2f}")
    
    print(f"\n  🎲 Monte Carlo: z-score = {mc_result['z_score']:.2f}")
    if mc_result['z_score'] > 3:
        print(f"     ✅ La Torah tiene estructura SIGNIFICATIVAMENTE no aleatoria")
    
    # Conclusión
    print(f"\n  {'═' * 60}")
    print(f"  💡 CONCLUSIÓN:")
    if mc_result['z_score'] > 3 or len(sig_sacred) > 0:
        print(f"  La Torah contiene frecuencias dominantes que NO aparecen en")
        print(f"  texto aleatorio con la misma distribución de letras.")
        print(f"  Existe una 'melodía' matemática oculta en su estructura.")
    else:
        print(f"  La estructura de frecuencias de la Torah es consistente")
        print(f"  con su distribución de letras. Las periodicidades")
        print(f"  requieren análisis más profundo.")
    print(f"  {'═' * 60}")
    
    print("\n✅ Análisis Fourier completo.")
