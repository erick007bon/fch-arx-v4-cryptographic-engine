"""
🗄️ RAG Y LANGCHAIN: VECTOR DATABASE SEARCH (TORAH I.A.)
===========================================================================
Simula la arquitectura de un motor RAG (Retrieval-Augmented Generation).
En una RAG típica, el usuario sube un PDF, este se polariza en vectores, y la
IA busca por proximidad (Cosine Similarity) para hallar respuestas.

Aquí nuestra base de datos NO es PDF de texto, es la matriz NumPy de la Torah.
Haremos una inyección vectorial de consulta: Le enviaremos un "Prompt
Matemático" y la DB Vectorial extraerá los Nodos Relevantes (Retrieve).
===========================================================================
"""
import os
import sys
import numpy as np

# Ignorar las advertencias
import warnings
warnings.filterwarnings('ignore')

from gensim.models import Word2Vec

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Diccionario teológico para humanos
MAPPING_DICTIONARY = {
    '26': 'YHVH (Dios)',
    '86': 'Elohim (Dios Naturaleza)',
    '207': 'Or (Luz)',
    '300': 'Shin (Fuego Creador)',
    '611': 'Torah',
    '85': 'Pe (Hablar/Boca)', 
    '1': 'Aleph (Unidad/Padre)',
    '400': 'Tav (Final/Materia)',
    '66': 'Galgal (Rueda/Ciclo)',
    '137': 'Kabalah / Constante Fina',
    '376': 'Shalom (Paz)',
    '501': 'Tehom (Abismo/Decapitado)'
}

def vector_db_search(query_vector, model, top_k=5):
    """
    Simulación perfecta de una Base de Datos Vectorial (Pinecone / ChromaDB)
    """
    print(f"\n🔍 [LangChain_Retriever] Escaneando DB Vectorial para Embedding...")
    
    # gensim model.wv hace cosine_similarity bajo el capó (La misma métrica de ChromaDB)
    try:
        results = model.wv.most_similar(positive=[query_vector], topn=top_k)
        print(f"✅ Búsqueda Semántica Completada. Retornando TOP-{top_k} Nodos:")
        
        for num, prob in results:
            tag = MAPPING_DICTIONARY.get(num, 'Token Desconocido')
            print(f" [DB_MATCH] Vector ID: {num} | Relevancia Teológica: {tag} | Confianza Cuántica: {prob*100:.2f}%")
        
    except KeyError:
        print(f"❌ Error DB: El token {query_vector} no tiene suficiente masa gravitacional en la base de datos.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'torah_gematria.model')
    
    if not os.path.exists(model_path):
        print("❌ DB ERROR: No hay Neural Embeddings.")
        sys.exit()
        
    print("🌐 CARGANDO RAG VECTOR DATABASE (Memoria Embeddings)")
    ai_model = Word2Vec.load(model_path)
    
    print("\n===================================================================")
    print("PROMPT INJECTION 1: EL INICIO (Aleph / 1)")
    print("Vamos a buscar qué tokens están semánticamente atados a la fuerza del 1.")
    vector_db_search('1', ai_model, top_k=6)
    
    print("\n===================================================================")
    print("PROMPT INJECTION 2: EL HABLAR (85)")
    print("En Génesis todo se crea mediante habla. Vamos a buscar a la 'Boca' (85).")
    vector_db_search('85', ai_model, top_k=6)
    
    print("\n===================================================================")
    print("PROMPT INJECTION 3: EL CAOS (501)")
    print("Si buscamos las energías atadas al Tehom (Materia caótica primordial).")
    vector_db_search('501', ai_model, top_k=6)
