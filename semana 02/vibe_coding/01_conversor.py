#!/usr/bin/env python3
def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9.0 / 5.0 + 32.0


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32.0) * 5.0 / 9.0



def main() -> None:
    while True:
        print('\nEscolha a conversão:')
        print('1 - Celsius para Fahrenheit')
        print('2 - Fahrenheit para Celsius')
        print('3 - Sair')
        choice = input('Opção (1/2/3): ').strip()

        if choice == '1':
            try:
                entrada = input("Informe a temperatura em Celsius: ")
                c = float(entrada.replace(',','.'))
            except ValueError:
                print("Entrada inválida. Use um número (ex: 36.6).")
                continue

            f = celsius_to_fahrenheit(c)
            print(f"{c:.2f} °C = {f:.2f} °F")

        elif choice == '2':
            try:
                entrada = input("Informe a temperatura em Fahrenheit: ")
                f = float(entrada.replace(',','.'))
            except ValueError:
                print("Entrada inválida. Use um número (ex: 98.6).")
                continue

            c = fahrenheit_to_celsius(f)
            print(f"{f:.2f} °F = {c:.2f} °C")

        elif choice == '3':
            print('Saindo. Obrigado!')
            break

        else:
            print('Opção inválida. Tente novamente.')


if __name__ == "__main__":
    main()
