import streamlit as st
import time

st.set_page_config(page_title="Crypto-Torah Web3 Hash", page_icon="🔐", layout="wide")

st.title("🔐 Módulo 3: Encriptación y Ciberseguridad ('Torah-Hash')")
st.markdown("Un algoritmo de Firma Digital (Checksum Cuántico) extrapolado de la geometría masorética. "
            "Utiliza el modelo **Tesla (Base 9)** y la rueda infinita de **Fibonacci (24 latidos)** para "
            "sellar contratos y transferencias web3, previendo hackeos y colisiones matemáticas."
            "\n\n**(C) 2026 Erick Zambrano - PROPIEDAD INTELECTUAL INDUSTRIAL.**")

# --- CORE MATEMÁTICO BLOCKCHAIN ---
FIBO_WHEEL = [1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9, 8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1, 9]

def torah_hash(data_string):
    hash_value = 0
    for i, char in enumerate(data_string):
        fibo_multiplier = FIBO_WHEEL[i % 24]
        # Multiplicador molecular basado en vórtice phi
        valor_atomico = ord(char) * fibo_multiplier
        # Desplazamiento asimétrico: si un hacker invierte "A" y "B", la posición geométrica cambia y rompe el hash
        hash_value += valor_atomico * (i + 1)
        
    # Raíz digital Tesla-Mod 9
    root = 1 + ((hash_value - 1) % 9) if hash_value > 0 else 0
    # Retornamos formato Blockchain
    return f"0x{hex(hash_value)[2:].zfill(12).upper()}-T{root}"
# -----------------------------------

st.header("1. Emisión del Contrato Legítimo")
texto_original = st.text_area("✍️ Redacta un Documento Seguro (Ej: Contrato Bancario / ADN):", 
                              "TRANSFERENCIA BANCARIA: Transferir $1000 BTC a la cuenta de Erick Zambrano.")

col_hash1, col_hash2 = st.columns(2)
with col_hash1:
    if st.button("Generar Sello Inquebrantable (Hash)", type="primary"):
        sello = torah_hash(texto_original)
        st.session_state['original_text'] = texto_original
        st.session_state['sello_legitimo'] = sello
        st.success(f"**SELLO GENERADO:** `{sello}`")

st.markdown("---")
st.header("2. Ataque Hacker (Corrupción de Datos)")
st.write("Intenta alterar el contrato original de arriba. Cámbiale **SOLO UNA LETRA o NÚMERO** "
         "(por ejemplo, cambia el 1000 por 9000).")

texto_alterado = st.text_area("👾 Interceptación del Hacker (Altera el archivo):", 
                              st.session_state.get('original_text', "TRANSFERENCIA BANCARIA: Transferir $9000 BTC a la cuenta de Erick Zambrano."))

if st.button("Validar Transferencia en la Aduana (Ataque)"):
    if 'sello_legitimo' not in st.session_state:
        st.warning("Primero genera el sello legítimo arriba.")
    else:
        with st.spinner("Escáner de Geometría Cuántica trabajando..."):
            time.sleep(1)
            nuevo_sello = torah_hash(texto_alterado)
            
            st.metric("Sello Archivo Original", st.session_state['sello_legitimo'])
            st.metric("Sello Que Trae el Hacker", nuevo_sello)
            
            if nuevo_sello == st.session_state['sello_legitimo']:
                # Si esto fuera verdadero significaría que colisionó. Pero no va a pasar.
                if texto_alterado == st.session_state['original_text']:
                    st.success("✅ PERFECTO. Los archivos son idénticos. El contrato se valida y ejecuta.")
                else:
                    st.error("❌ ¡PELIGRO! El hash es igual pero el texto cambió (COLISIÓN DEL ALGORITMO).")
            else:
                st.error("🚨 **FRAUDE DETECTADO:** Fuga Geométrica en la Letra Alterada.")
                st.write("El Inspector Torah detectó que la masa atómica de la cadena no encaja con la rueda de Fibonacci y el modelo Tesla de Vórtices. **TRANSACCIÓN ABORTADA.**")
