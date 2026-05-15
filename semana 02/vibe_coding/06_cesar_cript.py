#!/usr/bin/env python3
from pathlib import Path
from typing import List


def get_txt_files(folder: Path) -> List[Path]:
    return sorted(folder.glob('*.txt'))


def get_encrypted_files(folder: Path) -> List[Path]:
    return sorted(folder.glob('*_cesar_*.txt'))


def choose_file(files: List[Path], title: str) -> Path:
    if not files:
        raise FileNotFoundError(f'Nenhum arquivo {title.lower()} encontrado no diretório atual.')

    print(f'{title}:')
    for index, file in enumerate(files, start=1):
        print(f'  {index}. {file.name}')

    while True:
        escolha = input('Escolha um arquivo pelo número: ').strip()
        if escolha.isdigit():
            idx = int(escolha) - 1
            if 0 <= idx < len(files):
                return files[idx]
        print('Opção inválida. Tente novamente.')


def ask_shift(default: int = 3) -> int:
    while True:
        resposta = input(f'Escolha a chave de deslocamento (número inteiro, padrão {default}): ').strip()
        if resposta == '':
            return default
        if resposta.lstrip('-').isdigit():
            return int(resposta)
        print('Entrada inválida. Digite um número inteiro.')


def caesar_cipher(text: str, shift: int) -> str:
    resultado = []
    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            resultado.append(chr((ord(char) - ord(base) + shift) % 26 + ord(base)))
        else:
            resultado.append(char)
    return ''.join(resultado)


def encrypt_file(file_path: Path, shift: int) -> Path:
    content = file_path.read_text(encoding='utf-8')
    encrypted = caesar_cipher(content, shift)
    target_name = file_path.stem + f'_cesar_{shift}' + file_path.suffix
    target_path = file_path.with_name(target_name)
    target_path.write_text(encrypted, encoding='utf-8')
    return target_path


def decrypt_file(file_path: Path, shift: int) -> Path:
    content = file_path.read_text(encoding='utf-8')
    decrypted = caesar_cipher(content, -shift)
    target_name = file_path.stem + f'_decifrado_{shift}' + file_path.suffix
    target_path = file_path.with_name(target_name)
    target_path.write_text(decrypted, encoding='utf-8')
    return target_path


def read_file_contents(file_path: Path) -> None:
    print(f'\nConteúdo de {file_path.name}:')
    print('---')
    print(file_path.read_text(encoding='utf-8'))
    print('---')


def print_menu() -> None:
    print('\nMenu:')
    print('1 - Criptografar arquivo TXT')
    print('2 - Listar textos criptografados')
    print('3 - Descriptografar arquivo cifrado')
    print('4 - Ler arquivo TXT')
    print('5 - Sair')


def main() -> None:
    folder = Path.cwd()

    while True:
        print_menu()
        choice = input('Escolha uma opção: ').strip()

        if choice == '1':
            files = get_txt_files(folder)
            try:
                selected = choose_file(files, 'Arquivos TXT disponíveis')
            except FileNotFoundError as error:
                print(error)
                continue
            shift = ask_shift()
            result_path = encrypt_file(selected, shift)
            print(f'Arquivo criptografado criado: {result_path.name}')

        elif choice == '2':
            encrypted_files = get_encrypted_files(folder)
            if not encrypted_files:
                print('Nenhum arquivo criptografado encontrado.')
                continue
            print('Textos criptografados encontrados:')
            for file in encrypted_files:
                print(f'  - {file.name}')

        elif choice == '3':
            encrypted_files = get_encrypted_files(folder)
            try:
                selected = choose_file(encrypted_files, 'Arquivos criptografados disponíveis')
            except FileNotFoundError as error:
                print(error)
                continue
            shift = ask_shift()
            result_path = decrypt_file(selected, shift)
            print(f'Arquivo descriptografado criado: {result_path.name}')

        elif choice == '4':
            files = get_txt_files(folder)
            try:
                selected = choose_file(files, 'Arquivos TXT disponíveis para leitura')
            except FileNotFoundError as error:
                print(error)
                continue
            read_file_contents(selected)

        elif choice == '5':
            print('Saindo.')
            break

        else:
            print('Opção inválida. Tente novamente.')


if __name__ == '__main__':
    main()
