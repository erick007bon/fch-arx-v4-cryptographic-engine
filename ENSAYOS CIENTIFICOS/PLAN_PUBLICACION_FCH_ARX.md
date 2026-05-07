# PLAN MAESTRO — FCH-ARX V2 → PUBLICACIÓN CIENTÍFICA REAL
# Autor: Erick Reinaldo Flores Zambrano
# Horizonte: 2 meses (Mayo-Junio 2026)
# Meta: Enviar a RISTI, Scielo o IEEE Latin America Transactions

---

## FASE 1 — BLINDAJE TÉCNICO (Semanas 1-3)

### 1.1 Full NIST SP800-22 (las 15 pruebas, no solo SAC)
Las 15 pruebas estadísticas del NIST son el estándar de oro:

| # | Prueba | Qué mide |
|---|--------|----------|
| 1 | Frequency (Monobit) | Proporción de 1s y 0s |
| 2 | Block Frequency | Bloques balanceados |
| 3 | Runs | Secuencias de bits consecutivos |
| 4 | Longest Run | Racha máxima de 1s |
| 5 | Binary Matrix Rank | Independencia lineal |
| 6 | DFT Spectral | Periodicidades ocultas |
| 7 | Non-overlapping Templates | Patrones de bits |
| 8 | Overlapping Templates | Ocurrencias de patrones |
| 9 | Maurer Universal | Compresibilidad |
| 10 | Linear Complexity | Complejidad del registro |
| 11 | Serial | Uniformidad de pares |
| 12 | Approximate Entropy | Entropía aproximada |
| 13 | Cumulative Sums | Sumas parciales |
| 14 | Random Excursions | Variantes de excursión |
| 15 | Random Excursions Variant | Visitas a estados |

**Archivo:** `nist_full_battery.py` — Ejecuta las 15 pruebas sobre 1,000 hashes de FCH-ARX V2

### 1.2 Atbash y Albam como Capas de Permutación
Integrar los cifrados históricos de la Torá al FCH-ARX V3:

```
ATBASH LAYER (en la absorción):
  Antes de XOR: aplicar permutación Atbash a los bits de posición
  byte_mod = ATBASH_TABLE[byte % 22]  ← tabla de 22 posiciones

ALBAM LAYER (en la finalización):
  En las rondas pares: usar permutación Albam en lugar de ROL(7)
  Esto crea no-linealidad adicional basada en cifrados históricos probados

RESULTADO: FCH-ARX V3 = ARX + Atbash + Albam
```

Esto convierte el paper en algo ÚNICO: ningún algoritmo moderno incorpora
teoría criptográfica histórica de manera matemáticamente justificada.

### 1.3 Análisis Diferencial Básico
Probar: si cambio 1 bit de entrada, ¿cuántos bits cambian en promedio por ronda?
- Ronda 1: esperado ~1-2 bits
- Ronda 5: esperado ~50 bits
- Ronda 26: esperado ~128 bits (50% de 256)

**Archivo:** `differential_analysis.py`

---

## FASE 2 — EL PAPER (Semanas 4-6)

### Estructura del Artículo (IEEE format, 6-8 páginas)

```
TÍTULO:
"FCH-ARX: A Cryptographic Hash Function Derived from
Torah Mathematical Structures and ARX Architecture"

ABSTRACT (150 palabras):
FCH-ARX es un algoritmo hash de 256 bits que integra
constantes estructurales de la Torá hebrea (YHVH=26,
Omer=7, Tesla=3-6-9) en una arquitectura ARX moderna.
Resultados: SAC=49.95% (NIST aprobado), velocidad 185 MB/s
en C nativo, resistencia demostrada a ataques algebraicos.

SECCIONES:
1. Introducción — Marco matemático de la Torá
2. Arquitectura FCH-ARX — El trinomio ADD-ROTATE-XOR
3. Las Constantes Sagradas como Parámetros Criptográficos
4. Resultados del NIST SP800-22 (las 15 pruebas)
5. Análisis de Resistencia a Ataques
6. Comparación con SHA-256, BLAKE3, Keccak
7. Conclusiones y Trabajo Futuro
```

### La Contribución Nueva (lo que hace el paper aceptable)
No es "hice un hash". Es:
> "Demostramos que constantes numéricas presentes en textos
> sagrados de 3,500 años de antigüedad satisfacen las
> propiedades matemáticas requeridas para entropy maximization
> en funciones hash criptográficas modernas."

Eso sí es una hipótesis comprobable. Eso sí es ciencia.

---

## FASE 3 — LA WEB DE RETO (Semanas 7-8)

### Concepto: "Hash Challenge — Can You Break FCH-ARX?"

```
URL: fch-arx-challenge.vercel.app

PÁGINA 1 — El Reto:
  "Encuentra dos textos diferentes que produzcan el mismo hash FCH-ARX V2.
   Premio: Tu nombre en el paper como co-autor."

PÁGINA 2 — El Verificador:
  Input: Cualquier texto
  Output: Hash FCH-ARX V2 (256 bits, hex)
  Botón: "Verificar colisión" → si dos inputs dan el mismo hash → ROMPISTE EL ALGORITMO

PÁGINA 3 — El Marcador:
  Lista de intentos fallidos (anónimos)
  Contador de días desde el lanzamiento sin colisión

BACKEND: Python + FastAPI en Render (gratis)
FRONTEND: Next.js (ya sabes hacerlo)
```

### Seguridad del Reto
- Los hashes se calculan en el servidor (nadie ve el código fuente del algoritmo)
- Se registran todos los intentos en MongoDB (o PostgreSQL)
- Si alguien encuentra colisión → notificación automática por email

---

## FASE 4 — PUBLICACIÓN (Fin del Mes 2)

### Revistas objetivo (con factor de impacto):

| Revista | País | Factor | Tiempo revisión |
|---------|------|--------|-----------------|
| RISTI (Ibérica de SI) | Portugal/España | Indexada | 2-3 meses |
| IEEE Latin America Trans | Internacional | Q2 | 3-4 meses |
| Computación y Sistemas | México | Scopus | 2-3 meses |
| Ingenius (UPS Ecuador) | Ecuador | Local | 1-2 meses |

**Recomendación:** Enviar primero a Ingenius (Ecuador, revisión rápida) para
tener un paper publicado real, luego enviar versión mejorada a RISTI.

---

## CRONOGRAMA 8 SEMANAS

| Semana | Tarea | Entregable |
|--------|-------|------------|
| 1 | NIST full battery (15 tests) | nist_full_battery.py |
| 2 | FCH-ARX V3 (+ Atbash/Albam) | fch_arx_v3.py + .c |
| 3 | Análisis diferencial por rondas | differential_analysis.py |
| 4 | Comparación SHA256/BLAKE3/Keccak | benchmark_comparativo.py |
| 5 | Draft del paper (inglés) | fch_paper_draft.md |
| 6 | Revisión + figuras y tablas | paper_final.pdf |
| 7 | Web Challenge (backend+frontend) | Desplegado en Vercel |
| 8 | Envío a revista + anuncio LinkedIn | Submission confirmation |

---
*Guardado: 2026-04-21 | Proyecto 3 — Roadmap a Publicación*
