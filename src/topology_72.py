"""
🕸️ TOPOLOGÍA DE LOS 72 NOMBRES — Análisis de Red y Clustering
═══════════════════════════════════════════════════════════════════════
Los 72 Nombres no son entidades aisladas. Forman una RED.

Este script aplica matemática de grafos pura para descubrir:
1. ¿Cuál es el Nombre "central" de toda la red? (Hub)
2. ¿Existen "familias" naturales? (Clustering)
3. ¿La red tiene propiedades de "mundo pequeño"? (Small-World)
4. ¿Los clusters coinciden con la tradición (zodíaco, sefirot)?
5. ¿Qué pares de nombres tienen la conexión más fuerte?

Todo por consola. Matemática pura. Sin webapp.

Autor: Erick Reinaldo Flores Zambrano
═══════════════════════════════════════════════════════════════════════
"""

import json
import os
import sys
import numpy as np
from collections import Counter, defaultdict
from itertools import combinations

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gematria_engine import STANDARD, gematria_standard

# ═══════════════════════════════════════════════════════════════
# DATOS: Los 72 Nombres
# ═══════════════════════════════════════════════════════════════

def load_72_names():
    """Carga los 72 Nombres desde el JSON de referencia."""
    ref_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            'data', 'reference', '72_names_complete.json')
    
    if os.path.exists(ref_path):
        with open(ref_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Fallback: los 72 nombres hardcoded (del Zohar)
    names_raw = [
        "והו", "ילי", "סיט", "עלמ", "מהש", "ללה", "אכא", "כהת",
        "הזי", "אלד", "לאו", "ההע", "יזל", "מבה", "הרי", "הקם",
        "לאו", "כלי", "לוו", "פהל", "נלכ", "יאי", "מלה", "חהו",
        "נתה", "האא", "ירת", "שאה", "ריי", "אום", "לכב", "ושר",
        "יחו", "להח", "כוק", "מנד", "אני", "חעם", "רהע", "ייז",
        "ההה", "מיכ", "וול", "ילה", "סאל", "ערי", "עשל", "מיה",
        "והו", "דני", "החש", "עמם", "ננא", "נית", "מבה", "פוי",
        "נמם", "ייל", "הרח", "מצר", "ומב", "יהה", "ענו", "מחי",
        "דמב", "מנק", "איע", "חבו", "ראה", "יבם", "היי", "מום",
    ]
    
    names = []
    for i, name in enumerate(names_raw):
        letters = list(name)
        val = gematria_standard(name)
        names.append({
            'number': i + 1,
            'name': name,
            'letters': letters,
            'gematria': val,
            'digital_root': 1 + (val - 1) % 9 if val > 0 else 0,
            'mod7': val % 7,
        })
    
    return names


def digital_root(n):
    if n == 0: return 0
    return 1 + (n - 1) % 9

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True


# ═══════════════════════════════════════════════════════════════
# CONSTRUCCIÓN DE LA RED
# ═══════════════════════════════════════════════════════════════

def build_network(names):
    """
    Construye la red de conexiones entre los 72 Nombres.
    Tipos de conexión:
    1. Letras compartidas (2+ letras iguales)
    2. Suma sagrada (A+B = número sagrado)
    3. Gemelos (misma gematría)
    4. Espejo (gematría reversa)
    5. Raíz digital compartida
    6. Complemento a 7 (MOD7 de A + MOD7 de B = 7)
    """
    sacred_numbers = {
        7: 'Shabbat', 26: 'YHVH', 36: 'Chai²', 42: 'Ana Bekoach',
        72: '72 Nombres', 86: 'Elohim', 91: 'YHVH+Adonai',
        112: 'YHVH+Elohim', 137: 'Kabbalah', 216: '6³=72×3',
        358: 'Mashiaj', 376: 'Shalom', 400: 'Tav', 
        611: 'Torah', 613: 'Mitzvot', 666: 'Mishná?',
    }
    
    edges = []
    adj = defaultdict(list)  # Adjacency list
    
    for i, j in combinations(range(len(names)), 2):
        a = names[i]
        b = names[j]
        connections = []
        weight = 0
        
        # 1. Letras compartidas
        shared = set(a['letters']) & set(b['letters'])
        if len(shared) >= 2:
            connections.append(f"letras:{','.join(shared)}")
            weight += len(shared)
        
        # 2. Suma sagrada
        pair_sum = a['gematria'] + b['gematria']
        if pair_sum in sacred_numbers:
            connections.append(f"suma={pair_sum}({sacred_numbers[pair_sum]})")
            weight += 3  # Peso alto
        
        # 3. Gemelos (misma gematría)
        if a['gematria'] == b['gematria'] and i != j:
            connections.append(f"gemelos={a['gematria']}")
            weight += 2
        
        # 4. Misma raíz digital
        if a['digital_root'] == b['digital_root']:
            connections.append(f"raíz={a['digital_root']}")
            weight += 1
        
        # 5. Complemento MOD 7
        if (a['mod7'] + b['mod7']) % 7 == 0 and a['mod7'] != 0:
            connections.append(f"comp7:{a['mod7']}+{b['mod7']}")
            weight += 1
        
        if connections:
            edge = {
                'source': i,
                'target': j,
                'source_name': a['name'],
                'target_name': b['name'],
                'connections': connections,
                'weight': weight,
                'types': len(connections),
            }
            edges.append(edge)
            adj[i].append((j, weight))
            adj[j].append((i, weight))
    
    return edges, adj


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS 1: CENTRALIDAD — ¿Quién es el "Hub"?
# ═══════════════════════════════════════════════════════════════

def centrality_analysis(names, edges, adj):
    """
    Calcula múltiples medidas de centralidad:
    - Degree: número de conexiones
    - Weighted degree: suma de pesos
    - Betweenness: cuántos caminos más cortos pasan por el nodo
    """
    print("\n" + "=" * 70)
    print("🕸️ ANÁLISIS DE CENTRALIDAD — ¿Quién es el Hub de los 72 Nombres?")
    print("=" * 70)
    
    N = len(names)
    
    # Degree centrality
    degree = defaultdict(int)
    weighted_degree = defaultdict(float)
    
    for e in edges:
        degree[e['source']] += 1
        degree[e['target']] += 1
        weighted_degree[e['source']] += e['weight']
        weighted_degree[e['target']] += e['weight']
    
    # Top 10 por grado
    top_degree = sorted(range(N), key=lambda i: degree[i], reverse=True)
    
    print(f"\n  📊 Total nodos: {N}")
    print(f"  📊 Total conexiones: {len(edges)}")
    print(f"  📊 Densidad: {len(edges) / (N*(N-1)/2) * 100:.1f}%")
    print(f"  📊 Grado medio: {sum(degree.values()) / N:.1f}")
    
    print(f"\n  🔝 TOP 15 HUBs (por número de conexiones):")
    print(f"  {'#':>3} {'Nombre':>8} {'Gem':>5} {'Grado':>6} {'W-Grado':>8} {'Raíz':>5} {'MOD7':>5} {'Primo':>6}")
    print(f"  {'─'*3} {'─'*8} {'─'*5} {'─'*6} {'─'*8} {'─'*5} {'─'*5} {'─'*6}")
    
    for rank, i in enumerate(top_degree[:15]):
        n = names[i]
        print(f"  {rank+1:>3} {n['name']:>8} {n['gematria']:>5} {degree[i]:>6} {weighted_degree[i]:>8.0f} "
              f"{n['digital_root']:>5} {n['mod7']:>5} {'✅' if is_prime(n['gematria']) else '─':>6}")
    
    # El hub principal
    hub = top_degree[0]
    hub_name = names[hub]
    print(f"\n  🏆 HUB PRINCIPAL: #{hub_name['number']} {hub_name['name']} (gematría={hub_name['gematria']})")
    print(f"     Conexiones: {degree[hub]}")
    print(f"     Peso total: {weighted_degree[hub]:.0f}")
    print(f"     Raíz digital: {hub_name['digital_root']}")
    
    # ¿Cuáles de los hubs tienen gematría de Saturno (÷7)?
    saturn_hubs = [i for i in top_degree[:15] if names[i]['mod7'] == 0]
    if saturn_hubs:
        print(f"\n  🪐 Hubs divisibles por 7 (Saturno):")
        for i in saturn_hubs:
            n = names[i]
            print(f"     #{n['number']} {n['name']} = {n['gematria']} (grado={degree[i]})")
    
    return degree, weighted_degree, top_degree


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS 2: CLUSTERING — Familias naturales
# ═══════════════════════════════════════════════════════════════

def find_clusters(names, edges, adj):
    """
    K-Means manual sobre la gematría + propiedades de cada nombre.
    También detección de comunidades por propagación de etiquetas.
    """
    print("\n" + "=" * 70)
    print("🔬 CLUSTERING — ¿Existen familias naturales entre los 72 Nombres?")
    print("=" * 70)
    
    N = len(names)
    
    # Método 1: Agrupar por raíz digital (9 grupos naturales)
    print(f"\n  📊 FAMILIAS POR RAÍZ DIGITAL (1-9):")
    dr_groups = defaultdict(list)
    for n in names:
        dr_groups[n['digital_root']].append(n)
    
    for dr in sorted(dr_groups.keys()):
        members = dr_groups[dr]
        vals = [m['gematria'] for m in members]
        print(f"     Raíz {dr}: {len(members)} nombres — {', '.join(m['name'] for m in members)}")
        print(f"            Suma={sum(vals)}, Media={np.mean(vals):.0f}, "
              f"MOD7 de suma={sum(vals)%7}")
    
    # Método 2: Agrupar por MOD 7 (7 grupos = los 7 planetas/días)
    print(f"\n  📊 FAMILIAS POR MOD 7 (Los 7 planetas):")
    planet_names = {0: 'Saturno ♄', 1: 'Sol ☉', 2: 'Luna ☽', 3: 'Marte ♂', 
                    4: 'Mercurio ☿', 5: 'Júpiter ♃', 6: 'Venus ♀'}
    
    mod7_groups = defaultdict(list)
    for n in names:
        mod7_groups[n['mod7']].append(n)
    
    for mod in sorted(mod7_groups.keys()):
        members = mod7_groups[mod]
        print(f"     MOD7={mod} ({planet_names[mod]}): {len(members)} nombres")
        print(f"            {', '.join(f'{m['name']}({m['gematria']})' for m in members)}")
    
    # Método 3: Zodíaco tradicional (cada 6 nombres = 1 signo)
    print(f"\n  📊 FAMILIAS POR ZODÍACO (tradición: cada 6 nombres = 1 signo):")
    zodiac = ['♈ Aries', '♉ Tauro', '♊ Géminis', '♋ Cáncer', '♌ Leo', '♍ Virgo',
              '♎ Libra', '♏ Escorpio', '♐ Sagitario', '♑ Capricornio', '♒ Acuario', '♓ Piscis']
    
    for z_idx, sign in enumerate(zodiac):
        start = z_idx * 6
        end = start + 6
        members = names[start:end]
        vals = [m['gematria'] for m in members]
        total = sum(vals)
        print(f"     {sign}: #{start+1}-{end}")
        print(f"       Nombres: {' '.join(m['name'] for m in members)}")
        print(f"       Valores: {vals}")
        print(f"       Suma={total}, MOD7={total%7}, Raíz={digital_root(total)}, "
              f"{'✅ ÷7' if total%7==0 else ''}")
    
    # ¿Cuántos signos tienen suma divisible por 7?
    zodiac_sums = []
    for z_idx in range(12):
        members = names[z_idx*6:(z_idx+1)*6]
        zodiac_sums.append(sum(m['gematria'] for m in members))
    
    div7_signs = sum(1 for s in zodiac_sums if s % 7 == 0)
    print(f"\n     🪐 Signos con suma ÷7: {div7_signs}/12 ({div7_signs/12*100:.1f}%)")
    print(f"     Esperado por azar: {12/7:.1f} = {1/7*100:.1f}%")
    
    # Método 4: Detección de comunidades por vecindario
    print(f"\n  📊 COMUNIDADES POR CONEXIONES (Propagación de etiquetas):")
    labels = list(range(N))
    
    for iteration in range(20):
        changed = False
        for i in range(N):
            if i not in adj or not adj[i]:
                continue
            # Contar etiquetas de vecinos con peso
            neighbor_labels = Counter()
            for j, w in adj[i]:
                neighbor_labels[labels[j]] += w
            if neighbor_labels:
                best_label = neighbor_labels.most_common(1)[0][0]
                if labels[i] != best_label:
                    labels[i] = best_label
                    changed = True
        if not changed:
            break
    
    # Contar comunidades
    communities = defaultdict(list)
    for i, label in enumerate(labels):
        communities[label].append(i)
    
    # Filtrar comunidades con > 1 miembro
    real_communities = {k: v for k, v in communities.items() if len(v) > 1}
    
    print(f"     Comunidades detectadas: {len(real_communities)}")
    for comm_id, members in sorted(real_communities.items(), key=lambda x: -len(x[1])):
        member_names = [names[m] for m in members]
        vals = [n['gematria'] for n in member_names]
        total = sum(vals)
        print(f"\n     Comunidad (líder #{names[comm_id]['number']} {names[comm_id]['name']}):")
        print(f"       {len(members)} miembros: {', '.join(f'{n['name']}({n['gematria']})' for n in member_names)}")
        print(f"       Suma={total}, MOD7={total%7}, Raíz={digital_root(total)}")
        if len(members) <= 20:
            # ¿Qué tienen en común?
            shared_dr = Counter(n['digital_root'] for n in member_names).most_common(1)[0]
            shared_mod = Counter(n['mod7'] for n in member_names).most_common(1)[0]
            print(f"       Raíz digital dominante: {shared_dr[0]} ({shared_dr[1]}/{len(members)})")
            print(f"       MOD7 dominante: {shared_mod[0]} ({shared_mod[1]}/{len(members)})")
    
    return dr_groups, mod7_groups, real_communities


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS 3: CONEXIONES MÁS FUERTES — Parejas sagradas
# ═══════════════════════════════════════════════════════════════

def strongest_connections(names, edges):
    """¿Qué pares de nombres tienen la conexión más profunda?"""
    print("\n" + "=" * 70)
    print("💎 CONEXIONES MÁS FUERTES — Parejas Sagradas")
    print("=" * 70)
    
    # Ordenar por peso
    edges_sorted = sorted(edges, key=lambda e: e['weight'], reverse=True)
    
    print(f"\n  🔝 TOP 20 PAREJAS MÁS CONECTADAS:")
    print(f"  {'#':>3} {'Par':>18} {'Peso':>5} {'Tipos':>6} {'Conexiones'}")
    print(f"  {'─'*3} {'─'*18} {'─'*5} {'─'*6} {'─'*40}")
    
    for rank, e in enumerate(edges_sorted[:20]):
        a = names[e['source']]
        b = names[e['target']]
        pair = f"#{a['number']}{a['name']}+#{b['number']}{b['name']}"
        conns = '; '.join(e['connections'])
        print(f"  {rank+1:>3} {pair:>18} {e['weight']:>5} {e['types']:>6} {conns}")
    
    # Pares cuya suma = YHVH (26)
    print(f"\n  🔯 PARES CUYA SUMA = NÚMEROS SAGRADOS:")
    sacred_pairs = defaultdict(list)
    for e in edges:
        for conn in e['connections']:
            if 'suma=' in conn:
                sacred_pairs[conn].append(e)
    
    for sacred, pairs in sorted(sacred_pairs.items()):
        print(f"\n     {sacred}:")
        for e in pairs[:5]:
            a = names[e['source']]
            b = names[e['target']]
            print(f"       #{a['number']} {a['name']}({a['gematria']}) + #{b['number']} {b['name']}({b['gematria']})")
    
    return edges_sorted


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS 4: PROPIEDADES GLOBALES DE LA RED
# ═══════════════════════════════════════════════════════════════

def network_properties(names, edges, adj):
    """
    ¿La red de los 72 Nombres tiene propiedades de 'Small-World'?
    Un grafo Small-World tiene:
    - Alto coeficiente de clustering (los amigos de mis amigos son amigos)
    - Camino promedio corto (cualquier nodo alcanza a cualquier otro en pocos pasos)
    """
    print("\n" + "=" * 70)
    print("🌐 PROPIEDADES DE RED — ¿Es un 'Mundo Pequeño'?")
    print("=" * 70)
    
    N = len(names)
    
    # Coeficiente de clustering local
    clustering_coeffs = []
    for i in range(N):
        neighbors = [j for j, w in adj[i]]
        k = len(neighbors)
        if k < 2:
            clustering_coeffs.append(0)
            continue
        
        # Contar triángulos
        triangles = 0
        for a, b in combinations(neighbors, 2):
            if any(j == b for j, w in adj[a]):
                triangles += 1
        
        cc = 2 * triangles / (k * (k - 1))
        clustering_coeffs.append(cc)
    
    avg_clustering = np.mean(clustering_coeffs)
    
    # Comparar con grafo aleatorio
    p = len(edges) / (N * (N - 1) / 2)  # Probabilidad de arista
    random_clustering = p  # En grafo aleatorio C ≈ p
    
    print(f"\n  📊 MÉTRICAS DE RED:")
    print(f"     Nodos: {N}")
    print(f"     Aristas: {len(edges)}")
    print(f"     Densidad: {p*100:.1f}%")
    print(f"     Grado medio: {2*len(edges)/N:.1f}")
    print(f"     Grado máximo: {max(len(adj[i]) for i in range(N))}")
    print(f"     Grado mínimo: {min(len(adj[i]) for i in range(N)) if all(i in adj for i in range(N)) else 0}")
    
    print(f"\n  🔬 TEST DE MUNDO PEQUEÑO:")
    print(f"     Clustering medio (C):   {avg_clustering:.4f}")
    print(f"     Clustering aleatorio:   {random_clustering:.4f}")
    print(f"     Ratio C/Crand:          {avg_clustering/random_clustering:.2f}x")
    
    if avg_clustering / random_clustering > 2:
        print(f"     ✅ ALTO CLUSTERING — Los nombres forman 'camarillas'")
    else:
        print(f"     ─ Clustering normal")
    
    # Top 10 nodos más "camarilleros"
    top_cc = sorted(range(N), key=lambda i: clustering_coeffs[i], reverse=True)
    print(f"\n  🔝 Top 10 nodos con mayor clustering local:")
    for i in top_cc[:10]:
        n = names[i]
        print(f"     #{n['number']} {n['name']} = {n['gematria']} — CC={clustering_coeffs[i]:.4f} (grado={len(adj[i])})")
    
    # Distribución de grado (¿power law?)
    degrees = [len(adj[i]) for i in range(N)]
    degree_dist = Counter(degrees)
    
    print(f"\n  📊 DISTRIBUCIÓN DE GRADO:")
    max_deg = max(degrees) if degrees else 0
    for d in range(0, max_deg + 1, 5):
        count = sum(degree_dist.get(dd, 0) for dd in range(d, min(d+5, max_deg+1)))
        if count > 0:
            bar = '█' * count
            print(f"     {d:>3}-{min(d+4, max_deg):>3}: {count:>3} {bar}")
    
    return avg_clustering, random_clustering


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS 5: LA SIMETRÍA OCULTA
# ═══════════════════════════════════════════════════════════════

def hidden_symmetry(names):
    """
    ¿Existe simetría entre los 72 Nombres?
    - Primer nombre + último nombre
    - Nombre N + Nombre (73-N)
    - ¿Sus sumas forman patrones?
    """
    print("\n" + "=" * 70)
    print("🪞 SIMETRÍA OCULTA — Espejo entre los 72 Nombres")
    print("=" * 70)
    
    N = len(names)
    
    print(f"\n  📊 PAREJAS ESPEJO (Nombre i + Nombre {N+1}-i):")
    print(f"  {'i':>3} {'Nombre':>8} {'Gem':>5} {'←→':>3} {'Nombre':>8} {'Gem':>5} {'Suma':>6} {'÷7':>3} {'Raíz':>5}")
    print(f"  {'─'*3} {'─'*8} {'─'*5} {'─'*3} {'─'*8} {'─'*5} {'─'*6} {'─'*3} {'─'*5}")
    
    mirror_sums = []
    div7_count = 0
    
    for i in range(N // 2):
        j = N - 1 - i
        a = names[i]
        b = names[j]
        s = a['gematria'] + b['gematria']
        dr = digital_root(s)
        d7 = '✅' if s % 7 == 0 else '─'
        mirror_sums.append(s)
        if s % 7 == 0:
            div7_count += 1
        
        if i < 10 or s % 7 == 0 or is_prime(s):  # Mostrar primeros 10 y significativos
            extra = ''
            if is_prime(s): extra += ' PRIMO'
            if s % 26 == 0: extra += ' ÷YHVH'
            print(f"  {i+1:>3} {a['name']:>8} {a['gematria']:>5} {'←→':>3} {b['name']:>8} {b['gematria']:>5} {s:>6} {d7:>3} {dr:>5}{extra}")
    
    # Estadísticas de sumas espejo
    total_mirror = sum(mirror_sums)
    print(f"\n  📊 ESTADÍSTICAS DE SUMAS ESPEJO:")
    print(f"     Pares: {len(mirror_sums)}")
    print(f"     Suma total de todos los espejos: {total_mirror:,}")
    print(f"     Media: {np.mean(mirror_sums):.1f}")
    print(f"     Desv. estándar: {np.std(mirror_sums):.1f}")
    print(f"     Pares cuya suma ÷7: {div7_count}/{len(mirror_sums)} ({div7_count/len(mirror_sums)*100:.1f}%)")
    print(f"     Esperado: {1/7*100:.1f}%")
    print(f"     Ratio: {(div7_count/len(mirror_sums))/(1/7):.2f}x")
    print(f"     Suma total MOD 7: {total_mirror % 7}")
    print(f"     Suma total MOD 72: {total_mirror % 72}")
    print(f"     Raíz digital total: {digital_root(total_mirror)}")
    
    # ¿La suma de todos los 72 es divisible por 7?
    total_72 = sum(n['gematria'] for n in names)
    print(f"\n  🔯 SUMA DE LOS 72 NOMBRES: {total_72:,}")
    print(f"     MOD 7: {total_72 % 7}")
    print(f"     MOD 72: {total_72 % 72}")
    print(f"     MOD 26: {total_72 % 26}")
    print(f"     Raíz digital: {digital_root(total_72)}")
    print(f"     ÷7: {'✅ SI' if total_72 % 7 == 0 else '❌ No'}")
    print(f"     ÷72: {'✅ SI' if total_72 % 72 == 0 else '❌ No'}")
    
    # Factorización
    n = total_72
    factors = []
    temp = n
    for p in range(2, int(temp**0.5) + 1):
        while temp % p == 0:
            factors.append(p)
            temp //= p
    if temp > 1:
        factors.append(temp)
    print(f"     Factorización: {n} = {' × '.join(str(f) for f in factors)}")
    
    return mirror_sums


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("🕸️ TOPOLOGÍA DE LOS 72 NOMBRES DE DIOS")
    print("   Análisis de Red — Matemática Pura")
    print("=" * 70)
    
    # Cargar nombres
    print("\n📜 Cargando los 72 Nombres...")
    names = load_72_names()
    print(f"  ✅ {len(names)} nombres cargados")
    
    # Vista rápida
    print(f"\n  📊 VISTA RÁPIDA:")
    vals = [n['gematria'] for n in names]
    print(f"     Rango: [{min(vals)} — {max(vals)}]")
    print(f"     Media: {np.mean(vals):.1f}")
    print(f"     Mediana: {np.median(vals):.1f}")
    
    # Construir red
    print(f"\n🔗 Construyendo red de conexiones...")
    edges, adj = build_network(names)
    print(f"  ✅ {len(edges)} conexiones encontradas")
    
    # Análisis 1: Centralidad
    degree, w_degree, top_degree = centrality_analysis(names, edges, adj)
    
    # Análisis 2: Clustering
    dr_groups, mod7_groups, communities = find_clusters(names, edges, adj)
    
    # Análisis 3: Conexiones fuertes
    strongest = strongest_connections(names, edges)
    
    # Análisis 4: Propiedades de red
    avg_cc, rand_cc = network_properties(names, edges, adj)
    
    # Análisis 5: Simetría
    mirrors = hidden_symmetry(names)
    
    # === RESUMEN FINAL ===
    print("\n" + "=" * 70)
    print("🕸️ RESUMEN: TOPOLOGÍA DE LOS 72 NOMBRES")
    print("=" * 70)
    
    hub = names[top_degree[0]]
    print(f"\n  🏆 Hub principal: #{hub['number']} {hub['name']} = {hub['gematria']} ({degree[top_degree[0]]} conexiones)")
    print(f"  🔗 Conexiones totales: {len(edges)}")
    print(f"  📊 Clustering: {avg_cc:.4f} (vs aleatorio {rand_cc:.4f} — {avg_cc/rand_cc:.1f}x)")
    print(f"  👥 Comunidades naturales: {len(communities)}")
    
    total_72 = sum(n['gematria'] for n in names)
    print(f"  🔢 Suma de los 72: {total_72} (MOD7={total_72%7}, Raíz={digital_root(total_72)})")
    
    # Hallazgos de Saturno
    saturn_names = [n for n in names if n['mod7'] == 0]
    print(f"\n  🪐 NOMBRES DE SATURNO (÷7):")
    for n in saturn_names:
        print(f"     #{n['number']} {n['name']} = {n['gematria']} (raíz={n['digital_root']})")
    
    print(f"\n     Total nombres de Saturno: {len(saturn_names)}/72")
    print(f"     Suma: {sum(n['gematria'] for n in saturn_names)}")
    
    print("\n✅ Análisis topológico completo.")
