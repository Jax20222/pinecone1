from langchain_openai import ChatOpenAI

# Crear la instancia de ChatOpenAI
llm = ChatOpenAI()

# Invocar al modelo con un mensaje de prueba
response = llm.invoke("Hello, world!")

# Imprimir la respuesta del modelo
print(response)
