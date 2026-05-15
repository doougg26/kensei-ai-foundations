#!/usr/bin/env python3
import random
import string
from datetime import datetime


def ask_yes_no(prompt: str) -> bool:
    while True:
        resposta = input(f"{prompt} (s/n): ").strip().lower()
        if resposta in {'s', 'sim'}:
            return True
        if resposta in {'n', 'não', 'nao'}:
            return False
        print('Resposta inválida. Digite s ou n.')


def ask_length() -> int:
    while True:
        resposta = input('Digite o tamanho da senha desejada: ').strip()
        if not resposta.isdigit():
            print('Informe um número inteiro positivo.')
            continue
        tamanho = int(resposta)
        if tamanho < 1:
            print('O tamanho precisa ser maior que zero.')
            continue
        return tamanho


def generate_password(length: int, use_upper: bool, use_numbers: bool, use_symbols: bool) -> str:
    base_chars = list(string.ascii_lowercase)
    if use_upper:
        base_chars.extend(string.ascii_uppercase)
    if use_numbers:
        base_chars.extend(string.digits)
    if use_symbols:
        base_chars.extend('!@#$%^&*()-_=+[]{};:,.<>?')

    if not base_chars:
        raise ValueError('Nenhum conjunto de caracteres selecionado.')

    password = ''.join(random.choice(base_chars) for _ in range(length))
    return password


def save_passwords(passwords: list[str], prefix: str = 'senhas') -> str:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f'{prefix}_{timestamp}.txt'
    with open(file_name, 'w', encoding='utf-8') as arquivo:
        for senha in passwords:
            arquivo.write(f'{senha}\n')
    return file_name


def main() -> None:
    print('Gerador de senhas')
    length = ask_length()
    include_upper = ask_yes_no('Incluir letras maiúsculas?')
    include_numbers = ask_yes_no('Incluir números?')
    include_symbols = ask_yes_no('Incluir símbolos?')

    try:
        passwords = [generate_password(length, include_upper, include_numbers, include_symbols) for _ in range(5)]
        print('\nSenhas geradas:')
        for index, senha in enumerate(passwords, start=1):
            print(f'{index}. {senha}')

        file_name = save_passwords(passwords)
        print(f'As senhas foram salvas em {file_name}')
    except ValueError as error:
        print(f'Erro: {error}')


if __name__ == '__main__':
    main()
