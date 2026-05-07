#include <stdint.h>
#include <stddef.h>

#define PHI_CONST 0x9E3779B9
#define MODULO_216 216

// Rotación circular izquierda
static inline uint32_t _rol32(uint32_t val, uint32_t n) {
    n = n % 32;
    if (n == 0) n = 16;
    return (val << n) | (val >> (32 - n));
}

// Interfaz para Python (Exportable)
#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

EXPORT void fch_arx_v4_c(
    const uint8_t* message, 
    size_t msg_len,
    const uint32_t* names_energia,
    const uint32_t* names_r1,
    const uint32_t* names_r2,
    const uint32_t* names_r3,
    const uint8_t* pool,
    size_t pool_size,
    uint32_t* hash_out
) {
    uint32_t M[8];
    for(int i = 0; i < 8; i++) {
        M[i] = i * PHI_CONST + 0x5A5A5A5A;
    }

    // Pre-calculo de indices de arrays (reemplaza modulo % por sumas rapidas)
    size_t pool_idx = 0;
    size_t n_idx = 0;
    int idx = 0;

    // ── FASE 1: ABSORCIÓN (PROCESAMIENTO POR BLOQUES DE 32-BITS) ──
    // Se procesa la entropia en bloques de 4 bytes (Word-Level) para multiplicar x4 la velocidad
    size_t num_words = msg_len / 4;
    const uint32_t* msg_words = (const uint32_t*)message;

    for (size_t i = 0; i < num_words; i++) {
        uint32_t word = msg_words[i];
        
        // Acceso directo a memoria de 32-bits (cero overhead)
        uint32_t pool_v = ((const uint32_t*)pool)[pool_idx / 4];
        
        M[idx] = M[idx] + word + pool_v + names_energia[n_idx];
        
        M[idx] = _rol32(M[idx], names_r1[n_idx]);
        M[idx] = _rol32(M[idx], names_r2[n_idx]);
        M[idx] = _rol32(M[idx], names_r3[n_idx]);
        
        // Cachear las rotaciones
        uint32_t r1 = names_r1[n_idx];
        for (int j = 1; j < 8; j++) {
            uint32_t rot_val = (j * r1) % 32;
            if (rot_val == 0) rot_val = 1;
            M[(idx + j) % 8] ^= _rol32(M[idx], rot_val);
        }

        // Actualización ultra-rápida de indices sin divisiones
        pool_idx += MODULO_216;
        while(pool_idx >= pool_size) pool_idx -= pool_size;
        
        n_idx++;
        if (n_idx == 72) n_idx = 0;
        
        idx++;
        if (idx == 8) idx = 0;
    }
    
    // Procesar bytes residuales si el mensaje no es múltiplo de 4
    size_t remainder = msg_len % 4;
    if (remainder > 0) {
        uint32_t word = 0;
        for (size_t i = 0; i < remainder; i++) {
            word |= ((uint32_t)message[num_words * 4 + i]) << (i * 8);
        }
        uint32_t pool_v = pool[pool_idx]; // simple para el residual
        
        M[idx] = M[idx] + word + pool_v + names_energia[n_idx];
        M[idx] = _rol32(M[idx], names_r1[n_idx]);
        M[idx] = _rol32(M[idx], names_r2[n_idx]);
        M[idx] = _rol32(M[idx], names_r3[n_idx]);
        
        uint32_t r1 = names_r1[n_idx];
        for (int j = 1; j < 8; j++) {
            uint32_t rot_val = (j * r1) % 32;
            if (rot_val == 0) rot_val = 1;
            M[(idx + j) % 8] ^= _rol32(M[idx], rot_val);
        }
    }
    
    // ── FASE 2: PADDING ─────────────────────────────────────────
    M[0] ^= ((uint32_t)msg_len ^ 0x5EFE572A);
    M[7] ^= ((uint32_t)msg_len * PHI_CONST);
    
    // ── FASE 3: 72 RONDAS DEL SHEM HAMEPHORASH ──────────────────
    for (int r = 0; r < 72; r++) {
        uint32_t n_energia = names_energia[r];
        uint32_t n_r1 = names_r1[r];
        uint32_t n_r2 = names_r2[r];
        uint32_t n_r3 = names_r3[r];
        
        size_t final_pool_idx = (r * n_energia + 7) % pool_size;
        uint8_t pool_val = pool[final_pool_idx];
        
        for (int i = 0; i < 8; i++) {
            int j = (i + r + 1) % 8;
            
            M[i] = M[i] + M[j] + pool_val + n_energia;
            
            M[i] = _rol32(M[i], n_r1);
            M[i] = _rol32(M[i], n_r2);
            
            M[i] ^= _rol32(M[(i + 3) % 8], n_r3);
            M[i] ^= _rol32(M[(i + 7) % 8], n_r1);
        }
    }
    
    // Devolver el estado
    for(int i=0; i<8; i++) {
        hash_out[i] = M[i];
    }
}
