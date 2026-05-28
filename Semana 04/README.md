# Semana 04 - Gemini API

Projeto simples em Python para chamar a API do Gemini usando uma chave em `.env`.

## Configuracao

1. Crie um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale as dependencias:

```powershell
pip install -r requirements.txt
```

3. Crie o arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

4. Abra o `.env` e coloque sua chave:

```env
GEMINI_API_KEY=sua_chave_real_aqui
```

## Executar

```powershell
python gemini_api.py
```

O arquivo `.env` esta protegido pelo `.gitignore`, entao sua chave nao deve ir para o Git.

## Chatbot Cyber

```powershell
python chatbot_cyber.py
```

## Analisar Textos

Analisa `arquivo.txt` e salva em `analise.json`:

```powershell
python analisar_textos.py
```

Analisa um arquivo especifico:

```powershell
python analisar_textos.py texto.txt
```

Analisa uma pasta inteira de arquivos `.txt`:

```powershell
python analisar_textos.py .\textos
```

Escolhe outro arquivo de saida:

```powershell
python analisar_textos.py .\textos -o resultado.json
```

## Tradutor para pt-BR

Traduz `texto.txt` e salva `texto_pt.txt`:

```powershell
python tradutor_ptbr.py
```

Traduz texto direto:

```powershell
python tradutor_ptbr.py -t "Your firewall blocked the malware payload."
```

Traduz um arquivo `.txt` e salva com `_pt` no nome:

```powershell
python tradutor_ptbr.py -a texto.txt
```

Traduz todos os `.txt` de uma pasta:

```powershell
python tradutor_ptbr.py -p .\textos
```

Adiciona termos extras ao glossario para nao traduzir:

```powershell
python tradutor_ptbr.py -a texto.txt -g "prompt injection" -g "sandbox"
```

## Relatorio Executivo de CSV com IA

Analisa `steam_games.csv`, gera graficos e salva `relatorio_executivo.md`:

```powershell
python relatorio_csv_ia.py
```

Analisa outro CSV:

```powershell
python relatorio_csv_ia.py ..\Semana 03\cybersecurity_attacks_limpo.csv
```

Escolhe o nome do relatorio e a pasta dos graficos:

```powershell
python relatorio_csv_ia.py steam_games.csv -o relatorio_steam.md --charts-dir graficos_steam
```
