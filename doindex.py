import os
from pinecone import Pinecone, ServerlessSpec
import time

# Obtener las API keys desde las variables de entorno
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
if not pinecone_api_key:
    raise ValueError("La variable de entorno 'PINECONE_API_KEY' no está configurada.")

# Crear una instancia de Pinecone
pc = Pinecone(api_key=pinecone_api_key)

# Configurar la nube y la región para Pinecone desde variables de entorno (o usar valores predeterminados)
cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-west-1'  # Cambié a 'us-west-1' según el código anterior
spec = ServerlessSpec(cloud=cloud, region=region)

# Definir el nombre del índice
index_name = "neonato"  # El índice que estás usando

# Dimensión de los embeddings (asumiendo OpenAI embeddings con 1536 dimensiones)
dimension = 1536

# Crear el índice si no existe
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",  # Puedes cambiar a 'dotproduct' o 'euclidean' si es necesario
        spec=spec
    )
    # Esperar hasta que el índice esté listo
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
    print(f"Índice '{index_name}' creado exitosamente.")
else:
    print(f"Índice '{index_name}' ya existe.")

# Ver el estado del índice antes de realizar el "upsert"
print("Estado del índice antes del upsert:")
print(pc.Index(index_name).describe_index_stats())
print("\n")
