import pdfplumber

# Ruta del archivo PDF
pdf_path = r'C:\Users\jaime\OneDrive\Escritorio\Pinecone\rasa_seccion_1.pdf'  # Cambia el nombre de tu archivo PDF

# Función para convertir PDF a texto usando pdfplumber
def pdf_a_texto(pdf_path):
    texto_completo = ""
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n"
    return texto_completo

# Convertir el PDF a texto
texto = pdf_a_texto(pdf_path)

# Guardar el texto en un archivo de salida
with open(r'C:\Users\jaime\OneDrive\Escritorio\Pinecone\salida_mejorada.txt', 'w', encoding='utf-8') as archivo_texto:
    archivo_texto.write(texto)

print("El texto ha sido guardado en 'salida_mejorada.txt'")
