class Criterio:
    def __init__(self, nombre, ponderacion, tipo='max'):
        """
        Constructor de la clase Criterio.
        :param nombre: Nombre del criterio.
        :param ponderacion: Ponderación del criterio.
        :param tipo: Tipo del criterio ('max' para maximización o 'min' para minimización).
        """
        self.nombre = nombre
        self.ponderacion = ponderacion
        self.tipo = tipo  # max o min


class Alternativa:
    def __init__(self, nombre, valores):
        """
        Constructor de la clase Alternativa.
        :param nombre: Nombre de la alternativa.
        :param valores: Diccionario con los valores de los criterios para esta alternativa.
        """
        self.nombre = nombre
        self.valores = valores  # Diccionario {criterio_nombre: valor}


class SAW:
    def __init__(self, criterios, alternativas):
        """
        Constructor de la clase SAW.
        :param criterios: Lista de objetos Criterio.
        :param alternativas: Lista de objetos Alternativa.
        """
        self.criterios = criterios
        self.alternativas = alternativas

    def normalizar(self):
        """
        Normaliza los valores de las alternativas en función de los criterios (maximización o minimización).
        """
        # Normalizamos los valores para cada criterio
        normalizados = {}

        for criterio in self.criterios:
            valores_criterio = [alt.valores[criterio.nombre] for alt in self.alternativas]

            if criterio.tipo == 'max':
                max_valor = max(valores_criterio)
                normalizados[criterio.nombre] = [v / max_valor for v in valores_criterio]
            elif criterio.tipo == 'min':
                min_valor = min(valores_criterio)
                normalizados[criterio.nombre] = [min_valor / v for v in valores_criterio]

        return normalizados

    def calcular_puntajes(self):
        """
        Calcula el puntaje ponderado para cada alternativa.
        :return: Diccionario con los puntajes ponderados de cada alternativa.
        """
        normalizados = self.normalizar()
        puntajes = {}

        for alt in self.alternativas:
            puntaje = 0
            for criterio in self.criterios:
                valor_normalizado = normalizados[criterio.nombre][self.alternativas.index(alt)]
                puntaje += criterio.ponderacion * valor_normalizado
            puntajes[alt.nombre] = puntaje

        return puntajes

    def mejor_alternativa(self):
        """
        Devuelve la alternativa con el puntaje más alto y también muestra los puntajes de todas las alternativas.
        :return: Nombre de la mejor alternativa y sus puntajes.
        """
        puntajes = self.calcular_puntajes()

        # Imprimir los puntajes de todas las alternativas
        print("Puntajes de todas las alternativas:")
        for alt, puntaje in puntajes.items():
            print(f"{alt}: {puntaje:.3f}")

        mejor_alt = max(puntajes, key=puntajes.get)
        return mejor_alt, puntajes[mejor_alt]


# Ejemplo de uso
if __name__ == "__main__":
    # Definimos los criterios
    criterios = [
        Criterio("Precio", 0.4, tipo='min'),
        Criterio("Rendimiento", 0.3, tipo='max'),
        Criterio("Peso", 0.3, tipo='max')
    ]

    # Definimos las alternativas
    alternativas = [
        Alternativa("Laptop A", {"Precio": 300, "Rendimiento": 10, "Peso": 12}),
        Alternativa("Laptop B", {"Precio": 450, "Rendimiento": 15, "Peso": 16}),
        Alternativa("Laptop C", {"Precio": 500, "Rendimiento": 20, "Peso": 20})
    ]

    # Creamos el objeto SAW y calculamos la mejor alternativa
    saw = SAW(criterios, alternativas)
    mejor_alt, puntaje = saw.mejor_alternativa()

    print(f"\nLa mejor alternativa es {mejor_alt} con un puntaje de {puntaje:.3f}")
