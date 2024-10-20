import os
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings  # Asegurarnos de importar OpenAIEmbeddings

# Configurar las API keys desde las variables de entorno
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')  # También necesitas la API Key de OpenAI para los embeddings
if not pinecone_api_key or not openai_api_key:
    raise ValueError("Las variables de entorno 'PINECONE_API_KEY' y 'OPENAI_API_KEY' deben estar configuradas.")

# Crear una instancia de Pinecone con el nuevo constructor
pc = Pinecone(api_key=pinecone_api_key)

# Definir la nube y la región desde las variables de entorno o usar valores predeterminados
cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-west-1'
spec = ServerlessSpec(cloud=cloud, region=region)

# Definir el índice y el namespace
index_name = "neonato"
namespace = "Rasa01"

# Verificar si el índice ya existe, si no, crearlo
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Dimensión estándar de los embeddings de OpenAI
        metric='cosine',
        spec=spec
    )
    # Esperar hasta que el índice esté listo
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

# Conectar con el índice de Pinecone
index = pc.Index(index_name)

# Crear los embeddings con OpenAI (debe ser el mismo que usaste para generar los embeddings)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Aquí debes cargar los textos originales que usaste para generar los embeddings
md_header_splits = [
    "RASA AI es un framework de código abierto para crear asistentes conversacionales avanzados.",
    "RASA permite el desarrollo de chatbots utilizando técnicas de procesamiento de lenguaje natural (NLP) y aprendizaje automático (ML).",
    "El framework se compone de dos partes principales: RASA NLU y RASA Core.",
    "RASA NLU es responsable de comprender las intenciones del usuario y extraer las entidades relevantes de las frases.",
    "RASA Core gestiona el diálogo, tomando decisiones basadas en las entradas del usuario y el contexto de la conversación.",
    "Los asistentes creados con RASA pueden integrarse fácilmente con plataformas de mensajería como Facebook Messenger, Slack, y otros.",
    "RASA es altamente personalizable y permite entrenar modelos para diferentes lenguajes y dominios específicos."
]

# Subir los textos originales al namespace "Rasa01" para generar los embeddings y almacenarlos en Pinecone
vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings,  # Pasamos el objeto de embeddings correctamente
    namespace=namespace
)

vector_store.add_texts(texts=md_header_splits)

# Dar tiempo para que los vectores se suban
time.sleep(5)

# Verificar cuántos vectores se han subido en el índice "neonato"
print("Estado del índice después del upsert:")
print(index.describe_index_stats())
print("\n")

time.sleep(2)
