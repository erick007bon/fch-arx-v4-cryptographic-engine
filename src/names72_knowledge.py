"""
🔯 72 NOMBRES DE DIOS — BASE DE CONOCIMIENTO PROFUNDA + MOTOR IA
═══════════════════════════════════════════════════════════════════════
"Los 72 Nombres no son nombres en el sentido humano.
 Son 72 FRECUENCIAS de energía divina que existían ANTES
 de la creación del universo." — Zohar, Parashá Beshalaj

Este script:
1. Construye la base de conocimiento completa de los 72 Nombres
2. Analiza patrones profundos entre los nombres
3. Encuentra las conexiones con las Sefirot y los ángeles
4. Crea un motor de consulta inteligente
5. Genera la base de datos para la webapp IA

Fuentes: Zohar, Pardes Rimonim, Sefer Raziel, Sefer Yetzirah

Autor: Erick Reinaldo Flores Zambrano
═══════════════════════════════════════════════════════════════════════
"""

import json
import os
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from gematria_engine import (
    gematria_standard, gematria_ordinal, gematria_reduced,
    gematria_katan_mispari, gematria_atbash, gematria_gadol,
    extract_hebrew_letters, is_prime
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
REF_DIR = os.path.join(PROJECT_DIR, "data", "reference")
REPORT_DIR = os.path.join(PROJECT_DIR, "reports")


# ═══════════════════════════════════════════════════════════════
# BASE DE CONOCIMIENTO COMPLETA DE LOS 72 NOMBRES
# Fuente: Zohar sobre Éxodo 14:19-21 + tradición rabínica
# ═══════════════════════════════════════════════════════════════

# Los 72 trigramas extraídos de Éxodo 14:19-21
NAMES_72_RAW = [
    "והו", "ילי", "סיט", "עלמ", "מהש", "ללה", "אכא", "כהת",
    "הזי", "אלד", "לאו", "ההע", "יזל", "מבה", "הרי", "הקם",
    "לאו", "כלי", "לוו", "פהל", "נלך", "ייי", "מלה", "חהו",
    "נתה", "האא", "ירת", "שאה", "ריי", "אום", "לכב", "ושר",
    "יחו", "להח", "כוק", "מנד", "אני", "חעם", "רהע", "ייז",
    "ההה", "מיכ", "וול", "ילה", "סאל", "ערי", "עשל", "מיה",
    "והו", "דני", "החש", "עמם", "ננא", "נית", "מבה", "פוי",
    "נמם", "ייל", "הרח", "מצר", "ומב", "יהה", "ענו", "מחי",
    "דמב", "מנק", "איע", "חבו", "ראה", "יבמ", "היי", "מום",
]

# Base de conocimiento: cada nombre con sus atributos kabbalísticos
# Fuentes: Sefer Raziel HaMalakh, tradición rabínica, Zohar
KNOWLEDGE_72 = {
    1: {
        "purpose": "Divinidad, protección espiritual, viaje astral",
        "meditation": "Para conectar con la fuente de toda energía",
        "angel_suffix": "אל",
        "quality": "Voluntad divina",
        "sefirah": "Keter/Jesed",
        "element": "Aire",
        "planet": "Neptuno/Júpiter",
        "psalm": "Salmo 3:3",
        "day_range": "20-24 Marzo",
        "zodiac": "Aries",
    },
    2: {
        "purpose": "Iluminación espiritual, sabiduría mística",
        "meditation": "Para recibir inspiración y visión profética",
        "angel_suffix": "אל",
        "quality": "Iluminación",
        "sefirah": "Keter/Gevurah",
        "element": "Fuego",
        "planet": "Sol",
        "psalm": "Salmo 22:19",
        "day_range": "25-29 Marzo",
        "zodiac": "Aries",
    },
    3: {
        "purpose": "Paciencia, superar los obstáculos",
        "meditation": "Para la transformación del sufrimiento en sabiduría",
        "angel_suffix": "אל",
        "quality": "Paciencia divina",
        "sefirah": "Keter/Tiferet",
        "element": "Agua",
        "planet": "Saturno",
        "psalm": "Salmo 91:2",
        "day_range": "30 Marzo - 3 Abril",
        "zodiac": "Aries",
    },
    4: {
        "purpose": "Neutralizar negatividad, protección",
        "meditation": "Escudo contra energías destructivas",
        "angel_suffix": "יה",
        "quality": "Protección",
        "sefirah": "Keter/Netzaj",
        "element": "Tierra",
        "planet": "Júpiter",
        "psalm": "Salmo 25:6",
        "day_range": "4-8 Abril",
        "zodiac": "Aries",
    },
    5: {
        "purpose": "Curación, restauración de la salud",
        "meditation": "Activar la energía sanadora del universo",
        "angel_suffix": "אל",
        "quality": "Sanación",
        "sefirah": "Keter/Hod",
        "element": "Fuego",
        "planet": "Marte",
        "psalm": "Salmo 33:22",
        "day_range": "9-13 Abril",
        "zodiac": "Aries",
    },
    6: {
        "purpose": "Fertilidad, poder para crear",
        "meditation": "Para manifestar proyectos y sueños",
        "angel_suffix": "אל",
        "quality": "Creación",
        "sefirah": "Keter/Yesod",
        "element": "Agua",
        "planet": "Luna",
        "psalm": "Salmo 9:11",
        "day_range": "14-18 Abril",
        "zodiac": "Aries",
    },
    7: {
        "purpose": "Conciencia cósmica, conexión con lo alto",
        "meditation": "Para expandir la percepción espiritual",
        "angel_suffix": "אל",
        "quality": "Conciencia",
        "sefirah": "Keter/Malkut",
        "element": "Aire",
        "planet": "Mercurio",
        "psalm": "Salmo 103:19",
        "day_range": "19-23 Abril",
        "zodiac": "Tauro",
    },
    8: {
        "purpose": "Orden y estructura, deshacer el caos",
        "meditation": "Para traer orden divino al desorden",
        "angel_suffix": "אל",
        "quality": "Orden",
        "sefirah": "Jokhmah/Jesed",
        "element": "Tierra",
        "planet": "Saturno",
        "psalm": "Salmo 95:6",
        "day_range": "24-28 Abril",
        "zodiac": "Tauro",
    },
    # Nombres clave con conexión a Saturno
    26: {
        "purpose": "Eliminar la negatividad absoluta, purificación total",
        "meditation": "El nombre más puro — valor 7 = Shabbat/Saturno/Completitud",
        "angel_suffix": "אל",
        "quality": "Purificación suprema",
        "sefirah": "Tiferet/Hod",
        "element": "Agua",
        "planet": "SATURNO (valor = 7)",
        "psalm": "Salmo 119:145",
        "day_range": "7-11 Octubre",
        "zodiac": "Libra",
    },
    42: {
        "purpose": "Equilibrio entre dar y recibir",
        "meditation": "Para encontrar el balance en las relaciones",
        "angel_suffix": "אל",
        "quality": "Balance",
        "sefirah": "Hod/Netzaj",
        "element": "Aire",
        "planet": "Mercurio",
        "psalm": "Salmo 113:2",
        "day_range": "18-22 Enero",
        "zodiac": "Acuario",
    },
    72: {
        "purpose": "Las fuerzas espirituales ocultas, finalización de ciclos",
        "meditation": "Para cerrar ciclos y renacer espiritualmente",
        "angel_suffix": "אל",
        "quality": "Renacimiento",
        "sefirah": "Malkut/Malkut",
        "element": "Tierra",
        "planet": "Saturno",
        "psalm": "Salmo 116:7",
        "day_range": "15-20 Marzo",
        "zodiac": "Piscis",
    },
}


def build_complete_database():
    """
    Construye la base de datos completa de los 72 Nombres con
    TODOS los cálculos de gematría y atributos kabbalísticos.
    """
    print(f"\n{'═' * 70}")
    print(f"{'🔯 CONSTRUYENDO BASE DE CONOCIMIENTO — 72 NOMBRES DE DIOS':^70}")
    print(f"{'═' * 70}")
    
    database = []
    
    # Las 9 Sefirot inferiores (sin Keter para distribución de 8)
    sefira_cycle = [
        "Jesed", "Gevurah", "Tiferet", "Netzaj",
        "Hod", "Yesod", "Malkut", "Jesed"
    ]
    
    # Los 12 signos del zodíaco (6 nombres por signo)
    zodiac_cycle = [
        "Aries", "Aries", "Aries", "Aries", "Aries", "Aries",
        "Tauro", "Tauro", "Tauro", "Tauro", "Tauro", "Tauro",
        "Géminis", "Géminis", "Géminis", "Géminis", "Géminis", "Géminis",
        "Cáncer", "Cáncer", "Cáncer", "Cáncer", "Cáncer", "Cáncer",
        "Leo", "Leo", "Leo", "Leo", "Leo", "Leo",
        "Virgo", "Virgo", "Virgo", "Virgo", "Virgo", "Virgo",
        "Libra", "Libra", "Libra", "Libra", "Libra", "Libra",
        "Escorpio", "Escorpio", "Escorpio", "Escorpio", "Escorpio", "Escorpio",
        "Sagitario", "Sagitario", "Sagitario", "Sagitario", "Sagitario", "Sagitario",
        "Capricornio", "Capricornio", "Capricornio", "Capricornio", "Capricornio", "Capricornio",
        "Acuario", "Acuario", "Acuario", "Acuario", "Acuario", "Acuario",
        "Piscis", "Piscis", "Piscis", "Piscis", "Piscis", "Piscis",
    ]
    
    for idx, trigram in enumerate(NAMES_72_RAW):
        num = idx + 1
        
        # Gematría en múltiples sistemas
        std = gematria_standard(trigram)
        ordi = gematria_ordinal(trigram)
        red = gematria_reduced(trigram)
        dr = gematria_katan_mispari(trigram)
        atb = gematria_atbash(trigram)
        
        # Nombre del ángel (trigramo + sufijo)
        known = KNOWLEDGE_72.get(num, {})
        suffix = known.get("angel_suffix", "אל" if num % 2 == 1 else "יה")
        angel_name = trigram + suffix
        angel_val = gematria_standard(angel_name)
        
        # Letras individuales
        letters = extract_hebrew_letters(trigram)
        letter_vals = [gematria_standard(l) for l in letters]
        
        # Propiedades numéricas
        entry = {
            "number": num,
            "trigram": trigram,
            "letters": letters,
            "letter_values": letter_vals,
            
            # Gematría
            "gematria": {
                "standard": std,
                "ordinal": ordi,
                "reduced": red,
                "digital_root": dr,
                "atbash": atb,
            },
            
            # Propiedades numéricas
            "properties": {
                "is_prime": is_prime(std),
                "divisible_by_7": std % 7 == 0,
                "divisible_by_26": std % 26 == 0,
                "mod_7": std % 7,
                "mod_9": std % 9,
            },
            
            # Ángel asociado
            "angel": {
                "name": angel_name,
                "suffix": suffix,
                "suffix_meaning": "Dios (אל)" if suffix == "אל" else "Yah (יה)",
                "gematria": angel_val,
            },
            
            # Atributos kabbalísticos
            "kabbalah": {
                "zodiac": zodiac_cycle[idx] if idx < len(zodiac_cycle) else "—",
                "sefirah": known.get("sefirah", sefira_cycle[idx % 8]),
                "purpose": known.get("purpose", "Meditación y conexión espiritual"),
                "meditation": known.get("meditation", "Contemplar las letras para activar su energía"),
                "quality": known.get("quality", "Transformación espiritual"),
                "element": known.get("element", ["Fuego", "Agua", "Aire", "Tierra"][idx % 4]),
                "planet": known.get("planet", "—"),
                "psalm": known.get("psalm", "—"),
            },
            
            # Conexiones
            "connections": {
                "saturn_resonance": std % 7 == 0 or dr == 7,
                "yhvh_resonance": std % 26 == 0,
                "row_in_grid": (idx // 8) + 1,
                "col_in_grid": (idx % 8) + 1,
            },
        }
        
        database.append(entry)
    
    return database


def deep_analysis_72(database):
    """Análisis profundo de patrones en los 72 Nombres."""
    
    print(f"\n{'═' * 70}")
    print(f"{'📊 ANÁLISIS PROFUNDO DE LOS 72 NOMBRES':^70}")
    print(f"{'═' * 70}")
    
    # ═════════════════════════════════════════
    # 1. Estructura del cuadrado 8×9
    # ═════════════════════════════════════════
    
    print(f"""
   📖 LECCIÓN: EL CUADRADO DE LOS 72 NOMBRES
   ─────────────────────────────────────────────────────
   Los 72 Nombres se organizan en un cuadrado de 8×9.
   
   ¿Por qué 8 columnas? 
   • 8 = el número DESPUÉS de 7 (tras la completitud)
   • 8 = Brit Milá (circuncisión) al 8° día
   • 8 = el número de la TRASCENDENCIA
   
   ¿Por qué 9 filas?
   • 9 = las 9 Sefirot inferiores (sin Keter)
   • 9 = el número de la VERDAD (אמת = 441 = 4+4+1 = 9)
   • 9 × 8 = 72 = חסד (Jesed/Bondad = 72!)
   
   💡 72 = JESED (BONDAD). Los 72 Nombres son
   72 expresiones de la Bondad Divina.
   ─────────────────────────────────────────────────────
    """)
    
    # Imprimir cuadrado con valores
    print(f"   📐 EL CUADRADO con valores de gematría:\n")
    print(f"       {'Col1':>8} {'Col2':>8} {'Col3':>8} {'Col4':>8} {'Col5':>8} {'Col6':>8} {'Col7':>8} {'Col8':>8} {'SUMA':>8}")
    print(f"   {'─' * 82}")
    
    row_sums = []
    col_sums = [0] * 8
    
    for row in range(9):
        row_data = database[row*8 : (row+1)*8]
        vals = [d['gematria']['standard'] for d in row_data]
        row_sum = sum(vals)
        row_sums.append(row_sum)
        
        row_str = f"   F{row+1}: "
        for i, d in enumerate(row_data):
            v = d['gematria']['standard']
            col_sums[i] += v
            row_str += f"{d['trigram']}({v:>3}) "
        
        div7 = "🪐" if row_sum % 7 == 0 else "  "
        print(f"{row_str} = {row_sum:>5} {div7}")
    
    print(f"   {'─' * 82}")
    print(f"   Σ:  ", end="")
    for cs in col_sums:
        div7 = "🪐" if cs % 7 == 0 else "  "
        print(f"  {cs:>5}{div7}", end="")
    
    total = sum(col_sums)
    print(f"   {total:>5}")
    
    # ═════════════════════════════════════════
    # 2. Sumas de filas y columnas
    # ═════════════════════════════════════════
    
    print(f"\n   📊 Análisis de sumas:")
    print(f"\n   Filas:")
    for i, rs in enumerate(row_sums):
        dr = rs
        while dr >= 10:
            dr = sum(int(d) for d in str(dr))
        div7 = "🪐" if rs % 7 == 0 else "  "
        prime = "✡" if is_prime(rs) else " "
        print(f"      Fila {i+1}: {rs:>6} (raíz: {dr}) {div7} {prime}")
    
    print(f"\n   Columnas:")
    for i, cs in enumerate(col_sums):
        dr = cs
        while dr >= 10:
            dr = sum(int(d) for d in str(dr))
        div7 = "🪐" if cs % 7 == 0 else "  "
        print(f"      Col {i+1}: {cs:>6} (raíz: {dr}) {div7}")
    
    # ═════════════════════════════════════════
    # 3. Ángeles — los 72 nombres completos
    # ═════════════════════════════════════════
    
    print(f"\n{'─' * 70}")
    print(f"{'👼 LOS 72 ÁNGELES (Nombre + Sufijo Divino)':^70}")
    print(f"{'─' * 70}")
    
    print(f"""
   📖 LECCIÓN: CÓMO SE FORMAN LOS ÁNGELES
   ─────────────────────────────────────────────────────
   Cada uno de los 72 Nombres es la RAÍZ de un ángel.
   
   Para formar el nombre del ángel, se agrega:
   • אל (El = Dios) → Rafael, Gabriel, Miguel
   • יה (Yah = Dios) → Eliyahu (Elías), Zachariah
   
   Ejemplo: והו + אל = והואל (Vehu-El)
   El trigrama ES la frecuencia. El sufijo lo conecta a Dios.
   ─────────────────────────────────────────────────────
    """)
    
    print(f"   {'#':>3} {'Trigrama':>8} {'Ángel':>12} {'Gem.Tri':>8} {'Gem.Áng':>8} {'Zodíaco':>12} {'Sefirah':>12}")
    print(f"   {'─'*3} {'─'*8} {'─'*12} {'─'*8} {'─'*8} {'─'*12} {'─'*12}")
    
    for d in database:
        saturn = "🪐" if d['connections']['saturn_resonance'] else "  "
        print(f"   {d['number']:>3} {d['trigram']:>8} {d['angel']['name']:>12} "
              f"{d['gematria']['standard']:>8} {d['angel']['gematria']:>8} "
              f"{d['kabbalah']['zodiac']:>12} {d['kabbalah']['sefirah']:>12} {saturn}")
    
    # ═════════════════════════════════════════
    # 4. Patrones ocultos
    # ═════════════════════════════════════════
    
    print(f"\n{'─' * 70}")
    print(f"{'🔮 PATRONES OCULTOS EN LOS 72 NOMBRES':^70}")
    print(f"{'─' * 70}")
    
    # Nombres que comparten el mismo valor
    by_value = defaultdict(list)
    for d in database:
        by_value[d['gematria']['standard']].append(d)
    
    twins = {v: names for v, names in by_value.items() if len(names) >= 2}
    
    print(f"\n   👯 Nombres GEMELOS (mismo valor de gematría):")
    for val, names in sorted(twins.items()):
        names_str = ", ".join(f"#{n['number']}-{n['trigram']}" for n in names)
        print(f"      {val:>5} = {names_str}")
    
    # Nombre 26 = האא = 7 (profundización)
    print(f"\n   🪐 PROFUNDIZACIÓN: Nombre #26 (האא = 7)")
    n26 = database[25]
    print(f"""
      Las tres letras: ה(5) + א(1) + א(1) = 7
      
      ה = La ventana — lo que Dios exhala al mundo
      א = Alef — la unidad silenciosa de Dios (×2)
      
      Dos Alefs (unidad × 2) y una He (aliento):
      "El aliento de Dios que unifica dualidades"
      
      Este nombre está en la posición 26 — y 26 = יהוה
      ¡El nombre que vale 7 está en la posición del Nombre de Dios!
      
      7 × 26 = 182 = יעקב (Jacob/Israel)
      
      Esto NO es coincidencia. El Zohar enseña que el 
      nombre 26 es la llave secreta que conecta los 72 
      Nombres con el Tetragramatón.
    """)
    
    # Letras más frecuentes
    all_letters = []
    for d in database:
        all_letters.extend(d['letters'])
    
    letter_freq = Counter(all_letters)
    print(f"   📊 Frecuencia de letras en los 72 Nombres:")
    for letter, count in letter_freq.most_common():
        bar = '█' * count
        print(f"      {letter}: {bar} ({count})")
    
    # ═════════════════════════════════════════
    # 5. Tu conexión personal
    # ═════════════════════════════════════════
    
    print(f"\n{'─' * 70}")
    print(f"{'👤 TU NOMBRE PROTECTOR (72 Nombres + Erick)':^70}")
    print(f"{'─' * 70}")
    
    erick_val = 311
    erick_dr = 5
    
    # Buscar el nombre cuya gematría sea más cercana a la raíz de Erick
    closest = min(database, key=lambda d: abs(d['gematria']['standard'] - erick_val))
    same_root = [d for d in database if d['gematria']['digital_root'] == erick_dr]
    
    print(f"""
   Tu número: אריק = {erick_val} (raíz digital: {erick_dr})
   
   🔗 Nombre más cercano en valor:
      #{closest['number']} {closest['trigram']} = {closest['gematria']['standard']}
      Ángel: {closest['angel']['name']}
      Propósito: {closest['kabbalah']['purpose']}
   
   🌀 Nombres con tu misma raíz digital ({erick_dr}):""")
    
    for d in same_root:
        print(f"      #{d['number']:>2} {d['trigram']} = {d['gematria']['standard']:>4} "
              f"(raíz: {d['gematria']['digital_root']}) — {d['kabbalah']['quality']}")
    
    return database


def save_knowledge_base(database):
    """Guarda la base de conocimiento como JSON."""
    
    os.makedirs(REF_DIR, exist_ok=True)
    path = os.path.join(REF_DIR, "72_names_knowledge_base.json")
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({
            "title": "Los 72 Nombres de Dios — Base de Conocimiento Kabbalística",
            "source": "Zohar, Éxodo 14:19-21",
            "author": "Erick Reinaldo Flores Zambrano",
            "generated": time.strftime("%Y-%m-%d %H:%M"),
            "total_names": 72,
            "total_gematria_sum": sum(d['gematria']['standard'] for d in database),
            "names": database,
            "grid": {
                "rows": 9,
                "cols": 8,
                "explanation": "8 cols = Trascendencia, 9 rows = Sefirot, 72 = Jesed (Bondad)"
            },
            "instructions_for_ai": {
                "role": "Eres un Rabino sabio y un científico de datos. Respondes preguntas sobre los 72 Nombres con rigor kabbalístico y análisis numérico.",
                "context": "Los 72 Nombres se extraen de 3 versículos del Éxodo (14:19, 14:20, 14:21), cada uno con exactamente 72 letras. El versículo 19 se lee normal, el 20 al revés, el 21 normal. Combinando las letras en orden vertical se obtienen 72 trigramas.",
                "response_style": "Combina la tradición del Zohar con análisis estadístico. Siempre muestra los números y sus significados."
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n   💾 Base de conocimiento guardada: {path}")
    print(f"   📊 {len(database)} nombres con atributos completos")
    return path


def generate_72_report(database):
    """Genera un reporte profundo de los 72 Nombres."""
    
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, "72_nombres_profundo.md")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# 🔯 Los 72 Nombres de Dios — Análisis Profundo\n\n")
        f.write(f"**Fecha:** {time.strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Autor:** Erick Reinaldo Flores Zambrano\n")
        f.write(f"**Fuente:** Zohar sobre Éxodo 14:19-21\n\n")
        f.write("---\n\n")
        
        f.write("## 📋 Tabla Completa\n\n")
        f.write("| # | Trigrama | Ángel | Gematría | Raíz | Zodíaco | Sefirah | Saturno |\n")
        f.write("|---|---------|-------|----------|------|---------|---------|--------|\n")
        
        for d in database:
            saturn = "🪐" if d['connections']['saturn_resonance'] else ""
            f.write(f"| {d['number']} | {d['trigram']} | {d['angel']['name']} | "
                    f"{d['gematria']['standard']} | {d['gematria']['digital_root']} | "
                    f"{d['kabbalah']['zodiac']} | {d['kabbalah']['sefirah']} | {saturn} |\n")
        
        # Sección de patrones
        f.write("\n## 🔮 Patrones Descubiertos\n\n")
        
        saturn_names = [d for d in database if d['connections']['saturn_resonance']]
        f.write(f"### Nombres con resonancia de Saturno: {len(saturn_names)}/72\n\n")
        for d in saturn_names:
            f.write(f"- #{d['number']} {d['trigram']} = {d['gematria']['standard']} "
                    f"(raíz: {d['gematria']['digital_root']})\n")
        
        f.write("\n---\n")
        f.write("*Base de conocimiento para IA Kabbalística*\n")
    
    print(f"   📄 Reporte: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("🔯 72 NOMBRES DE DIOS — BASE DE CONOCIMIENTO PARA IA")
    print("   'Los 72 Nombres son 72 ventanas al Infinito.' — Zohar")
    print("=" * 70)
    
    start = time.time()
    
    # 1. Construir base de datos
    database = build_complete_database()
    
    # 2. Análisis profundo
    deep_analysis_72(database)
    
    # 3. Guardar como JSON
    kb_path = save_knowledge_base(database)
    
    # 4. Generar reporte
    generate_72_report(database)
    
    elapsed = time.time() - start
    
    print(f"\n{'═' * 70}")
    print(f"✅ BASE DE CONOCIMIENTO LISTA EN {elapsed:.1f} SEGUNDOS")
    print(f"   📦 KB: data/reference/72_names_knowledge_base.json")
    print(f"   📄 Reporte: reports/72_nombres_profundo.md")
    print(f"   🤖 Lista para la IA → Próximo paso: Webapp")
    print(f"{'═' * 70}")


if __name__ == "__main__":
    main()
