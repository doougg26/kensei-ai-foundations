def calcularAreaTriangulo(a, b):

    area = a * b / 2
    return(area)

altura = int(input("digite a altura: "))
base = int(input("digite a base: "))

resultado = calcularAreaTriangulo(altura, base)
print("a area é:", resultado)

