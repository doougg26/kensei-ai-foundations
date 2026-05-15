# Projetos de Python

Este repositório contém vários scripts Python de exercícios e utilitários organizados na pasta `semana 02`.

## Estrutura

- `semana 02/`: pasta com os scripts Python desenvolvidos.
- `README.md`: documentação dos projetos.

## Projetos

### `semana 02/converte_celsius.py`
Script interativo de conversão de temperatura.
- Permite escolher entre converter Celsius para Fahrenheit ou Fahrenheit para Celsius.
- Usa um menu em loop que retorna à tela inicial até o usuário optar por sair.

### `semana 02/lista_compras.py`
Aplicação de lista de compras com menu.
- Adiciona, exibe e remove itens da lista.
- Carrega a lista anterior de `lista_compras.txt` se existir.
- Salva a lista atual em `lista_compras.txt` ao sair.

### `semana 02/quiz_cyberseguranca.py`
Quiz interativo sobre cibersegurança.
- Aplica 10 perguntas de múltipla escolha.
- Usa tempo limite para cada questão quando solicitado.
- Exibe pontuação final e mensagem de aprovação se o usuário acertar 3 ou mais.

### `semana 02/gerador_senhas.py`
Gerador de senhas usando `random`.
- O usuário escolhe o tamanho da senha.
- Permite incluir letras maiúsculas, números e símbolos.
- Gera 5 senhas de uma vez.
- Salva as senhas em um arquivo TXT com timestamp.

### `semana 02/organiza_arquivos.py`
Organizador de arquivos por extensão.
- Cria subpastas `imagens`, `docs`, `audio`, `video` e `outros`.
- Move arquivos do diretório atual para a pasta de acordo com sua extensão.
- Exibe relatório da quantidade de arquivos movidos por categoria.

### `semana 02/cesar_txt.py`
Ferramenta de cifra de César para arquivos TXT.
- Lista arquivos `.txt` no diretório atual.
- Criptografa um arquivo selecionado com deslocamento escolhido.
- Lista arquivos criptografados encontrados.
- Descriptografa arquivos cifrados e gera nova versão.
- Permite ler o conteúdo de qualquer arquivo TXT selecionado.

## Como usar

Abra um terminal, navegue para `z:\Nova pasta (3)\semana 02` e execute o script desejado:

```bash
python "semana 02/<nome_do_script>.py"
```

Substitua `<nome_do_script>` pelo nome do arquivo, por exemplo `converte_celsius.py`.

## Observação

Os scripts são independentes e foram criados como pequenos exercícios Python para aprendizado de lógica, manipulação de arquivos e interação com o usuário.
