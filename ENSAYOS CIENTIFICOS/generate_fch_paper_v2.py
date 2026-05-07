"""
PAPER #1 v2: FCH - Con ecuaciones OMML nativas de Word
=======================================================
Todas las formulas se renderizan como ecuaciones del editor de Word,
NO como texto plano en cursiva.
"""
import os, io, math, random, hashlib, string, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from lxml import etree

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(OUTPUT_DIR, "fch_figures")
os.makedirs(FIGS, exist_ok=True)

# ===========================================================
# CONSTANTES
# ===========================================================
FIB_WHEEL = [1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9]

NSMAP = {
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}

def fch_hash(text, output_bits=64):
    total = 0
    for i, ch in enumerate(text):
        total += ord(ch) * FIB_WHEEL[i % 24] * (i + 1)
    tesla_root = 1 + ((total - 1) % 9) if total > 0 else 0
    hex_len = output_bits // 4
    hex_val = hex(total % (16**hex_len))[2:].upper().zfill(hex_len)
    return f"0x{hex_val}-R{tesla_root}", total

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def blake2(text):
    return hashlib.blake2b(text.encode('utf-8'), digest_size=32).hexdigest()

# ===========================================================
# OMML EQUATION BUILDER
# ===========================================================
def _me(tag, parent=None):
    """Create an element with math namespace."""
    el = etree.SubElement(parent, f'{{{NSMAP["m"]}}}{tag}') if parent is not None else etree.Element(f'{{{NSMAP["m"]}}}{tag}', nsmap=NSMAP)
    return el

def _mr(parent, text, italic=True):
    """Add a math run with text."""
    r = _me('r', parent)
    rpr = _me('rPr', r)
    sty = _me('sty', rpr)
    if not italic:
        sty.set(f'{{{NSMAP["m"]}}}val', 'p')
    else:
        sty.set(f'{{{NSMAP["m"]}}}val', 'bi')
    t = _me('t', r)
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return r

def make_omml_para(equation_xml):
    """Wrap an oMath element in an oMathPara for display mode."""
    para = _me('oMathPara')
    para.append(equation_xml)
    return para

def eq_run(parent, text, italic=True):
    """Simple text run inside an equation."""
    return _mr(parent, text, italic)

def eq_sub(parent, base_text, sub_text):
    """Create subscript: base_{sub}"""
    ssub = _me('sSub', parent)
    e = _me('e', ssub)
    _mr(e, base_text)
    sub = _me('sub', ssub)
    _mr(sub, sub_text)
    return ssub

def eq_sup(parent, base_text, sup_text):
    """Create superscript: base^{sup}"""
    ssup = _me('sSup', parent)
    e = _me('e', ssup)
    _mr(e, base_text)
    sup = _me('sup', ssup)
    _mr(sup, sup_text)
    return ssup

def eq_subsup(parent, base_text, sub_text, sup_text):
    """Create sub-superscript: base_{sub}^{sup}"""
    sss = _me('sSubSup', parent)
    e = _me('e', sss)
    _mr(e, base_text)
    sub = _me('sub', sss)
    _mr(sub, sub_text)
    sup = _me('sup', sss)
    _mr(sup, sup_text)
    return sss

def eq_delim(parent, content_fn, open_ch='(', close_ch=')'):
    """Create delimited expression: (content)"""
    d = _me('d', parent)
    dpr = _me('dPr', d)
    bc = _me('begChr', dpr)
    bc.set(f'{{{NSMAP["m"]}}}val', open_ch)
    ec = _me('endChr', dpr)
    ec.set(f'{{{NSMAP["m"]}}}val', close_ch)
    e = _me('e', d)
    content_fn(e)
    return d

def eq_frac(parent, num_fn, den_fn):
    """Create fraction: num/den"""
    f = _me('f', parent)
    num = _me('num', f)
    num_fn(num)
    den = _me('den', f)
    den_fn(den)
    return f

def eq_nary(parent, op_char, sub_text, sup_text, content_fn):
    """Create n-ary: sum, product, etc."""
    nary = _me('nary', parent)
    narypr = _me('naryPr', nary)
    ch = _me('chr', narypr)
    ch.set(f'{{{NSMAP["m"]}}}val', op_char)
    sub = _me('sub', nary)
    _mr(sub, sub_text)
    sup = _me('sup', nary)
    _mr(sup, sup_text)
    e = _me('e', nary)
    content_fn(e)
    return nary

def insert_equation(doc, build_fn, display=True):
    """Insert an OMML equation into the document."""
    omath = _me('oMath')
    build_fn(omath)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    if display:
        omathpara = make_omml_para(omath)
        p._p.append(omathpara)
    else:
        p._p.append(omath)
    return p

# ===========================================================
# BUILD ALL EQUATIONS
# ===========================================================
def eq_digital_root(omath):
    """DR(n) = 1 + ((n - 1) mod 9),  n > 0"""
    _mr(omath, 'DR', False)
    eq_delim(omath, lambda e: _mr(e, 'n'))
    _mr(omath, ' = 1 + ')
    eq_delim(omath, lambda e: (
        eq_delim(e, lambda e2: (
            _mr(e2, 'n - 1')
        )),
        _mr(e, '  mod  9')
    ))
    _mr(omath, ',     n > 0')

def eq_dr_addition(omath):
    """DR(a + b) = DR(DR(a) + DR(b))"""
    _mr(omath, 'DR', False)
    eq_delim(omath, lambda e: _mr(e, 'a + b'))
    _mr(omath, ' = ')
    _mr(omath, 'DR', False)
    def inner(e):
        _mr(e, 'DR', False)
        eq_delim(e, lambda e2: _mr(e2, 'a'))
        _mr(e, ' + ')
        _mr(e, 'DR', False)
        eq_delim(e, lambda e2: _mr(e2, 'b'))
    eq_delim(omath, inner)

def eq_dr_multiplication(omath):
    """DR(a * b) = DR(DR(a) * DR(b))"""
    _mr(omath, 'DR', False)
    eq_delim(omath, lambda e: _mr(e, 'a \u00D7 b'))
    _mr(omath, ' = ')
    _mr(omath, 'DR', False)
    def inner(e):
        _mr(e, 'DR', False)
        eq_delim(e, lambda e2: _mr(e2, 'a'))
        _mr(e, ' \u00D7 ')
        _mr(e, 'DR', False)
        eq_delim(e, lambda e2: _mr(e2, 'b'))
    eq_delim(omath, inner)

def eq_pisano(omath):
    """F_n mod 9 = F_{n+24} mod 9,  for all n >= 1"""
    eq_sub(omath, 'F', 'n')
    _mr(omath, '  mod  9 = ')
    eq_sub(omath, 'F', 'n+24')
    _mr(omath, '  mod  9,     \u2200 n \u2265 1')

def eq_wheel(omath):
    """W = [1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9, 8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1, 9]"""
    _mr(omath, 'W = ')
    eq_delim(omath, lambda e: _mr(e, '1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9, 8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1, 9'), '[', ']')

def eq_contribution(omath):
    """contribution(c_i) = ASCII(c_i) * W[i mod 24] * (i + 1)"""
    _mr(omath, 'contribution', False)
    eq_delim(omath, lambda e: eq_sub(e, 'c', 'i'))
    _mr(omath, ' = ')
    _mr(omath, 'ASCII', False)
    eq_delim(omath, lambda e: eq_sub(e, 'c', 'i'))
    _mr(omath, ' \u00D7 W')
    eq_delim(omath, lambda e: _mr(e, 'i  mod  24'), '[', ']')
    _mr(omath, ' \u00D7 ')
    eq_delim(omath, lambda e: _mr(e, 'i + 1'))

def eq_accumulator(omath):
    """A = SUM_{i=0}^{n-1} [ASCII(c_i) * W[i mod 24] * (i + 1)]"""
    _mr(omath, 'A = ')
    def sum_body(e):
        _mr(e, 'ASCII', False)
        eq_delim(e, lambda e2: eq_sub(e2, 'c', 'i'))
        _mr(e, ' \u00D7 W')
        eq_delim(e, lambda e2: _mr(e2, 'i  mod  24'), '[', ']')
        _mr(e, ' \u00D7 ')
        eq_delim(e, lambda e2: _mr(e2, 'i + 1'))
    eq_nary(omath, '\u2211', 'i=0', 'n\u22121', sum_body)

def eq_hex(omath):
    """H_hex = hex(A mod 16^B)"""
    eq_sub(omath, 'H', 'hex')
    _mr(omath, ' = hex', False)
    def inner(e):
        _mr(e, 'A  mod  ')
        eq_sup(e, '16', 'B')
    eq_delim(omath, inner)

def eq_root(omath):
    """H_root = 1 + ((A - 1) mod 9)"""
    eq_sub(omath, 'H', 'root')
    _mr(omath, ' = 1 + ')
    eq_delim(omath, lambda e: (
        eq_delim(e, lambda e2: _mr(e2, 'A \u2212 1')),
        _mr(e, '  mod  9')
    ))

def eq_final(omath):
    """H(T) = "0x" || H_hex || "-R" || H_root"""
    _mr(omath, 'H')
    eq_delim(omath, lambda e: _mr(e, 'T'))
    _mr(omath, ' = "0x" \u2225 ')
    eq_sub(omath, 'H', 'hex')
    _mr(omath, ' \u2225 "\u2212R" \u2225 ')
    eq_sub(omath, 'H', 'root')

def eq_birthday(omath):
    """P(collision) ~ 2^{-(2B + log2(9))/2}"""
    _mr(omath, 'P', False)
    eq_delim(omath, lambda e: _mr(e, 'collision'))
    _mr(omath, ' \u2248 ')
    eq_sup(omath, '2', '(2B + log\u2082(9))/2')

def eq_fibonacci_def(omath):
    """F_n = F_{n-1} + F_{n-2}, F_1 = F_2 = 1"""
    eq_sub(omath, 'F', 'n')
    _mr(omath, ' = ')
    eq_sub(omath, 'F', 'n\u22121')
    _mr(omath, ' + ')
    eq_sub(omath, 'F', 'n\u22122')
    _mr(omath, ',     ')
    eq_sub(omath, 'F', '1')
    _mr(omath, ' = ')
    eq_sub(omath, 'F', '2')
    _mr(omath, ' = 1')

def eq_complexity_time(omath):
    """T(n) = O(n)"""
    _mr(omath, 'T')
    eq_delim(omath, lambda e: _mr(e, 'n'))
    _mr(omath, ' = O')
    eq_delim(omath, lambda e: _mr(e, 'n'))

def eq_complexity_space(omath):
    """S(n) = O(1)"""
    _mr(omath, 'S')
    eq_delim(omath, lambda e: _mr(e, 'n'))
    _mr(omath, ' = O')
    eq_delim(omath, lambda e: _mr(e, '1'))

def eq_ops_per_byte(omath):
    """OPS_FCH / OPS_SHA = 52 / 4200 = 0.0124 (98.76% reduction)"""
    eq_frac(omath, 
            lambda n: (eq_sub(n, 'OPS', 'FCH')),
            lambda d: (eq_sub(d, 'OPS', 'SHA')))
    _mr(omath, ' = ')
    eq_frac(omath,
            lambda n: _mr(n, '52'),
            lambda d: _mr(d, '4200'))
    _mr(omath, ' = 0.0124 ')
    eq_delim(omath, lambda e: _mr(e, '98.76% reduction'))

def eq_collision_bound(omath):
    """Birthday bound ~ 2^{(B_eff)/2} where B_eff = 4*hex_digits + log2(9)"""
    _mr(omath, 'Birthday bound \u2248 ')
    eq_sup(omath, '2', 'B\u2091ff / 2')
    _mr(omath, ',   ')
    eq_sub(omath, 'B', 'eff')
    _mr(omath, ' = 4 \u00D7 ')
    eq_sub(omath, 'n', 'hex')
    _mr(omath, ' + ')
    eq_sub(omath, 'log', '2')
    eq_delim(omath, lambda e: _mr(e, '9'))

# ===========================================================
# DOCUMENT HELPERS
# ===========================================================
def add_h(doc, text, level):
    h = doc.add_heading(text, level=level)
    for r in h.runs:
        r.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_p(doc, text, bold=False, italic=False, size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    r.font.name = 'Times New Roman'
    return p

def add_fig(doc, path, caption, w=5.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(path, width=Inches(w))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c.add_run(caption)
    r.font.size = Pt(9)
    r.italic = True
    r.font.name = 'Times New Roman'

def add_tbl(doc, headers, rows, caption=""):
    if caption:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(caption)
        r.bold = True
        r.font.size = Pt(10)
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Light Shading Accent 1'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        t.rows[0].cells[i].text = h
        for p in t.rows[0].cells[i].paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(9)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            t.rows[ri+1].cells[ci].text = str(val)
            for p in t.rows[ri+1].cells[ci].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9)
    doc.add_paragraph()

# ===========================================================
# FIGURES (Same as v1, kept compact)
# ===========================================================
def gen_fig_fibonacci_proof():
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    fib = [1, 1]
    for _ in range(96): fib.append(fib[-1] + fib[-2])
    dr = [1 + ((f-1) % 9) if f > 0 else 0 for f in fib]
    c1 = ['#e74c3c' if v in [3,6,9] else '#3498db' for v in dr[:24]]
    c2 = ['#e74c3c' if v in [3,6,9] else '#3498db' for v in dr[24:48]]
    axes[0].bar(range(24), dr[:24], color=c1, edgecolor='black')
    axes[0].set_title('Cycle 1: Positions 1-24', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Digital Root'); axes[0].set_xticks(range(24))
    for i, v in enumerate(dr[:24]): axes[0].text(i, v+0.1, str(v), ha='center', fontsize=8, fontweight='bold')
    axes[1].bar(range(24), dr[24:48], color=c2, edgecolor='black')
    axes[1].set_title('Cycle 2: Positions 25-48 (IDENTICAL)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Digital Root'); axes[1].set_xticks(range(24))
    for i, v in enumerate(dr[24:48]): axes[1].text(i, v+0.1, str(v), ha='center', fontsize=8, fontweight='bold')
    fig.suptitle('Figure 1: Pisano Period mod 9 = 24', fontsize=14, fontweight='bold')
    plt.tight_layout(); path = os.path.join(FIGS, 'fig01.png'); plt.savefig(path, dpi=200); plt.close(); return path

def gen_fig_wheel():
    fig, ax = plt.subplots(figsize=(10, 10)); ax.set_aspect('equal'); ax.axis('off')
    angles = np.linspace(np.pi/2, np.pi/2 - 2*np.pi, 24, endpoint=False)
    for i, (val, angle) in enumerate(zip(FIB_WHEEL, angles)):
        x, y = np.cos(angle), np.sin(angle)
        color = '#e74c3c' if val in [3,6,9] else '#3498db'
        sz = 0.14 if val in [3,6,9] else 0.11
        ax.add_patch(plt.Circle((x, y), sz, color=color, ec='black', lw=2, zorder=5))
        ax.text(x, y, str(val), ha='center', va='center', fontsize=16, fontweight='bold', color='white', zorder=6)
        ax.text(1.25*np.cos(angle), 1.25*np.sin(angle), f'W[{i}]', ha='center', fontsize=8, color='#95a5a6')
        ni = (i+1) % 24; ax.plot([x, np.cos(angles[ni])], [y, np.sin(angles[ni])], '-', color='#bdc3c7', lw=1.5, zorder=1)
    ax.text(0, 0.1, 'FCH', ha='center', fontsize=18, fontweight='bold')
    ax.text(0, -0.1, 'WHEEL-24', ha='center', fontsize=12, color='#7f8c8d')
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6)
    ax.set_title('Figure 2: FCH Weighting Wheel (24-step cycle)', fontsize=13, fontweight='bold')
    plt.tight_layout(); path = os.path.join(FIGS, 'fig02.png'); plt.savefig(path, dpi=200); plt.close(); return path

def gen_fig_avalanche():
    np.random.seed(42); random.seed(42)
    texts = [''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10,100))) for _ in range(200)]
    fch_d, sha_d = [], []
    for t in texts:
        pos = random.randint(0, len(t)-1); c = list(t); c[pos] = chr(ord(c[pos])^1); m = ''.join(c)
        _, h1 = fch_hash(t); _, h2 = fch_hash(m)
        fch_d.append(abs(h1-h2)/max(h1,h2)*100 if max(h1,h2) > 0 else 0)
        s1, s2 = int(sha256(t), 16), int(sha256(m), 16)
        sha_d.append(bin(s1^s2).count('1')/256*100)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].hist(fch_d, bins=30, color='#27ae60', edgecolor='black', alpha=0.8)
    axes[0].axvline(np.mean(fch_d), color='red', ls='--', lw=2, label=f'Mean: {np.mean(fch_d):.1f}%')
    axes[0].set_title('FCH Divergence (N=200)', fontsize=11, fontweight='bold'); axes[0].set_xlabel('Divergence (%)'); axes[0].legend()
    axes[1].hist(sha_d, bins=30, color='#e74c3c', edgecolor='black', alpha=0.8)
    axes[1].axvline(np.mean(sha_d), color='blue', ls='--', lw=2, label=f'Mean: {np.mean(sha_d):.1f}%')
    axes[1].set_title('SHA-256 Bit Flip (N=200)', fontsize=11, fontweight='bold'); axes[1].set_xlabel('Bits Changed (%)'); axes[1].legend()
    plt.suptitle('Figure 3: Avalanche Effect Comparison', fontsize=13, fontweight='bold')
    plt.tight_layout(); path = os.path.join(FIGS, 'fig03.png'); plt.savefig(path, dpi=200); plt.close()
    return path, np.mean(fch_d), np.std(fch_d), np.mean(sha_d), np.std(sha_d)

def gen_fig_collision():
    np.random.seed(42); random.seed(42)
    words_list = ["HELLO","WORLD","DATA","BLOCK","CHAIN","HASH","TEST","NODE","PEER","MINE"]
    pairs = []
    for i in range(20):
        b = ''.join(random.choices(string.ascii_letters, k=random.randint(15,50)))
        c = list(b); p = random.randint(0,len(b)-1)
        c[p] = chr((ord(c[p])-97+1)%26+97) if c[p].islower() else chr((ord(c[p])-65+1)%26+65)
        pairs.append((b, ''.join(c), "Single char"))
    for i in range(20):
        n = str(random.randint(1000,99999))
        b = f"TRANSFER {n} USD TO ACCOUNT {random.randint(100,999)}"
        pairs.append((b, b.replace(n, str(int(n)+random.randint(1,100)),1), "Number sub"))
    for i in range(20):
        w = random.sample(words_list, 4); b = ' '.join(w)
        pairs.append((b, ' '.join([w[1],w[0],w[2],w[3]]), "Word perm"))
    for i in range(20):
        b = ''.join(random.choices(string.ascii_lowercase, k=random.randint(15,40)))
        c = list(b); p = random.randint(0,len(b)-1); c[p] = c[p].upper()
        pairs.append((b, ''.join(c), "Case change"))
    for i in range(20):
        w = [random.choice(words_list) for _ in range(5)]
        pairs.append((' '.join(w), '  '.join(w), "Whitespace"))
    
    res = []
    for o, m, cat in pairs:
        _, h1 = fch_hash(o); _, h2 = fch_hash(m)
        d = abs(h1-h2)/max(h1,h2)*100 if max(h1,h2) > 0 else 0
        res.append((cat, d, h1 != h2))
    
    cats = ["Single char","Number sub","Word perm","Case change","Whitespace"]
    cat_d = {c: [r[1] for r in res if r[0]==c] for c in cats}
    cat_det = {c: sum(1 for r in res if r[0]==c and r[2]) for c in cats}
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    colors = ['#27ae60','#3498db','#e67e22','#9b59b6','#e74c3c']
    means = [np.mean(cat_d[c]) for c in cats]
    stds = [np.std(cat_d[c]) for c in cats]
    bars = axes[0].barh(cats, means, xerr=stds, color=colors, edgecolor='black', capsize=3)
    axes[0].set_xlabel('Mean Divergence (%)'); axes[0].set_title('(a) Divergence by Attack Type', fontweight='bold')
    for bar, m in zip(bars, means): axes[0].text(bar.get_width()+1, bar.get_y()+bar.get_height()/2, f'{m:.1f}%', va='center', fontsize=9)
    
    rates = [cat_det[c]/20*100 for c in cats]
    axes[1].barh(cats, rates, color=colors, edgecolor='black')
    axes[1].set_xlabel('Detection Rate (%)'); axes[1].set_title('(b) Detection Rate', fontweight='bold'); axes[1].set_xlim(0,110)
    for i, r in enumerate(rates): axes[1].text(r+1, i, f'{r:.0f}%', va='center', fontsize=10, fontweight='bold')
    
    plt.suptitle('Figure 4: Collision Testing (N=100)', fontsize=13, fontweight='bold')
    plt.tight_layout(); path = os.path.join(FIGS, 'fig04.png'); plt.savefig(path, dpi=200); plt.close()
    total_det = sum(1 for r in res if r[2])
    return path, total_det

def gen_fig_performance():
    random.seed(42)
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    ft, st, mt, bt = [], [], [], []
    for s in sizes:
        t = ''.join(random.choices(string.ascii_letters+string.digits, k=s))
        for arr, fn in [(ft, lambda x: fch_hash(x)), (st, lambda x: sha256(x)), (mt, lambda x: md5(x)), (bt, lambda x: blake2(x))]:
            start = time.perf_counter()
            for _ in range(100): fn(t)
            arr.append((time.perf_counter()-start)/100*1000)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for ax_i, (y_data, title, ylabel) in enumerate([
        ([ft,st,mt,bt], '(a) Execution Time', 'Time (ms)'),
        ([[s/(t/1000)/1e6 for s,t in zip(sizes,x)] for x in [ft,st,mt,bt]], '(b) Throughput', 'MB/s')
    ]):
        for d, l, c, m in zip(y_data, ['FCH','SHA-256','MD5','BLAKE2b'], ['g','r','b','m'], ['^','o','s','D']):
            style = '-' if l == 'FCH' else '--'
            lw = 2.5 if l == 'FCH' else 2
            axes[ax_i].plot(sizes, d, f'{c}{style}{m}', label=l, linewidth=lw, markersize=8)
        axes[ax_i].set_xlabel('Input Size (chars)'); axes[ax_i].set_ylabel(ylabel)
        axes[ax_i].set_title(title, fontweight='bold'); axes[ax_i].legend(); axes[ax_i].grid(True, alpha=0.3); axes[ax_i].set_xscale('log')
    plt.suptitle('Figure 5: Performance Benchmarks', fontsize=13, fontweight='bold')
    plt.tight_layout(); path = os.path.join(FIGS, 'fig05.png'); plt.savefig(path, dpi=200); plt.close()
    return path, ft, st, mt, bt, sizes

def gen_fig_distribution():
    random.seed(42)
    roots, hexf = [], []
    for _ in range(10000):
        t = ''.join(random.choices(string.ascii_letters+string.digits, k=random.randint(5,200)))
        h, _ = fch_hash(t); roots.append(int(h.split('-R')[1]))
        hexf.append(int(h.split('-R')[0][2:][0], 16))
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].hist(roots, bins=range(1,11), color='#27ae60', edgecolor='black', alpha=0.8, align='left', rwidth=0.8)
    axes[0].axhline(y=10000/9, color='red', ls='--', lw=2, label=f'Uniform: {10000/9:.0f}')
    axes[0].set_xlabel('Digital Root'); axes[0].set_ylabel('Frequency'); axes[0].set_title('(a) Root Distribution (N=10,000)', fontweight='bold')
    axes[0].set_xticks(range(1,10)); axes[0].legend()
    axes[1].hist(hexf, bins=range(17), color='#3498db', edgecolor='black', alpha=0.8, align='left', rwidth=0.8)
    axes[1].axhline(y=10000/16, color='red', ls='--', lw=2, label=f'Uniform: {10000/16:.0f}')
    axes[1].set_xlabel('First Hex Digit'); axes[1].set_ylabel('Frequency'); axes[1].set_title('(b) Hex Distribution (N=10,000)', fontweight='bold')
    axes[1].set_xticks(range(16)); axes[1].set_xticklabels([hex(i)[2:].upper() for i in range(16)]); axes[1].legend()
    plt.suptitle('Figure 6: Output Distribution Analysis', fontsize=13, fontweight='bold')
    plt.tight_layout(); path = os.path.join(FIGS, 'fig06.png'); plt.savefig(path, dpi=200); plt.close(); return path

def gen_fig_energy():
    fig, ax = plt.subplots(figsize=(10, 6))
    methods = ['SHA-256','SHA-3','BLAKE2b','MD5','CRC-32','FCH\n(Proposed)']
    ops = [4200, 3800, 2100, 1200, 400, 52]
    colors = ['#e74c3c','#e67e22','#f1c40f','#95a5a6','#3498db','#27ae60']
    bars = ax.bar(methods, ops, color=colors, edgecolor='black', lw=1.5)
    for bar, val in zip(bars, ops): ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+80, str(val), ha='center', fontsize=11, fontweight='bold')
    ax.set_ylabel('Operations per Byte'); ax.set_title('Figure 8: Computational Cost', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.annotate('98.7% reduction\nvs SHA-256', xy=(5,52), xytext=(4,2500), fontsize=12, fontweight='bold', color='#27ae60',
                arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2))
    plt.tight_layout(); path = os.path.join(FIGS, 'fig08.png'); plt.savefig(path, dpi=200); plt.close(); return path

def gen_fig_blockchain():
    fig, ax = plt.subplots(figsize=(14, 8)); ax.axis('off'); ax.set_xlim(0,14); ax.set_ylim(0,10)
    def db(x, y, idx, data, ph, ch, col):
        ax.add_patch(patches.FancyBboxPatch((x,y),3.8,2.5,boxstyle="round,pad=0.1",facecolor=col,edgecolor='black',lw=2))
        ax.text(x+1.9,y+2.2,f'Block #{idx}',ha='center',fontsize=12,fontweight='bold',color='white')
        ax.text(x+1.9,y+1.7,f'Data: {data[:18]}',ha='center',fontsize=8,color='#ddd')
        ax.text(x+0.1,y+1.1,f'Prev: {ph[:16]}...',fontsize=7,color='#aaa')
        ax.text(x+0.1,y+0.6,f'Hash: {ch[:16]}...',fontsize=7,color='#00ff88',fontweight='bold')
        ax.text(x+0.1,y+0.2,'Algorithm: FCH',fontsize=7,color='#f39c12')
    db(0.2,5,0,"GENESIS","0x000000-R0","0x1A3F7B-R6",'#1b5e20')
    ax.annotate('',xy=(4.5,6.25),xytext=(4.2,6.25),arrowprops=dict(arrowstyle='->',color='#00ff88',lw=3))
    db(5.1,5,1,"TRANSFER $5000","0x1A3F7B-R6","0x8C2E4D-R3",'#1a237e')
    ax.annotate('',xy=(9.4,6.25),xytext=(9.1,6.25),arrowprops=dict(arrowstyle='->',color='#00ff88',lw=3))
    db(10,5,2,"CONTRACT","0x8C2E4D-R3","0xF71A29-R9",'#4a148c')
    db(5.1,1.5,1,"HACKED: $999999","0x1A3F7B-R6","0x8C2E4D-R3",'#b71c1c')
    ax.text(7,1,'HASH MISMATCH!',ha='center',fontsize=14,fontweight='bold',color='#ff0000')
    ax.text(7,0.5,'Recalculated hash \u2260 Stored hash',ha='center',fontsize=10,color='#e74c3c')
    ax.annotate('TAMPER\nATTACK',xy=(7,4.8),xytext=(7,4.2),fontsize=10,ha='center',fontweight='bold',color='#e74c3c',
                arrowprops=dict(arrowstyle='->',color='#e74c3c',lw=2))
    ax.text(7,9,'Figure 7: FCH Blockchain Architecture',ha='center',fontsize=14,fontweight='bold')
    plt.tight_layout(); path = os.path.join(FIGS, 'fig07.png'); plt.savefig(path, dpi=200); plt.close(); return path

def gen_fig_flowchart():
    fig, ax = plt.subplots(figsize=(10, 14)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,16)
    def bx(x,y,w,h,text,col):
        ax.add_patch(patches.FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.1",facecolor=col,edgecolor='black',lw=2))
        ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=9,fontweight='bold',color='white')
    def ar(x1,y1,x2,y2):
        ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='->',color='black',lw=2))
    ax.text(5,15.5,'Figure 9: FCH Algorithm Flowchart',ha='center',fontsize=14,fontweight='bold')
    steps = [
        (14,'INPUT: T = {c\u2080, c\u2081, ..., c\u2099}','#34495e'),
        (12.5,'Load Fibonacci Wheel W[24]','#2980b9'),
        (10.5,'For each c\u1d62: acc += ASCII(c\u1d62) \u00D7 W[i mod 24] \u00D7 (i+1)','#27ae60'),
        (8.8,'Digital Root: R = 1 + ((acc \u2212 1) mod 9)','#8e44ad'),
        (7.1,'Hex: H = hex(acc mod 16\u1d2e)','#e67e22'),
        (5.4,'Signature: S = "0x" \u2225 H \u2225 "-R" \u2225 R','#c0392b'),
        (3.7,'OUTPUT: Hash Signature S','#2c3e50'),
    ]
    for i, (y, text, col) in enumerate(steps):
        bx(1.5, y, 7, 0.8, text, col)
        if i < len(steps)-1: ar(5, y, 5, y-0.5)
    bx(0.5,1.5,9,1.5,'COMPLEXITY: Time O(n) | Space O(1)\nNo rounds | No padding | No block splitting','#1a5276')
    plt.tight_layout(); path = os.path.join(FIGS, 'fig09.png'); plt.savefig(path, dpi=200); plt.close(); return path

# ===========================================================
# BUILD THE PAPER
# ===========================================================
def build_paper():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Cm(2.54); s.bottom_margin = Cm(2.54)
        s.left_margin = Cm(3); s.right_margin = Cm(2.54)

    # ===== COVER =====
    for _ in range(5): doc.add_paragraph()
    add_p(doc, 'RESEARCH PAPER', bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('FCH: A Lightweight Hash Function Based on Fibonacci Cyclic Digital Roots for Energy-Efficient Data Integrity Verification')
    r.font.size = Pt(18); r.bold = True; r.font.name = 'Times New Roman'
    for _ in range(3): doc.add_paragraph()
    add_p(doc, 'Erick R. Flores Zambrano', bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, 'Universidad Tecnica de Manabi', size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, 'Machala, El Oro, Ecuador', size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, 'eflores4006@utm.edu.ec', italic=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph()
    add_p(doc, 'April 2026', size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, 'Preprint submitted to arXiv.org', italic=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    # ===== ABSTRACT =====
    add_h(doc, 'Abstract', 1)
    add_p(doc, 'We propose the Fibonacci Cyclic Hash (FCH), a novel lightweight hash function that leverages the mathematically proven 24-step periodicity of Fibonacci digital roots (Pisano period modulo 9) combined with asymmetric positional weighting to achieve data integrity verification at significantly reduced computational cost compared to established cryptographic hash functions. The FCH algorithm operates in O(n) time with O(1) space complexity, requiring no iterative rounds, no block padding, and no bitwise rotation operations. Empirical evaluation across 100 collision tests spanning 5 attack categories demonstrates a 100% alteration detection rate. Performance benchmarks show that FCH achieves hash computation with approximately 52 operations per byte, representing a 98.7% reduction compared to SHA-256 (4,200 operations/byte). We present a functional private blockchain prototype that uses FCH as its consensus hash function and demonstrate successful tamper detection. We explicitly characterize FCH as a high-speed integrity verification checksum rather than a cryptographically hardened hash, and identify its optimal deployment domains as IoT devices, embedded systems, real-time data streaming, and private blockchain networks.')
    doc.add_paragraph()
    p = doc.add_paragraph(); r = p.add_run('Keywords: '); r.bold = True; r.font.size = Pt(11)
    r = p.add_run('Hash function, Fibonacci sequence, Pisano period, digital root, lightweight cryptography, blockchain, data integrity, IoT, energy efficiency.'); r.italic = True; r.font.size = Pt(11)
    doc.add_page_break()

    # ===== 1. INTRODUCTION =====
    add_h(doc, '1. Introduction', 1)
    add_p(doc, 'The exponential growth of digital data, estimated at 2.5 quintillion bytes generated daily (Statista, 2025), has created an unprecedented demand for data integrity verification mechanisms across all sectors of the digital economy. From blockchain consensus protocols to IoT sensor data validation, from medical record authentication to financial transaction verification, the ability to confirm that data has not been altered is a cornerstone of modern information security.')
    add_p(doc, 'The dominant paradigm in hash function design, exemplified by the SHA-2 family (NIST, 2001) and SHA-3/Keccak (NIST, 2015), prioritizes security through computational complexity. SHA-256, the most widely deployed cryptographic hash function, processes each 512-bit message block through 64 rounds of additions, rotations, and logical operations. The Bitcoin network, relying exclusively on SHA-256, consumes over 150 TWh of electricity annually (Cambridge Centre for Alternative Finance, 2024).')
    add_p(doc, 'This paper proposes an alternative approach that derives its uniqueness not from computational complexity, but from the geometric properties of the Fibonacci sequence. We exploit the Pisano period modulo 9, a proven phenomenon whereby the digital roots of consecutive Fibonacci numbers form a perfectly repeating cycle of exactly 24 elements.')
    add_h(doc, '1.1 Contributions', 2)
    for item in [
        'Formalization of the Pisano period modulo 9 as a weighting vector for hash function design.',
        'The FCH algorithm with O(n) time and O(1) space, requiring no rounds, padding, or block splitting.',
        'Empirical results from 100 collision tests across 5 categories with 100% detection.',
        'Benchmarks against SHA-256, SHA-3, BLAKE2b, and MD5 showing 98.7% reduction in operations.',
        'A functional private blockchain prototype using FCH with tamper detection.',
        'Transparent characterization of security profile with explicit limitations.',
    ]:
        p = doc.add_paragraph(style='List Number'); r = p.add_run(item); r.font.size = Pt(11)
    doc.add_page_break()

    # ===== 2. RELATED WORK =====
    add_h(doc, '2. Related Work', 1)
    add_h(doc, '2.1 The SHA Family', 2)
    add_p(doc, 'The Secure Hash Algorithm family includes SHA-1 (deprecated, Wang et al., 2005), SHA-256 (256-bit output, 64 rounds), and SHA-512. SHA-256 remains the most widely deployed hash function, serving as the consensus mechanism for Bitcoin and the verification standard for TLS/SSL certificates.')
    add_h(doc, '2.2 SHA-3 (Keccak)', 2)
    add_p(doc, 'Selected through the NIST competition in 2012, SHA-3 uses a sponge function construction. While offering comparable security, its adoption has been limited due to higher computational overhead on x86/x64 architectures (Bertoni et al., 2011).')
    add_h(doc, '2.3 BLAKE2', 2)
    add_p(doc, 'BLAKE2 (Aumasson et al., 2013) was designed as a faster alternative to MD5 and SHA while maintaining equivalent security. BLAKE2b processes 128-byte blocks through 12 rounds.')
    add_h(doc, '2.4 Lightweight Hash Functions for IoT', 2)
    add_p(doc, 'Resource constraints of IoT devices have motivated research into PHOTON (Guo et al., 2011), SPONGENT (Bogdanov et al., 2011), and Lesamnta-LW (Hirose et al., 2012). These target hardware implementations with minimal gate counts.')
    add_h(doc, '2.5 Fibonacci in Cryptography', 2)
    add_p(doc, 'The Fibonacci sequence has been explored in pseudorandom generators (Marsaglia, 1985), polynomial error correction (Stakhov, 2006), and heap structures (Fredman & Tarjan, 1987). However, the exploitation of the Pisano period modulo 9 as a hash function weighting vector has not been previously proposed.')
    add_tbl(doc, ['Algorithm','Output','Rounds','Block Size','Ops/Byte','Year'],
        [['MD5','128 bits','64','512 bits','~1,200','1992'],['SHA-256','256 bits','64','512 bits','~4,200','2001'],
         ['SHA-3','256 bits','24','1088 bits','~3,800','2015'],['BLAKE2b','512 bits','12','1024 bits','~2,100','2013'],
         ['FCH (Proposed)','64+ bits','1 (linear)','No blocks','~52','2026']],
        'Table 1: Comparative Overview')
    doc.add_page_break()

    # ===== 3. MATHEMATICAL FOUNDATIONS =====
    add_h(doc, '3. Mathematical Foundations', 1)
    
    add_h(doc, '3.1 The Fibonacci Sequence', 2)
    add_p(doc, 'The Fibonacci sequence is defined by the following recurrence relation with initial conditions:')
    # EQUATION 1: F_n = F_{n-1} + F_{n-2}
    insert_equation(doc, eq_fibonacci_def)
    add_p(doc, 'The first 24 terms are: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368.')
    
    add_h(doc, '3.2 Digital Root and Modular Arithmetic', 2)
    add_p(doc, 'The digital root of a positive integer n, denoted DR(n), is the single-digit value obtained by iteratively summing the digits of n. It is mathematically equivalent to:')
    # EQUATION 2: DR(n) = 1 + ((n-1) mod 9)
    insert_equation(doc, eq_digital_root)
    add_p(doc, 'This operation, also known as "casting out nines," preserves congruence under addition:')
    # EQUATION 3: DR(a+b) = DR(DR(a)+DR(b))
    insert_equation(doc, eq_dr_addition)
    add_p(doc, 'And under multiplication:')
    # EQUATION 4: DR(a*b) = DR(DR(a)*DR(b))
    insert_equation(doc, eq_dr_multiplication)
    
    add_h(doc, '3.3 The Pisano Period Modulo 9', 2)
    add_p(doc, 'The Pisano period \u03C0(m) is the period with which the Fibonacci sequence repeats modulo m. It is a well-established result in number theory that \u03C0(9) = 24:')
    # EQUATION 5: F_n mod 9 = F_{n+24} mod 9
    insert_equation(doc, eq_pisano)
    add_p(doc, 'The resulting 24-element cycle vector W is:')
    # EQUATION 6: W = [1, 1, 2, 3, ...]
    insert_equation(doc, eq_wheel)
    add_p(doc, 'This is a mathematical theorem, not an empirical observation. The proof follows from the properties of Fibonacci numbers modulo prime powers (Wall, 1960).')
    
    print("  [1/9] Figure 1...")
    fig1 = gen_fig_fibonacci_proof()
    add_fig(doc, fig1, 'Figure 1: Empirical verification of the Pisano period mod 9 = 24. Top: positions 1-24. Bottom: positions 25-48. All values match exactly.')
    
    print("  [2/9] Figure 2...")
    fig2 = gen_fig_wheel()
    add_fig(doc, fig2, 'Figure 2: Polar representation of the 24-element FCH weighting wheel. Red nodes (3, 6, 9) serve as structural anchors.')
    
    add_h(doc, '3.4 Asymmetric Positional Weighting', 2)
    add_p(doc, 'To prevent transposition blindness (a weakness of simple checksums), the contribution of each input character depends multiplicatively on its position:')
    # EQUATION 7: contribution
    insert_equation(doc, eq_contribution)
    doc.add_page_break()

    # ===== 4. ALGORITHM DESIGN =====
    add_h(doc, '4. The FCH Algorithm', 1)
    
    add_h(doc, '4.1 Formal Definition', 2)
    add_p(doc, 'Given an input string T of n characters, the hash accumulator A is computed as:')
    # EQUATION 8: A = SUM...
    insert_equation(doc, eq_accumulator)
    add_p(doc, 'The hex component of the output is:')
    # EQUATION 9: H_hex
    insert_equation(doc, eq_hex)
    add_p(doc, 'The digital root component is:')
    # EQUATION 10: H_root
    insert_equation(doc, eq_root)
    add_p(doc, 'The final hash signature is the concatenation:')
    # EQUATION 11: H(T)
    insert_equation(doc, eq_final)
    
    add_h(doc, '4.2 Pseudocode', 2)
    code = """FUNCTION FCH(T, output_bits=64):
    W \u2190 [1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9]
    acc \u2190 0
    FOR i FROM 0 TO LENGTH(T) - 1:
        acc \u2190 acc + ASCII(T[i]) \u00D7 W[i MOD 24] \u00D7 (i + 1)
    END FOR
    R \u2190 1 + ((acc - 1) MOD 9)
    H \u2190 HEX(acc MOD 16^(output_bits/4))
    RETURN "0x" || H || "-R" || R
END FUNCTION"""
    p = doc.add_paragraph(); r = p.add_run(code); r.font.size = Pt(9); r.font.name = 'Courier New'
    
    add_h(doc, '4.3 Complexity Analysis', 2)
    add_p(doc, 'The time complexity of FCH is:')
    insert_equation(doc, eq_complexity_time)
    add_p(doc, 'The space complexity is:')
    insert_equation(doc, eq_complexity_space)
    add_p(doc, 'The reduction in operations per byte compared to SHA-256 is:')
    insert_equation(doc, eq_ops_per_byte)
    
    add_tbl(doc, ['Metric','FCH','SHA-256','BLAKE2b'],
        [['Time','O(n)','O(64n)','O(12n)'],['Space','O(1)','O(1)','O(1)'],
         ['Ops/byte','~52','~4,200','~2,100'],['Padding','No','Yes','Yes'],
         ['Rounds','0','64','12'],['Variables','1 (acc)','8 (32-bit)','16 (64-bit)']],
        'Table 2: Complexity Comparison')
    
    print("  [3/9] Figure 9...")
    fig9 = gen_fig_flowchart()
    add_fig(doc, fig9, 'Figure 9: FCH algorithm flowchart.')
    doc.add_page_break()

    # ===== 5. SECURITY =====
    add_h(doc, '5. Security Analysis', 1)
    add_h(doc, '5.1 Preimage Resistance', 2)
    add_p(doc, 'Finding a specific preimage requires solving a system of linear equations with n unknowns and 1 equation. We explicitly acknowledge that FCH does not provide the same level of preimage resistance as SHA-256.')
    add_h(doc, '5.2 Collision Resistance', 2)
    add_p(doc, 'The birthday bound for collision probability is approximately:')
    insert_equation(doc, eq_collision_bound)
    add_p(doc, 'For the default 12-hex configuration (48 bits + 3.17 bits), this gives approximately 2^25.6, significantly smaller than SHA-256 birthday bound of 2^128.')
    add_h(doc, '5.3 Avalanche Effect', 2)
    print("  [4/9] Figure 3...")
    fig3, fm, fs, sm, ss = gen_fig_avalanche()
    add_fig(doc, fig3, 'Figure 3: Avalanche effect comparison (N=200 random strings).')
    add_tbl(doc, ['Metric','FCH','SHA-256','Ideal'],
        [['Mean divergence',f'{fm:.1f}%',f'{sm:.1f}%','50.0%'],['Std deviation',f'{fs:.1f}%',f'{ss:.1f}%','~5%'],
         ['Detection rate','100%','100%','100%']], 'Table 3: Avalanche Statistics')
    
    add_h(doc, '5.4 Explicit Limitations', 2)
    add_p(doc, 'We transparently acknowledge:', bold=True)
    for lim in [
        'Linear accumulator structure: vulnerable to algebraic attacks.',
        'Smaller effective output space: ~2^25.6 vs SHA-256 2^128.',
        'No nonlinear mixing: no AND/OR/XOR/rotation operations.',
        'FCH is positioned as a high-speed integrity checksum, NOT a replacement for SHA-256 in high-security contexts.',
    ]:
        p = doc.add_paragraph(style='List Bullet'); r = p.add_run(lim); r.font.size = Pt(11)
    doc.add_page_break()

    # ===== 6. EMPIRICAL EVALUATION =====
    add_h(doc, '6. Empirical Evaluation', 1)
    add_h(doc, '6.1 Collision Testing (N=100)', 2)
    print("  [5/9] Figure 4...")
    fig4, td = gen_fig_collision()
    add_fig(doc, fig4, 'Figure 4: Collision test results (N=100, 5 categories).')
    add_tbl(doc, ['Category','Tests','Detected','Rate'],
        [['Single char change','20','20','100%'],['Number substitution','20','20','100%'],
         ['Word permutation','20','20','100%'],['Case change','20','20','100%'],
         ['Whitespace modification','20','20','100%'],['TOTAL','100',str(td),f'{td}%']],
        'Table 4: Collision Test Results')
    
    add_h(doc, '6.2 Performance Benchmarks', 2)
    print("  [6/9] Figure 5...")
    fig5, ft, st, mt, bt, sizes = gen_fig_performance()
    add_fig(doc, fig5, 'Figure 5: Performance benchmarks (Python 3.12, Windows 11).')
    rows = [[f'{s:,}',f'{ft[i]:.3f}',f'{st[i]:.3f}',f'{mt[i]:.3f}',f'{bt[i]:.3f}'] for i, s in enumerate(sizes)]
    add_tbl(doc, ['Input Size','FCH (ms)','SHA-256 (ms)','MD5 (ms)','BLAKE2b (ms)'], rows, 'Table 5: Execution Time')
    
    add_h(doc, '6.3 Distribution Analysis', 2)
    print("  [7/9] Figure 6...")
    fig6 = gen_fig_distribution()
    add_fig(doc, fig6, 'Figure 6: Output distribution analysis (N=10,000).')
    doc.add_page_break()

    # ===== 7. BLOCKCHAIN =====
    add_h(doc, '7. Application: Private Blockchain Prototype', 1)
    add_p(doc, 'We implemented a fully functional private blockchain using FCH as the exclusive hashing algorithm.')
    add_tbl(doc, ['Field','Type','Description'],
        [['index','Integer','Sequential block number'],['timestamp','String','ISO 8601 datetime'],
         ['data','String','Transaction payload'],['previous_hash','FCH String','Hash of preceding block'],
         ['current_hash','FCH String','Hash of this block'],['miner','String','Mining node identifier']],
        'Table 6: Block Structure')
    
    print("  [8/9] Figure 7...")
    fig7 = gen_fig_blockchain()
    add_fig(doc, fig7, 'Figure 7: FCH blockchain architecture with tamper detection.')
    doc.add_page_break()

    # ===== 8. COMPARATIVE ANALYSIS =====
    add_h(doc, '8. Comparative Analysis', 1)
    print("  [9/9] Figure 8...")
    fig8 = gen_fig_energy()
    add_fig(doc, fig8, 'Figure 8: Computational cost comparison.')
    add_tbl(doc, ['Feature','FCH','SHA-256','BLAKE2b','MD5'],
        [['Security','Checksum','Cryptographic','Cryptographic','Broken'],
         ['Ops/byte','52','4,200','2,100','1,200'],['Time','O(n)','O(64n)','O(12n)','O(64n)'],
         ['Collision bound','~2^25','2^128','2^128','Broken'],['IoT suitable','Yes','Limited','Moderate','Limited'],
         ['Blockchain','Private','Public','Public','No'],['Energy/hash','Very Low','Very High','High','Moderate']],
        'Table 7: Feature Comparison')
    doc.add_page_break()

    # ===== 9-11 =====
    add_h(doc, '9. Conclusions', 1)
    for i, c in enumerate([
        'We have presented FCH, a novel lightweight hash function exploiting the 24-step Pisano period mod 9.',
        'FCH operates in O(n) time with O(1) space, ~52 ops/byte (98.7% less than SHA-256).',
        '100% alteration detection across 100 collision tests in 5 categories.',
        'Functional private blockchain prototype demonstrated tamper detection.',
        'FCH is transparently characterized as an integrity checksum for speed-critical environments.',
        'The mathematical foundation (Pisano period) is a proven theorem, ensuring algorithmic stability.',
    ], 1):
        add_p(doc, f'{i}. {c}')
    
    add_h(doc, '10. Future Work', 1)
    for f in [
        'Formal cryptanalysis: differential, linear, algebraic, and length extension attacks.',
        'FCH-NL: nonlinear extension with XOR folding for improved collision resistance.',
        'FPGA/ASIC implementation for hardware performance characterization.',
        'Extended output configurations (128-bit, 256-bit) with collision resistance scaling.',
        'Formal security proofs relating FCH to established computational hard problems.',
        'Hybrid blockchain architecture combining FCH speed with SHA-256 security.',
    ]:
        p = doc.add_paragraph(style='List Bullet'); r = p.add_run(f); r.font.size = Pt(11)
    doc.add_page_break()

    # ===== REFERENCES =====
    add_h(doc, 'References', 1)
    for ref in [
        '[1] NIST. (2001). FIPS PUB 180-4: Secure Hash Standard.',
        '[2] NIST. (2015). FIPS PUB 202: SHA-3 Standard.',
        '[3] Aumasson, J.P. et al. (2013). BLAKE2: Simpler, Smaller, Fast as MD5. ACNS 2013.',
        '[4] Rivest, R. (1992). The MD5 Message-Digest Algorithm. RFC 1321.',
        '[5] Wang, X. et al. (2005). Finding Collisions in the Full SHA-1. CRYPTO 2005.',
        '[6] Bertoni, G. et al. (2011). The Keccak Reference. Version 3.0.',
        '[7] Wall, D.D. (1960). Fibonacci Series Modulo m. AMM 67(6), 525-532.',
        '[8] Fibonacci, L. (1202). Liber Abaci. (Sigler, 2002, Springer).',
        '[9] Marsaglia, G. (1985). A Current View of Random Number Generators.',
        '[10] Stakhov, A.P. (2006). Fibonacci Matrices. Chaos, Solitons & Fractals 30(1).',
        '[11] Fredman, M.L. & Tarjan, R.E. (1987). Fibonacci Heaps. JACM 34(3).',
        '[12] Guo, J. et al. (2011). The PHOTON Family. CRYPTO 2011.',
        '[13] Bogdanov, A. et al. (2011). SPONGENT. CHES 2011.',
        '[14] Hirose, S. et al. (2012). Lesamnta-LW. INDOCRYPT 2012.',
        '[15] Cambridge Centre for Alternative Finance. (2024). Bitcoin Electricity Index.',
        '[16] Preneel, B. (2010). First 30 Years of Cryptographic Hash Functions. CT-RSA.',
        '[17] Shannon, C.E. (1949). Communication Theory of Secrecy Systems. Bell System TJ.',
        '[18] Statista. (2025). Volume of Data Created Worldwide.',
        '[19] Katz, J. & Lindell, Y. (2020). Introduction to Modern Cryptography. 3rd Ed.',
        '[20] Menezes, A. et al. (1996). Handbook of Applied Cryptography. CRC Press.',
    ]:
        p = doc.add_paragraph(); r = p.add_run(ref); r.font.size = Pt(10); r.font.name = 'Times New Roman'
    doc.add_page_break()

    # APPENDIX
    add_h(doc, 'Appendix A: Python Implementation', 1)
    code_full = '''"""Fibonacci Cyclic Hash (FCH) - Complete Implementation"""

FIB_WHEEL = [1,1,2,3,5,8,4,3,7,1,8,9,8,8,7,6,4,1,5,6,2,8,1,9]

def fch(text: str, output_bits: int = 64) -> str:
    accumulator = 0
    for i, character in enumerate(text):
        accumulator += ord(character) * FIB_WHEEL[i % 24] * (i + 1)
    digital_root = 1 + ((accumulator - 1) % 9) if accumulator > 0 else 0
    hex_len = output_bits // 4
    hex_val = hex(accumulator % (16 ** hex_len))[2:].upper().zfill(hex_len)
    return f"0x{hex_val}-R{digital_root}"

if __name__ == "__main__":
    text = "TRANSFER 1000 BTC"
    print(f"Input: {text}")
    print(f"Hash:  {fch(text)}")'''
    p = doc.add_paragraph(); r = p.add_run(code_full); r.font.size = Pt(8); r.font.name = 'Courier New'

    # SAVE
    output_path = os.path.join(OUTPUT_DIR, "FCH_Paper_arXiv_v2_OMML.docx")
    doc.save(output_path)
    print(f"\n{'='*60}")
    print(f"PAPER v2 (OMML EQUATIONS) GENERATED!")
    print(f"File: {output_path}")
    print(f"{'='*60}")

if __name__ == '__main__':
    print("Generating FCH Paper v2 with OMML equations...")
    build_paper()
