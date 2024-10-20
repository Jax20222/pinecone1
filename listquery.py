import os
import time
from pinecone import Pinecone

# Configurar las API keys desde las variables de entorno
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
if not pinecone_api_key:
    raise ValueError("La variable de entorno 'PINECONE_API_KEY' no está configurada.")

# Crear una instancia de Pinecone
pc = Pinecone(api_key=pinecone_api_key)

# Definir el índice y el namespace que estás utilizando
index_name = "neonato"
namespace = "Rasa01"

# Conectar con el índice de Pinecone
index = pc.Index(index_name)

# Abrir el archivo para guardar los resultados
with open("resultados_consulta.txt", "w") as file:
    # Listar y consultar los registros en el namespace "Rasa01"
    for ids in index.list(namespace=namespace):
        query = index.query(
            id=ids[0],  # Obtener el primer ID del listado
            namespace=namespace, 
            top_k=1,  # Obtener el vector más cercano (k=1)
            include_values=True,
            include_metadata=True
        )
        # Guardar el resultado en el archivo
        file.write(f"Resultado para ID {ids[0]}:\n")
        file.write(str(query))  # Convertir el resultado a string y escribir en el archivo
        file.write("\n\n")
        
print("Consulta completada y resultados guardados en 'resultados_consulta.txt'.")
