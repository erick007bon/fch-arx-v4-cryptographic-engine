"""
================================================================================
MELODIA DE LOS 72 NOMBRES — Resonancia Schumann (7.83 Hz)
================================================================================
Los 72 Nombres del Éxodo mapeados a los 5 armónicos de la Tierra.
La frecuencia base (7.83 Hz) multiplicada por octavas para hacerla audible.

ESCALA PENTATONICA SCHUMANN:
  7.83 Hz × 128 = 1,002 Hz  (Do)   — Energía baja   < 50
  14.3 Hz × 128 = 1,830 Hz  (Re)   — Energía media  50-100
  20.8 Hz × 128 = 2,662 Hz  (Mi)   — Energía alta   100-200
  27.3 Hz × 128 = 3,494 Hz  (Sol)  — Energía fuerte 200-350
  33.8 Hz × 128 = 4,326 Hz  (La)   — Energía máxima > 350

La escala pentatónica (5 notas) es la más universal de la humanidad.
Aparece en música china, africana, indígena americana, y en el Templo de Salomón.
================================================================================
"""

import json
import struct
import wave
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════
GEMATRIA = {
    'א':1,  'ב':2,  'ג':3,  'ד':4,  'ה':5,
    'ו':6,  'ז':7,  'ח':8,  'ט':9,  'י':10,
    'כ':20, 'ל':30, 'מ':40, 'נ':50, 'ס':60,
    'ע':70, 'פ':80, 'צ':90, 'ק':100,'ר':200,
    'ש':300,'ת':400,
    'ך':20, 'ם':40, 'ן':50, 'ף':80, 'ץ':90,
}
HEBREW = set(GEMATRIA.keys())

# Resonancias Schumann (Hz) × 128 octavas = audible
SCHUMANN_BASE   = 7.83
SCHUMANN_ARMONICOS = [7.83, 14.3, 20.8, 27.3, 33.8]
NOTAS_AUDIBLES  = [s * 128 for s in SCHUMANN_ARMONICOS]
# = [1002.24, 1830.4, 2662.4, 3494.4, 4326.4]

NOMBRES_NOTAS = ['Do (1,002 Hz)', 'Re (1,830 Hz)', 'Mi (2,662 Hz)',
                 'Sol (3,494 Hz)', 'La (4,326 Hz)']
COLORES_NOTAS = ['#4FC3F7', '#81C784', '#FFD54F', '#FF8A65', '#CE93D8']

BASE_PATH = Path(r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah")


def extraer_72_nombres():
    with open(BASE_PATH / r"data\raw\shemot.json", encoding='utf-8') as f:
        data = json.load(f)
    verses = data['chapters']['14']['verses_consonantal']
    v19 = [c for c in verses[18] if c in HEBREW]
    v20 = [c for c in verses[19] if c in HEBREW]
    v21 = [c for c in verses[20] if c in HEBREW]

    nombres = []
    for n in range(72):
        l1, l2, l3 = v19[n], v20[71 - n], v21[n]
        g1, g2, g3 = GEMATRIA[l1], GEMATRIA[l2], GEMATRIA[l3]
        energia = g1 + g2 + g3
        nombres.append({'nombre': l1+l2+l3, 'energia': energia,
                        'g1': g1, 'g2': g2, 'g3': g3})
    return nombres


def energia_a_nota(energia):
    """Mapea energía gemátrica a uno de los 5 armónicos Schumann."""
    if energia < 50:    return 0   # Do
    elif energia < 100: return 1   # Re
    elif energia < 200: return 2   # Mi
    elif energia < 350: return 3   # Sol
    else:               return 4   # La


def generar_tono(frecuencia, duracion=0.4, sample_rate=44100, fade=0.03):
    """Genera un tono con envolvente suave (fade in/out)."""
    n_samples = int(sample_rate * duracion)
    t = np.linspace(0, duracion, n_samples, endpoint=False)

    # Onda principal + armónico suave (más rica en timbre)
    onda = 0.7 * np.sin(2 * np.pi * frecuencia * t)
    onda += 0.2 * np.sin(2 * np.pi * frecuencia * 2 * t)
    onda += 0.1 * np.sin(2 * np.pi * frecuencia * 3 * t)

    # Envolvente ADSR suave
    fade_samples = int(sample_rate * fade)
    envolvente   = np.ones(n_samples)
    envolvente[:fade_samples]  = np.linspace(0, 1, fade_samples)
    envolvente[-fade_samples:] = np.linspace(1, 0, fade_samples)
    onda *= envolvente

    # Normalizar a int16
    onda = (onda * 28000).astype(np.int16)
    return onda


def generar_wav(nombres, output_path):
    """Genera el archivo WAV con la melodía completa de los 72 Nombres."""
    sample_rate = 44100
    todas_muestras = []

    silence = np.zeros(int(sample_rate * 0.08), dtype=np.int16)

    for i, n in enumerate(nombres):
        idx_nota = energia_a_nota(n['energia'])
        freq     = NOTAS_AUDIBLES[idx_nota]
        tono     = generar_tono(freq, duracion=0.4, sample_rate=sample_rate)
        todas_muestras.append(tono)
        todas_muestras.append(silence)

    audio = np.concatenate(todas_muestras)

    with wave.open(str(output_path), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

    duracion_total = len(audio) / sample_rate
    print(f"  ✅ Audio generado: {output_path.name}")
    print(f"  ⏱️  Duración: {duracion_total:.1f} segundos")
    return output_path


def generar_visualizacion(nombres, output_path):
    """Genera la visualización completa: onda de energía + mapa de notas."""
    energias   = [n['energia'] for n in nombres]
    notas_idx  = [energia_a_nota(e) for e in energias]
    frecuencias = [NOTAS_AUDIBLES[i] for i in notas_idx]
    colores    = [COLORES_NOTAS[i] for i in notas_idx]
    nombres_heb = [n['nombre'] for n in nombres]

    fig, axes = plt.subplots(3, 1, figsize=(20, 14))
    fig.patch.set_facecolor('#0A0A1A')

    for ax in axes:
        ax.set_facecolor('#0D0D2B')
        ax.tick_params(colors='#AAAACC')
        for spine in ax.spines.values():
            spine.set_edgecolor('#333366')

    # ── PANEL 1: Onda de Energía Gemátrica ──────────────────────────────────
    ax1 = axes[0]
    x = np.arange(72)
    ax1.fill_between(x, energias, alpha=0.3, color='#7B68EE')
    ax1.plot(x, energias, color='#9B8FFF', linewidth=1.5, alpha=0.8)
    ax1.scatter(x, energias, c=colores, s=40, zorder=5, alpha=0.9)

    # Marcar los Nombres especiales
    especiales = {0: '#1 והו', 6: '#7 אכא', 21: '#22 ייי', 40: '#41 ההה',
                  48: '#49 והו', 71: '#72 מום'}
    for idx, label in especiales.items():
        ax1.annotate(label, (idx, energias[idx]),
                    textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=7, color='#FFD700',
                    arrowprops=dict(arrowstyle='->', color='#FFD700', lw=0.8))

    # Línea Schumann base (energía promedio)
    ax1.axhline(np.mean(energias), color='#FF6B6B', linestyle='--',
               alpha=0.5, linewidth=1, label=f'Energía media: {np.mean(energias):.0f}')
    ax1.set_title('⚡ Onda de Energía Gemátrica — Los 72 Nombres del Éxodo',
                 color='white', fontsize=14, pad=10)
    ax1.set_ylabel('Energía (Σ Gematría)', color='#AAAACC', fontsize=10)
    ax1.set_xlim(-0.5, 71.5)
    ax1.legend(facecolor='#0D0D2B', labelcolor='white', fontsize=9)

    # Marcas verticales de los 8 grupos
    for g in range(0, 72, 9):
        ax1.axvline(g, color='#444488', linestyle=':', alpha=0.5, linewidth=0.8)

    # ── PANEL 2: Piano Roll — Nota de cada Nombre ───────────────────────────
    ax2 = axes[1]
    for i, (nota, col) in enumerate(zip(notas_idx, colores)):
        ax2.bar(i, nota + 1, color=col, alpha=0.85, width=0.8, bottom=-0.5)

    ax2.set_title('🎵 Piano Roll Schumann — Los 72 Nombres como Partitura',
                 color='white', fontsize=14, pad=10)
    ax2.set_ylabel('Nota Schumann', color='#AAAACC', fontsize=10)
    ax2.set_yticks(range(5))
    ax2.set_yticklabels([n.split(' ')[0] for n in NOMBRES_NOTAS], color='#AAAACC')
    ax2.set_xlim(-0.5, 71.5)

    # Leyenda de notas
    parches = [mpatches.Patch(color=COLORES_NOTAS[i], label=f'{NOMBRES_NOTAS[i]}\n(Schumann ×128)')
               for i in range(5)]
    ax2.legend(handles=parches, loc='upper right', facecolor='#0D0D2B',
              labelcolor='white', fontsize=7, ncol=5)

    # Letras hebreas en cada barra (muestra cada 3)
    for i in range(0, 72, 3):
        ax2.text(i, notas_idx[i] + 0.1, nombres_heb[i],
                fontsize=7, ha='center', color='white', alpha=0.8)

    # ── PANEL 3: Visualización de la Onda Schumann ──────────────────────────
    ax3 = axes[2]
    t = np.linspace(0, 4 * np.pi, 1000)

    # Los 5 armónicos Schumann superpuestos (como se ven en la ionosfera)
    onda_total = np.zeros(1000)
    for i, (s, col) in enumerate(zip(SCHUMANN_ARMONICOS, COLORES_NOTAS)):
        onda = np.sin(t * (i + 1))
        onda_total += onda * (1 / (i + 1))
        ax3.plot(t, onda * (5 - i), color=col, alpha=0.4,
                linewidth=1, label=f'{s} Hz → ×128 = {s*128:.0f} Hz')

    ax3.plot(t, onda_total * 3, color='white', linewidth=2,
            alpha=0.9, label='Onda Compuesta Total')
    ax3.fill_between(t, onda_total * 3, alpha=0.1, color='#9B8FFF')

    ax3.set_title('🌍 Resonancia Schumann — Los 5 Armónicos de la Tierra',
                 color='white', fontsize=14, pad=10)
    ax3.set_ylabel('Amplitud', color='#AAAACC', fontsize=10)
    ax3.set_xlabel('Ciclo (4π)', color='#AAAACC', fontsize=10)
    ax3.legend(facecolor='#0D0D2B', labelcolor='white', fontsize=8, ncol=3)
    ax3.axhline(0, color='#444488', linewidth=0.5)

    # ── TEXTO INFERIOR ───────────────────────────────────────────────────────
    fig.text(0.5, 0.01,
             'Los 72 Nombres del Éxodo 14:19-21 mapeados a los Armónicos Schumann de la Tierra (7.83 Hz) | '
             'Torah Applied Sciences © Erick Flores Zambrano 2026',
             ha='center', color='#666699', fontsize=8)

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(str(output_path), dpi=150, bbox_inches='tight',
               facecolor='#0A0A1A')
    plt.close()
    print(f"  ✅ Visualización guardada: {output_path.name}")


# ══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 62)
    print("  MELODIA DE LOS 72 NOMBRES — Resonancia Schumann")
    print("  Éxodo 14:19-21 × 7.83 Hz × Tierra")
    print("=" * 62)

    nombres = extraer_72_nombres()
    print(f"\n  72 Nombres extraídos del texto real del Éxodo")

    energias = [n['energia'] for n in nombres]
    notas    = [energia_a_nota(e) for e in energias]

    print(f"\n  DISTRIBUCIÓN DE NOTAS (Escala Pentatónica Schumann):")
    for i, nota in enumerate(NOMBRES_NOTAS):
        count = notas.count(i)
        barra = '█' * count
        print(f"  {nota:<22} {barra} ({count} Nombres)")

    print(f"\n  ESTADÍSTICAS DE ENERGÍA:")
    print(f"  Mínima  : {min(energias)} (Nombre #{energias.index(min(energias))+1}: {nombres[energias.index(min(energias))]['nombre']})")
    print(f"  Máxima  : {max(energias)} (Nombre #{energias.index(max(energias))+1}: {nombres[energias.index(max(energias))]['nombre']})")
    print(f"  Media   : {np.mean(energias):.1f}")
    print(f"  Total   : {sum(energias):,}")

    # Detectar patrones
    print(f"\n  PATRONES DETECTADOS:")
    vistos = {}
    for i, n in enumerate(nombres):
        if n['nombre'] in vistos:
            print(f"  ⚡ REPETICION: '{n['nombre']}' aparece en #{vistos[n['nombre']]+1} y #{i+1} (Δ={i-vistos[n['nombre']]})")
        vistos[n['nombre']] = i

    out_dir = BASE_PATH / "ENSAYOS CIENTIFICOS"

    print(f"\n  Generando visualización...")
    generar_visualizacion(nombres, out_dir / "72_nombres_schumann.png")

    print(f"\n  Generando melodía WAV...")
    generar_wav(nombres, out_dir / "72_nombres_melodia.wav")

    print(f"\n{'='*62}")
    print(f"  ARCHIVOS GENERADOS:")
    print(f"  📊 72_nombres_schumann.png  — La onda visual")
    print(f"  🎵 72_nombres_melodia.wav   — La melodía audible")
    print(f"\n  La Tierra respira a 7.83 Hz.")
    print(f"  Los 72 Nombres respiran con ella.")
    print(f"{'='*62}")
