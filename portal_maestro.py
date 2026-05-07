import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Torah Applied Sciences - Portal Maestro", page_icon="⚛️", layout="wide")

st.markdown("""
<div style='text-align: center; color: white;'>
    <h1 style='font-size: 3rem;'>⚛️ SISTEMA OPERATIVO: TORAH APPLIED SCIENCES</h1>
    <h3>Autor: Erick Flores Zambrano (2026)</h3>
    <hr>
</div>
""", unsafe_allow_html=True)

st.write("Bienvenido al Portal Maestro Corporativo de Biomímesis Cuántica. Este Dashboard agrupa la trilogía de software " 
         "basado en la ingeniería mística del Medio Oriente antiguo, transpilado a Python. Selecciona el módulo de la investigación científica:")

# Pestañas Superiores
tab1, tab2, tab3 = st.tabs([
    "🧬 Mód 1: Almacenamiento Cero-Entropía (Torah-DNA)", 
    "🧠 Mód 2: Topología Scale-Free & Alzheimer", 
    "🔐 Mód 3: Tesla-Hash & Ciberseguridad Web3"
])

with tab1:
    st.subheader("Simulador de Recuperación Física de Datos (Erasure Coding Geométrico)")
    st.write("Herramienta desarrollada para probar el teorema de paridad Saturno-Base 7 sin respaldos en la nube.")
    st.markdown("[Abrir en Pestaña Completa](http://localhost:8501)")
    components.iframe("http://localhost:8501", width=1300, height=850, scrolling=True)

with tab2:
    st.subheader("Simulador Clínico Neuronal")
    st.write("Fuerza el daño radiactivo / neuronal en redes Genéricas vs Redes de Hub-Concéntrico Hebreo.")
    st.markdown("[Abrir en Pestaña Completa](http://localhost:8502)")
    components.iframe("http://localhost:8502", width=1300, height=850, scrolling=True)

with tab3:
    st.subheader("Validador Criptográfico Aduanero (Vórtices)")
    st.write("Genera Checksums basados en la espiral de Fibonacci para prevenir colisiones bancarias y mutaciones informativas.")
    st.markdown("[Abrir en Pestaña Completa](http://localhost:8503)")
    components.iframe("http://localhost:8503", width=1300, height=850, scrolling=True)

st.markdown("---")
st.markdown("<div style='text-align: center;'>Propiedad Intelectual Protegida - Las aplicaciones corren en micro-servicios de hardware local.</div>", unsafe_allow_html=True)
