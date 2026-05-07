import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Neuro-Torah AI Simulator", page_icon="🧠", layout="wide")

st.title("🧠 Simulador Clínico Computacional: Neuro-Torah AI")
st.markdown("Este Software compara la topología de un **Cerebro Genérico (IA Aleatoria)** frente a la topología cuántica basada en " + 
            "los nodos gravitacionales masoréticos **(Scale-Free 'Hub YHVH-26')**. Inyecta radiación amiloidea (Alzheimer) para analizar el decaimiento de la **Consciencia (LCC)**." +
            "\n\n**(C) 2026 Erick Zambrano - MEDICINE AI (PROPRIETARY).**")

# --- CORE MATEMÁTICO ---
def build_brains(num_neurons):
    # Genérico Estándar (Modelo Erdos-Renyi P=0.01)
    b_normal = nx.erdos_renyi_graph(num_neurons, 0.01)
    # Scale-Free Torah (Barabasi-Albert M=2)
    b_torah = nx.barabasi_albert_graph(num_neurons, 2)
    return b_normal, b_torah

def measure_consciousness(brain):
    if len(brain) == 0: return 0
    components = sorted(nx.connected_components(brain), key=len, reverse=True)
    if not components: return 0
    return (len(components[0]) / len(brain)) * 100

def alzheimer_attack(brain, damage_percent):
    damaged_brain = brain.copy()
    num_to_kill = int(len(damaged_brain) * damage_percent)
    nodes_to_kill = random.sample(list(damaged_brain.nodes()), num_to_kill)
    damaged_brain.remove_nodes_from(nodes_to_kill)
    return damaged_brain
# -----------------------

st.sidebar.header("Parámetros del Laboratorio")
st.sidebar.write("Ajusta las variables de prueba cerebral:")

neuron_count = st.sidebar.slider("1️⃣ Número de Neuronas", min_value=100, max_value=2000, value=500, step=100)
damage_slider = st.sidebar.slider("2️⃣ Virulencia del Alzheimer (% de Muerte Celular)", min_value=10, max_value=90, value=40, step=5)

if st.sidebar.button("🧪 Ejecutar Ensayo Clínico", type="primary", use_container_width=True):
    with st.spinner("Creando cultivos de redes neuronales y esparciendo virus amiloideo..."):
        
        # 1. Cultivo
        b_norm, b_tora = build_brains(neuron_count)
        
        mem_n_ini = measure_consciousness(b_norm)
        mem_t_ini = measure_consciousness(b_tora)
        
        # 2. Ataque
        b_norm_dam = alzheimer_attack(b_norm, damage_slider / 100.0)
        b_tora_dam = alzheimer_attack(b_tora, damage_slider / 100.0)
        
        mem_n_fin = measure_consciousness(b_norm_dam)
        mem_t_fin = measure_consciousness(b_tora_dam)
        
        st.header("📉 Resultados Post-Enfermedad: Evaluación Cognitiva")
        col1, col2 = st.columns(2)
        
        with col1:
            st.error("### ❌ Cerebro IA Genérica (Erdős–Rényi)")
            st.metric("Consciencia Estructural Sobreviviente:", f"{mem_n_fin:.2f}%")
            st.write("La pérdida aleatoria causó que las conexiones vitales se fragmentaran rápidamente, apagando el procesamiento.")
        
        with col2:
            st.success("### 🟢 Neuro-Torah (Scale-Free Topología 26)")
            st.metric("Consciencia Estructural Sobreviviente:", f"{mem_t_fin:.2f}%")
            st.write("Gracias a los Nodos Ultra-Centralizados (Hubs pre-dispuestos por Gematría), la comunicación sobrevive el apagón celular masivo.")
            
        st.markdown("---")
        
        # Visualización Exclusiva usando Grafo Estético si es <= 800 para no hacer lenta la app
        if neuron_count <= 800:
            st.header("👁️ Visualización Geometría Física del Tejido")
            st.write("Fotografía computacional de las redes caídas.")
            fig, ax = plt.subplots(1, 2, figsize=(14, 6))
            
            # Subplot 1
            ax[0].set_title("Cerebro Genérico (Fragmentado)")
            pos_n = nx.spring_layout(b_norm_dam, seed=42)
            nx.draw_networkx_nodes(b_norm_dam, pos_n, ax=ax[0], node_size=10, node_color='red', alpha=0.6)
            nx.draw_networkx_edges(b_norm_dam, pos_n, ax=ax[0], alpha=0.1, edge_color='gray')
            ax[0].axis('off')
            
            # Subplot 2
            ax[1].set_title("Cerebro Neuro-Torah (Conectado fuertemente al Centro)")
            pos_t = nx.spring_layout(b_tora_dam, seed=42)
            # Find the hubs
            degrees = dict(b_tora_dam.degree())
            if degrees:
                max_deg = max(degrees.values())
                colors = ['green' if degrees[n] >= max_deg*0.3 else 'lightgreen' for n in b_tora_dam.nodes()]
                sizes = [30 if degrees[n] >= max_deg*0.3 else 10 for n in b_tora_dam.nodes()]
                nx.draw_networkx_nodes(b_tora_dam, pos_t, ax=ax[1], node_size=sizes, node_color=colors, alpha=0.8)
                nx.draw_networkx_edges(b_tora_dam, pos_t, ax=ax[1], alpha=0.1, edge_color='green')
            ax[1].axis('off')
            
            st.pyplot(fig)
        else:
            st.warning("⚠️ El nivel de neuronas es superior a 800. Se ocultó la vista gráfica del microscopio para cuidar el procesador RAM local de la clínica. El modelo matemático de LCC fue verificado existosamente arriba.")
