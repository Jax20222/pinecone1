from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/convert_pdf', methods=['POST'])
def convert_pdf():
    # Recibe el archivo PDF subido desde Postman
    file = request.files['pdf']
    
    # Guardar el archivo PDF en la carpeta actual donde se ejecuta app.py (que es backend)
    pdf_path = os.path.join(os.path.dirname(__file__), file.filename)  # Eliminamos 'backend' duplicado
    
    try:
        file.save(pdf_path)
        print(f"Archivo PDF guardado en: {pdf_path}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return jsonify({'error': f"Error al guardar el archivo: {e}"}), 500

    # Ruta al intérprete de Python en el entorno virtual
    python_executable = r'C:\Users\jaime\OneDrive\Escritorio\Pinecone\env\Scripts\python.exe'

    # Ejecuta lumber.py pasándole la ruta del archivo PDF subido
    result = subprocess.run([python_executable, 'lumber.py', pdf_path], cwd=os.path.dirname(__file__), capture_output=True, text=True)

    # Verifica si hubo algún error en la ejecución de lumber.py
    if result.returncode != 0:
        print(f"Error en la ejecución de lumber.py: {result.stderr}")
        return jsonify({'error': f"Error en lumber.py: {result.stderr}"}), 500

    # Ruta absoluta del archivo de salida
    output_path = os.path.join(os.path.dirname(__file__), 'salida_mejorada.txt')

    # Lee el archivo convertido a texto
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"Archivo de salida leído correctamente desde: {output_path}")
    except FileNotFoundError:
        print(f"El archivo {output_path} no se encontró.")
        return jsonify({'error': f"Archivo de salida no encontrado en {output_path}"}), 500

    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
