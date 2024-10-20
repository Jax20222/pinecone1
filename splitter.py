from langchain.text_splitter import MarkdownHeaderTextSplitter

# Cargar el contenido del archivo de texto
with open(r'C:\Users\jaime\OneDrive\Escritorio\Pinecone\salida_lumber.txt', 'r', encoding='utf-8') as archivo_texto:
    markdown_document = archivo_texto.read()

# Definir los encabezados para dividir el documento basado en encabezados H2
headers_to_split_on = [
    ("##", "Header 2")
]

# Inicializar el MarkdownHeaderTextSplitter
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on, strip_headers=False
)

# Dividir el documento en fragmentos basados en los encabezados
md_header_splits = markdown_splitter.split_text(markdown_document)

# Guardar los fragmentos en un archivo
with open(r'C:\Users\jaime\OneDrive\Escritorio\Pinecone\salida_fragmentos.txt', 'w', encoding='utf-8') as archivo_fragmentos:
    for fragment in md_header_splits:
        archivo_fragmentos.write(str(fragment) + "\n\n")

print("Los fragmentos han sido guardados en 'salida_fragmentos.txt'")
print(md_header_splits)
print("\n")