import os

# FCH-ARX V3: Hash Tensorial Grado Militar
# Entropia ELS + Cubo de Saturno + Operaciones ARX
# Copyright: Erick Zambrano

FILE_GENESIS = r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah\ENSAYOS CIENTIFICOS\KOREN_GENESIS_78064_PERFECTO.txt"

# Constantes Fundacionales
MODULO_32 = 0xFFFFFFFF
GENESIS_LENGTH = 78064

# Cargamos el archivo a memoria
if not os.path.exists(FILE_GENESIS):
    raise FileNotFoundError(f"El texto masorético no fue encontrado en: {FILE_GENESIS}")

with open(FILE_GENESIS, "r", encoding="utf-8") as f:
    GENESIS_TEXT = f.read()

# Validacion Masoretica Absoluta
if len(GENESIS_TEXT) != GENESIS_LENGTH:
    raise ValueError(f"CRITICO: El Dataset fue alterado. Logitud actual: {len(GENESIS_TEXT)}")

def rotl32(x, n):
    """Rotación a la izquierda sobre 32 bits (ARX - Rotate)"""
    return ((x << (n & 31)) | (x >> (32 - (n & 31)))) & MODULO_32

class QuantumTorahHash:
    def __init__(self):
        # 8 Registros base inspirados en SHA-256 (Primos raiz) para iniciar Caos
        self.state = [
            0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
            0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19
        ]
        
    def _absorber_byte(self, b):
        """
        Pilar del V3: Inyecta M[idx] hacia el state pero extrae el XOR Key del Genesis
        usando saltos Topologicos (Geometría).
        """
        for j in range(8):
            # Ecuación de Salto (Fijada en Saturno 26, 7 y Tesla 9)
            # Incorporamos self.state[j] al indice para que colapsen cascadas si un solo bit cambia.
            indice_salto = (b * 26 + j * 9 + self.state[j]) % GENESIS_LENGTH
            
            # S-Box Extracción
            # Extraemos la letra y sacamos su Entropia Unicode
            entropia = ord(GENESIS_TEXT[indice_salto]) 
            
            # 1. ADD (Suma no lineal)
            self.state[j] = (self.state[j] + b + entropia + (j * 7)) & MODULO_32
            
            # 2. ROTATE (Omer 7, Hub 26)
            rot = 7 if (j % 2 == 0) else 26
            self.state[j] = rotl32(self.state[j], rot)
            
            # 3. XOR Dinámico Cuántico
            self.state[j] ^= entropia
            self.state[j] ^= (b << 8)
            
        # Vórtice de difusion Tesla Cruzada (Cruza los 8 registros)
        self.state[0] = (self.state[0] ^ self.state[7]) & MODULO_32
        self.state[1] = (self.state[1] ^ self.state[6]) & MODULO_32
        self.state[2] = (self.state[2] ^ self.state[5]) & MODULO_32
        self.state[3] = (self.state[3] ^ self.state[4]) & MODULO_32
            
    def update(self, datos_bytes: bytes):
        for b in datos_bytes:
            self._absorber_byte(b)
            
    def _hervor_final(self):
        # 26 Rondas Sagradas de "Blank" para disipar el Efecto Avalancha y blindarlo al 50.00%
        for i in range(26):
            # Le pasamos el indice de iteración + constantes Tesla
            self._absorber_byte(i ^ 0x369)
            
    def hexdigest(self):
        self._hervor_final()
        return "".join(f"{r:08x}" for r in self.state)


def fch_arx_v3_hash(mensaje, codificacion="utf-8"):
    """
    Funcion Helper simple. 
    Transforma un string o bytes en un Hash Hexadecimal Cuántico V3.
    """
    if isinstance(mensaje, str):
        mensaje = mensaje.encode(codificacion)
    
    motor = QuantumTorahHash()
    motor.update(mensaje)
    return motor.hexdigest()

if __name__ == '__main__':
    print("--- FCH-ARX V3 TENSOR ---")
    print(f"Torah Engine Carga: OK ({GENESIS_LENGTH} chars)")
    
    msg1 = "ERICK"
    msg2 = "ERICKZ"
    
    print("\nEjecutando Avalancha Primaria:")
    print(f" Hash('{msg1}') = {fch_arx_v3_hash(msg1)}")
    print(f" Hash('{msg2}')= {fch_arx_v3_hash(msg2)}")
