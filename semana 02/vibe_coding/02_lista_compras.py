#!/usr/bin/env python3
import os
from typing import List


def add_item(shopping_list: List[str], item: str) -> None:
    item = item.strip()
    if item:
        shopping_list.append(item)
        print(f'Adicionado: {item}')
    else:
        print('Nenhum item informado.')


def view_list(shopping_list: List[str]) -> None:
    if not shopping_list:
        print('Lista de compras vazia.')
        return
    print('Lista de compras:')
    for i, item in enumerate(shopping_list, start=1):
        print(f'{i}. {item}')


def remove_item(shopping_list: List[str], identifier: str) -> None:
    identifier = identifier.strip()
    if not identifier:
        print('Informe o número ou nome do item a remover.')
        return

    # Tenta remover por índice
    if identifier.isdigit():
        idx = int(identifier) - 1
        if 0 <= idx < len(shopping_list):
            removed = shopping_list.pop(idx)
            print(f'Removido: {removed}')
        else:
            print('Índice inválido.')
        return

    # Remove pela primeira correspondência do nome
    try:
        shopping_list.remove(identifier)
        print(f'Removido: {identifier}')
    except ValueError:
        print('Item não encontrado na lista.')


def save_list(shopping_list: List[str], file_path: str = 'lista_compras.txt') -> None:
    with open(file_path, 'w', encoding='utf-8') as arquivo:
        for item in shopping_list:
            arquivo.write(f'{item}\n')
    print(f'Lista salva em {file_path}')


def load_list(file_path: str = 'lista_compras.txt') -> List[str]:
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as arquivo:
        return [line.strip() for line in arquivo if line.strip()]


def main() -> None:
    shopping_list: List[str] = []

    menu = ('\nMenu:\n'
            '1 - Adicionar item\n'
            '2 - Ver lista\n'
            '3 - Remover item\n'
            '4 - Carregar lista anterior\n'
            '5 - Sair\n')

    while True:
        print(menu)
        choice = input('Escolha uma opção: ').strip()

        if choice == '1':
            item = input('Digite o item para adicionar: ')
            add_item(shopping_list, item)
        elif choice == '2':
            view_list(shopping_list)
        elif choice == '3':
            ident = input('Informe o número ou nome do item a remover: ')
            remove_item(shopping_list, ident)
        elif choice == '4':
            if os.path.exists('lista_compras.txt'):
                shopping_list = load_list()
                print('Lista anterior carregada.')
                view_list(shopping_list)
            else:
                print('Nenhum arquivo de lista salvo encontrado.')
        elif choice == '5':
            save_list(shopping_list)
            print('Saindo. Boa compra!')
            break
        else:
            print('Opção inválida. Tente novamente.')


if __name__ == '__main__':
    main()
