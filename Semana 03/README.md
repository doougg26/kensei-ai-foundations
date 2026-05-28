# Semana 03 - Dados com Pandas e Matplotlib

Esta semana teve como foco transformar arquivos CSV em informacao util usando Python. A base veio do PDF **Kensei AI Foundations - Semana 03: Dados com Pandas**, que apresentou o fluxo essencial de uma analise de dados: carregar, explorar, limpar, filtrar, agrupar, visualizar e documentar.

## O que foi feito

Foram trabalhados dois datasets principais:

- `cybersecurity_attacks.csv`: registros de ataques ciberneticos.
- `01_Netflix_2016_2025.csv`: dados de titulos da Netflix entre 2016 e 2025.

Tambem foi criado um menu para consultar arquivos de malware na pasta `relacao-malwares`, usando os CSVs de ransomware, spyware e trojan.

## Scripts criados

### Ataques ciberneticos

- `01_explorar_dados.py`: carrega o CSV, exibe primeiras linhas, informacoes gerais, estatisticas, nulos e duplicados.
- `02_limpar_dados.py`: remove duplicados, preenche nulos, converte datas e remove registros invalidos.
- `03_filtrar_agrupar.py`: filtra ataques DDoS do ultimo mes do dataset e mostra o top 10 por localidade.
- `04_graficos.py`: gera graficos com Matplotlib.
- `05_analise_completa.py`: executa o pipeline completo em um unico script.

Graficos gerados:

- `grafico_top_10_paises.png`
- `grafico_ataques_por_mes.png`
- `grafico_tipos_ataque.png`

### Netflix

- `exibir_netflix_sem_duplicados.py`: carrega o CSV da Netflix, remove duplicados, exibe os dados e cria graficos.

Graficos gerados:

- `netflix_generos.png`
- `netflix_anos.png`
- `netflix_tipos.png`

### Malwares

- `menu_malwares.py`: exibe um menu para consultar os arquivos `Ransomware.csv`, `Spy.csv` e `Trojan.csv`.

## Conclusoes

Aprendi que trabalhar com dados reais exige mais do que apenas abrir um arquivo. O processo envolve entender a estrutura do dataset, verificar tipos de dados, identificar valores nulos, remover duplicados e preparar as colunas antes de analisar.

No dataset de ataques ciberneticos, a limpeza foi uma etapa importante para tornar a analise confiavel. Depois disso, foi possivel filtrar ataques DDoS, agrupar por localidade e gerar um ranking com os locais mais afetados no ultimo mes disponivel.

Nos dados da Netflix, foi possivel observar como Pandas facilita a leitura e organizacao de dados em tabela. Com Matplotlib, os dados ganharam uma forma visual, permitindo comparar generos, anos e tipos de producao de maneira mais clara.

## O que foi aprendido

- O que sao dados estruturados, semi-estruturados e nao-estruturados.
- O que e um dataset e onde encontrar datasets reais.
- Como usar `pandas.read_csv()` para carregar arquivos CSV.
- Como usar `head()`, `info()`, `describe()`, `isna()` e `duplicated()` para explorar dados.
- Como limpar dados com `drop_duplicates()`, `fillna()`, `dropna()` e `pd.to_datetime()`.
- Como filtrar linhas usando condicoes.
- Como agrupar dados com `groupby()`.
- Como ordenar rankings com `sort_values()`.
- Como criar graficos de barras, linha e pizza com Matplotlib.
- Como salvar graficos em arquivos PNG.
- Como documentar uma analise em um `README.md`.

## Relacao com o PDF

O PDF mostrou que Pandas funciona como um "Excel dentro do Python", permitindo manipular tabelas com poucas linhas de codigo. Na pratica, isso apareceu ao carregar CSVs, limpar dados, contar registros e gerar estatisticas.

Tambem foi reforcado que Matplotlib transforma tabelas em visualizacoes. Isso foi aplicado nos graficos de ataques por mes, top 10 localidades, tipos de ataque, generos da Netflix, titulos por ano e tipos de producao.

O principal aprendizado foi o pipeline completo:

1. Escolher um dataset.
2. Carregar e explorar.
3. Limpar os dados.
4. Filtrar e agrupar.
5. Visualizar com graficos.
6. Documentar as conclusoes.

Esse fluxo e a base para projetos maiores de dados, seguranca, automacao e inteligencia artificial.
