#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

const uint64_t FIB_WHEEL[24] = {1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9};

// Implementando FCH en C nativo para mostrar su velocidad bruta
uint64_t fch_hash(const char *data, size_t length) {
    uint64_t acc = 0;
    // Bucle altamente optimizado. El compilador en -O3 hará maravillas.
    for (size_t i = 0; i < length; i++) {
        acc += (uint64_t)(data[i]) * FIB_WHEEL[i % 24] * (i + 1);
    }
    return acc;
}

int main() {
    size_t size = 1024 * 1024 * 500; // 500 Megabytes
    char *data = (char *)malloc(size);
    if (!data) {
        printf("Fallo reservando memoria.\\n");
        return 1;
    }
    
    // Llenar memoria con data aleatoria simulada
    for(size_t i = 0; i < size; i++) {
        data[i] = (char)(i % 256);
    }

    printf("=========================================\\n");
    printf("[CAJA BLANCA] BENCHMARK FCH EN C NATIVO\\n");
    printf("=========================================\\n");
    printf("Procesando %zu Megabytes en Memoria Ram...\\n", size / (1024*1024));

    clock_t start = clock();
    uint64_t result = fch_hash(data, size);
    clock_t end = clock();

    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    double throughput = (size / (1024.0 * 1024.0)) / time_spent;

    int root = 1 + ((result - 1) % 9);
    
    printf("Acumulador base : %llu\\n", (unsigned long long)result);
    printf("Raiz (Root)     : %d\\n", root);
    printf("Tiempo de proc. : %.4f Segundos\\n", time_spent);
    printf("Throughput      : %.2f MB/segundo !\\n", throughput);
    printf("=========================================\\n");
    
    free(data);
    return 0;
}
