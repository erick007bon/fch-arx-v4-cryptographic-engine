# -*- coding: utf-8 -*-
import sys, math
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

n = 71475

def factorizar(n):
    orig = n
    factores = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factores.append(d)
            n //= d
        d += 1
    if n > 1:
        factores.append(n)
    return factores

def es_primo(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def raiz_digital(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

factores = factorizar(n)
print("=" * 55)
print(f"  ANALISIS NUMERICO COMPLETO: {n}")
print("=" * 55)
print(f"  Factores primos : {factores}")
canon = " x ".join(str(f) for f in factores)
print(f"  Forma canonica  : {canon}")

divisores = [i for i in range(1, n+1) if n % i == 0]
print(f"  Num. divisores  : {len(divisores)}")
print(f"  Divisores       : {divisores}")

rd = raiz_digital(n)
sd = sum(int(d) for d in str(n))
print(f"  Suma de digitos : {sd} -> raiz digital : {rd}")
print(f"  Es primo        : {es_primo(n)}")
print(f"  Raiz cuadrada   : {math.sqrt(n):.6f}")
print(f"  Hex             : {hex(n).upper()}")
print(f"  Binario         : {bin(n)}")

print()
print("  === RELACIONES CON NUMEROS SAGRADOS ===")
sagrados = [
    (7,'Shabat'), (9,'Tesla'), (17,'TOV'), (18,'CHAI'),
    (22,'Letras'), (24,'Rueda'), (26,'YHVH'), (32,'Senderos'),
    (36,'LamVav'), (40,'Mem'), (49,'Omer'), (50,'Nun'),
    (72,'Nombres'), (216,'Letras72')
]
for k, nombre in sagrados:
    r = n % k
    exact = "EXACTO!" if r == 0 else ""
    print(f"  {n} mod {k:3d} ({nombre:10s}) = {r:5d}  {exact}")

print()
print("  === OPERACIONES ESPECIALES ===")
print(f"  71475 = 3 x 25 x 953")
print(f"  953 es primo     : {es_primo(953)}")
print(f"  Suma de factores : {sum(factores)}")
print(f"  3 + 5 + 5 + 953  = {3+5+5+953}")

# Triangular
k_tri = (-1 + math.sqrt(1 + 8*n)) / 2
print(f"  Si triangular: k = {k_tri:.6f}")
print(f"    -> NO es numero triangular (k no es entero)")

# Fibonacci
fibs = [1, 1]
while fibs[-1] < n:
    fibs.append(fibs[-1] + fibs[-2])
print(f"  Fibonacci menor  : {fibs[-2]}")
print(f"  Fibonacci mayor  : {fibs[-1]}")
print(f"  Diferencia menor : {n - fibs[-2]}")

print()
print("  === RELACION CON LA TORA ===")
genesis = 78064
print(f"  Genesis letras   : {genesis}")
print(f"  71475 / 78064    : {71475/78064*100:.4f}%")
print(f"  78064 - 71475    : {78064 - 71475}")
print(f"  71475 * 26 (YHVH): {71475*26}")
print(f"  71475 * 72 (Nomb): {71475*72}")
print(f"  71475 / 26       : {71475/26:.4f}")
print(f"  71475 / 72       : {71475/72:.4f}")
print(f"  71475 / 17 (TOV) : {71475/17:.4f}")
print(f"  71475 / 953      : {71475/953:.4f}")

# En base 9 (Tesla/Saturno)
def a_base(n, base):
    if n == 0: return '0'
    digits = []
    while n:
        digits.append(str(n % base))
        n //= base
    return ''.join(reversed(digits))

print()
print("  === REPRESENTACION EN OTRAS BASES ===")
print(f"  Base 7  (Shabat) : {a_base(71475, 7)}")
print(f"  Base 9  (Saturn) : {a_base(71475, 9)}")
print(f"  Base 10 (decimal): 71475")
print(f"  Base 22 (letras) : {a_base(71475, 22)}")
print(f"  Base 26 (YHVH)   : {a_base(71475, 26)}")

# Suma de cuadrados
print()
print("  === CURIOSIDADES ALGEBRAICAS ===")
print(f"  7^2 + 1^2 + 4^2 + 7^2 + 5^2 = {7**2 + 1**2 + 4**2 + 7**2 + 5**2}")
print(f"  (7+1+4+7+5) = {7+1+4+7+5} -> {raiz_digital(7+1+4+7+5)}")
print(f"  (7*1*4*7*5) = {7*1*4*7*5}")
print(f"  71 + 475    = {71+475} -> raiz = {raiz_digital(71+475)}")
print(f"  714 + 75    = {714+75} -> raiz = {raiz_digital(714+75)}")
print(f"  7147 + 5    = {7147+5} -> raiz = {raiz_digital(7147+5)}")
print()
print("=" * 55)
