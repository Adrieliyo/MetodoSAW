from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
from criterio import Criterio
from alternativa import Alternativa
from saw import SAW
import csv
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET'])
def bienvenida():
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Bienvenido al Algoritmo SAW</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 900px; margin: 0 auto; }
                h1 { color: #333; }
                p { margin-bottom: 10px; }
                pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
            </style>
        </head>
        <body>
            <h1>Bienvenido al Algoritmo SAW (Simple Additive Weighting)</h1>
            <p>Este algoritmo te ayuda a tomar decisiones basadas en múltiples criterios.</p>
            <p>Utiliza el endpoint /saw con una solicitud POST para evaluar alternativas.</p>
            <p>Ejemplo de uso:</p>
            <pre>
                {
                  "criterios": [
                    {"nombre": "Precio", "ponderacion": 0.4, "tipo": "min"},
                    {"nombre": "Rendimiento", "ponderacion": 0.3, "tipo": "max"},
                    {"nombre": "Peso", "ponderacion": 0.3, "tipo": "max"}
                  ],
                  "alternativas": [
                    {"nombre": "Opción A", "valores": {"Precio": 300, "Rendimiento": 10, "Peso": 12}},
                    {"nombre": "Opción B", "valores": {"Precio": 450, "Rendimiento": 15, "Peso": 16}},
                    {"nombre": "Opción C", "valores": {"Precio": 500, "Rendimiento": 20, "Peso": 20}}
                  ]
                }
            </pre>
            <p>Formato del archivo CSV para /saw_csv:</p>
            <pre>
                Criterio,Ponderacion,Tipo
                Precio,0.4,min
                Rendimiento,0.3,max
                Peso,0.3,max
                
                Alternativa,Precio,Rendimiento,Peso
                Opción A,300,10,12
                Opción B,450,15,16
                Opción C,500,20,20
            </pre>
        </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/saw', methods=['POST'])
def calcular():
    try:
        data = request.json

        # Leer los criterios desde la solicitud
        criterios = []
        for criterio in data['criterios']:
            criterios.append(Criterio(criterio['nombre'], criterio['ponderacion'], criterio['tipo']))

        # Leer las alternativas desde la solicitud
        alternativas = []
        for alternativa in data['alternativas']:
            alternativas.append(Alternativa(alternativa['nombre'], alternativa['valores']))

        saw = SAW(criterios, alternativas)
        mejor_alt, puntaje = saw.mejor_alternativa()
        puntajes = saw.calcular_puntajes()  # Obtiene los puntajes de todas las alternativas

        return jsonify({
            'mejor_alternativa': mejor_alt,
            'puntaje': puntaje,
            'todos_puntajes': puntajes
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/saw_csv', methods=['POST'])
def calcular_desde_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            criterios, alternativas = procesar_csv(file_path)
            saw = SAW(criterios, alternativas)
            mejor_alt, puntaje = saw.mejor_alternativa()
            puntajes = saw.calcular_puntajes()

            # Eliminar el archivo después de procesarlo
            os.remove(file_path)

            return jsonify({
                'mejor_alternativa': mejor_alt,
                'puntaje': puntaje,
                'todos_puntajes': puntajes
            })
        except Exception as e:
            # Asegúrate de eliminar el archivo en caso de error
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'File type not allowed'}), 400


def procesar_csv(file_path):
    criterios = []
    alternativas = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Procesar criterios
        next(reader)  # Saltar la línea de encabezado de criterios
        for row in reader:
            if not row or not row[0]:  # Línea en blanco o vacía indica el fin de los criterios
                break
            if len(row) < 3:
                raise ValueError(f"Formato incorrecto en la fila de criterios: {row}")
            criterios.append(Criterio(row[0], float(row[1]), row[2]))

        if not criterios:
            raise ValueError("No se encontraron criterios en el archivo CSV")

        # Procesar alternativas
        try:
            next(reader)  # Saltar la línea de encabezado de alternativas
        except StopIteration:
            raise ValueError("No se encontraron alternativas en el archivo CSV")

        criterio_nombres = [c.nombre for c in criterios]
        for row in reader:
            if not row:  # Saltar filas vacías
                continue
            if len(row) != len(criterio_nombres) + 1:
                raise ValueError(f"Formato incorrecto en la fila de alternativa: {row}")
            nombre = row[0]
            try:
                valores = {criterio_nombres[i]: float(row[i + 1]) for i in range(len(criterio_nombres))}
            except ValueError as e:
                raise ValueError(f"Error al convertir valores a números en la fila: {row}. Error: {str(e)}")
            alternativas.append(Alternativa(nombre, valores))

        if not alternativas:
            raise ValueError("No se encontraron alternativas válidas en el archivo CSV")

    return criterios, alternativas


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5100)