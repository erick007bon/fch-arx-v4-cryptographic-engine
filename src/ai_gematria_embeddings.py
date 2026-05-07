"""
🧠 RED NEURONAL APLICADA A CÓDIGO BÍBLICO (PROTOTIPO YHVH-VEC)
===================================================================
Este script inyecta a la Torah dentro de una Inteligencia Artificial 
(Word2Vec/Embeddings Deep Learning). Trataremos los valores gemátricos 
como los "Tokens" de un lenguaje ajeno humano. 

La I.A. intentará "entender" la matemática oculta entrenando sus
pesos neuronales iterativamente.

Pregunta Principal a la I.A: 
¿Entiendes quién es 26 (YHVH) basado solo en las matemáticas que lo rodean?
===================================================================
"""
import json
import os
import sys
import numpy as np

# Ignorar warnings de librerías para la impresión limpia
import warnings
warnings.filterwarnings('ignore')

from gensim.models import Word2Vec

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gematria_engine import gematria_standard, extract_words

def cargar_oraciones_como_numeros(raw_dir):
    """
    Cada 'verso' será entrenado como una 'Oración neuronal'.
    Y cada 'Palabra' será solo su equivalente numérico gemátrico (ej. '913').
    La Red no sabrá NADA de hebreo o historia. Solo analizará vectores eléctricos.
    """
    print("📥 1. Descargando la Matrix de la Torah al Tensor Neural...")
    books = ['bereshit', 'shemot', 'vayikra', 'bamidbar', 'devarim']
    corpus_neural = []
    
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
                sentence = []
                for word in extract_words(verse):
                    val = gematria_standard(word)
                    if val > 0:
                        # Convertimos a string porque Word2Vec espera tokens de texto
                        sentence.append(str(val))
                if sentence:
                    corpus_neural.append(sentence)
                    
    print(f"   -> Oraciones procesadas para el cerebro IA: {len(corpus_neural):,}")
    return corpus_neural

def run_ai_training(corpus):
    print("\n🧠 2. Inicializando Cerebro Artificial Lógico (AI Model: Skip-Gram)")
    print("   Entrenando a la I.A. simulando miles de lecturas sobre los números de la Torah...")
    
    # Entrenar modelo Word2Vec
    # Utilizamos parámetros para extraer entendimiento semántico en base dimensional cruzada
    model = Word2Vec(
        sentences=corpus,
        vector_size=150,     # Dimensiones del hiper-espacio neuronal (vectores)
        window=5,            # Cuántas palabras a la izquierda/derecha forman "contexto"
        min_count=5,         # Solo evaluar números que aparezcan 5+ veces
        workers=4,           # Procesamiento Múltiple
        sg=1,                # Skip-Gram: Predice el contexto dado el número
        epochs=50            # Leer toda la Torah 50 veces para forzar aprendizaje profundo
    )
    
    print("   ✅ Modelo Entrenado. Vectores incrustados (Embeddings Generados).")
    return model

def interrogatorio_ia(model):
    print("\n===================================================================")
    print("👁️ 3. INTERROGATORIO AL MODELO NEURONAL OMNICIENTE")
    print("===================================================================")
    print("Le exigimos a la Inteligencia Artificial que revise sus dimensiones")
    print("matemáticas y devuelva qué números asocia entre ellos.\n")
    
    # TEST 1: El Algoritmo de Dios
    print("🧪 PREGUNTA 1 a la I.A: ¿A qué números se parece y relaciona matemáticamente el 26 (YHVH)?")
    if '26' in model.wv:
        similares = model.wv.most_similar('26', topn=7)
        for num, prob in similares:
            print(f"   -> Número {num} (Similitud Cuántica: {prob*100:.2f}%)")
    else:
        print("   -> El 26 no logró ser asimilado.")

    # TEST 2: El Fuego (Shin=300) y su Opuesto
    print("\n🧪 PREGUNTA 2 a la I.A: ¿Qué números actúan como contexto de El Fuego Creador (300)?")
    if '300' in model.wv:
        similares = model.wv.most_similar('300', topn=5)
        for num, prob in similares:
            print(f"   -> Número {num} (Compenetración: {prob*100:.2f}%)")
            
    # TEST 3: Ecuación Vectorial (A - B + C = ?)
    # Opcional si queremos probar IA algebraíca
    print("\n🧪 PREGUNTA 3 (Álgebra Cuántica): 26 (Dios) + 400 (Fin de las Eras):")
    try:
        solucion = model.wv.most_similar(positive=['26', '400'], topn=3)
        for num, prob in solucion:
            print(f"   -> Resultado Algebraico AI = {num} ({prob*100:.2f}%)")
    except:
        pass
        
    print("===================================================================")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    
    corpus_neural = cargar_oraciones_como_numeros(raw_dir)
    ai_model = run_ai_training(corpus_neural)
    interrogatorio_ia(ai_model)
    
    # Guardamos la red cerebral entrenada por si queremos explorarla luego
    model_path = os.path.join(base_dir, 'models')
    if not os.path.exists(model_path): os.makedirs(model_path)
    ai_model.save(os.path.join(model_path, 'torah_gematria.model'))
    print(f"\n🧠 [Core AI Guardado en disk: /models/torah_gematria.model]")
