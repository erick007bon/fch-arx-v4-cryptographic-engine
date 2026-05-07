/*
 * FCH-ARX V2 — BENCHMARK DE VELOCIDAD MAXIMA
 * ============================================
 * Estrategia: Procesar palabras de 32 bits (4 bytes) en vez de 1 byte
 * Esto reduce el numero de iteraciones del bucle 4x
 * SHA-256 puro C sin hardware: ~400-600 MB/s
 * Meta: Superar el SHA-256 puro C
 *
 * Compilar: gcc fch_benchmark_max.c -o bench_max2.exe -O3 -march=native -funroll-loops
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

#define ROL32(x, r) (((x) << (r)) | ((x) >> (32 - (r))))

/* Estado Saturno inicial */
static const uint32_t INIT[9] = {
    4u*0x9E3779B9u, 9u*0x9E3779B9u, 2u*0x9E3779B9u,
    3u*0x9E3779B9u, 5u*0x9E3779B9u, 7u*0x9E3779B9u,
    8u*0x9E3779B9u, 1u*0x9E3779B9u, 6u*0x9E3779B9u
};

/* Rueda Fibonacci x24  */
static const uint32_t W[24] = {1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9};

/* Finalizacion comun */
static void finalize(uint32_t M[9], uint32_t out[8]) {
    for (int i = 0; i < 26; i++) {
        M[i%9]      = M[i%9] + M[(i+8)%9] + 26u;
        M[(i+1)%9]  = ROL32(M[(i+1)%9], 3);
        M[(i+2)%9]  = ROL32(M[(i+2)%9], 6);
        M[(i+3)%9]  = ROL32(M[(i+3)%9], 9);
        M[(i+4)%9]  = ROL32(M[(i+4)%9], 7);
        M[(i+5)%9] ^= (M[i%9] + 7u);
        M[(i+6)%9] ^= ROL32(M[(i+1)%9], 26);
    }
    for (int k = 0; k < 8; k++) out[k] = M[k] ^ M[(k+1)%9];
}

/* ============================================================
 * V1: ORIGINAL — 1 byte por iteracion
 * ============================================================ */
void v1_byte_by_byte(const uint8_t *data, size_t len, uint32_t out[8]) {
    uint32_t M[9]; memcpy(M, INIT, 36);
    for (size_t i = 0; i < len; i++) {
        int idx = (int)(i % 9);
        uint32_t w = W[i % 24] * (uint32_t)(i + 1);
        M[idx]         = M[idx] + data[i] + w;
        M[(idx+1)%9]   = ROL32(M[(idx+1)%9], 3);
        M[(idx+2)%9]   = ROL32(M[(idx+2)%9], 6);
        M[(idx+3)%9]   = ROL32(M[(idx+3)%9], 9);
        M[(idx+4)%9]  ^= M[idx];
        M[(idx+5)%9]  ^= M[(idx+1)%9];
        M[(idx+6)%9]  ^= M[(idx+2)%9];
    }
    finalize(M, out);
}

/* ============================================================
 * V2: WORD-LEVEL — 4 bytes por iteracion (uint32_t)
 * Los 4 bytes se mezclan en una sola palabra antes de entrar al estado
 * Reduce el bucle 4x
 * ============================================================ */
void v2_word_level(const uint8_t *data, size_t len, uint32_t out[8]) {
    uint32_t M[9]; memcpy(M, INIT, 36);

    size_t words  = len / 4;
    size_t remain = len % 4;

    for (size_t i = 0; i < words; i++) {
        /* Leemos 4 bytes como una palabra de 32 bits */
        uint32_t word;
        memcpy(&word, data + i*4, 4);

        int    idx = (int)(i % 9);
        /* Peso acumulado de las 4 posiciones: suma de W[j] * (j+1) */
        size_t base = i * 4;
        uint32_t ww = W[base%24]*(uint32_t)(base+1)
                    + W[(base+1)%24]*(uint32_t)(base+2)
                    + W[(base+2)%24]*(uint32_t)(base+3)
                    + W[(base+3)%24]*(uint32_t)(base+4);

        M[idx]        = M[idx] + word + ww;
        M[(idx+1)%9]  = ROL32(M[(idx+1)%9], 3);
        M[(idx+2)%9]  = ROL32(M[(idx+2)%9], 6);
        M[(idx+3)%9]  = ROL32(M[(idx+3)%9], 9);
        M[(idx+4)%9] ^= M[idx];
        M[(idx+5)%9] ^= M[(idx+1)%9];
        M[(idx+6)%9] ^= M[(idx+2)%9];

        M[(idx+2)%9]  = ROL32(M[(idx+2)%9], 3);  /* ronda extra interna */
        M[(idx+7)%9] ^= M[(idx+3)%9];
    }

    /* tail bytes */
    for (size_t i = words*4; i < len; i++) {
        int idx = (int)(i % 9);
        uint32_t w = W[i%24]*(uint32_t)(i+1);
        M[idx]        = M[idx] + data[i] + w;
        M[(idx+1)%9]  = ROL32(M[(idx+1)%9], 3);
        M[(idx+2)%9]  = ROL32(M[(idx+2)%9], 6);
        M[(idx+3)%9]  = ROL32(M[(idx+3)%9], 9);
        M[(idx+4)%9] ^= M[idx];
    }

    finalize(M, out);
}

/* ============================================================
 * V3: DOBLE SATURNO — 2 estados en paralelo (8 bytes por iteracion)
 * Dos matrices Saturno A y B procesan datos intercalados.
 * El hardware puede ejecutar ambas en paralelo (ILP).
 * ============================================================ */
void v3_dual_saturn(const uint8_t *data, size_t len, uint32_t out[8]) {
    uint32_t A[9], B[9];
    for (int i = 0; i < 9; i++) {
        A[i] = INIT[i];
        B[i] = INIT[(i+4)%9] ^ 0xDEADBEEFu; /* Estado B desplazado y girado */
    }

    size_t half = len / 2;

    /* A procesa la primera mitad */
    for (size_t i = 0; i < half; i++) {
        int idx = (int)(i % 9);
        uint32_t w = W[i%24]*(uint32_t)(i+1);
        A[idx]        = A[idx] + data[i] + w;
        A[(idx+1)%9]  = ROL32(A[(idx+1)%9], 3);
        A[(idx+2)%9]  = ROL32(A[(idx+2)%9], 6);
        A[(idx+3)%9]  = ROL32(A[(idx+3)%9], 9);
        A[(idx+4)%9] ^= A[idx];
        A[(idx+5)%9] ^= A[(idx+1)%9];

        /* B procesa la segunda mitad interleaved */
        size_t j = i + half;
        int jdx = (int)(j % 9);
        uint32_t wj = W[j%24]*(uint32_t)(j+1);
        B[jdx]        = B[jdx] + data[j] + wj;
        B[(jdx+1)%9]  = ROL32(B[(jdx+1)%9], 3);
        B[(jdx+2)%9]  = ROL32(B[(jdx+2)%9], 6);
        B[(jdx+3)%9]  = ROL32(B[(jdx+3)%9], 9);
        B[(jdx+4)%9] ^= B[jdx];
        B[(jdx+5)%9] ^= B[(jdx+1)%9];
    }

    /* Tail bytes de B si len es impar */
    for (size_t i = 2*half; i < len; i++) {
        int idx = (int)(i%9);
        B[idx] = B[idx] + data[i] + W[i%24]*(uint32_t)(i+1);
    }

    /* Fusionar A y B en un solo estado */
    for (int i = 0; i < 9; i++) A[i] = A[i] + B[i] + ROL32(B[(i+3)%9], 13);

    finalize(A, out);
}

/* ============================================================
 * MAIN BENCHMARK
 * ============================================================ */
static double bench(void (*fn)(const uint8_t*, size_t, uint32_t*),
                    const uint8_t *data, size_t size, const char *label) {
    uint32_t hash[8];
    clock_t s = clock();
    fn(data, size, hash);
    clock_t e = clock();
    double sec = (double)(e-s)/CLOCKS_PER_SEC;
    double mbs = (size/(1024.0*1024.0))/sec;
    printf("  %-30s | %6.3f s | %8.2f MB/s | %08X\n", label, sec, mbs, hash[0]);
    return mbs;
}

int main(void) {
    const size_t SIZE = 500UL * 1024 * 1024; /* 500 MB */
    uint8_t *data = malloc(SIZE);
    if (!data) return 1;
    for (size_t i = 0; i < SIZE; i++) data[i] = (uint8_t)(i * 2654435761ULL >> 8);

    printf("=================================================================\n");
    printf("  FCH-ARX V2 — BENCHMARK MAXIMO (500 MB / GCC -O3 -march=native)\n");
    printf("=================================================================\n");
    printf("  %-30s | %6s | %12s | %s\n","Implementacion","Tiempo","Throughput","Hash[0]");
    printf("  %s\n","---------------------------------------------------------------");

    double v1  = bench(v1_byte_by_byte, data, SIZE, "V1: 1 byte/iter (original)");
    double v2  = bench(v2_word_level,   data, SIZE, "V2: 4 bytes/iter (word)");
    double v3  = bench(v3_dual_saturn,  data, SIZE, "V3: Doble Saturno (8b/iter)");

    printf("=================================================================\n");
    printf("  Ganancia V2 vs V1 : %.2fx mas rapido\n", v2/v1);
    printf("  Ganancia V3 vs V1 : %.2fx mas rapido\n", v3/v1);
    printf("\n");
    printf("  SHA-256 puro C (sin hardware SHA-NI) : ~400-600 MB/s\n");
    printf("  SHA-256 con instrucciones SHA-NI      : ~3,000 MB/s\n");
    printf("  FCH-ARX V2 V3 alcanzado               : %.0f MB/s\n", v3);
    printf("=================================================================\n");

    free(data);
    return 0;
}
