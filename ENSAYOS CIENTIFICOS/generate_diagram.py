import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('off')

# Title
plt.text(0.5, 0.95, "FIGURA 1: DIAGRAMA DE FLUJO DEL METODO DE PARIDAD GEOMETRICA", 
         horizontalalignment='center', fontsize=14, fontweight='bold')

def draw_box(ax, x, y, width, height, text):
    rect = patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='black', facecolor='lightgray')
    ax.add_patch(rect)
    plt.text(x + width/2, y + height/2, text, horizontalalignment='center', verticalalignment='center', fontsize=10, fontweight='bold')

# Boxes
draw_box(ax, 0.3, 0.8, 0.4, 0.1, "1. INGESTA DE DATOS (Input)")
# Arrow down
plt.arrow(0.5, 0.8, 0, -0.05, head_width=0.02, head_length=0.02, fc='k', ec='k')

draw_box(ax, 0.2, 0.65, 0.6, 0.1, "2. DISTRIBUCION EN MATRIZ (Base-7)")
plt.arrow(0.5, 0.65, 0, -0.05, head_width=0.02, head_length=0.02, fc='k', ec='k')

draw_box(ax, 0.2, 0.5, 0.6, 0.1, "3. INYECCION DE PARIDAD (Checksum X,Y)")
plt.arrow(0.5, 0.5, 0, -0.05, head_width=0.02, head_length=0.02, fc='k', ec='k')

draw_box(ax, 0.1, 0.35, 0.35, 0.1, "4A. CORRUPCION\n(Perdida de Bits)")
plt.arrow(0.275, 0.35, 0, -0.05, head_width=0.02, head_length=0.02, fc='k', ec='k')

draw_box(ax, 0.55, 0.35, 0.35, 0.1, "4B. INTERSECCION\n(Aislamiento de Error)")
plt.arrow(0.5, 0.4, 0.05, -0.05, head_width=0.02, head_length=0.02, fc='k', ec='k')

# Recovery
draw_box(ax, 0.3, 0.2, 0.4, 0.1, "5. RECONSTRUCCION MATEMATICA\n(Output)")
plt.arrow(0.275, 0.25, 0.1, -0.05, head_width=0.02, head_length=0.02, fc='k', ec='k')
plt.arrow(0.725, 0.35, -0.1, -0.1, head_width=0.02, head_length=0.02, fc='k', ec='k')

# Save to PDF
pdf_path = r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah\ENSAYOS CIENTIFICOS\diagrama_patente.pdf"
plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
print(f"PDF generado en: {pdf_path}")
