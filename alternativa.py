class Alternativa:
    def __init__(self, nombre, valores):
        """
        Constructor de la clase Alternativa.
        :param nombre: Nombre de la alternativa.
        :param valores: Diccionario con los valores de los criterios para esta alternativa.
        """
        self.nombre = nombre
        self.valores = valores  # Diccionario {criterio_nombre: valor}