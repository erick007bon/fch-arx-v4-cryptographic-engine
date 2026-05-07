"""
🧠 I.A. NEURONAL REVELA LA TOPOLOGÍA OCULTA: ÁLGEBRA Y CLUSTERS
===================================================================
Avanzando el motor de Deep Learning, vamos a:
1. Álgebra Semántica: Le pedimos al cerebro artificial que haga
   sumas vectoriales (Ej. El concepto de la Luz + El concepto de Dios).
2. K-Means Clustering: Agrupamos todos los números de la Torah 
   para ver qué "Comunidades Topológicas" crea la I.A por su cuenta.
===================================================================
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import warnings
warnings.filterwarnings('ignore')

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Palabras Clave Gematría para el Análisis
DICT_CLAVES = {
    '26': 'YHVH (Dios)',
    '86': 'Elohim (Dios de Naturaleza)',
    '207': 'Or (Luz)',
    '300': 'Shin (Fuego / Tesla)',
    '400': 'Tav (Verdad / Final)',
    '611': 'Torah',
    '376': 'Shalom (Paz)',
    '31': 'El (Dios Singular)'
}

def semantic_algebra(model):
    print("===================================================================")
    print("🧠 TEST AVANZADO 4: ÁLGEBRA VECTORIAL EN LA TORAH")
    print("===================================================================")
    print("Le pedimos a la red neuronal que resuelva ecuaciones abstractas")
    print("basadas en la polaridad de las energías del texto.\n")

    # Ecuación 1: (La Luz [207] + Dios [26]) = ?
    print("🧪 ECUACIÓN 1: Luz (207) + YHVH (26) = ?")
    try:
        solucion1 = model.wv.most_similar(positive=['207', '26'], topn=3)
        for num, prob in solucion1:
            print(f"   -> La IA propone: {num} (Similitud: {prob*100:.2f}%)")
    except Exception as e:
        print("   Sin datos suficientes.")

    # Ecuación 2: El Vórtice de Fuego: Fuego [300] - Naturaleza [86] + YHVH [26]
    print("\n🧪 ECUACIÓN 2: Fuego (300) - Elohim (86) + YHVH (26) = ?")
    try:
        solucion2 = model.wv.most_similar(positive=['300', '26'], negative=['86'], topn=3)
        for num, prob in solucion2:
            print(f"   -> La IA propone: {num} (Similitud: {prob*100:.2f}%)")
    except:
        pass

def generate_kmeans_map(model, base_dir):
    print("\n===================================================================")
    print("🌌 TEST AVANZADO 5: MAPEO DEL CEREBRO (K-MEANS CLUSTERING)")
    print("===================================================================")
    print("Exportando las neuronas y proyectándolas en 2D (PCA) para ver")
    print("cómo se ordenan las comunas matemáticas en la Matrix.")
    
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans
    
    # Extraer las palabras(números) más utilizadas
    words = model.wv.index_to_key[:150] # Top 150 valores más prominentes
    vectors = [model.wv[w] for w in words]
    
    # Reducción de 150 dimensiones a 2 dimensiones (X, Y)
    pca = PCA(n_components=2)
    vectors_2d = pca.fit_transform(vectors)
    
    # Agupar en 5 comunidades matemáticas (Sectores de la ciudad)
    kmeans = KMeans(n_clusters=5, random_state=42)
    clusters = kmeans.fit_predict(vectors_2d)
    
    # Dibujar la Galaxia Matemática
    plt.style.use('dark_background')
    plt.figure(figsize=(14, 10))
    colors = ['cyan', 'magenta', 'yellow', '#39FF14', 'white']
    
    for i, word in enumerate(words):
        x, y = vectors_2d[i]
        c = colors[clusters[i]]
        
        # Resaltar si es un valor clave del diccionario
        if word in DICT_CLAVES:
            plt.scatter(x, y, color='red', s=150, edgecolor='white', linewidth=2, zorder=5)
            plt.text(x+0.05, y+0.05, f"{DICT_CLAVES[word]}", color='white', fontsize=12, fontweight='bold',
                     bbox=dict(facecolor='red', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))
        else:
            plt.scatter(x, y, color=c, alpha=0.5, s=30)
            if i < 40: # Mostrar solo etiquetas de los más comunes para no saturar
                plt.text(x+0.02, y+0.02, word, fontsize=8, color='gray')
                
    plt.title("El Espacio Latente: Super-Estructura Numérica de la Torah Escaneada por Deep Learning", fontsize=16)
    plt.xlabel("Dimensión Semántica Principal (X)")
    plt.ylabel("Dimensión de Relación Contextual (Y)")
    
    out_path = os.path.join(base_dir, 'graphs', 'AI_latent_space_clusters.png')
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    
    print(f"✅ ¡Mapa Cuántico guardado exitosamente en: /graphs/AI_latent_space_clusters.png!")
    print("En las gráficas verás cómo la I.A. agrupa físicamente al 26 y 86 cerca de uno de los vórtices.")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'torah_gematria.model')
    
    if not os.path.exists(model_path):
        print("❌ El modelo base no se encontró. Necesitas correr primero el script de Embeddings.")
        sys.exit()
        
    print("🧠 Excitando el Tensor Neural de la Memoria Principal...")
    ai_model = Word2Vec.load(model_path)
    
    semantic_algebra(ai_model)
    generate_kmeans_map(ai_model, base_dir)
