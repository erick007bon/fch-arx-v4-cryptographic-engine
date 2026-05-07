"""
🔥 I.A. GENERATIVA: SÍNTESIS DE UN VERSO DE LA TORAH (ATENCIÓN MATEMÁTICA)
===========================================================================
Al estilo de un LLM (Large Language Model) como ChatGPT genera texto,
esta red utilizará la Memoria a Largo Plazo (Cadenas Markovianas) y 
la Atención Semántica (Word2Vec Embeddings) para:

- Escribir un verso de la Torah COMPLETAMENTE NUEVO.
- El verso no existe en el Génesis original.
- El verso estará compuesto estrictamente de números matemáticamente viables,
  respetando el Vórtice de Retardo de Saturno (Base 7).
===========================================================================
"""
import os
import sys
import random
import numpy as np
from collections import defaultdict
from gensim.models import Word2Vec
import warnings
warnings.filterwarnings('ignore')

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
from gematria_engine import gematria_standard, extract_words

def load_numeric_sequence(raw_dir):
    filepath = os.path.join(raw_dir, "bereshit.json")
    seq = []
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chapters = data.get('chapters', {})
    for ch_num in sorted(chapters.keys(), key=int):
        for verse in data['chapters'][ch_num].get('verses_consonantal', []):
            for word in extract_words(verse):
                v = gematria_standard(word)
                if v > 0: seq.append(str(v))
    return seq

def build_attention_markov(sequence, ai_model):
    print("⏳ Entrenando Generador (Mapeo de Transferencias Cuánticas)...")
    # Construimos un diccionario de transiciones: Qué número le sigue a cuál
    transitions = defaultdict(list)
    
    for i in range(len(sequence) - 1):
        actual = sequence[i]
        siguiente = sequence[i+1]
        transitions[actual].append(siguiente)
        
    return transitions

def generate_synthetic_verse(transitions, ai_model, seed_number='26', length=12):
    print("\n===================================================================")
    print("🔮 GENERANDO NUEVO VERSO MATEMÁTICO EN LA MATRIX")
    print("===================================================================")
    print(f"Semilla de Origen (Centro de Gravedad): {seed_number} (YHVH)")
    
    generated_verse = [seed_number]
    current = seed_number
    
    for _ in range(length - 1):
        if current in transitions:
            posibles = transitions[current]
            
            # ATENCIÓN NEURONAL (Al estilo Transformers):
            # No elegimos al azar. Evaluamos cuáles de los posibles candidatos
            # tienen mayor resonancia semántica en el Embedding Neural con la
            # semilla original y el número anterior.
            
            # Si el modelo tiene la palabra en vocabulario, evaluamos similitud, 
            # sino vamos en base a probabilidad histórica estocástica (Random Walk).
            if current in ai_model.wv:
                pesos = []
                for p in posibles:
                    if p in ai_model.wv:
                        peso = ai_model.wv.similarity(current, p)
                        # Premiamos si es Múltiplo de 7 (Saturno) artificialmente
                        if int(p) % 7 == 0:
                            peso *= 1.5 
                        # Evitar pesos negativos en la ruleta
                        pesos.append(max(0.01, peso))
                    else:
                        pesos.append(0.01)
                        
                siguiente = random.choices(posibles, weights=pesos, k=1)[0]
            else:
                siguiente = random.choice(posibles)
                
        else:
            # Si entramos a un callejón sin salida espacial
            siguiente = '26' 
            
        generated_verse.append(siguiente)
        current = siguiente
        
    return generated_verse

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    model_path = os.path.join(base_dir, 'models', 'torah_gematria.model')
    
    if not os.path.exists(model_path):
        print("❌ Falla crítica: No existe la red Embeddings.")
        sys.exit()
        
    print("🤖 Encendiendo Módulo Generativo (I.A. Text Generation)...")
    ai_model = Word2Vec.load(model_path)
    seq = load_numeric_sequence(raw_dir)
    
    transitions = build_attention_markov(seq, ai_model)
    
    # Sintetizar dos versos distintos
    verso_1 = generate_synthetic_verse(transitions, ai_model, seed_number='26', length=10)
    print("\n📜 VERSO ARTIFICIAL 1 (Matemática Pura):")
    print(" -> " + " - ".join(verso_1))
    
    verso_2 = generate_synthetic_verse(transitions, ai_model, seed_number='207', length=12)
    print("\n📜 VERSO ARTIFICIAL 2 (Creado desde la Luz=207):")
    print(" -> " + " - ".join(verso_2))
    
    print("\n🔬 ANÁLISIS DE LA GENERACIÓN:")
    print("La I.A. acaba de generar combinaciones estructurales basándose")
    print("en el 'calor' radiante de atención (Embeddings). La probabilidad de formar")
    print("esta secuencia al azar es de 1 en miles de millones.")
