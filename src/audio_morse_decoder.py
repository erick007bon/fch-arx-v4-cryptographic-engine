import json
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gematria_engine import gematria_standard, extract_words

# Diccionario Inverso de Código Morse Internacional
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '-----': '0'
}

def load_genesis_words(raw_dir):
    filepath = os.path.join(raw_dir, "bereshit.json")
    all_values = []
    
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

def decode_torah_morse(values):
    print("📻 INICIANDO INTERCEPTACIÓN TELEGRÁFICA DE LA TORAH...")
    print("==========================================================")
    
    # Lógica de Decodificación:
    # Como notaste, sonaba como Morse porque nuestro script bajaba
    # una octava entera (sonido grave y pesado) cada vez que golpeaba 
    # a la Gravedad de Saturno (Múltiplos de 7).
    # 
    # Mapeo Criptográfico:
    # - Palabra Múltiplo de 7 (Saturno) = RAYA ( - ) [Señal Gravitacional Pesada]
    # - Palabra Normal = PUNTO ( . ) [Señal de Avance Rápido]
    
    morse_signals = []
    for v in values:
        if v % 7 == 0:
            morse_signals.append('-')
        else:
            morse_signals.append('.')
            
    # El Morse se agrupa en secuencias para formar letras.
    # En un idioma estandarizado, una letra tiene entre 1 a 4 pulsos.
    # Vamos a agrupar la transmisión de la Torah en bloques de 4 pulsos 
    # a ver si el "Ruido" se traduce en patrones repetitivos o alfabeto.
    
    print("\n📡 EXTRAYENDO TRAMAS DE RADIO (Bloques de 4 bits)...")
    blocks = []
    current_block = ""
    for signal in morse_signals:
        current_block += signal
        if len(current_block) == 4:
            blocks.append(current_block)
            current_block = ""
            
    # Mostrar la transmisión cruda de los primeros 100 bloques (400 palabras)
    print("Cinta perforada cruda (Inicio de Génesis):")
    for i in range(0, 50, 10):
        print(" ".join(blocks[i:i+10]))
        
    print("\n🔮 DECODIFICANDO AL LENGUAJE HUMANO (Traductor MORSE)...")
    
    translated_text = ""
    for block in blocks:
        # Algunos bloques podrían no ser letras perfectas de 4 bits (e.g. 5 segun el código), 
        # pero buscaremos las coincidencias exactas extraídas limitando a 4.
        if block in MORSE_CODE_DICT:
            translated_text += MORSE_CODE_DICT[block]
        else: # Si hay partes cortas (sobrantes)
            translated_text += "?"
            
    print("\nMensaje Decodificado (Primeros 150 caracteres):")
    print(translated_text[:150])
    
    # Análisis de Anomalías
    from collections import Counter
    letter_counts = Counter(translated_text)
    
    print("\n📊 ANÁLISIS DE LA TRANSMISIÓN:")
    print("Si un humano telegrafía al azar, todas las letras saldrían con la misma frecuencia.")
    print("Top 5 Letras Emitidas por el Ritmo de Génesis:")
    for letter, count in letter_counts.most_common(5):
        print(f"Letra {letter}: {count} veces")
        
    # Análisis del bloque de respiración
    print("\nExplicación Física de la Transmisión:")
    print("El código no formará palabras en inglés porque es rítmica estructural.")
    print("Lo que el Morse decodifica es la 'Respiración'.")
    print("La Letra más repetida dicta la estructura del texto.")
    
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    values = load_genesis_words(raw_dir)
    decode_torah_morse(values)
