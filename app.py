from flask import Flask, request, jsonify, render_template_string
from criterio import Criterio
from alternativa import Alternativa
from saw import SAW

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, port=5100)