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