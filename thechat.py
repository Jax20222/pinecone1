import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from pinecone import Pinecone

# Configurar las API keys desde las variables de entorno
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')
if not pinecone_api_key or not openai_api_key:
    raise ValueError("Las variables de entorno 'PINECONE_API_KEY' y 'OPENAI_API_KEY' deben estar configuradas.")

# Crear una instancia de Pinecone con el nuevo constructor
pc = Pinecone(api_key=pinecone_api_key)

# Definir el índice y el namespace que estás utilizando
index_name = "neonato"
namespace = "Rasa01"

# Conectar con el índice de Pinecone
index = pc.Index(index_name)

# Crear los embeddings con OpenAI
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Crear un retriever utilizando PineconeVectorStore
retriever = PineconeVectorStore(
    index=index,
    embedding=embeddings,  # Pasamos los embeddings aquí
    namespace=namespace
).as_retriever()

# Obtener el prompt de Retrieval QA Chat desde el hub de langchain
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

# Configurar el LLM de OpenAI (ChatGPT)
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name='gpt-4',  # Puedes cambiar el modelo según tu preferencia
    temperature=0.0  # Controlar la creatividad del modelo (0.0 es más preciso)
)

# Recuperar los documentos relevantes utilizando invoke()
docs = retriever.invoke("¿Qué es RASA AI?")

# Crear la cadena que combina los documentos recuperados con el LLM
combine_docs_chain = create_stuff_documents_chain(
    llm, retrieval_qa_chat_prompt
)

# A partir de aquí se inician las PREGUNTAS

# Primera pregunta
query1 = "¿Cuáles son las principales características de RASA AI?"

# Usar invoke en la cadena, pasando tanto el contexto (documentos) como la consulta (input)
response1 = combine_docs_chain.invoke({
    "context": docs,
    "input": query1  # Pasamos la consulta original como input
})

print("Respuesta a la primera pregunta:\n", response1)

# Segunda pregunta
query2 = "¿Qué componentes principales tiene RASA AI?"

# Usar invoke en la cadena, pasando tanto el contexto (documentos) como la consulta (input)
response2 = combine_docs_chain.invoke({
    "context": docs,
    "input": query2
})

print("Respuesta a la segunda pregunta:\n", response2)

# Tercera pregunta
query3 = "¿Cuáles son las dos principales partes que componen el framework de RASA AI?"

# Usar invoke en la cadena, pasando tanto el contexto (documentos) como la consulta (input)
response3 = combine_docs_chain.invoke({
    "context": docs,
    "input": query3
})

print("Respuesta a la tercera pregunta:\n", response3)

# Cuarta pregunta
query4 = "Mi asistente RASA no está comprendiendo las intenciones correctamente. ¿Qué debo revisar primero?"

# Usar invoke en la cadena, pasando tanto el contexto (documentos) como la consulta (input)
response4 = combine_docs_chain.invoke({
    "context": docs,
    "input": query4
})

print("Respuesta a la cuarta pregunta:\n", response4)