from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter

class RifaPDF(FPDF):
    def add_rifa(self, numero, x_vertical, y_vertical, x_horizontal, y_horizontal):
        # Número no canto esquerdo (vertical)
        self.set_font('Arial', '', 12)
        self.set_xy(x_vertical, y_vertical)
        self.rotate(90, x_vertical, y_vertical)
        self.cell(10, 10, numero, align='C')
        self.rotate(0)  # Reset da rotação

        # Número no canto direito (horizontal)
        self.set_xy(x_horizontal, y_horizontal)
        self.cell(20, 10, numero, align='C')

def gerar_rifas_com_modelo(pdf_base, output_pdf, total_rifas):
    # Coordenadas convertidas para pontos
    mm_to_pt = lambda mm: mm * 1
    posicoes_verticais_esquerda = [mm_to_pt(y) for y in [32, 58, 85, 112, 139, 165, 192, 218, 244, 270]]
    posicoes_verticais_direita = [mm_to_pt(y) for y in [16, 42, 69, 96, 122, 149, 176, 201, 228, 254]]
    x_vertical = mm_to_pt(1)      # Posição horizontal da numeração esquerda
    x_horizontal = mm_to_pt(167) # Posição horizontal da numeração direita

    # Carregar o modelo original
    reader = PdfReader(pdf_base)
    writer = PdfWriter()

    pdf = RifaPDF()
    pdf.set_auto_page_break(auto=False)
    pagina_atual = 0

    for i in range(1, total_rifas + 1):
        numero = f"{i:03d}"  # Formato 3 dígitos
        rifa_index = (i - 1) % 10  # Índice dentro da página (0 a 9)
        
        if rifa_index == 0:
            pagina_atual += 1
            pdf.add_page()

        # Adicionar os números nos locais corretos
        pdf.add_rifa(
            numero,
            x_vertical=x_vertical,
            y_vertical=posicoes_verticais_esquerda[rifa_index],
            x_horizontal=x_horizontal,
            y_horizontal=posicoes_verticais_direita[rifa_index]
        )

    temp_pdf = "temp_numeracao2.pdf"
    pdf.output(temp_pdf)

    # Mesclar numeração com o modelo original
    temp_reader = PdfReader(temp_pdf)
    for base_page, temp_page in zip(reader.pages, temp_reader.pages):
        base_page.merge_page(temp_page)
        writer.add_page(base_page)

    # Salvar o PDF final
    with open(output_pdf, "wb") as out_file:
        writer.write(out_file)

# Caminho dos arquivos
base = "C:/Users/Micro/Documents/PIBTV/Rifa02_Eletros.pdf"
output = "C:/Users/Micro/Documents/PIBTV/Numerado_Rifa02_Eletros.pdf"
gerar_rifas_com_modelo(base, output, total_rifas=250)
