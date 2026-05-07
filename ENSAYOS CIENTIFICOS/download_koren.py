import urllib.request

url = "https://users.cecs.anu.edu.au/~bdm/dilugim/DataFiles/genesis.txt"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    print("Descargando archivo exacto genesis.txt desde ANU...")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        # Los archivos de McKay en ANU estan en texto plano.
        text = resp.read().decode('utf-8').strip()
        
    ALFABETO = set('אבגדהוזחטיכלמנסעפצקרשתךםןףץ')
    puro = "".join(c for c in text if c in ALFABETO)
    
    print(f"Letras encontradas: {len(puro)}")
    if len(puro) == 78064:
        with open('KOREN_GENESIS_78064.txt', 'w', encoding='utf-8') as f:
            f.write(puro)
        print("EXITO. ARCHIVO KOREN 78064 CREADO.")
    else:
        print("Falló el target:", len(puro))
        
except Exception as e:
    print("Error:", e)
