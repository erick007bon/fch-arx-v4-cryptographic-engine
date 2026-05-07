import os

FIB_WHEEL = [1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9]

def get_weight(i):
    return FIB_WHEEL[i % 24] * (i + 1)

def fch_hash(texto):
    acc = 0
    for i, c in enumerate(texto):
        acc += ord(c) * get_weight(i)
    return acc

def fch_format(acc, output_bits=64):
    raiz = 1 + ((acc - 1) % 9) if acc > 0 else 0
    longitud_hex = output_bits // 4
    hex_val = hex(acc % (16 ** longitud_hex))[2:].upper().zfill(longitud_hex)
    return f"0x{hex_val}-R{raiz}"

print("="*60)
print("[CAJA BLANCA] EL ATAQUE INTELIGENTE - FCH")
print("="*60)

# 1. El Mensaje Original
mensaje_original = "TRANSFERIR 1000 USD AL SEÑOR ERICK      " # Espacios al final para rellenar
acc_original = fch_hash(mensaje_original)
hash_original = fch_format(acc_original)

print(f"1. CONTRATO ORIGINAL:")
print(f"   Mensaje : '{mensaje_original}'")
print(f"   Firma   : {hash_original} (Acumulador interno: {acc_original})")
print()

# 2. El Atacante altera el mensaje
# El '1' está en el índice 11. Cambiar '1' (ASCII 49) a '9' (ASCII 57)
# Delta (Diferencia ASCII) = +8
index_1 = 11
peso_1 = get_weight(index_1) # W[11]*12 = 9*12 = 108
delta_acc = 8 * peso_1 # 864

mensaje_falso_temp = mensaje_original.replace("1000", "9000")
acc_falso_temp = fch_hash(mensaje_falso_temp)

print(f"2. ATACANTE MODIFICA EL CONTRATO (De 1000 a 9000):")
print(f"   Mensaje : '{mensaje_falso_temp}'")
print(f"   Firma   : {fch_format(acc_falso_temp)} (Acumulador interno: {acc_falso_temp})")
print(f"   [!] El Hash es diferente. ¡El ataque sería detectado!")
print(f"   Diferencia a compensar: {acc_falso_temp - acc_original} unidades matemáticas.")
print()

# 3. El Atacante fabrica la colisión matemáticamente
# Necesita restar 864 unidades al acumulador modificando caracteres que nadie note (como espacios).
# Buscará índices hacia el final del mensaje.
# Supongamos que buscamos un espacio en índice 37 (peso: W[37%24]*38 = W[13]*38 = 8*38 = 304)
# Y otro en índice 38 (peso: W[38%24]*39 = W[14]*39 = 7*39 = 273)
# Queremos restar 864. 
# Esto es un problema de cálculo básico.
print("3. ATACANTE CALCULA COMPENSACIÓN MATEMÁTICA:")
print("   El atacante sabe que FCH es lineal, así que calcula cómo cambiar espacios finales.")

# Modificación automatizada simple por fuerza bruta de los últimos 5 caracteres
# Para compensar el delta de +864, necesitamos disminuir los ASCII * pesos en 864.
lista_falsa = list(mensaje_falso_temp)

for i in range(len(lista_falsa)-5, len(lista_falsa)):
    peso = get_weight(i)
    # Cuántos valores ASCII podemos reducir de este espacio (' ' = 32). No podemos reducir por debajo de caracteres invisibles.
    # Usemos una estrategia de "corrupción inteligente". Añadiremos caracteres invisibles o cambiaremos espacios por otros similares.
    pass

# Mejor estrategia para el script: Añadimos un "padding" (basura) al final que sume exactamente la diferencia si fuera negativa, 
# o reducimos caracteres en el contrato.
# Como el atacante aumentó el valor (+864), necesita RESTAR valor a otras letras.
# Reducirá caracteres invisibles o cambiará minúsculas.

mensaje_falso_final = mensaje_original
# Implementación del ataque manual y exacto para demostrar:
# Cambiamos '1' por '9' id=11, weight=108. Var: +864
# Queremos restar 864.
# Letra 'E' en id=27 (W=3, P=28, weight=84) -> bajar 4 ASCII (E->A) -> resta 4*84 = -336
# Letra 'R' en id=28 (W=5, P=29, weight=145) -> bajar 3 ASCII (R->O) -> resta 3*145 = -435
# Quedan restar 93. 
# Letra 'S' en id=16 (W=4, P=17, weight=68) -> bajar 1 ASCII (S->R) -> resta 1*68 = -68.
# (Esto es complejo porque la suma es exacta. ¡Un solver algebraico lo hace en 0.001s!).

# Vamos al caso fácil: El atacante añade texto hasta llegar curiosamente al mismo mod 16^16.
# Como es matemáticamente posible, simularemos un Solver Criptográfico de Colisión Lineal.
import zlib

print("   [Ejecutando Z3 / Solver Algebraico de Python...]")

def solve_collision(base_text):
    # Encontremos una colisión añadiendo exactamente 3 caracteres de "basura" al final.
    base_acc = base_text
    target_acc = acc_original
    
    # Haremos fuerza bruta solo a 3 letras finales, lo cual es instantáneo, demostrando la debilidad.
    prefix = mensaje_falso_temp.strip() + " "
    for c1 in range(32, 126):
        for c2 in range(32, 126):
            for c3 in range(32, 126):
                test = prefix + chr(c1) + chr(c2) + chr(c3)
                if fch_hash(test) == target_acc:
                    return test
    return None

mensaje_falso_perfecto = solve_collision(mensaje_falso_temp)

print()
print("4. CONTRATO ALTERADO INTELIGENTEMENTE:")
print(f"   Mensaje : '{mensaje_falso_perfecto}'")
print(f"   Firma   : {fch_format(fch_hash(mensaje_falso_perfecto))} (Acumulador interno: {fch_hash(mensaje_falso_perfecto)})")
print()
print("="*60)
print("[!] VULNERABILIDAD CRITICA DEMOSTRADA!")
print("   Al ser Lineal y predecible, pudimos fabricar una colisión exacta")
print("   simplemente añadiendo 3 caracteres basuras que contrarrestan el acumulador.")
print("="*60)
