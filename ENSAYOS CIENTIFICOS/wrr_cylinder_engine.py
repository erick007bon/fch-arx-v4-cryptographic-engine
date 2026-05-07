import sys
import copy

sys.stdout.reconfigure(encoding='utf-8')

archivo = r'C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah\ENSAYOS CIENTIFICOS\KOREN_GENESIS_78064_PERFECTO.txt'

try:
    with open(archivo, 'r', encoding='utf-8') as f:
        text = f.read()
except Exception as e:
    print("Error abriendo el archivo Koren:", e)
    sys.exit(1)

def buscar_els(palabra, min_salto=2, max_salto=2000):
    resultados = []
    longitud = len(palabra)
    n_letras = len(text)
    
    for i in range(n_letras):
        if text[i] == palabra[0]:
            # Hacia Adelante
            for salto in range(min_salto, max_salto + 1):
                if i + (longitud - 1) * salto < n_letras:
                    match = True
                    for k in range(1, longitud):
                        if text[i + k * salto] != palabra[k]:
                            match = False
                            break
                    if match:
                        resultados.append((i, salto))
            # Hacia Atras (Salto Negativo)
            for salto in range(min_salto, max_salto + 1):
                if i - (longitud - 1) * salto >= 0:
                    match = True
                    for k in range(1, longitud):
                        if text[i - k * salto] != palabra[k]:
                            match = False
                            break
                    if match:
                        resultados.append((i, -salto))
    
    resultados.sort(key=lambda x: abs(x[1]))
    return resultados

def render_cylinder(central_idx, salto_h, rango_h=15, rango_v=5):
    grid = []
    start_row = -rango_v
    end_row = rango_v
    start_col = -rango_h
    end_col = rango_h
    
    for r in range(start_row, end_row + 1):
        fila = []
        for c in range(start_col, end_col + 1):
            idx_1D = central_idx + (r * salto_h) + c
            if 0 <= idx_1D < len(text):
                fila.append(text[idx_1D])
            else:
                fila.append(' ')
        grid.append(fila)
        
    return grid

def calcular_matriz_ejemplo():
    print("="*60)
    print(" ESCÁNER INTERACTIVO DE CÓDIGOS DE LA TORÁ (ELS)")
    print(" Busca cruces y correlaciones ocultas en el Génesis.")
    print("="*60)
    
    # Inputs interactivos para que el usuario aprenda explorando
    w1 = input("\nIngresa la PRIMERA palabra en Hebreo (ej. ישראל): ").strip()
    w2 = input("Ingresa la SEGUNDA palabra en Hebreo (ej. משה): ").strip()
    
    if not w1 or not w2:
        print("Debes ingresar palabras.")
        return

    print(f"\n[+] Mapeando Word 1: {w1} ...")
    els1_list = buscar_els(w1, 2, 2000)
    if not els1_list:
        print(f"La palabra '{w1}' no existe como código ELS (salto<2000) en Génesis.")
        return
    else:
        print(f" -> Encontrada {len(els1_list)} veces.")
        
    print(f"[+] Mapeando Word 2: {w2} ...")
    els2_list = buscar_els(w2, 2, 2000)
    if not els2_list:
        print(f"La palabra '{w2}' no existe como código ELS (salto<2000) en Génesis.")
        return
    else:
        print(f" -> Encontrada {len(els2_list)} veces.")
        
    # Cruce Euclidiano (Correlacion Topologica)
    mejor_par = None
    min_distancia = 9999999
    
    for e1 in els1_list:
        for e2 in els2_list:
            dist = abs(e1[0] - e2[0])
            if dist < min_distancia and dist > 10: 
                min_distancia = dist
                mejor_par = (e1, e2)
                
    if not mejor_par:
        print("No hay parche topologico cercano. Se rechaza la correlación.")
        return

    e1_pos, e1_salto = mejor_par[0]
    e2_pos, e2_salto = mejor_par[1]
    
    print(f"\n>>> ¡CORRELACIÓN ENCONTRADA! <<<")
    print(f" Ambas palabras se cruzan matemáticamente cerca.")
    print(f" {w1} (Salto: {e1_salto}) | {w2} (Salto: {e2_salto})")
    
    h = abs(e1_salto)
    rango_horizontal = 10
    rango_vertical = max(30, int(min_distancia / h)) + max(len(w1), len(w2))
    
    malla = render_cylinder(e1_pos, h, rango_h=rango_horizontal, rango_v=rango_vertical)
    
    filas = len(malla)
    cols = len(malla[0])
    
    idx_w1 = [e1_pos + i*e1_salto for i in range(len(w1))]
    idx_w2 = [e2_pos + i*e2_salto for i in range(len(w2))]
    
    print(f"\n[ RECONSTRUCCIÓN FORENSE-VISUAL ]")
    print(f" (Ancho del papiro h = {h})\n")
    
    for r in range(filas):
        linea = ""
        tiene_letra_clave = False
        for c in range(cols):
            val_col = c - rango_horizontal
            val_row = r - rango_vertical
            idx_1D = e1_pos + (val_row * h) + val_col
            
            letra_cruda = malla[r][c]
            if idx_1D in idx_w1:
                linea += f"[{letra_cruda}] " 
                tiene_letra_clave = True
            elif idx_1D in idx_w2:
                linea += f"<{letra_cruda}> " 
                tiene_letra_clave = True
            else:
                linea += f" {letra_cruda}  "
                
        if tiene_letra_clave or (r % 3 == 0): 
            linea_inversa = "".join(reversed(linea.split(" ")))
            print(f"{r:>3} | {linea_inversa}")

    print("\n[+] Visualizacion Finalizada.")
    print("="*60)

if __name__ == '__main__':
    while True:
        calcular_matriz_ejemplo()
        resp = input("\n¿Probar otra correlación? (s/n): ")
        if resp.lower() != 's':
            break
