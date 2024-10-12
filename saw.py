from criterio import Criterio
from alternativa import Alternativa

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

            """puntajes[alt.nombre] = puntaje"""
            # Redondear puntaje a 4 decimales
            puntajes[alt.nombre] = round(puntaje, 4)

        return puntajes

    def mejor_alternativa(self):
        """
        Devuelve la alternativa con el puntaje más alto y también muestra los puntajes de todas las alternativas.
        :return: Nombre de la mejor alternativa y sus puntajes.
        """
        puntajes = self.calcular_puntajes()

        print("Puntajes de todas las alternativas:")
        for alt, puntaje in puntajes.items():
            print(f"{alt}: {puntaje}")

        mejor_alt = max(puntajes, key=puntajes.get)
        return mejor_alt, puntajes[mejor_alt]