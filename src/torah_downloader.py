"""
🔯 Torah Downloader — Descarga los 5 Libros de Moisés desde Sefaria API
═══════════════════════════════════════════════════════════════════════
Fuente: https://www.sefaria.org/api
Texto: Torah completa en hebreo con nikkud (vocales)
Autor: Erick Reinaldo Flores Zambrano
Proyecto: 08_gematria_torah
═══════════════════════════════════════════════════════════════════════
"""

import json
import os
import time
import urllib.request
import re
import sys

# Forzar UTF-8 en Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN - Los 5 Libros de Moisés (Torah/Pentateuco)
# ═══════════════════════════════════════════════════════════════

TORAH_BOOKS = {
    "bereshit": {
        "name_hebrew": "בראשית",
        "name_english": "Genesis",
        "name_spanish": "Génesis",
        "sefaria_ref": "Genesis",
        "chapters": 50
    },
    "shemot": {
        "name_hebrew": "שמות",
        "name_english": "Exodus",
        "name_spanish": "Éxodo",
        "sefaria_ref": "Exodus",
        "chapters": 40
    },
    "vayikra": {
        "name_hebrew": "ויקרא",
        "name_english": "Leviticus",
        "name_spanish": "Levítico",
        "sefaria_ref": "Leviticus",
        "chapters": 27
    },
    "bamidbar": {
        "name_hebrew": "במדבר",
        "name_english": "Numbers",
        "name_spanish": "Números",
        "sefaria_ref": "Numbers",
        "chapters": 36
    },
    "devarim": {
        "name_hebrew": "דברים",
        "name_english": "Deuteronomy",
        "name_spanish": "Deuteronomio",
        "sefaria_ref": "Deuteronomy",
        "chapters": 34
    }
}

# Directorio de datos
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
RAW_DATA_DIR = os.path.join(PROJECT_DIR, "data", "raw")

# ═══════════════════════════════════════════════════════════════
# FUNCIONES
# ═══════════════════════════════════════════════════════════════

def clean_hebrew_text(text):
    """
    Limpia el texto hebreo removiendo tags HTML y caracteres no deseados.
    Mantiene: letras hebreas, nikkud (vocales), espacios.
    """
    if not text:
        return ""
    # Remover tags HTML (<big>, </big>, etc.)
    text = re.sub(r'<[^>]+>', '', text)
    # Limpiar espacios múltiples
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def strip_nikkud(text):
    """
    Remueve nikkud (vocales) y trope (cantilación) del texto hebreo.
    Deja solo las letras consonánticas puras para cálculo de gematría.
    
    Rangos Unicode:
    - 0x0591-0x05BD: Cantilación y marcas
    - 0x05BF: Rafe
    - 0x05C1-0x05C2: Shin/Sin dots
    - 0x05C4-0x05C5: Upper/Lower dots
    - 0x05C7: Qamats qatan
    """
    if not text:
        return ""
    # Remover todas las marcas de cantilación y vocales (Unicode block)
    result = re.sub(r'[\u0591-\u05C7]', '', text)
    # Remover maqaf (guión hebreo) y otros signos de puntuación hebreos
    result = re.sub(r'[\u05BE\u05C0\u05C3\u05C6\u05F3\u05F4]', '', result)
    # Remover sof pasuq (fin de versículo ׃)
    result = result.replace('׃', '')
    return result.strip()


def fetch_chapter(book_ref, chapter_num, max_retries=3):
    """
    Descarga un capítulo completo desde la API de Sefaria.
    
    Args:
        book_ref: Nombre del libro en inglés (ej: "Genesis")
        chapter_num: Número del capítulo
        max_retries: Intentos máximos ante fallo
    
    Returns:
        Lista de versículos en hebreo
    """
    url = f"https://www.sefaria.org/api/texts/{book_ref}.{chapter_num}?context=0"
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'GematriaTorahProject/1.0 (Academic Research)'
            })
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                he_text = data.get('he', [])
                
                # Si es un string (un solo versículo), convertir a lista
                if isinstance(he_text, str):
                    he_text = [he_text]
                
                # Limpiar cada versículo
                cleaned = [clean_hebrew_text(v) for v in he_text if v]
                return cleaned
                
        except Exception as e:
            print(f"    ⚠️  Error en {book_ref} cap {chapter_num} (intento {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))  # Backoff exponencial
            else:
                print(f"    ❌  FALLO PERMANENTE: {book_ref} cap {chapter_num}")
                return []


def download_book(book_key, book_info):
    """
    Descarga un libro completo de la Torah.
    
    Returns:
        dict con toda la información del libro
    """
    print(f"\n📖 Descargando: {book_info['name_hebrew']} ({book_info['name_spanish']})")
    print(f"   Capítulos: {book_info['chapters']}")
    print(f"   Fuente: Sefaria API ({book_info['sefaria_ref']})")
    print(f"   {'─' * 50}")
    
    book_data = {
        "metadata": {
            "key": book_key,
            "name_hebrew": book_info["name_hebrew"],
            "name_english": book_info["name_english"],
            "name_spanish": book_info["name_spanish"],
            "total_chapters": book_info["chapters"],
            "source": "Sefaria API",
            "downloaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "encoding": "UTF-8"
        },
        "chapters": {},
        "stats": {
            "total_verses": 0,
            "total_words_with_nikkud": 0,
            "total_words_consonantal": 0
        }
    }
    
    total_verses = 0
    total_words = 0
    
    for ch in range(1, book_info["chapters"] + 1):
        # Rate limiting: respetar la API de Sefaria
        if ch > 1:
            time.sleep(0.5)  # 500ms entre requests
        
        verses = fetch_chapter(book_info["sefaria_ref"], ch)
        
        if verses:
            # Crear versión sin nikkud para gematría
            verses_consonantal = [strip_nikkud(v) for v in verses]
            
            book_data["chapters"][str(ch)] = {
                "verses_with_nikkud": verses,
                "verses_consonantal": verses_consonantal,
                "num_verses": len(verses)
            }
            
            total_verses += len(verses)
            for v in verses_consonantal:
                total_words += len(v.split())
            
            # Progreso visual
            progress = ch / book_info["chapters"] * 100
            bar = '█' * int(progress / 5) + '░' * (20 - int(progress / 5))
            print(f"   [{bar}] {progress:5.1f}% | Cap {ch:2d}/{book_info['chapters']} | {len(verses)} versículos", end='\r')
    
    book_data["stats"]["total_verses"] = total_verses
    book_data["stats"]["total_words_consonantal"] = total_words
    
    print(f"\n   ✅ {book_info['name_hebrew']}: {total_verses} versículos, ~{total_words} palabras")
    
    return book_data


def save_book(book_key, book_data):
    """Guarda un libro descargado como JSON."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    filepath = os.path.join(RAW_DATA_DIR, f"{book_key}.json")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, ensure_ascii=False, indent=2)
    
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"   💾 Guardado: {filepath} ({size_mb:.2f} MB)")
    return filepath


# ═══════════════════════════════════════════════════════════════
# EJECUCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("🔯 TORAH DOWNLOADER — Descarga de los 5 Libros de Moisés")
    print("   Fuente: Sefaria.org (Texto Autoritativo)")
    print("   Formato: JSON con hebreo original + consonántico")
    print("=" * 60)
    
    all_stats = {}
    grand_total_verses = 0
    grand_total_words = 0
    
    for book_key, book_info in TORAH_BOOKS.items():
        # Verificar si ya existe
        filepath = os.path.join(RAW_DATA_DIR, f"{book_key}.json")
        if os.path.exists(filepath):
            print(f"\n⏭️  {book_info['name_hebrew']} ya descargado. Saltando...")
            # Cargar stats existentes
            with open(filepath, 'r', encoding='utf-8') as f:
                existing = json.load(f)
                v = existing["stats"]["total_verses"]
                w = existing["stats"]["total_words_consonantal"]
                grand_total_verses += v
                grand_total_words += w
                all_stats[book_key] = {"verses": v, "words": w}
            continue
        
        # Descargar
        book_data = download_book(book_key, book_info)
        save_book(book_key, book_data)
        
        v = book_data["stats"]["total_verses"]
        w = book_data["stats"]["total_words_consonantal"]
        grand_total_verses += v
        grand_total_words += w
        all_stats[book_key] = {"verses": v, "words": w}
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE DESCARGA")
    print("=" * 60)
    print(f"{'Libro':<15} {'Hebreo':<10} {'Versículos':>12} {'Palabras':>12}")
    print("-" * 50)
    for book_key, stats in all_stats.items():
        info = TORAH_BOOKS[book_key]
        print(f"{info['name_spanish']:<15} {info['name_hebrew']:<10} {stats['verses']:>12,} {stats['words']:>12,}")
    print("-" * 50)
    print(f"{'TOTAL':<15} {'תורה':<10} {grand_total_verses:>12,} {grand_total_words:>12,}")
    print("=" * 60)
    print("✅ Torah completa descargada. Lista para análisis de gematría.")
    print(f"📂 Datos guardados en: {RAW_DATA_DIR}")


if __name__ == "__main__":
    main()
