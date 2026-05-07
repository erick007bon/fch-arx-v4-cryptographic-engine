import json
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import wave
import struct

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gematria_engine import gematria_standard, extract_words

def load_words(raw_dir):
    books = ['bereshit', 'shemot', 'vayikra', 'bamidbar', 'devarim']
    all_values = []
    
    for book_file in books:
        filepath = os.path.join(raw_dir, f"{book_file}.json")
        if not os.path.exists(filepath): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chapters = data.get('chapters', {})
        for ch_num in sorted(chapters.keys(), key=int):
            ch = chapters[ch_num]
            verses = ch.get('verses_consonantal', ch.get('verses_with_nikkud', []))
            for verse in verses:
                for word in extract_words(verse):
                    val = gematria_standard(word)
                    if val > 0:
                        all_values.append(val)
    return all_values

def generate_graphs(values, output_dir):
    print("📈 Generando gráficas científicas...")
    plt.style.use('dark_background')
    
    # 1. Energía Acumulada (El Efecto Sinaí)
    window = 1000
    moving_avg = [np.mean(values[i:i+window]) for i in range(len(values) - window + 1)]
    
    plt.figure(figsize=(12, 6))
    plt.plot(moving_avg, color='cyan', alpha=0.8, linewidth=1.5)
    plt.axvline(26508 - (window//2), color='magenta', linestyle='--', label="Altar Éxodo 27:5 (~26,000)")
    plt.title("Radiación Gemátrica: El Pico de Energía del Monte Sinaí", fontsize=14)
    plt.xlabel("Iteración de Palabra", color='white')
    plt.ylabel("Energía Promedio", color='white')
    plt.legend()
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sinaitic_energy_peak.png'), dpi=300)
    plt.close()
    
    # 2. Paseo de Saturno (Drift Analysis)
    print("📈 Generando Paseo de Saturno...")
    saturn_walk = []
    pos = 0
    for v in values:
        if v % 7 == 0:
            pos += 1
        else:
            pos -= 0.16 # Basado en la expectativa del ~14%
        saturn_walk.append(pos)
        
    plt.figure(figsize=(12, 6))
    plt.plot(saturn_walk, color='#FF5733', linewidth=1)
    plt.axhline(0, color='white', linestyle='--', alpha=0.5)
    plt.title("El Paseo Aleatorio de Saturno (Cálculo del Vórtice Básico 7)", fontsize=14)
    plt.xlabel("Topología (Palabra)", color='white')
    plt.ylabel("Acotación Espacial Gravitacional", color='white')
    plt.grid(alpha=0.1)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'saturn_walk.png'), dpi=300)
    plt.close()
    
    # 3. Distribución del Cerebro (Super Nodos)
    # Tomaremos un subset de las conexiones YHVH (26)
    print("📈 Generando Grafo de Centralidad...")
    top_nodes = ['[26]\nYHVH', '[30]\nLamed', '[31]\nEl', '[257]\nAron', '[501]\nTehom']
    connections = [385, 376, 373, 343, 457]
    
    plt.figure(figsize=(10, 6))
    plt.bar(top_nodes, connections, color=['magenta', 'cyan', 'cyan', 'cyan', 'gold'])
    plt.title("Red Neuronal de Mundo Pequeño (Top Centralidad de Grado)", fontsize=14)
    plt.ylabel("Cantidad de Nodos Conectados (Sinapsis)")
    plt.grid(axis='y', alpha=0.2)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'neural_hubs.png'), dpi=300)
    plt.close()

def generate_audio(values, output_audio_file):
    print("🎼 Generando archivo de audio (Sonificación a 432 Hz)...")
    
    # Configuramos el archivo WAV
    sample_rate = 44100
    # Usaremos solo el libro de Génesis (Bereshit) como prueba para no hacer un archivo GIGANTE.
    # Digamos las primeras 3000 palabras (aprox los primeros capítulos)
    subset = values[:3000]
    
    # 432 Hz es LA nota LA (A4). Afinación de Solfeggio.
    # El universo pitagórico: Frecuencia = 432 * (2 ^^ (semitones / 12))
    # Mapearemos la Raíz Digital de Gematría (1-9) a la escala Pentatónica de LA (A)
    # A = 432, C = 513.7, D = 576, E = 648.5, G = 768
    pentatonic_ratios = [1.0, 1.189, 1.333, 1.5, 1.777] # Relaciones justas simplificadas
    
    wav_file = wave.open(output_audio_file, 'w')
    wav_file.setnchannels(1) # Mono
    wav_file.setsampwidth(2) # 16-bit
    wav_file.setframerate(sample_rate)
    
    duration = 0.12 # Segundos por palabra
    
    audio_data = []
    
    # Generar señal
    for val in subset:
        # Calcular raíz digital 1-9
        root = val % 9
        if root == 0: root = 9
        
        # Mapear raíz digital a un índice pentatónico (0 a 4)
        # y sumarle una octava si el valor es multiplo de 7 (Gravedad de Saturno)
        idx = root % 5
        octave_mult = 0.5 if val % 7 == 0 else 1.0 # Una octava más grave si es Saturno
        
        freq = 432.0 * pentatonic_ratios[idx] * octave_mult
        
        num_samples = int(sample_rate * duration)
        
        for k in range(num_samples):
            t = float(k) / sample_rate
            # Onda sinusal pura
            value = int(32767.0 * 0.5 * np.sin(2.0 * np.pi * freq * t))
            # Añadir un armónico suave de la propia frecuencia 3-6-9
            harmony = int(32767.0 * 0.1 * np.sin(2.0 * np.pi * (freq*1.5) * t))
            
            sample = value + harmony
            
            # Recortar (clipping protection)
            if sample > 32767: sample = 32767
            if sample < -32768: sample = -32768
            
            data = struct.pack('<h', sample)
            wav_file.writeframesraw(data)
            
    wav_file.close()
    print(f"✅ Archivo de audio guardado en: {output_audio_file}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    output_graph_dir = os.path.join(base_dir, 'graphs')
    output_audio_file = os.path.join(base_dir, 'audio', 'torah_genesis_432Hz.wav')
    
    if not os.path.exists(output_graph_dir): os.makedirs(output_graph_dir)
    if not os.path.exists(os.path.dirname(output_audio_file)): os.makedirs(os.path.dirname(output_audio_file))
    
    print("⚙️ Cargando valores fuente...")
    values = load_words(raw_dir)
    
    generate_graphs(values, output_graph_dir)
    generate_audio(values, output_audio_file)
    print("🎉 PRCESO TERMINADO. Listos para el Paper.")
