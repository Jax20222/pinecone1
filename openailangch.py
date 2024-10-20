import os
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings  # Import actualizado para OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as VectorStorePinecone

# Configurar las API keys desde las variables de entorno
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')

# Verificar que las API keys se han cargado correctamente
if not pinecone_api_key:
    raise ValueError("La variable de entorno 'PINECONE_API_KEY' no está configurada.")
if not openai_api_key:
    raise ValueError("La variable de entorno 'OPENAI_API_KEY' no está configurada.")

# Crear una instancia de Pinecone
pc = Pinecone(
    api_key=pinecone_api_key
)

# Verificar si el índice ya existe, si no, crearlo
index_name = "neonato"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Dimensión para OpenAI embeddings
        metric='cosine',  # Cambia la métrica si es necesario
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-1'  # Cambia la región si es necesario
        )
    )
    print(f"Índice '{index_name}' creado en Pinecone.")
else:
    print(f"Índice '{index_name}' ya existe en Pinecone.")

# Crear los embeddings con OpenAI (importación actualizada)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Leer el contenido de 'salida_mejorada.txt'
file_path = 'C:/Users/jaime/OneDrive/Escritorio/Pinecone/salida_mejorada.txt'
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    print(f"Contenido de '{file_path}' leído correctamente.")
except FileNotFoundError:
    raise FileNotFoundError(f"No se encontró el archivo en la ruta especificada: {file_path}")

# Dividir el texto en fragmentos si es necesario (opcional)
text_fragments = text.split("\n\n")  # Aquí se divide por párrafos o como prefieras

# Conectar con el vector store Pinecone e insertar el texto leído del archivo
vector_store = VectorStorePinecone.from_texts(
    [
        "RASA AI es un framework de código abierto para crear asistentes conversacionales avanzados.",
        "RASA permite el desarrollo de chatbots utilizando técnicas de procesamiento de lenguaje natural (NLP) y aprendizaje automático (ML).",
        "El framework se compone de dos partes principales: RASA NLU y RASA Core.",
        "RASA NLU es responsable de comprender las intenciones del usuario y extraer las entidades relevantes de las frases.",
        "RASA Core gestiona el diálogo, tomando decisiones basadas en las entradas del usuario y el contexto de la conversación.",
        "Los asistentes creados con RASA pueden integrarse fácilmente con plataformas de mensajería como Facebook Messenger, Slack, y otros.",
        "RASA es altamente personalizable y permite entrenar modelos para diferentes lenguajes y dominios específicos."
    ],
    embeddings,
    index_name=index_name
)

print("Texto desde 'salida_mejorada.txt' ha sido almacenado en Pinecone exitosamente.")
print(pc.Index(index_name).describe_index_stats())
print("\n")