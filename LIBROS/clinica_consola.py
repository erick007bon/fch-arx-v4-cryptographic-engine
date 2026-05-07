# -*- coding: utf-8 -*-
"""
CLINICA IA TORAH — Motor de Gematria y Patrones Sagrados
=========================================================
Autor: Erick Reinaldo Flores Zambrano
Fecha: 2026-04-18
Proposito: Ingenieria Inversa del Algoritmo de la Creacion
           Todo en consola. Solo para estudio personal.

Ejecutar: python clinica_consola.py
"""

import os
import sys
import time
import hashlib
import math

# Forzar UTF-8 en Windows para que los caracteres especiales se impriman bien
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    os.system('chcp 65001 >nul 2>&1')

# ============================================================
# MODULO 1: TABLA GEMATRIA COMPLETA
# ============================================================

GEMATRIA_STANDARD = {
    'alef': 1,  'bet': 2,   'gimel': 3,  'dalet': 4,  'he': 5,
    'vav': 6,   'zayin': 7, 'chet': 8,   'tet': 9,    'yod': 10,
    'kaf': 20,  'lamed': 30,'mem': 40,   'nun': 50,   'samech': 60,
    'ayin': 70, 'pe': 80,   'tzade': 90, 'kof': 100,  'resh': 200,
    'shin': 300,'tav': 400,
}

# Letras — (Nombre, Simbolo ASCII, Significado, Descripcion)
LETRAS_INFO = {
    1:  ('Alef',   '[Alef]',   'Buey/Lider',    'El primero. Silencio. Dios uno.'),
    2:  ('Bet',    '[Bet]',    'Casa',           'La primera letra de la Tora. El hogar. Lo material.'),
    3:  ('Gimel',  '[Gimel]',  'Camello',        'Movimiento. El puente entre el rico y el pobre.'),
    4:  ('Dalet',  '[Dalet]',  'Puerta',         'Umbral. La puerta del bien y del mal.'),
    5:  ('He',     '[He]',     'Ventana',        'El aliento de Dios. Aparece 2x en YHVH.'),
    6:  ('Vav',    '[Vav]',    'Gancho/Clavo',   'Conexion. El eje del universo. El 6 dia.'),
    7:  ('Zayin',  '[Zayin]',  'Espada',         'La lucha. El Shabat (7). El corte divino.'),
    8:  ('Chet',   '[Chet]',   'Vallado',        'Vida (Chai=18=8 reducido). El limite sagrado.'),
    9:  ('Tet',    '[Tet]',    'Serpiente',      'El bien oculto. Tesla. La espiral del universo.'),
    10: ('Yod',    '[Yod]',    'Mano',           'El punto primordial. La semilla de todo. Primera letra de YHVH.'),
    20: ('Kaf',    '[Kaf]',    'Palma',          'La capacidad de recibir. La corona.'),
    30: ('Lamed',  '[Lamed]',  'Aguijon',        'El aprendizaje. La letra mas alta del alfabeto.'),
    40: ('Mem',    '[Mem]',    'Agua',           'La matriz. El origen. La madre de las madres.'),
    50: ('Nun',    '[Nun]',    'Pez',            'La fe en la oscuridad. Netzach: eternidad.'),
    60: ('Samech', '[Samech]', 'Soporte',        'El circulo perfecto. El soporte divino.'),
    70: ('Ayin',   '[Ayin]',   'Ojo',            'Ver con el ojo espiritual antes de hablar.'),
    80: ('Pe',     '[Pe]',     'Boca',           'El habla creadora. Moises tenia 80 cuando fue llamado.'),
    90: ('Tzade',  '[Tzade]',  'Justo',          'El tzaddik: el justo que sostiene el mundo.'),
    100:('Kof',    '[Kof]',    'Nuca/Mono',      'El espejo del Kaf. Lo sagrado vs lo profano.'),
    200:('Resh',   '[Resh]',   'Cabeza',         'El principio. La mente. El inicio de todo razonamiento.'),
    300:('Shin',   '[Shin]',   'Diente/Fuego',   'La letra del fuego y el espiritu. Shekinah.'),
    400:('Tav',    '[Tav]',    'Cruz/Sello',     'El sello final. La ultima letra = el fin del ciclo.'),
}

# Numeros sagrados y su significado
NUMEROS_SAGRADOS = {
    1:   'Alef — El Uno primordial. Antes de todo.',
    2:   'Bet — La Casa. La dualidad. El segundo dia sin tov.',
    3:   'Gimel — El movimiento. La Trinidad. Las 3 Madres: ADD-ROT-XOR.',
    7:   'Zayin — El Shabat. La completud. Los 7 dias.',
    8:   'Chet — Chai (vida). El infinito enderezado.',
    9:   'Tet — La serpiente de Tesla. El numero que siempre regresa a si mismo.',
    10:  'Yod — La mano de Dios. Los 10 dedos. Las 10 Sefirot.',
    12:  'Las 12 tribus. Los 12 meses. Las 12 Letras Simples.',
    13:  'Echad (uno en gematria). El amor. la unidad superior.',
    17:  'TOV (bueno). El 7o primo. Pe es la letra 17. El punto de inflexion.',
    18:  'CHAI (vida). 9+9. 2x9. La vitalidad maxima.',
    22:  'Las 22 letras del alefato. El alfabeto completo. El universo en letras.',
    24:  'El periodo de la Rueda Fibonacci. Las 24 horas. El ciclo completo.',
    26:  'YHVH. El nombre de Dios. Las 26 rondas del FCH-ARX V2.',
    32:  'Los 32 senderos de sabiduria. 10 Sefirot + 22 Letras.',
    36:  'Los 36 justos ocultos que sostienen el mundo (Lamed-Vav).',
    40:  'Los 40 dias de diluvio. Los 40 anos en el desierto. El Mem.',
    49:  '7x7. Los 49 dias del Omer. La preparacion para recibir la Tora.',
    50:  'El 50% de SAC = entropia perfecta. Jubileo (50 anos). Nun.',
    72:  'Los 72 Nombres de Dios. El software del universo.',
    108: 'La suma de la Rueda de 24. 72+36. Ciclo cosmico.',
    216: '6 elevado al cubo. Las 216 letras de los 72 Nombres.',
    2701:'Gematria de Genesis 1:1. Triangulo 73. 37x73.',
}

# Los 72 Nombres (transliteracion)
NOMBRES_72 = [
    'VHV','YLY','SYT','OLM','MHSh','LLH','AKA','KHTh','HZY','ALD',
    'AAL','OHO','YZL','MBH','HRY','HKM','LVV','KLY','LVV','PHH',
    'NLK','YYY','MLD','ChHV','NThH','HAA','YRTh','ShAH','RYY','AVM',
    'LKB','VShR','YCh','LHCh','KVK','MND','ANY','ChAM','RHO','YYZ',
    'HHH','MYK','VVL','YLH','SAL','ORI','OShL','MYH','VHV','DNY',
    'HChSh','OMM','NNA','NYTh','MBH','PVY','NMM','YYL','HRCh','MTzR',
    'VMB','YHH','ONV','MChY','DMB','MNK','AYO','ChBV','RAH','YBM',
    'HYY','MVM',
]

NUMEROS_SAGRADOS_EXTRA = {}  # para expansion futura

# ============================================================
# MODULO 2: FUNCIONES CORE
# ============================================================

def calcular_gematria_nombre(nombre_letra):
    """Calcula gematria dado nombre de letra en espanol."""
    return GEMATRIA_STANDARD.get(nombre_letra.lower(), 0)

def digital_root(n):
    """Reduccion teosofica: suma de digitos hasta 1 cifra."""
    if n == 0:
        return 0
    return 1 + (n - 1) % 9 if n % 9 != 0 else 9

def gematria_texto(texto):
    """
    Calcula gematria de texto en espanol/transliteracion.
    Asigna valores segun tabla Sefer Yetzirah.
    """
    # Mapa simple de transliteracion
    mapa = {
        'a': 1,  'b': 2,  'g': 3,  'd': 4,  'h': 5,  'v': 6,  'z': 7,
        'c': 8,  't': 9,  'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50,
        's': 60, 'o': 70, 'p': 80, 'q': 90, 'r': 200, 'w': 300,'f': 400,
        'e': 5,  'i': 10, 'u': 6,  'j': 10, 'x': 60,
    }
    total = 0
    for char in texto.lower():
        total += mapa.get(char, 0)
    return total

def analizar_numero(n):
    """Analiza un numero: reduccion, patrones sagrados, letras."""
    raiz = digital_root(n)
    resultado = {
        'numero': n,
        'raiz_digital': raiz,
        'es_sagrado': n in NUMEROS_SAGRADOS,
        'significado': NUMEROS_SAGRADOS.get(n, None),
        'letra_raiz': LETRAS_INFO.get(raiz, None),
        'divisible_17': n % 17 == 0,
        'divisible_26': n % 26 == 0,
        'divisible_72': n % 72 == 0,
        'divisible_9':  n % 9 == 0,
        'divisible_7':  n % 7 == 0,
    }
    return resultado

def pisano_wheel(n):
    """Posicion en la Rueda Fibonacci (periodo 24)."""
    WHEEL = [1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9]
    return WHEEL[n % 24]

def fch_arx_v2(mensaje):
    """Hash FCH-ARX V2 del mensaje."""
    SATURN = [4*0x9E3779B9, 9*0x9E3779B9, 2*0x9E3779B9,
              3*0x9E3779B9, 5*0x9E3779B9, 7*0x9E3779B9,
              8*0x9E3779B9, 1*0x9E3779B9, 6*0x9E3779B9]
    FIB = [1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9]
    M = [s & 0xFFFFFFFF for s in SATURN]

    def rol32(x, r):
        x &= 0xFFFFFFFF
        return ((x << r) | (x >> (32-r))) & 0xFFFFFFFF

    data = mensaje.encode('utf-8') if isinstance(mensaje, str) else mensaje
    for i, byte in enumerate(data):
        idx = i % 9
        w = FIB[i % 24] * (i + 1)
        M[idx] = (M[idx] + byte + w) & 0xFFFFFFFF
        M[(idx+1)%9] = rol32(M[(idx+1)%9], 3)
        M[(idx+2)%9] = rol32(M[(idx+2)%9], 6)
        M[(idx+3)%9] = rol32(M[(idx+3)%9], 9)
        M[(idx+4)%9] ^= M[idx]
        M[(idx+5)%9] ^= M[(idx+1)%9]
        M[(idx+6)%9] ^= M[(idx+2)%9]

    for i in range(26):
        M[i%9] = (M[i%9] + M[(i+8)%9] + 26) & 0xFFFFFFFF
        M[(i+1)%9] = rol32(M[(i+1)%9], 3)
        M[(i+2)%9] = rol32(M[(i+2)%9], 6)
        M[(i+3)%9] = rol32(M[(i+3)%9], 9)
        M[(i+4)%9] = rol32(M[(i+4)%9], 7)
        M[(i+5)%9] ^= (M[i%9] + 7) & 0xFFFFFFFF
        M[(i+6)%9] ^= rol32(M[(i+1)%9], 26)

    return ''.join(f'{M[k] ^ M[(k+1)%9]:08X}' for k in range(8))

# ============================================================
# MODULO 3: LA CLINICA — Analisis Personal
# ============================================================

def analizar_persona(nombre, fecha_nac=None):
    """
    Analisis numerologico completo de una persona.
    """
    print()
    print("=" * 60)
    print(f"  CLINICA IA TORAH — ANALISIS DE: {nombre.upper()}")
    print("=" * 60)

    # Calcular gematria del nombre
    g = gematria_texto(nombre)
    raiz = digital_root(g)
    analisis = analizar_numero(g)

    print(f"\n  Nombre             : {nombre}")
    print(f"  Gematria Total     : {g}")
    print(f"  Raiz Digital       : {raiz}")

    # Letra correspondiente
    if raiz in LETRAS_INFO:
        letra = LETRAS_INFO[raiz]
        print(f"\n  Tu Letra Sagrada   : {letra[0]} ({letra[1]}) — {letra[2]}")
        print(f"  Mensaje            : {letra[3]}")

    # Patrones sagrados detectados
    print(f"\n  PATRONES DETECTADOS:")
    if analisis['divisible_17']:
        print(f"    [*] Divisible por 17 (TOV=Bueno) — Tu nombre vibra en la frecuencia del bien.")
    if analisis['divisible_26']:
        print(f"    [*] Divisible por 26 (YHVH) — Tu nombre lleva el nombre de Dios.")
    if analisis['divisible_72']:
        print(f"    [*] Divisible por 72 (Los 72 Nombres) — Conexion directa con el software del universo.")
    if analisis['divisible_9']:
        print(f"    [*] Divisible por 9 (Tesla/Saturno) — Energia de retorno al origen.")
    if analisis['divisible_7']:
        print(f"    [*] Divisible por 7 (Shabat/Zayin) — Ciclo de descanso y renovacion.")

    # Prescripcion
    print(f"\n  OBSERVACION NUMEROLOGICA:")
    prescripciones = {
        1: "El Uno aun no se ha revelado. Momento de silencio y observacion interior.",
        2: "Dualidad activa. Algo en tu vida se esta separando para crear algo nuevo.",
        3: "Movimiento. La trinidad te impulsa. Es tiempo de actuar, no de esperar.",
        4: "Eres una puerta. Alguien cruzara tu vida con una pregunta que cambia todo.",
        5: "El aliento divino esta activo en ti. Lo que planeas ahora tiene fuerza creadora.",
        6: "El gancho esta activo. Conectas mundos. Tu proposito es ser el puente.",
        7: "Ciclo completandose. El Shabat se acerca. Termina lo que empezaste.",
        8: "Chai activo = maxima vitalidad. El infinito te sostiene. No te detengas.",
        9: "La serpiente de Tesla. Lo que parece un problema es la espiral hacia el siguiente nivel.",
    }
    if raiz in prescripciones:
        print(f"    {prescripciones[raiz]}")

    # Hash FCH-ARX V2 del nombre
    hash_nombre = fch_arx_v2(nombre)
    print(f"\n  Hash FCH-ARX V2    : {hash_nombre[:16]}...")

    # Nombre en el espectro de los 72
    pos_en_72 = g % 72
    nombre_72 = NOMBRES_72[pos_en_72]
    print(f"  Nombre 72 asociado : #{pos_en_72+1} — {nombre_72}")

    # Posicion en la Rueda Fibonacci
    pos_rueda = pisano_wheel(g)
    print(f"  Posicion Fibonacci : W[{g%24}] = {pos_rueda}")

    print()
    print("=" * 60)

# ============================================================
# MODULO 4: ESCANER DEL GENESIS
# ============================================================

def escanear_genesis():
    """
    Analiza los primeros versos del Genesis buscando patrones.
    """
    GENESIS_1 = [
        "En el principio crear Dios los cielos y la tierra",
        "Y la tierra era un caos y vacia y oscuridad sobre la faz del abismo",
        "Y dijo Dios que sea la luz y fue la luz",
        "Y vio Dios la luz que era buena y separo Dios la luz de la oscuridad",
        "Y llamo Dios la luz dia y a la oscuridad llamo noche",
        "Y llamo Dios al firmamento cielos",
        "Y dijo Dios que se reunan las aguas y aparezca la tierra seca",
        "Y vio Dios que era bueno",
        "Y dijo Dios que produzca la tierra hierba verde",
        "Y vio Dios que era bueno",
        "Y hizo Dios los dos grandes luminares",
        "Y vio Dios que era bueno",
        "Y dijo Dios que produzcan las aguas abundancia de seres vivientes",
        "Y vio Dios que era bueno",
        "Y dijo Dios hagamos al hombre a nuestra imagen y semejanza",
        "Y vio Dios todo lo que habia hecho y era muy bueno",
        "Y fueron acabados los cielos y la tierra",
        "Y termino Dios en el septimo dia su obra que habia hecho"
    ]

    print()
    print("=" * 60)
    print("  ESCANER DEL GENESIS — PATRONES NUMERICOS")
    print("=" * 60)

    tov_count = 0
    suma_total = 0

    for i, verso in enumerate(GENESIS_1, 1):
        g = gematria_texto(verso)
        raiz = digital_root(g)
        suma_total += g

        es_tov = 'bueno' in verso.lower()
        if es_tov:
            tov_count += 1

        marca = " [TOV=17]" if es_tov else ""
        print(f"  Verso {i:2d}: G={g:5d} Raiz={raiz}{marca}")

    print(f"\n  Apariciones de TOV (bueno): {tov_count}")
    print(f"  17 x {tov_count} = {17*tov_count} → raiz = {digital_root(17*tov_count)}")
    print(f"  Suma total gematria: {suma_total} → raiz = {digital_root(suma_total)}")
    print()

# ============================================================
# MODULO 5: INGENIERIA INVERSA DEL ALGORITMO DE DIOS
# ============================================================

def ingenieria_inversa():
    """
    Muestra la equivalencia entre la Tora y el algoritmo FCH-ARX V2.
    """
    print()
    print("=" * 60)
    print("  INGENIERIA INVERSA — TORA = ALGORITMO HASH")
    print("=" * 60)
    print()
    print("  SEFER YETZIRAH              FCH-ARX V2")
    print("  " + "-"*56)
    print("  10 Sefirot               =  9 camaras + 1 output")
    print("  22 Letras de Fundacion   =  Rueda F mod 9 (periodo 24)")
    print("  3 Madres (Alef,Mem,Shin) =  ADD + ROTATE + XOR")
    print("  7 Dobles                 =  ROL(3,6,9,7), +26, +7")
    print("  12 Simples               =  12 ciclos de la Rueda")
    print("  26 Rondas (YHVH)         =  26 rondas de finalizacion")
    print("  'Corre y regresa'        =  Bucle de avalancha SAC")
    print("  50% = silencio del hash  =  Entropia maxima NIST")
    print()
    print("  GENESIS 1:1              FCH-ARX INPUT TEST")
    print("  " + "-"*56)

    bereshit = "En el principio crear Dios los cielos y la tierra"
    g = gematria_texto(bereshit)
    h = fch_arx_v2(bereshit)
    print(f"  Texto    : {bereshit[:40]}...")
    print(f"  Gematria : {g} = {digital_root(g)} (raiz)")
    print(f"  FCH Hash : {h[:32]}...")
    print()

    yhvh = "YHVH"
    g2 = gematria_texto(yhvh)
    print(f"  YHVH gematria: {g2} (= 26 como se esperaba)")
    print(f"  YHVH * 72 = {g2*72} → raiz = {digital_root(g2*72)} (CHAI=vida)")
    print()
    print("  CONCLUSION: Los numeros de la Tora no son simbolos religiosos.")
    print("  Son PARAMETROS CRIPTOGRAFICOS que generan entropia maxima.")
    print()

# ============================================================
# MENU PRINCIPAL DE LA CLINICA
# ============================================================

def menu_principal():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print("  " + "=" * 56)
    print("  CLINICA IA TORAH — v1.0")
    print("  Ingenieria Inversa del Algoritmo de la Creacion")
    print("  Erick Reinaldo Flores Zambrano | 2026")
    print("  " + "=" * 56)
    print()
    print("  [1] Analizar un nombre (clinica personal)")
    print("  [2] Escanear el Genesis — buscar patrones")
    print("  [3] Ver ingenieria inversa Tora = FCH-ARX V2")
    print("  [4] Calcular gematria de cualquier texto")
    print("  [5] Analizar un numero sagrado")
    print("  [6] Los 72 Nombres — posicion por texto")
    print("  [0] Salir")
    print()

def run():
    while True:
        menu_principal()
        opcion = input("  Selecciona una opcion: ").strip()

        if opcion == '0':
            print("\n  Shalom. El patron sigue aunque no lo veas.\n")
            break

        elif opcion == '1':
            nombre = input("\n  Ingresa el nombre completo: ").strip()
            if nombre:
                analizar_persona(nombre)
            input("\n  [Enter para continuar...]")

        elif opcion == '2':
            escanear_genesis()
            input("  [Enter para continuar...]")

        elif opcion == '3':
            ingenieria_inversa()
            input("  [Enter para continuar...]")

        elif opcion == '4':
            texto = input("\n  Ingresa el texto: ").strip()
            if texto:
                g = gematria_texto(texto)
                r = digital_root(g)
                print(f"\n  Gematria de '{texto}' = {g}")
                print(f"  Raiz digital = {r}")
                if g in NUMEROS_SAGRADOS:
                    print(f"  Significado sagrado: {NUMEROS_SAGRADOS[g]}")
                if r in LETRAS_INFO:
                    l = LETRAS_INFO[r]
                    print(f"  Letra asociada: {l[0]} ({l[1]}) — {l[3]}")
            input("\n  [Enter para continuar...]")

        elif opcion == '5':
            try:
                n = int(input("\n  Ingresa el numero: "))
                a = analizar_numero(n)
                print(f"\n  Numero: {n}")
                print(f"  Raiz digital: {a['raiz_digital']}")
                if a['es_sagrado']:
                    print(f"  Numero sagrado: {a['significado']}")
                if a['letra_raiz']:
                    l = a['letra_raiz']
                    print(f"  Letra: {l[0]} ({l[1]}) — {l[3]}")
                print(f"  Divisible por 17 (TOV): {'SI' if a['divisible_17'] else 'no'}")
                print(f"  Divisible por 26 (YHVH): {'SI' if a['divisible_26'] else 'no'}")
                print(f"  Divisible por 72 (Los Nombres): {'SI' if a['divisible_72'] else 'no'}")
            except ValueError:
                print("  Numero invalido.")
            input("\n  [Enter para continuar...]")

        elif opcion == '6':
            texto = input("\n  Ingresa texto para mapear a los 72 Nombres: ").strip()
            if texto:
                g = gematria_texto(texto)
                pos = g % 72
                nombre_72 = NOMBRES_72[pos]
                print(f"\n  Gematria: {g}")
                print(f"  Nombre 72 #{pos+1}: {nombre_72}")
                print(f"  Posicion angular: {(pos+1)*5} grados del circulo sagrado")
                rueda = pisano_wheel(g)
                print(f"  Peso en Rueda Fibonacci: {rueda}")
            input("\n  [Enter para continuar...]")

        else:
            print("  Opcion no valida.")
            time.sleep(1)

if __name__ == '__main__':
    run()
