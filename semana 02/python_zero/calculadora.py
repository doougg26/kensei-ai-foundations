def soma(a, b):
    return a + b

def multiplicar(a,b):
    return a * b

def subtrair(a,b):
    return a-b

def dividir(a,b):
    return a/b

a = int(input("digite o primeiro numero:"))
b = int(input("digite o segundo numero:"))
opcao = int(input("selecione uma função: 1 - soma, 2 - multiplicação, 3 - subtração, 4 - Divisão:"))
if opcao ==1:
    resultado = soma(a,b)
    print("A soma de ",a ," + ", b, " = ", resultado)

elif opcao ==2:
    resultado = multiplicar(a,b)
    print("A multiplicação de ",a ," x ", b, " = ", resultado)

elif opcao == 3:
    resultado = subtrair(a,b)
    print("A subtração de ",a ," - ", b, " = ", resultado)

elif opcao ==4:
    resultado = dividir(a,b)
    print("A divisão de ",a ," / ", b, " = ", resultado)

else:
    print("opção inválida!")