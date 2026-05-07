"""
================================================================================
FCH-ARX V3 — ANÁLISIS DE FRECUENCIA GEMÁTRICA DEL GÉNESIS (C)
================================================================================
Rabbi-Scientist Mode: Busca los "Nodos de Poder" del Génesis.
Las letras no son iguales. Las más frecuentes son los HUBs de la entropía —
el equivalente al Nodo 26 (YHVH) que encontramos en la red neuronal.

Si el Génesis es el "ADN del algoritmo", sus letras más frecuentes son los
"codones dominantes", los que definen qué tipo de entropía se genera.
================================================================================
"""
import json
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Sin pantalla, guardamos a archivo
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter

# ── Tabla Gemátrica ──────────────────────────────────────────────────────────
GEMATRIA = {
    'א': 1,   'ב': 2,   'ג': 3,   'ד': 4,   'ה': 5,
    'ו': 6,   'ז': 7,   'ח': 8,   'ט': 9,   'י': 10,
    'כ': 20,  'ך': 20,  'ל': 30,  'מ': 40,  'ם': 40,
    'נ': 50,  'ן': 50,  'ס': 60,  'ע': 70,  'פ': 80,
    'ף': 80,  'צ': 90,  'ץ': 90,  'ק': 100, 'ר': 200,
    'ש': 300, 'ת': 400,
}

LETTER_NAMES = {
    'א': 'Aleph',  'ב': 'Bet',    'ג': 'Gimel', 'ד': 'Dalet',
    'ה': 'He',     'ו': 'Vav',    'ז': 'Zayin', 'ח': 'Chet',
    'ט': 'Tet',    'י': 'Yod',    'כ': 'Kaf',   'ך': 'Kaf-f',
    'ל': 'Lamed',  'מ': 'Mem',    'ם': 'Mem-f', 'נ': 'Nun',
    'ן': 'Nun-f',  'ס': 'Samech', 'ע': 'Ayin',  'פ': 'Pe',
    'ף': 'Pe-f',   'צ': 'Tsadi',  'ץ': 'Tsadi-f','ק': 'Kuf',
    'ר': 'Resh',   'ש': 'Shin',   'ת': 'Tav',
}

GENESIS_PATH = r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah\data\raw\bereshit.json"

def load_and_analyze():
    with open(GENESIS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    counter       = Counter()
    gematria_vals = []
    verse_sums    = []
    chapter_data  = {}

    chapters = data['chapters']
    for cap_num, cap_data in chapters.items():
        cap_energy = 0
        for verse in cap_data.get('verses_consonantal', []):
            verse_val = 0
            for char in verse:
                if char in GEMATRIA:
                    counter[char] += 1
                    val = GEMATRIA[char]
                    gematria_vals.append(val)
                    verse_val += val
                    cap_energy += val
            if verse_val > 0:
                verse_sums.append(verse_val)
        chapter_data[int(cap_num)] = cap_energy

    total_letters = sum(counter.values())

    # ── REPORTE CONSOLA ──────────────────────────────────────────────────────
    print("=" * 70)
    print("  ANÁLISIS DE FRECUENCIA GEMÁTRICA — GÉNESIS COMPLETO")
    print("  FCH-ARX V3 | Erick Flores Zambrano | Torah Applied Sciences 2026")
    print("=" * 70)
    print(f"\n  Total letras analizadas : {total_letters:,}")
    print(f"  Total energía gemátrica : {sum(gematria_vals):,}")
    print(f"  Energía promedio/letra  : {np.mean(gematria_vals):.2f}")
    print(f"  Versículos procesados   : {len(verse_sums):,}")
    print()
    print(f"  {'#':<4} {'Letra':<8} {'Nombre':<12} {'Valor':<8} {'Frec.':<10} {'%':<8} {'Rol en Entropía'}")
    print(f"  {'-'*70}")

    # Detectar "YHVH-Like hubs" = letras cuya frecuencia % es múltiplo de 7, 9 o 26
    top = counter.most_common()
    for rank, (letter, freq) in enumerate(top, 1):
        pct     = freq / total_letters * 100
        val     = GEMATRIA[letter]
        name    = LETTER_NAMES.get(letter, '?')
        energy  = freq * val

        # Clasificación de rol
        if pct > 10:
            role = "🔴 SUPER-HUB (>10%)"
        elif pct > 7:
            role = "🟠 Hub Mayor (7-10%)"
        elif pct > 5:
            role = "🟡 Hub Menor (5-7%)"
        elif pct > 3:
            role = "🟢 Nodo Activo"
        else:
            role = "⚪ Nodo Débil"

        print(f"  {rank:<4} {letter:<8} {name:<12} {val:<8} {freq:<10,} {pct:<8.2f} {role}")

    print()

    # ── ANÁLISIS DE LOS VÓRTICES (3-6-9) ────────────────────────────────────
    print("  🌀 ANÁLISIS DE VÓRTICES TESLA (letras cuyo valor es múltiplo de 3, 6 o 9)")
    print(f"  {'-'*50}")
    vortex_freq = 0
    for letter, val in GEMATRIA.items():
        if val % 9 == 0 or val % 3 == 0:
            vortex_freq += counter.get(letter, 0)
    print(f"  Letras vórtice (val%3==0): {vortex_freq:,} ({vortex_freq/total_letters*100:.2f}% del texto)")

    # Letra con más energía total (freq × valor)
    energies = {l: counter.get(l,0)*v for l,v in GEMATRIA.items()}
    top_energy = sorted(energies.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"\n  ⚡ TOP 5 LETRAS POR ENERGÍA TOTAL (Frecuencia × Valor Gemátrico):")
    for l, e in top_energy:
        print(f"     {l} ({LETTER_NAMES.get(l,'?')}) = {e:,} unidades de energía")

    # Capítulo de mayor energía
    max_cap   = max(chapter_data, key=chapter_data.get)
    max_energy= chapter_data[max_cap]
    print(f"\n  🔥 CAPÍTULO DE MAYOR ENERGÍA: Génesis {max_cap} → {max_energy:,} unidades")

    # Entropía de Shannon del corpus
    probs     = np.array([counter[l] for l in GEMATRIA if l in counter]) / total_letters
    shannon_h = -np.sum(probs * np.log2(probs + 1e-12))
    print(f"\n  📐 ENTROPÍA DE SHANNON del Génesis: {shannon_h:.4f} bits")
    print(f"     (Máximo teórico para 22 letras: {np.log2(22):.4f} bits)")
    print(f"     Eficiencia de uso de la entropía: {(shannon_h/np.log2(22))*100:.2f}%")

    # ── GRÁFICO 1: BARRAS DE FRECUENCIA ─────────────────────────────────────
    letters_sorted = [x[0] for x in top]
    freqs_sorted   = [x[1] for x in top]
    vals_sorted    = [GEMATRIA[l] for l in letters_sorted]
    names_sorted   = [f"{LETTER_NAMES.get(l,'?')}\n({GEMATRIA[l]})" for l in letters_sorted]

    # Color por valor gemátrico (más alto = más rojo)
    max_val = max(vals_sorted)
    colors  = plt.cm.RdYlGn_r([v/max_val for v in vals_sorted])

    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.patch.set_facecolor('#0d0d1a')
    for ax in axes.flat:
        ax.set_facecolor('#0d0d1a')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        for spine in ax.spines.values():
            spine.set_edgecolor('#333355')

    # Plot 1: Frecuencia de letras
    ax1 = axes[0, 0]
    bars = ax1.bar(names_sorted, [f/total_letters*100 for f in freqs_sorted], color=colors, edgecolor='#333355')
    ax1.set_title('Frecuencia de Letras Hebreas (% del Corpus)\nGénesis Completo — 73,128 letras', fontsize=12, pad=10)
    ax1.set_xlabel('Letra Hebrea (Valor Gemátrico)', fontsize=10)
    ax1.set_ylabel('Frecuencia (%)', fontsize=10)
    ax1.axhline(y=100/27, color='cyan', linestyle='--', alpha=0.5, label=f'Uniform={100/27:.1f}%')
    ax1.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=8)
    for bar, pct in zip(bars, [f/total_letters*100 for f in freqs_sorted]):
        if pct > 5:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.1, f'{pct:.1f}%',
                    ha='center', va='bottom', fontsize=6, color='white')

    # Plot 2: Energía por letra
    ax2 = axes[0, 1]
    energies_sorted = [counter.get(l,0)*GEMATRIA[l] for l in letters_sorted]
    colors2 = plt.cm.plasma([e/max(energies_sorted) for e in energies_sorted])
    ax2.bar(names_sorted, energies_sorted, color=colors2, edgecolor='#333355')
    ax2.set_title('Energía Gemátrica Total por Letra\n(Frecuencia × Valor)', fontsize=12, pad=10)
    ax2.set_xlabel('Letra Hebrea (Valor Gemátrico)', fontsize=10)
    ax2.set_ylabel('Energía Total (unidades)', fontsize=10)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))

    # Plot 3: Energía acumulada por capítulo
    ax3 = axes[1, 0]
    caps = sorted(chapter_data.keys())
    cap_energies = [chapter_data[c] for c in caps]
    ax3.fill_between(caps, cap_energies, alpha=0.6, color='#7b2fff')
    ax3.plot(caps, cap_energies, color='#c084fc', linewidth=1.5)
    ax3.set_title('Energía Gemátrica por Capítulo del Génesis\n"El Latido del Texto"', fontsize=12, pad=10)
    ax3.set_xlabel('Capítulo', fontsize=10)
    ax3.set_ylabel('Energía Total (unidades)', fontsize=10)
    ax3.axvline(x=max_cap, color='yellow', linestyle='--', alpha=0.7, label=f'Cap {max_cap} (Pico)')
    ax3.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=8)
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))

    # Plot 4: Distribución de energía por verso (histograma)
    ax4 = axes[1, 1]
    ax4.hist(verse_sums, bins=60, color='#00d4ff', edgecolor='#003d4d', alpha=0.8)
    ax4.axvline(np.mean(verse_sums), color='yellow', linestyle='--', linewidth=1.5, label=f'Media={np.mean(verse_sums):.0f}')
    ax4.axvline(np.median(verse_sums), color='lime', linestyle='--', linewidth=1.5, label=f'Mediana={np.median(verse_sums):.0f}')
    ax4.set_title('Distribución de Energía por Versículo\n"La Campana de la Torah"', fontsize=12, pad=10)
    ax4.set_xlabel('Energía Gemátrica del Versículo', fontsize=10)
    ax4.set_ylabel('Número de Versículos', fontsize=10)
    ax4.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=8)

    plt.suptitle('⬡ GÉNESIS — MAPA DE ENTROPÍA ORGÁNICA (FCH-ARX V3)\nErick Flores Zambrano | Torah Applied Sciences 2026',
                 fontsize=14, color='white', y=1.01, fontweight='bold')

    plt.tight_layout()
    OUT = r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah\visualizations\genesis_entropy_map.png"
    plt.savefig(OUT, dpi=150, bbox_inches='tight', facecolor='#0d0d1a')
    print(f"\n  📊 Gráfico guardado en: {OUT}")
    plt.close()

    return counter, gematria_vals, verse_sums, chapter_data

if __name__ == "__main__":
    counter, vals, verses, caps = load_and_analyze()
    print("\n  ✅ Análisis C completado. El Génesis revela sus nodos de poder.\n")
