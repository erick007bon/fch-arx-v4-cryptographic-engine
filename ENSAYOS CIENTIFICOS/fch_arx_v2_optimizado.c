/*
 * FCH-ARX V2 OPTIMIZADO — Benchmark de Velocidad
 * ================================================
 * Tecnicas aplicadas:
 *   1. Tablas pre-calculadas: elimina i%9 e i%24 (division = lenta)
 *   2. Loop Unrolling x8: procesa 8 bytes por iteracion en vez de 1
 *   3. Variables en registro (register): sugiere al CPU mantener vars en cache L1
 *   4. Expansion de la Rueda Fibonacci: acceso directo sin modulo
 *   5. Comparativa: Original vs Optimizado vs "Estimado SHA-256 C puro"
 *
 * Compilar: gcc fch_arx_v2_optimizado.c -o bench_opt.exe -O3 -march=native
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

/* ============================================================
 * CONSTANTES GLOBALES
 * ============================================================ */

/* Cuadrado Magico de Saturno x Constante Aurea (Phi) */
static const uint32_t SATURN_INIT[9] = {
    (4u * 0x9E3779B9u),
    (9u * 0x9E3779B9u),
    (2u * 0x9E3779B9u),
    (3u * 0x9E3779B9u),
    (5u * 0x9E3779B9u),
    (7u * 0x9E3779B9u),
    (8u * 0x9E3779B9u),
    (1u * 0x9E3779B9u),
    (6u * 0x9E3779B9u)
};

/* Rueda de Fibonacci mod-9 de periodo 24 */
static const uint32_t FIB_WHEEL[24] = {
    1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9
};

/*
 * TECNICA 1: Expansion de la tabla combinada W[i] * (i+1)
 * Pre-calculamos los primeros 512 valores para eliminar la multiplicacion
 * en el loop. Para i >= 512, seguimos calculando (textos largos).
 */
#define PRECOMPUTE_SIZE 512
static uint32_t WEIGHT_TABLE[PRECOMPUTE_SIZE];

static void init_weight_table(void) {
    for (int i = 0; i < PRECOMPUTE_SIZE; i++) {
        WEIGHT_TABLE[i] = FIB_WHEEL[i % 24] * (uint32_t)(i + 1);
    }
}

/* Macro ROL de 32 bits (el compilador lo convierte en 1 instruccion CPU) */
#define ROL32(x, r) (((x) << (r)) | ((x) >> (32 - (r))))

/* ============================================================
 * VERSION 1: FCH-ARX V2 ORIGINAL (Sin optimizaciones manuales)
 * ============================================================ */
void fch_arx_original(const uint8_t *data, size_t length, uint32_t *out) {
    uint32_t M[9];
    memcpy(M, SATURN_INIT, sizeof(M));

    for (size_t i = 0; i < length; i++) {
        uint32_t val  = (uint32_t)data[i];
        uint32_t W    = FIB_WHEEL[i % 24] * (uint32_t)(i + 1);
        int      idx  = (int)(i % 9);

        M[idx]            = M[idx] + val + W;
        M[(idx+1) % 9]    = ROL32(M[(idx+1) % 9], 3);
        M[(idx+2) % 9]    = ROL32(M[(idx+2) % 9], 6);
        M[(idx+3) % 9]    = ROL32(M[(idx+3) % 9], 9);
        M[(idx+4) % 9]   ^= M[idx];
        M[(idx+5) % 9]   ^= M[(idx+1) % 9];
        M[(idx+6) % 9]   ^= M[(idx+2) % 9];
    }

    /* Finalizacion: 26 rondas Trinomio */
    for (int i = 0; i < 26; i++) {
        M[i % 9]          = M[i % 9] + M[(i+8) % 9] + 26u;
        M[(i+1) % 9]      = ROL32(M[(i+1) % 9], 3);
        M[(i+2) % 9]      = ROL32(M[(i+2) % 9], 6);
        M[(i+3) % 9]      = ROL32(M[(i+3) % 9], 9);
        M[(i+4) % 9]      = ROL32(M[(i+4) % 9], 7);
        M[(i+5) % 9]     ^= (M[i % 9] + 7u);
        M[(i+6) % 9]     ^= ROL32(M[(i+1) % 9], 26);
    }

    for (int k = 0; k < 8; k++) out[k] = M[k] ^ M[(k+1) % 9];
}

/* ============================================================
 * VERSION 2: FCH-ARX V2 OPTIMIZADO
 *   - Tabla WEIGHT_TABLE[] elimina i%24 y multiplicacion
 *   - idx se incrementa manualmente (sin i%9)
 *   - Loop unrolling x9 (ciclo completo de Saturno)
 * ============================================================ */
void fch_arx_optimized(const uint8_t *data, size_t length, uint32_t *out) {
    register uint32_t M0 = SATURN_INIT[0];
    register uint32_t M1 = SATURN_INIT[1];
    register uint32_t M2 = SATURN_INIT[2];
    register uint32_t M3 = SATURN_INIT[3];
    register uint32_t M4 = SATURN_INIT[4];
    register uint32_t M5 = SATURN_INIT[5];
    register uint32_t M6 = SATURN_INIT[6];
    register uint32_t M7 = SATURN_INIT[7];
    register uint32_t M8 = SATURN_INIT[8];

    /* Procesamos bloques de 9 bytes (1 ciclo de Saturno completo)
     * Esto elimina la condicion i%9 del loop original. */
    size_t full_cycles = length / 9;
    size_t remainder   = length % 9;
    size_t base        = 0;

    for (size_t cycle = 0; cycle < full_cycles; cycle++, base += 9) {
        /* 9 bytes = 1 ciclo completo. idx fijo por posicion. */
        /* Byte 0 -> idx=0 */
        uint32_t w = (base < PRECOMPUTE_SIZE) ? WEIGHT_TABLE[base] : FIB_WHEEL[base%24]*(uint32_t)(base+1);
        M0 = M0 + (uint32_t)data[base] + w;
        M1 = ROL32(M1, 3); M2 = ROL32(M2, 6); M3 = ROL32(M3, 9);
        M4 ^= M0; M5 ^= M1; M6 ^= M2;

        /* Byte 1 -> idx=1 */
        w = ((base+1) < PRECOMPUTE_SIZE) ? WEIGHT_TABLE[base+1] : FIB_WHEEL[(base+1)%24]*(uint32_t)(base+2);
        M1 = M1 + (uint32_t)data[base+1] + w;
        M2 = ROL32(M2, 3); M3 = ROL32(M3, 6); M4 = ROL32(M4, 9);
        M5 ^= M1; M6 ^= M2; M7 ^= M3;

        /* Byte 2 -> idx=2 */
        w = ((base+2) < PRECOMPUTE_SIZE) ? WEIGHT_TABLE[base+2] : FIB_WHEEL[(base+2)%24]*(uint32_t)(base+3);
        M2 = M2 + (uint32_t)data[base+2] + w;
        M3 = ROL32(M3, 3); M4 = ROL32(M4, 6); M5 = ROL32(M5, 9);
        M6 ^= M2; M7 ^= M3; M8 ^= M4;

        /* Byte 3 -> idx=3 */
        w = ((base+3) < PRECOMPUTE_SIZE) ? WEIGHT_TABLE[base+3] : FIB_WHEEL[(base+3)%24]*(uint32_t)(base+4);
        M3 = M3 + (uint32_t)data[base+3] + w;
        M4 = ROL32(M4, 3); M5 = ROL32(M5, 6); M6 = ROL32(M6, 9);
        M7 ^= M3; M8 ^= M4; M0 ^= M5;

        /* Byte 4 -> idx=4 */
        w = ((base+4) < PRECOMPUTE_SIZE) ? WEIGHT_TABLE[base+4] : FIB_WHEEL[(base+4)%24]*(uint32_t)(base+5);
        M4 = M4 + (uint32_t)data[base+4] + w;
        M5 = ROL32(M5, 3); M6 = ROL32(M6, 6); M7 = ROL32(M7, 9);
        M8 ^= M4; M0 ^= M5; M1 ^= M6;

        /* Byte 5 -> idx=5 */
        w = ((base+5) < PRECOMPUTE_SIZE) ? WEIGHT_TABLE[base+5] : FIB_WHEEL[(base+5)%24]*(uint32_t)(base+6);
        M5 = M5 + (uint32_t)data[base+5] + w;
        M6 = ROL32(M6, 3); M7 = ROL32(M7, 6); M8 = ROL32(M8, 9);
        M0 ^= M5; M1 ^= M6; M2 ^= M7;

        /* Byte 6 -> idx=6 */
        w = ((base+6) < PRECOMPUTE_SIZE) ? WEIGHT_TABLE[base+6] : FIB_WHEEL[(base+6)%24]*(uint32_t)(base+7);
        M6 = M6 + (uint32_t)data[base+6] + w;
        M7 = ROL32(M7, 3); M8 = ROL32(M8, 6); M0 = ROL32(M0, 9);
        M1 ^= M6; M2 ^= M7; M3 ^= M8;

        /* Byte 7 -> idx=7 */
        w = ((base+7) < PRECOMPUTE_SIZE) ? WEIGHT_TABLE[base+7] : FIB_WHEEL[(base+7)%24]*(uint32_t)(base+8);
        M7 = M7 + (uint32_t)data[base+7] + w;
        M8 = ROL32(M8, 3); M0 = ROL32(M0, 6); M1 = ROL32(M1, 9);
        M2 ^= M7; M3 ^= M8; M4 ^= M0;

        /* Byte 8 -> idx=8 */
        w = ((base+8) < PRECOMPUTE_SIZE) ? WEIGHT_TABLE[base+8] : FIB_WHEEL[(base+8)%24]*(uint32_t)(base+9);
        M8 = M8 + (uint32_t)data[base+8] + w;
        M0 = ROL32(M0, 3); M1 = ROL32(M1, 6); M2 = ROL32(M2, 9);
        M3 ^= M8; M4 ^= M0; M5 ^= M1;
    }

    /* Procesar bytes restantes (tail) */
    for (size_t i = base; i < length; i++) {
        int idx = (int)(i % 9);
        uint32_t M[9] = {M0,M1,M2,M3,M4,M5,M6,M7,M8};
        uint32_t ww = (i < PRECOMPUTE_SIZE) ? WEIGHT_TABLE[i] : FIB_WHEEL[i%24]*(uint32_t)(i+1);
        M[idx]          = M[idx] + (uint32_t)data[i] + ww;
        M[(idx+1)%9]    = ROL32(M[(idx+1)%9], 3);
        M[(idx+2)%9]    = ROL32(M[(idx+2)%9], 6);
        M[(idx+3)%9]    = ROL32(M[(idx+3)%9], 9);
        M[(idx+4)%9]   ^= M[idx];
        M[(idx+5)%9]   ^= M[(idx+1)%9];
        M[(idx+6)%9]   ^= M[(idx+2)%9];
        M0=M[0];M1=M[1];M2=M[2];M3=M[3];M4=M[4];
        M5=M[5];M6=M[6];M7=M[7];M8=M[8];
    }

    /* Finalizacion Trinomio (26 rondas) */
    uint32_t MF[9] = {M0,M1,M2,M3,M4,M5,M6,M7,M8};
    for (int i = 0; i < 26; i++) {
        MF[i%9]       = MF[i%9] + MF[(i+8)%9] + 26u;
        MF[(i+1)%9]   = ROL32(MF[(i+1)%9], 3);
        MF[(i+2)%9]   = ROL32(MF[(i+2)%9], 6);
        MF[(i+3)%9]   = ROL32(MF[(i+3)%9], 9);
        MF[(i+4)%9]   = ROL32(MF[(i+4)%9], 7);
        MF[(i+5)%9]  ^= (MF[i%9] + 7u);
        MF[(i+6)%9]  ^= ROL32(MF[(i+1)%9], 26);
    }

    for (int k = 0; k < 8; k++) out[k] = MF[k] ^ MF[(k+1)%9];
}

/* ============================================================
 * BENCHMARK
 * ============================================================ */
static double bench(void (*fn)(const uint8_t*, size_t, uint32_t*),
                    const uint8_t *data, size_t size, const char *label) {
    uint32_t hash[8];
    clock_t start = clock();
    fn(data, size, hash);
    clock_t end   = clock();

    double secs  = (double)(end - start) / CLOCKS_PER_SEC;
    double mbps  = (size / (1024.0 * 1024.0)) / secs;

    printf("  %-28s | %7.3f s | %8.2f MB/s | Hash[0]: %08X\n",
           label, secs, mbps, hash[0]);
    return mbps;
}

int main(void) {
    init_weight_table();

    size_t SIZE = 500UL * 1024 * 1024; /* 500 MB */
    uint8_t *data = (uint8_t*)malloc(SIZE);
    if (!data) { puts("Sin memoria."); return 1; }

    /* Relleno pseudo-aleatorio */
    for (size_t i = 0; i < SIZE; i++) data[i] = (uint8_t)(i * 6364136223846793005ULL >> 56);

    printf("=============================================================\n");
    printf("  FCH-ARX V2 — BENCHMARK COMPARATIVO (500 MB)\n");
    printf("  Compilado con: GCC -O3 -march=native\n");
    printf("=============================================================\n");
    printf("  %-28s | %7s | %12s | %s\n", "Implementacion", "Tiempo", "Throughput", "Hash[0]");
    printf("  %s\n", "------------------------------------------------------------");

    double orig = bench(fch_arx_original,  data, SIZE, "FCH-ARX V2 Original");
    double opt  = bench(fch_arx_optimized, data, SIZE, "FCH-ARX V2 Optimizado");

    printf("=============================================================\n");
    printf("  Ganancia de velocidad: %.2fx mas rapido\n", opt / orig);
    printf("  (SHA-256 hardware C: ~3,000 MB/s como referencia)\n");
    printf("=============================================================\n");

    free(data);
    return 0;
}
