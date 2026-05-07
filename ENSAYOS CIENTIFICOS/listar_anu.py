import urllib.request
import re

url = 'https://users.cecs.anu.edu.au/~bdm/dilugim/torah.html'
print(f"Examinando index en {url} para encontrar la carpeta data exacta...")

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        
        # Buscamos links a txt o zip
        links = re.findall(r'href=[\'"]?([^\'" >]+(?:txt|zip))', html)
        print("Archivos encontrados en la web del Dr. McKay:")
        for link in set(links):
            print(" -", link)
            
except Exception as e:
    print("Error:", e)
