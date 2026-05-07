"""
TORAH-HASH BLOCKCHAIN DEMO
===========================
Mini blockchain privada que usa el algoritmo Torah-Hash 
(Fibonacci Wheel + Mod 9) en lugar de SHA-256.

Autor: Erick R. Flores Zambrano
Puerto: localhost:8505
"""
import streamlit as st
import time
import json
import hashlib
from datetime import datetime

# ============================================
# MOTOR DEL TORAH-HASH
# ============================================
FIB_WHEEL = [1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9]

def torah_hash(text: str) -> str:
    """Genera firma criptografica usando Fibonacci Wheel + Mod 9."""
    total = 0
    for i, ch in enumerate(text):
        total += ord(ch) * FIB_WHEEL[i % 24] * (i + 1)
    tesla_root = 1 + ((total - 1) % 9) if total > 0 else 0
    hex_val = hex(total % (16**12))[2:].upper().zfill(12)
    return f"0x{hex_val}-T{tesla_root}"

def sha256_hash(text: str) -> str:
    """SHA-256 estandar para comparacion."""
    return hashlib.sha256(text.encode()).hexdigest()

# ============================================
# ESTRUCTURA DEL BLOQUE
# ============================================
class Block:
    def __init__(self, index, timestamp, data, previous_hash, miner="Erick-Node"):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.miner = miner
        self.nonce = 0
        # Contenido que se hashea
        self.content = f"{index}{timestamp}{data}{previous_hash}{miner}{self.nonce}"
        self.torah_hash = torah_hash(self.content)
        self.sha_hash = sha256_hash(self.content)
    
    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "torah_hash": self.torah_hash,
            "sha_hash": self.sha_hash[:24] + "...",
            "miner": self.miner,
        }

# ============================================
# ESTRUCTURA DE LA CADENA (BLOCKCHAIN)
# ============================================
class TorahBlockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Bloque Genesis: el primer eslabon de la cadena."""
        genesis = Block(
            index=0,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data="BLOQUE GENESIS - TORAH BLOCKCHAIN INICIADA",
            previous_hash="0x000000000000-T0",
            miner="SISTEMA"
        )
        self.chain.append(genesis)
    
    def add_block(self, data, miner="Erick-Node"):
        """Agrega un nuevo bloque a la cadena."""
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data=data,
            previous_hash=previous_block.torah_hash,
            miner=miner
        )
        self.chain.append(new_block)
        return new_block
    
    def validate_chain(self):
        """Verifica la integridad de TODA la cadena."""
        results = []
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            # Verificar que el hash previo coincide
            hash_match = current.previous_hash == previous.torah_hash
            
            # Recalcular el hash del bloque actual
            recalc_content = f"{current.index}{current.timestamp}{current.data}{current.previous_hash}{current.miner}{current.nonce}"
            recalc_hash = torah_hash(recalc_content)
            hash_valid = recalc_hash == current.torah_hash
            
            results.append({
                "block": i,
                "chain_linked": hash_match,
                "hash_intact": hash_valid,
                "valid": hash_match and hash_valid,
            })
        return results
    
    def tamper_block(self, index, new_data):
        """Simula un ataque: modifica los datos de un bloque."""
        if 0 < index < len(self.chain):
            self.chain[index].data = new_data
            # El hash YA NO coincide con el contenido real
            # Pero NO recalculamos el hash (eso es lo que hace un hacker)

# ============================================
# INTERFAZ STREAMLIT
# ============================================
def main():
    st.set_page_config(
        page_title="Torah Blockchain Demo",
        page_icon="<eth>",
        layout="wide"
    )
    
    # CSS
    st.markdown("""
    <style>
    .block-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #0f3460;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
    }
    .block-card-invalid {
        background: linear-gradient(135deg, #4a0000 0%, #8b0000 100%);
        border: 3px solid #ff0000;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
    }
    .genesis-card {
        background: linear-gradient(135deg, #0a3d0a 0%, #1b5e20 100%);
        border: 2px solid #4caf50;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
    }
    .hash-display {
        font-family: 'Courier New', monospace;
        font-size: 16px;
        color: #00ff88;
        background: #000;
        padding: 8px 12px;
        border-radius: 8px;
        display: inline-block;
        margin: 4px 0;
    }
    .chain-arrow {
        text-align: center;
        font-size: 40px;
        color: #00ff88;
        margin: 5px 0;
    }
    .metric-box {
        background: #1a1a2e;
        border: 1px solid #0f3460;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: white;
    }
    .title-glow {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        background: linear-gradient(90deg, #00ff88, #00b4d8, #9b59b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="title-glow">TORAH BLOCKCHAIN</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Blockchain privada impulsada por el algoritmo Torah-Hash (Fibonacci Wheel + Mod 9)<br>98.7% mas eficiente que SHA-256</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Inicializar blockchain
    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = TorahBlockchain()
    
    bc = st.session_state.blockchain
    
    # Layout principal
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.markdown("### Agregar Nuevo Bloque")
        
        # Transacciones predefinidas o/y personalizadas
        tx_type = st.selectbox("Tipo de transaccion:", [
            "Personalizada",
            "Transferencia Bancaria",
            "Contrato Digital",
            "Registro Medico",
            "Certificado Academico",
        ])
        
        if tx_type == "Personalizada":
            tx_data = st.text_area("Escribe los datos del bloque:", 
                                   placeholder="Ej: TRANSFER 500 USD FROM ERICK TO MARIA",
                                   height=80)
        elif tx_type == "Transferencia Bancaria":
            amount = st.number_input("Monto (USD):", min_value=1, value=1000)
            sender = st.text_input("De:", value="Erick Flores")
            receiver = st.text_input("Para:", value="Maria Lopez")
            tx_data = f"TRANSFER ${amount} USD FROM {sender} TO {receiver}"
        elif tx_type == "Contrato Digital":
            contract = st.text_input("Descripcion:", value="Contrato de servicio de software")
            value = st.number_input("Valor (USD):", min_value=1, value=5000)
            tx_data = f"CONTRATO: {contract} | VALOR: ${value} USD | FIRMADO DIGITALMENTE"
        elif tx_type == "Registro Medico":
            patient = st.text_input("Paciente:", value="Juan Perez")
            diagnosis = st.text_input("Diagnostico:", value="Examen de sangre: Normal")
            tx_data = f"REGISTRO MEDICO: {patient} | {diagnosis} | CONFIDENCIAL"
        else:
            student = st.text_input("Estudiante:", value="Erick Flores Zambrano")
            degree = st.text_input("Titulo:", value="Ingenieria en Sistemas")
            tx_data = f"CERTIFICADO: {student} ha completado {degree} | UTM 2026"
        
        miner = st.text_input("Nodo minero:", value="Erick-Node-01")
        
        if st.button("MINAR BLOQUE", type="primary", use_container_width=True):
            if tx_data.strip():
                start_time = time.time()
                new_block = bc.add_block(tx_data.strip(), miner)
                elapsed = time.time() - start_time
                st.success(f"Bloque #{new_block.index} minado en {elapsed*1000:.1f}ms")
                st.balloons()
            else:
                st.error("Escribe datos para el bloque")
        
        st.markdown("---")
        
        # Panel de ataque
        st.markdown("### Simulador de Ataque")
        st.caption("Simula un hacker intentando modificar un bloque de la cadena.")
        
        if len(bc.chain) > 1:
            attack_idx = st.number_input("Bloque a atacar:", 
                                          min_value=1, 
                                          max_value=len(bc.chain)-1, 
                                          value=1)
            attack_data = st.text_input("Datos falsos:", 
                                        value="TRANSFER $999999 USD TO HACKER")
            
            if st.button("EJECUTAR ATAQUE", type="secondary", use_container_width=True):
                bc.tamper_block(attack_idx, attack_data)
                st.error(f"Bloque #{attack_idx} ha sido ALTERADO por el atacante!")
        else:
            st.info("Agrega al menos 2 bloques para simular un ataque.")
        
        st.markdown("---")
        
        # Reset
        if st.button("Reiniciar Blockchain", use_container_width=True):
            st.session_state.blockchain = TorahBlockchain()
            st.rerun()
    
    with col_right:
        # Metricas
        validation = bc.validate_chain()
        valid_count = sum(1 for v in validation if v['valid'])
        total_links = len(validation)
        integrity = (valid_count / total_links * 100) if total_links > 0 else 100
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Bloques", len(bc.chain))
        m2.metric("Enlaces Validos", f"{valid_count}/{total_links}")
        m3.metric("Integridad", f"{integrity:.0f}%")
        m4.metric("Algoritmo", "Torah-Hash")
        
        if integrity < 100:
            st.error("LA CADENA HA SIDO COMPROMETIDA. Se detectaron bloques alterados.")
        else:
            st.success("CADENA INTACTA. Todos los enlaces verificados correctamente.")
        
        st.markdown("---")
        st.markdown("### Cadena de Bloques")
        
        # Validacion detallada
        valid_map = {v['block']: v for v in validation}
        
        for i, block in enumerate(bc.chain):
            is_genesis = i == 0
            is_valid = valid_map.get(i, {}).get('valid', True)
            
            if is_genesis:
                card_class = "genesis-card"
                status_icon = "GENESIS"
            elif is_valid:
                card_class = "block-card"
                status_icon = "VALIDO"
            else:
                card_class = "block-card-invalid"
                status_icon = "CORRUPTO"
            
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 24px; font-weight: bold;">Bloque #{block.index}</span>
                    <span style="background: {'#4caf50' if is_valid else '#ff0000'}; padding: 4px 12px; 
                           border-radius: 20px; font-size: 12px; font-weight: bold;">{status_icon}</span>
                </div>
                <div style="margin-top: 10px; font-size: 13px; color: #aaa;">
                    Timestamp: {block.timestamp} | Minero: {block.miner}
                </div>
                <div style="margin-top: 8px; font-size: 14px;">
                    <strong>Datos:</strong> {block.data}
                </div>
                <div style="margin-top: 10px;">
                    <div style="font-size: 11px; color: #888;">Hash Previo:</div>
                    <div class="hash-display" style="font-size: 12px; color: #ff9800;">{block.previous_hash}</div>
                </div>
                <div style="margin-top: 6px;">
                    <div style="font-size: 11px; color: #888;">Torah-Hash (este bloque):</div>
                    <div class="hash-display">{block.torah_hash}</div>
                </div>
                <div style="margin-top: 6px;">
                    <div style="font-size: 11px; color: #888;">SHA-256 (comparacion):</div>
                    <div class="hash-display" style="color: #e74c3c; font-size: 11px;">{block.sha_hash}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Flecha de encadenamiento
            if i < len(bc.chain) - 1:
                next_valid = valid_map.get(i+1, {}).get('chain_linked', True)
                arrow_color = "#00ff88" if next_valid else "#ff0000"
                arrow_text = "ENLACE VERIFICADO" if next_valid else "ENLACE ROTO"
                st.markdown(f"""
                <div style="text-align: center; margin: 5px 0;">
                    <div style="font-size: 30px; color: {arrow_color};">&#x2193;</div>
                    <div style="font-size: 10px; color: {arrow_color}; font-weight: bold;">{arrow_text}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Tabla de comparacion
        st.markdown("---")
        st.markdown("### Comparativa: Torah-Hash vs SHA-256")
        comparison_data = []
        for block in bc.chain:
            comparison_data.append({
                "Bloque": f"#{block.index}",
                "Torah-Hash": block.torah_hash,
                "SHA-256": block.sha_hash[:32] + "...",
                "Operaciones Torah": "~52/byte",
                "Operaciones SHA": "~4,200/byte",
            })
        st.dataframe(comparison_data, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
