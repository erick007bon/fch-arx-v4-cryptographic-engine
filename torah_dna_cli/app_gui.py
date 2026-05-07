import streamlit as st
import os
import torah_dna

st.set_page_config(page_title="Torah-DNA Storage UI", page_icon="🧬", layout="wide")

st.title("🧬 Torah-DNA Storage: Zero Entropy Data Retention")
st.markdown("Este Software empaqueta archivos físicos usando la matriz algorítmica multidimensional **Omer (7x7)** derivada de la geometría Teológica de Sanación, capaz de resucitar *" + 
            "información sin usar un respaldo de copia base.*" +
            "\n\n**(C) 2026 Erick Zambrano - IP PROPRIETARY SOFTWARE.**")

# Setup Temp Workspace
WORKSPACE = "gui_workspace"
if not os.path.exists(WORKSPACE):
    os.makedirs(WORKSPACE)

# States
if "uploaded_file_path" not in st.session_state:
    st.session_state.uploaded_file_path = None
if "encoded_file_path" not in st.session_state:
    st.session_state.encoded_file_path = None
if "mutated_file_path" not in st.session_state:
    st.session_state.mutated_file_path = None
if "healed_file_path" not in st.session_state:
    st.session_state.healed_file_path = None

uploaded_file = st.file_uploader("1️⃣ Sube  un Archivo para Blindar (ej. un .txt)", type=['txt', 'json', 'csv'])

if uploaded_file is not None:
    # Save physical copy for Toran Engine
    file_path = os.path.join(WORKSPACE, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state.uploaded_file_path = file_path
    st.success(f"Archivo crudo cargado: {uploaded_file.name} (Tamaño: {uploaded_file.size} bytes)")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("🔒 1. CODIFICACIÓN")
    st.write("Inyecta 'Nodos de Saturno Base-7'")
    if st.button("Aplicar Matriz Torah", use_container_width=True) and st.session_state.uploaded_file_path:
        with st.spinner("Construyendo matriz holográfica de paridad..."):
            encoded_path = torah_dna.encode(st.session_state.uploaded_file_path)
            st.session_state.encoded_file_path = encoded_path
            
            encoded_size = os.path.getsize(encoded_path)
            st.success(f"¡ADN Estructurado exitosamente!\nSu volumen protector ascendió a {encoded_size} bytes.")

with col2:
    st.header("☢️ 2. IRRADIACIÓN")
    st.write("Simulación de Ataque/Destrucción Celular")
    if st.button("Infectar con Radiación", type="primary", use_container_width=True) and st.session_state.encoded_file_path:
        with st.spinner("Destruyendo Bytes aleatorios..."):
            mut_path = torah_dna.irradiate(st.session_state.encoded_file_path)
            st.session_state.mutated_file_path = mut_path
            
            st.warning("💥 ARCHIVO AHORA ESTÁ FÍSICAMENTE CORRUPTO Y SUS LETRAS HAN ENTRADO EN ENTROPÍA MENGUANTE.")
            
            if mut_path.endswith('.txt.tora_dna.mutated') or mut_path.endswith('.json.tora_dna.mutated') or mut_path.endswith('.csv.tora_dna.mutated'):
                try:
                    with open(mut_path, "r", encoding="utf-8", errors='ignore') as f:
                        content_mutated = f.read()
                    st.text_area("Contenido Dañado (Fuga de Entropía)", value=content_mutated, height=150)
                except Exception:
                    pass
            
            with open(mut_path, "rb") as f_mut:
                st.download_button(
                    label="Descargar Archivo Enfermo",
                    data=f_mut,
                    file_name=os.path.basename(mut_path),
                    mime="application/octet-stream"
                )

with col3:
    st.header("🔬 3. SANACIÓN")
    st.write("Triangulación Geométrica")
    if st.button("Ejecutar Escáner Torah", use_container_width=True) and st.session_state.mutated_file_path:
        with st.spinner("Midiendo gravedad 7x7..."):
            out_name = os.path.join(WORKSPACE, "RESURRECTED_" + os.path.basename(st.session_state.uploaded_file_path))
            torah_dna.heal(st.session_state.mutated_file_path, out_name)
            st.session_state.healed_file_path = out_name
            
            st.success(f"✅ SANACIÓN COMPLETA. Se usó el teorema de intersección para restaurar los átomos de data borrados.")
            
            # Show original output vs resurrected output if it's text
            if out_name.endswith('.txt') or out_name.endswith('.json') or out_name.endswith('.csv'):
                with open(out_name, "r", encoding="utf-8", errors='ignore') as f:
                    content = f.read()
                st.text_area("Contenido Orgánico Resucitado", value=content, height=150)
            
            with open(out_name, "rb") as file:
                btn = st.download_button(
                    label="Descargar Archivo Perfecto",
                    data=file,
                    file_name=os.path.basename(out_name),
                    mime="text/plain"
                )
