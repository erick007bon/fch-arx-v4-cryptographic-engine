import os
from fpdf import FPDF

class LegalPDF(FPDF):
    def header(self):
        # Arial bold 12
        self.set_font('Arial', 'B', 12)
        # Move to the right
        self.cell(1)
        # Title
        self.cell(0, 10, 'INSTITUTO ECUATORIANO DE PROPIEDAD INTELECTUAL (SENADI)', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        body = body.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, body)
        self.ln()

output_dir = r"C:\Users\Erick Zambrano\Desktop\linkedin\PROYECTOS\08_gematria_torah\ENSAYOS CIENTIFICOS"

# 1. MEMORIA TECNICA
pdf1 = LegalPDF()
pdf1.add_page()
pdf1.set_font('Arial', 'B', 14)
pdf1.cell(0, 10, 'MEMORIA TECNICA DE INVENCION', align='C')
pdf1.ln(10)

pdf1.chapter_title('TITULO DE LA INVENCION:')
pdf1.chapter_body('Metodo informatico para la deteccion y recuperacion autonoma de datos corruptos mediante paridad geometrica sin redundancia de red.')

pdf1.chapter_title('INVENTOR:')
pdf1.chapter_body('Erick R. Flores Zambrano')

pdf1.chapter_title('1. CAMPO TECNICO DE LA INVENCION')
pdf1.chapter_body('La presente invencion se refiere al campo de la bioinformatica, la ingenieria de software y el almacenamiento magnetico/estado solido de datos. De forma especifica, propone un metodo informatico (algoritmo autonomo) para la recuperacion de fallos y correccion de bytes corrompidos matematicamente mediante interseccion de conjuntos y paridad base-7, mitigando la retencion de datos en reposos a largo plazo.')

pdf1.chapter_title('2. ESTADO DE LA TECNICA (ANTECEDENTES)')
pdf1.chapter_body('En la industria actual, la preservacion de informacion contra el "Bit-Rot" (desgaste fisico de medios de almacenamiento o impacto radiactivo/cosmico) depende altamente de Sistemas RAID (Generalmente RAID-5 o RAID-6) o codigos Erasure de Reed-Solomon. El problema principal de estos metodos tradicionales radica en que requieren copias de seguridad estancadas (Backups 1:1) o una penalizacion masiva del espacio de disco. Cuando no existe un servidor espejo en redundancia, el byte destruido se considera informacion irremediablemente muerta.')

pdf1.chapter_title('3. DESCRIPCION DETALLADA DE LA INVENCION')
pdf1.chapter_body('La invencion aborda el problema de la perdida informatica mediante la omision deliberada de la necesidad de servidores en espejo ("Sin redundancia de red"). El metodo se fundamenta en estructurar los mapas de bits originales en bloques bidimensionales (matrices hibridas base 7x7) que interconectan la matematica posicional del dato puro.\n\nEl flujo informatico comprende:\n1. Paso de Extraccion y Serializacion: El software descompone cualquier archivo origen en sus valores decimales crudos correspondientes a los arrays de bytes.\n2. Distribucion en Base-7: Se acopla la serializacion en matrices iterativas de septima columna (Omer 7x7). El sistema inyecta topologicamente Nodos de Paridad por cada cuadrante horizontal y cuadrante cruzado vertical.\n3. Escudo de Gravedad Computacional: Al guardarse el archivo "protegido", el peso atomico de la matriz viaja junto al contenedor.\n4. Resurreccion y Deteccion Autofagica: Si un evento descompone o altera ("muta") un bit especifico dentro de la estructura base-7, el validador algebraico escanea los ejes de comprobacion cruzada. Al colisionar una resta de ejes erroneos, el sistema extrae las coordenadas asimetricas del bit destruido. Restando la masa conocida sobreviviente del total guardado algebraicamente, el bit muerto se recalculada e inyecta fisicamente en la memoria muerta.')

pdf1.chapter_title('4. VENTAJAS SOBRE LO CONOCIDO')
pdf1.chapter_body('- Coste cero de operaciones de hardware cruzado (No requiere servidores en cluster).\n- Tolerancia determinista al fallo.\n- Aplicabilidad de traduccion inmediata a bases nitrogenadas moleculares (ADN Artificial) o cintas magneticas de resguardo bancario donde es imposible cargar servidores espejo bajo capas de sal.')

pdf1.output(os.path.join(output_dir, "SENADI_Memoria_Tecnica.pdf"))

# 2. REIVINDICACIONES
pdf2 = LegalPDF()
pdf2.add_page()
pdf2.set_font('Arial', 'B', 14)
pdf2.cell(0, 10, 'REIVINDICACIONES', align='C')
pdf2.ln(10)

revs = ("1. Un metodo informatico autonomo para la deteccion, correccion y recuperacion in-situ de datos corruptos caracterizado "
        "porque no requiere infraestructura de servidores redundante (tipo espejo, cluster, o copias de seguridad de archivo estancado), "
        "comprendiendo dicho metodo las siguientes fases computacionales: \n"
        "(a) Serializar la data digital objetivo (binaria, hexadecimal, texto) abstrayendola hasta sus representaciones atomicas en valores decimales; \n"
        "(b) Transpilar e inyectar el arreglo serializado de datos dentro de matrices bidimensionales cuya estructura geometrica constrine un ciclo forzado de base-7 (topologia 7x7); \n"
        "(c) Calcular matematicamente de forma autonoma una suma de comprobacion (Checksum) algoritmica para cada cuadrante matricial (Horizontal X, y Vertical Y); \n"
        "(d) Concatenar dicho super-vector de comprobacion metrica al cuerpo del fichero contenedor como escudo de retencion entropica; \n"
        "(e) Escanear la estructura base mediante triangulacion cruzada para deducir la existencia de una mutacion entropica dentro del contenedor alterado. \n"
        "(f) Recuperar matematicamente la coordenada precisa donde yace el byte descompuesto infiriendolo a partir de las sumas dimensionales restantes, reemplazando la base muerta por la matriz inmaculada deducida sin interactuar en la web. \n\n"
        "2. El metodo informatico de la reivindicacion 1, en el cual las estructuras matriciales se basan en la arquitectura posicional de "
        "Super-Hubs y ciclos de septima dimension extraidos de proporciones biomimeticas masoreticas, previniendo el colapso global de bits rotos (Bit-Rot).\n\n"
        "3. El metodo informatico de la reivindicacion 1, caracterizado porque se ejecuta mediante procesamiento en CPU estandar para la conservacion de "
        "ficheros magneticos y es completamente traducible a bases organicas (Tolerancia en discos de ADN cristalizado).\n\n"
        "4. Un sistema ejecutador de recuperacion de error, configurado fisicamente por un procesador y codigo fuente que almacena e "
        "implementa de manera automatica los pasos detallados de la reivindicacion 1.")

pdf2.chapter_body(revs)
pdf2.output(os.path.join(output_dir, "SENADI_Reivindicaciones.pdf"))

print("¡PDFs Legales del SENADI Creados!")
