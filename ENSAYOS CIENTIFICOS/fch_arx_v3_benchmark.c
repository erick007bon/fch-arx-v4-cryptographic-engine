/*
================================================================================
FCH-ARX V3 BENCHMARK — Motor del Génesis (B)
Implementación en C puro para medir velocidad real en MB/s
Compilar: gcc -O3 -o fch_arx_v3_bench fch_arx_v3_benchmark.c && fch_arx_v3_bench
================================================================================
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

/* Constantes del Trinomio */
#define ROUNDS    26
#define PHI_CONST 0x9E3779B9U
static const uint32_t SATURN_SQUARE[9] = {4,9,2,3,5,7,8,1,6};
static const uint32_t FIBONACCI_24[24] = {1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9};

/* Piscina de Entropía: cargada desde Genesis (simplificada como array global) */
#define POOL_SIZE 73128
static uint8_t genesis_pool[POOL_SIZE];

/* Rotación de bits izquierda 32-bit */
static inline uint32_t rol32(uint32_t val, int n) {
    n &= 31;
    return (val << n) | (val >> (32 - n));
}

/* FCH-ARX V3: Hash de 256 bits */
void fch_arx_v3(const uint8_t *msg, size_t len, uint8_t *digest) {
    uint32_t M[9];
    for (int i = 0; i < 9; i++)
        M[i] = (SATURN_SQUARE[i] * PHI_CONST);

    /* FASE 1: ABSORCIÓN */
    for (size_t i = 0; i < len; i++) {
        int idx       = i % 9;
        uint32_t w    = FIBONACCI_24[i % 24];
        uint32_t pool = genesis_pool[(i * 26) % POOL_SIZE];

        M[idx] = (M[idx] + msg[i] + pool * w * (uint32_t)(i + 1));
        M[idx] = rol32(M[idx], 3);
        M[idx] = rol32(M[idx], 6);
        M[idx] = rol32(M[idx], 9);
        if (msg[i] % 7 == 0)
            M[idx] = rol32(M[idx], 7);

        for (int j = 1; j < 9; j++)
            M[(idx + j) % 9] ^= rol32(M[idx], j * 3);
    }

    /* FASE 2: PADDING */
    M[0] ^= (uint32_t)len;
    M[8] ^= (uint32_t)(len * PHI_CONST);

    /* FASE 3: 26 RONDAS YHVH */
    for (int r = 0; r < ROUNDS; r++) {
        uint32_t pv = genesis_pool[(r * 7 + 13) % POOL_SIZE];
        for (int i = 0; i < 9; i++) {
            int j   = (i + r + 1) % 9;
            M[i]    = (M[i] + M[j] + pv + r + 1);
            M[i]    = rol32(M[i], 3 + (r % 7));
            M[i]    = rol32(M[i], 6);
            M[i]   ^= rol32(M[(i + 3) % 9], 9);
            M[i]   ^= rol32(M[(i + 7) % 9], 26);
        }
    }

    /* SALIDA: 8 × 32 bits = 256 bits */
    for (int i = 0; i < 8; i++) {
        digest[i*4+0] = (M[i] >> 24) & 0xFF;
        digest[i*4+1] = (M[i] >> 16) & 0xFF;
        digest[i*4+2] = (M[i] >>  8) & 0xFF;
        digest[i*4+3] =  M[i]        & 0xFF;
    }
}

/* Generar piscina de entropía simulada (mismos valores que Python) */
void init_genesis_pool_simulated() {
    /* Valores gemátricos cíclicos — aproximación sin cargar JSON */
    /* Valores gemátricos mod 256: Shin=300→44, Tav=400→144 */
    static const uint16_t GEMATRIA_CYCLE_RAW[] = {
        1,2,3,4,5,6,7,8,9,10,20,20,30,40,40,50,50,60,70,80,80,90,90,100,200,300,400
    };
    for (int i = 0; i < POOL_SIZE; i++)
        genesis_pool[i] = (uint8_t)(GEMATRIA_CYCLE_RAW[i % 27] % 256);
}

int main() {
    printf("============================================================\n");
    printf("  FCH-ARX V3 BENCHMARK — Motor del Genesis\n");
    printf("  Erick Flores Zambrano | Torah Applied Sciences 2026\n");
    printf("============================================================\n\n");

    init_genesis_pool_simulated();

    /* Preparar datos de prueba (500 MB) */
    #define BLOCK_SIZE   4096
    #define TOTAL_MB     500
    #define TOTAL_BLOCKS (TOTAL_MB * 1024 * 1024 / BLOCK_SIZE)

    uint8_t *data   = (uint8_t*)malloc(BLOCK_SIZE);
    uint8_t  digest[32];

    /* Rellenar con datos pseudoaleatorios */
    for (int i = 0; i < BLOCK_SIZE; i++)
        data[i] = (uint8_t)(i * 7 + 9);

    printf("  Procesando %d MB en bloques de %d bytes...\n", TOTAL_MB, BLOCK_SIZE);
    fflush(stdout);

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    for (long b = 0; b < TOTAL_BLOCKS; b++) {
        data[0] = (uint8_t)(b & 0xFF);   /* Variar entrada */
        fch_arx_v3(data, BLOCK_SIZE, digest);
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);

    double elapsed = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;
    double mb_s    = TOTAL_MB / elapsed;

    printf("  Datos procesados : %d MB\n", TOTAL_MB);
    printf("  Tiempo           : %.3f segundos\n", elapsed);
    printf("  Velocidad        : %.2f MB/s\n", mb_s);
    printf("\n  Ultimo hash: ");
    for (int i = 0; i < 16; i++) printf("%02x", digest[i]);
    printf("...\n");
    printf("\n============================================================\n");
    printf("  COMPARACION:\n");
    printf("  FCH-ARX V3 (Genesis)  : %.2f MB/s\n", mb_s);
    printf("  FCH-ARX V2 (IHLD)     : 451.26 MB/s  (ref anterior)\n");
    printf("  SHA-256 + SHA-NI      : ~3000 MB/s   (hardware dedicado)\n");
    printf("============================================================\n");

    free(data);
    return 0;
}
