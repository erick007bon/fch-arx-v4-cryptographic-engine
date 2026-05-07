import ctypes
import time
import os
import struct
from pathlib import Path

# Cargar la librería C nativa
dll_path = Path(__file__).parent / "fch_arx_v4_fast.dll"
try:
    fch_c_lib = ctypes.CDLL(str(dll_path))
except Exception as e:
    print(f"Error cargando {dll_path}: {e}")
    exit(1)

# Configurar argumentos de la función C
# void fch_arx_v4_c(const uint8_t* message, size_t msg_len, const uint32_t* names_energia, const uint32_t* names_r1, const uint32_t* names_r2, const uint32_t* names_r3, const uint8_t* pool, size_t pool_size, uint32_t* hash_out)
fch_c_lib.fch_arx_v4_c.argtypes = [
    ctypes.c_char_p,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_uint32)
]
fch_c_lib.fch_arx_v4_c.restype = None

# Importar funciones base para extraer nombres y pool
from fch_arx_v4_core import extraer_72_nombres, cargar_genesis, fch_arx_v4

class FCHARXv4_Fast:
    def __init__(self, nombres_72, genesis_pool):
        # Convertir nombres_72 a arreglos de ctypes
        self.energia_arr = (ctypes.c_uint32 * 72)(*[n['energia'] for n in nombres_72])
        self.r1_arr = (ctypes.c_uint32 * 72)(*[n['r1'] for n in nombres_72])
        self.r2_arr = (ctypes.c_uint32 * 72)(*[n['r2'] for n in nombres_72])
        self.r3_arr = (ctypes.c_uint32 * 72)(*[n['r3'] for n in nombres_72])
        
        # Convertir pool a arreglo ctypes
        self.pool_size = len(genesis_pool)
        self.pool_arr = (ctypes.c_uint8 * self.pool_size)(*genesis_pool)

    def hash(self, message: bytes) -> bytes:
        msg_len = len(message)
        hash_out = (ctypes.c_uint32 * 8)()
        fch_c_lib.fch_arx_v4_c(
            message, msg_len,
            self.energia_arr, self.r1_arr, self.r2_arr, self.r3_arr,
            self.pool_arr, self.pool_size,
            hash_out
        )
        
        # Devolver exactamente como struct.pack('>8I', ...) del original
        return struct.pack('>8I', *hash_out)

if __name__ == "__main__":
    BASE = r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah"
    print("\n  Cargando Entropía...")
    nombres_72 = extraer_72_nombres(BASE + r"\data\raw\shemot.json")
    genesis_pool = cargar_genesis(BASE + r"\data\raw\bereshit.json")

    fast_engine = FCHARXv4_Fast(nombres_72, genesis_pool)

    # 1. Verificación de Correctitud Matemática
    print("\n  [+] Verificando consistencia matemática C vs Python...")
    test_msg = b"Erick Flores Zambrano - FCH-ARX V4"
    h_py = fch_arx_v4(test_msg, nombres_72, genesis_pool)
    h_c  = fast_engine.hash(test_msg)

    print(f"  Py Hash: {h_py.hex()}")
    print(f"  C  Hash: {h_c.hex()}")
    if h_py == h_c:
        print("  ✅ VERIFICACION EXITOSA: El motor C produce el hash matemáticamente exacto.")
    else:
        print("  ❌ ERROR: Desviación matemática detectada.")
        exit(1)

    # 2. Benchmark de Velocidad
    MB_TEST = 100  # 100 Megabytes
    chunk_size = 1024 * 1024  # 1 MB blocks
    print(f"\n  [+] Iniciando Benchmark de Velocidad Extrema ({MB_TEST} MB en memoria)")
    test_data = os.urandom(chunk_size)  # Generar 1 MB aleatorio

    print(f"  > Evaluando FCH-ARX V4 (C Engine Optimizad) sobre bloques de 1MB...")
    t0 = time.time()
    for _ in range(MB_TEST):
        _ = fast_engine.hash(test_data)
    t1 = time.time()

    elapsed = t1 - t0
    mbs = MB_TEST / elapsed

    print("=" * 62)
    print("  RESULTADOS DEL BENCHMARK V4 (THROUGHPUT)")
    print("=" * 62)
    print(f"  Arquitectura    : x86_64 Native C (Loop Unrolling)")
    print(f"  Volumen testado : {MB_TEST} MB")
    print(f"  Tiempo total    : {elapsed:.3f} segundos")
    print(f"  Rendimiento     : {mbs:.2f} MB/s")
    print("=" * 62)

    if mbs > 300:
        print("  🚀 ¡OBJETIVO CUMPLIDO! Superamos la barrera de los 300 MB/s.")
    else:
        print("  ⚠️ El rendimiento quedó por debajo de los 300 MB/s esperados.")
