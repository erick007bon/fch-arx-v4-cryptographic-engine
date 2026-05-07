"""
🔯 EXTRACCIÓN DE LOS 72 NOMBRES DE DIOS
═══════════════════════════════════════════════════════════════════════
שם המפורש — Shem HaMephorash
"El Nombre Explícito" — Los 72 Nombres de Dios

Fuente: Éxodo (Shemot) 14:19-21
Tradición: Zohar, Parashat Beshalach

3 versículos consecutivos, cada uno con 72 letras.
72 × 3 = 216 letras = el número de letras del Nombre de Dios.

Estos versículos describen el momento de la División del Mar Rojo — 
el momento de máxima revelación divina en la narrativa bíblica.

Autor: Erick Reinaldo Flores Zambrano
═══════════════════════════════════════════════════════════════════════
"""

import json
import os
import sys

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gematria_engine import (
    extract_hebrew_letters, strip_nikkud,
    gematria_standard, gematria_ordinal, gematria_reduced,
    gematria_katan_mispari, gematria_atbash, gematria_all_methods,
    is_prime, display_72_names, display_gematria
)

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
RAW_DATA_DIR = os.path.join(PROJECT_DIR, "data", "raw")
REF_DATA_DIR = os.path.join(PROJECT_DIR, "data", "reference")

# Los 72 Nombres según la tradición (para verificación)
TRADITIONAL_72_NAMES = [
    "והו", "ילי", "סיט", "עלם", "מהש", "ללה", "אכא", "כהת",
    "הזי", "אלד", "לאו", "ההע", "יזל", "מבה", "הרי", "הקם",
    "לאו", "כלי", "לוו", "פהל", "נלך", "ייי", "מלה", "חהו",
    "נתה", "האא", "ירת", "שאה", "ריי", "אום", "לכב", "ושר",
    "יחו", "להח", "כוק", "מנד", "אני", "חעם", "רהע", "ייז",
    "ההה", "מיכ", "וול", "ילה", "סאל", "ערי", "עשל", "מיה",
    "והו", "דני", "החש", "עמם", "ננא", "נית", "מבה", "פוי",
    "נמם", "ייל", "הרח", "מצר", "ומב", "יהה", "ענו", "מחי",
    "דמב", "מנק", "איע", "חבו", "ראה", "יבם", "היי", "מום",
]


# ═══════════════════════════════════════════════════════════════
# EXTRAER LOS 72 NOMBRES
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("🔯 EXTRACCIÓN DE LOS 72 NOMBRES DE DIOS — שם המפורש")
    print("   Shem HaMephorash — El Nombre Explícito")
    print("   Fuente: Éxodo (שמות) 14:19-21")
    print("=" * 70)
    
    # Cargar Éxodo (Shemot)
    shemot_path = os.path.join(RAW_DATA_DIR, "shemot.json")
    
    if not os.path.exists(shemot_path):
        print("❌ Error: No se encontró shemot.json. Ejecuta torah_downloader.py primero.")
        return
    
    with open(shemot_path, 'r', encoding='utf-8') as f:
        shemot_data = json.load(f)
    
    # Obtener capítulo 14
    chapter_14 = shemot_data.get('chapters', {}).get('14', {})
    verses_nikkud = chapter_14.get('verses_with_nikkud', [])
    
    if len(verses_nikkud) < 21:
        print(f"❌ Error: Capítulo 14 tiene solo {len(verses_nikkud)} versículos")
        return
    
    # ─── Los 3 versículos sagrados ────────────────────────────
    print(f"\n{'─' * 70}")
    print("📜 LOS 3 VERSÍCULOS DE LA DIVISIÓN DEL MAR ROJO")
    print(f"{'─' * 70}")
    
    v19_raw = verses_nikkud[18]
    v20_raw = verses_nikkud[19]
    v21_raw = verses_nikkud[20]
    
    v19_clean = strip_nikkud(v19_raw)
    v20_clean = strip_nikkud(v20_raw)
    v21_clean = strip_nikkud(v21_raw)
    
    print(f"\n📖 Éxodo 14:19")
    print(f"   {v19_clean}")
    
    print(f"\n📖 Éxodo 14:20")
    print(f"   {v20_clean}")
    
    print(f"\n📖 Éxodo 14:21")
    print(f"   {v21_clean}")
    
    # ─── Extraer letras puras ────────────────────────────────
    v19_letters = extract_hebrew_letters(v19_raw)
    v20_letters = extract_hebrew_letters(v20_raw)
    v21_letters = extract_hebrew_letters(v21_raw)
    
    print(f"\n{'─' * 70}")
    print("🔢 CONTEO DE LETRAS")
    print(f"{'─' * 70}")
    print(f"   Versículo 19: {len(v19_letters)} letras")
    print(f"   Versículo 20: {len(v20_letters)} letras")
    print(f"   Versículo 21: {len(v21_letters)} letras")
    print(f"   TOTAL: {len(v19_letters) + len(v20_letters) + len(v21_letters)} letras")
    print(f"   (Esperado: 72 + 72 + 72 = 216)")
    
    # ─── Verificar el conteo de 72 ────────────────────────────
    all_72 = (len(v19_letters) == 72 and len(v20_letters) == 72 and len(v21_letters) == 72)
    
    if all_72:
        print(f"\n   ✅ ¡PERFECTO! Cada versículo tiene exactamente 72 letras.")
        print(f"   216 letras = el número de letras del Nombre de Dios.")
    else:
        print(f"\n   ⚠️  Los conteos no son exactamente 72.")
        print(f"   Esto puede ser por variantes textuales o letras especiales.")
        print(f"   Procediendo con los datos disponibles...")
    
    # ─── Construir los 72 Nombres ────────────────────────────
    print(f"\n{'─' * 70}")
    print("🔯 CONSTRUYENDO LOS 72 NOMBRES")
    print(f"{'─' * 70}")
    print(f"   Método: Zohar, Parashat Beshalach")
    print(f"   Versículo 19 → dirección normal (derecha a izquierda)")
    print(f"   Versículo 20 → dirección INVERTIDA (izquierda a derecha)")
    print(f"   Versículo 21 → dirección normal (derecha a izquierda)")
    
    # Invertir versículo 20
    v20_reversed = list(reversed(v20_letters))
    
    # Usar el mínimo para evitar errores
    num_names = min(len(v19_letters), len(v20_letters), len(v21_letters))
    
    names_72 = []
    for i in range(num_names):
        letter_1 = v19_letters[i]
        letter_2 = v20_reversed[i]
        letter_3 = v21_letters[i]
        
        name = letter_1 + letter_2 + letter_3
        std_val = gematria_standard(name)
        
        names_72.append({
            'number': i + 1,
            'name': name,
            'letter_1': letter_1,
            'letter_2': letter_2,
            'letter_3': letter_3,
            'gematria_standard': std_val,
            'gematria_ordinal': gematria_ordinal(name),
            'gematria_reduced': gematria_reduced(name),
            'gematria_atbash': gematria_atbash(name),
            'digital_root': gematria_katan_mispari(name),
            'is_prime': is_prime(std_val),
            'divisible_by_7': std_val % 7 == 0,
            'divisible_by_26': std_val % 26 == 0,  # 26 = YHVH
        })
    
    # ─── MOSTRAR LOS 72 NOMBRES ────────────────────────────
    print(f"\n{'═' * 70}")
    print(f"{'🔯 LOS 72 NOMBRES DE DIOS — שם המפורש':^70}")
    print(f"{'═' * 70}")
    
    print(f"\n{'#':>3}  {'Nombre':>6}  {'Std':>5}  {'Ord':>5}  {'Red':>4}  {'Raíz':>4}  {'Primo':>5}  {'÷7':>3}  {'÷26':>4}")
    print(f"{'─'*3}  {'─'*6}  {'─'*5}  {'─'*5}  {'─'*4}  {'─'*4}  {'─'*5}  {'─'*3}  {'─'*4}")
    
    for n in names_72:
        primo = "✡" if n['is_prime'] else " "
        div7 = "🪐" if n['divisible_by_7'] else "  "
        div26 = "יה" if n['divisible_by_26'] else "  "
        print(f"{n['number']:>3}  {n['name']:>6}  {n['gematria_standard']:>5}  "
              f"{n['gematria_ordinal']:>5}  {n['gematria_reduced']:>4}  "
              f"{n['digital_root']:>4}  {primo:>5}  {div7:>3}  {div26:>4}")
    
    # ─── CUADRADO MÁGICO DE LOS 72 NOMBRES (8×9) ────────────
    print(f"\n{'═' * 70}")
    print(f"{'📐 CUADRADO DE LOS 72 NOMBRES (8 columnas × 9 filas)':^70}")
    print(f"{'═' * 70}")
    print(f"   (Se leen en todas las direcciones — derecha, izquierda, arriba, abajo)")
    print()
    
    # Organizar en cuadrado 8×9 = 72
    cols = 8
    rows = (num_names + cols - 1) // cols
    
    for row in range(rows):
        line = "   "
        for col in range(cols):
            idx = row * cols + col
            if idx < len(names_72):
                line += f"  {names_72[idx]['name']}  "
            else:
                line += "       "
        print(line)
    
    # ─── ESTADÍSTICAS PROFUNDAS ────────────────────────────
    all_std = [n['gematria_standard'] for n in names_72]
    all_roots = [n['digital_root'] for n in names_72]
    
    total = sum(all_std)
    primes_count = sum(1 for n in names_72 if n['is_prime'])
    div7_count = sum(1 for n in names_72 if n['divisible_by_7'])
    div26_count = sum(1 for n in names_72 if n['divisible_by_26'])
    
    # Distribución de raíces digitales
    root_dist = {}
    for r in all_roots:
        root_dist[r] = root_dist.get(r, 0) + 1
    
    print(f"\n{'═' * 70}")
    print(f"{'📊 ANÁLISIS ESTADÍSTICO DE LOS 72 NOMBRES':^70}")
    print(f"{'═' * 70}")
    
    print(f"\n   🔢 Suma total de gematría (estándar): {total:,}")
    print(f"   📊 Promedio: {total / len(names_72):.2f}")
    print(f"   📏 Rango: [{min(all_std)} — {max(all_std)}]")
    
    print(f"\n   ✡️  Nombres con valor primo: {primes_count}/{len(names_72)} ({primes_count/len(names_72)*100:.1f}%)")
    print(f"   🪐 Divisibles por 7 (Saturno): {div7_count}/{len(names_72)} ({div7_count/len(names_72)*100:.1f}%)")
    print(f"   יה Divisibles por 26 (YHVH): {div26_count}/{len(names_72)} ({div26_count/len(names_72)*100:.1f}%)")
    
    print(f"\n   🌀 Distribución de Raíces Digitales (1-9):")
    for root in sorted(root_dist.keys()):
        bar = '█' * root_dist[root]
        print(f"      {root}: {bar} ({root_dist[root]})")
    
    # ─── Conexión con Saturno ────────────────────────────
    print(f"\n{'═' * 70}")
    print(f"{'🪐 CONEXIÓN CON SATURNO (שבתאי)':^70}")
    print(f"{'═' * 70}")
    
    shabbtai_val = 712  # שבתי (sin alef)
    shabbtai_kollel = 713  # con kollel
    
    # ¿Algún nombre suma 7, 70, 700?
    saturno_nums = [7, 14, 21, 28, 35, 42, 49, 70, 77, 700, 712, 713]
    for target in saturno_nums:
        matches = [n for n in names_72 if n['gematria_standard'] == target]
        if matches:
            for m in matches:
                print(f"   🔗 Nombre #{m['number']} ({m['name']}) = {target}")
    
    # Nombres con raíz digital 7 (Saturno)
    root7 = [n for n in names_72 if n['digital_root'] == 7]
    if root7:
        print(f"\n   🪐 Nombres con raíz digital 7 (resonancia de Saturno):")
        for n in root7:
            print(f"      #{n['number']:>2} {n['name']} = {n['gematria_standard']} (raíz: 7)")
    
    # ─── Guardar resultados ────────────────────────────
    output = {
        'metadata': {
            'source': 'Éxodo (Shemot) 14:19-21',
            'tradition': 'Zohar, Parashat Beshalach',
            'total_names': len(names_72),
            'letter_counts': {
                'v19': len(v19_letters),
                'v20': len(v20_letters),
                'v21': len(v21_letters),
                'total': len(v19_letters) + len(v20_letters) + len(v21_letters)
            }
        },
        'verses': {
            'v19_consonantal': ''.join(v19_letters),
            'v20_consonantal': ''.join(v20_letters),
            'v21_consonantal': ''.join(v21_letters),
        },
        'names': names_72,
        'statistics': {
            'total_sum': total,
            'average': round(total / len(names_72), 2),
            'min': min(all_std),
            'max': max(all_std),
            'primes': primes_count,
            'divisible_by_7': div7_count,
            'divisible_by_26': div26_count,
            'digital_root_distribution': root_dist,
        }
    }
    
    output_path = os.path.join(REF_DATA_DIR, "72_names_of_god.json")
    os.makedirs(REF_DATA_DIR, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultados guardados en: {output_path}")
    print(f"\n{'═' * 70}")
    print(f"✅ Extracción de los 72 Nombres completada.")
    print(f"{'═' * 70}")


if __name__ == "__main__":
    main()
