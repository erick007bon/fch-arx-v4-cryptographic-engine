# Torah Applied Sciences — Contexto del Proyecto

## Terminología Clave del Dominio (Lenguaje Compartido)

| Término | Significado en este proyecto |
|---------|------------------------------|
| **FCH-ARX V3** | Algoritmo de hash criptográfico que usa el Génesis como Piscina de Entropía |
| **Piscina de Entropía** | Los **78,364** valores gemátricos del Génesis en memoria (bytearray) — 22 formas normales + 5 sofit |
| **IHLD** | Generador sintético del V2 — `(i*7+9)%256`. OBSOLETO, reemplazado en V3 |
| **SAC Test** | Strict Avalanche Criterion — protocolo NIST FIPS 180-4 para validar hashes |
| **Gematría** | Sistema donde cada letra hebrea tiene valor numérico (Aleph=1...Tav=400) |
| **YHVH-26** | El Nombre divino = valor gemátrico 26. Número de rondas de finalización del algoritmo |
| **Trinomio** | La arquitectura ARX: Add + Rotate + XOR |
| **Rueda Pisano** | Fibonacci módulo 9, período 24. Pesos de absorción del hash |
| **Cuadrado de Saturno** | `[4,9,2,3,5,7,8,1,6]` — estado inicial de las 9 cámaras de 32 bits |
| **Tesla 3-6-9** | Las rotaciones de bits: ROL(3), ROL(6), ROL(9) |
| **Hub Rojo** | Letra con >10% de frecuencia en el corpus (Yod=11.57%, Vav=10.81%) |
| **Entropía de Shannon** | Medida de aleatoriedad del corpus: el Génesis tiene 4.2215 bits (94.66% del máximo) |
| **Capítulo 41** | El capítulo de mayor energía gemátrica: Sueños del Faraón (228,697 unidades) |
| **bereshit.json** | El Génesis completo descargado desde Sefaria API (50 caps, 1,533 vers, 73,128 letras) |
| **gbrain** | Servidor MCP de memoria persistente (garrytan/gbrain) — instalado en Claude Desktop |

## Archivos Clave del Proyecto

```
08_gematria_torah/
├── data/raw/bereshit.json              ← Génesis completo (Sefaria API)
├── ENSAYOS CIENTIFICOS/
│   ├── fch_arx_v3_core.py             ← Motor V3 + SAC Test (RESULTADO: 49.9909%)
│   ├── genesis_entropy_analysis.py    ← Análisis de frecuencia + gráficos
│   └── fch_arx_v3_benchmark.c         ← Benchmark de velocidad en C
├── visualizations/
│   └── genesis_entropy_map.png        ← Mapa de entropía orgánica del Génesis
├── FCH_ARX_V3_CORE.md                 ← Documentación oficial V3
├── TORA_MASTER_LOG.md                 ← Diario de descubrimientos
└── .claude/commands/                  ← Skills de Matt Pocock instaladas
```

## Resultados Científicos Confirmados (2026-04-29)

| Experimento | Resultado |
|------------|-----------|
| SAC Test V3 (10,000 pares) | **49.9909%** ✅ NIST APROBADO |
| Desviación del 50% ideal | **0.0091%** (5.4x mejor que V2) |
| Corpus del Génesis (exacto) | **78,364 letras** (22 formas + 5 sofit) |
| Corpus corregido (2026-04-30) | +5,236 sofit — Ley del Sofer aplicada |
| Entropía de Shannon corpus | **4.2215 bits** (94.66% del máximo teórico) |
| Super-Hubs del Génesis | Yod(11.57%) + Vav(10.81%) + Aleph(9.75%) + He(8.03%) = **YHVH** |
| Capítulo de mayor energía | **Génesis 41** (Sueños del Faraón) = 228,697 unidades |

## Estado Actual

- **FCH-ARX V3**: Motor funcional con Génesis real. SAC NIST aprobado.
- **Análisis C**: Frecuencias, energías, entropía de Shannon documentados.
- **Benchmark B**: Código C compilable listo en `fch_arx_v3_benchmark.c`.
- **Próximo**: Paper científico + benchmark compilado + FCH-ARX-512 bits.
