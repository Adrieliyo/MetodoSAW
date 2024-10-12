from criterio import Criterio
from alternativa import Alternativa
from saw import SAW


if __name__ == '__main__':
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

    print(f"\nLa mejor alternativa es {mejor_alt} con un puntaje de {puntaje}")

