# Relatório Executivo: Análise de Dados de Jogos Steam

**Data:** 18 de Maio de 2024
**Analista:** Analista Sênior de Dados
**Fonte de Dados:** `steam_games.csv`

---

## 1. Sumário Executivo

Este relatório apresenta uma análise exploratória dos dados de jogos da plataforma Steam, abrangendo 40.833 entradas e 22 atributos. O objetivo é fornecer uma visão geral da estrutura dos dados, identificar padrões, anomalias e áreas que requerem atenção para futuras análises ou tomadas de decisão estratégicas.

Os principais achados incluem uma alta incidência de valores ausentes em colunas críticas como `recent_reviews`, `mature_content` e `achievements`, o que pode impactar a completude de análises futuras. Observou-se uma grande variação nos preços originais e de desconto, com a presença de outliers significativos. A maioria das entradas refere-se a "aplicativos" (jogos individuais), e há uma concentração notável de desenvolvedores e editoras no dataset.

Recomendações incluem a priorização da limpeza de dados, investigação de anomalias de preços e aprofundamento na análise de gêneros e tags populares para identificar tendências de mercado.

---

## 2. Visão Geral dos Dados

O dataset `steam_games.csv` contém informações sobre 40.833 jogos, bundles e assinaturas da Steam, organizadas em 22 colunas. As colunas variam de identificadores únicos (URL, nome), descrições textuais, informações de reviews, datas de lançamento, detalhes de desenvolvedores e editoras, tags, requisitos de sistema, até dados de precificação.

**Estrutura do Dataset:**
*   **Linhas:** 40.833
*   **Colunas:** 22
*   **Colunas Numéricas:** `achievements`, `original_price_num`, `discount_price_num`
*   **Colunas Categóricas:** As demais 19 colunas, incluindo `url`, `types`, `name`, `release_date`, `developer`, `publisher`, `popular_tags`, `genre`, e informações de reviews e preços em formato de texto.

---

## 3. Principais Achados

### 3.1. Qualidade dos Dados e Valores Ausentes

A análise revela uma quantidade significativa de valores ausentes em várias colunas, o que pode comprometer a robustez de certas análises.

*   **`recent_reviews`:** 38.127 valores ausentes (aproximadamente 93% do total), indicando que a maioria dos jogos não possui reviews recentes ou essa informação não foi capturada.
*   **`mature_content`:** 37.936 valores ausentes (aproximadamente 93%), sugerindo que a maioria dos jogos não possui classificação de conteúdo maduro ou essa informação não está disponível.
*   **`achievements`:** 28.639 valores ausentes (aproximadamente 70%), o que significa que grande parte dos jogos não possui conquistas ou essa informação não foi registrada.
*   **`discount_price` e `discount_price_num`:** 26.290 valores ausentes (aproximadamente 64%), indicando que a maioria dos jogos não está em promoção no momento da coleta dos dados.
*   **`minimum_requirements` e `recommended_requirements`:** Cerca de 19.700 valores ausentes (aproximadamente 48%), limitando a análise de requisitos de sistema.

A visualização dos valores ausentes pode ser observada no gráfico abaixo:
![Gráfico de Valores Ausentes](Z:/Nova pasta (3)/Semana 04/graficos_relatorio/grafico_valores_ausentes.png)

### 3.2. Estatísticas Numéricas

*   **`achievements`:**
    *   Média: 77.24
    *   Desvio Padrão: 448.5 (alto, indicando grande variabilidade)
    *   Mínimo: 1
    *   Máximo: 9.821
    *   A distribuição é altamente assimétrica, com 75% dos jogos tendo até 38 conquistas, mas alguns poucos jogos com um número extremamente alto.
*   **`original_price_num`:**
    *   Média: 57.95
    *   Desvio Padrão: 5425.06 (extremamente alto)
    *   Mínimo: -1.0 (indica um erro ou dado inválido)
    *   Máximo: 730.640.0 (um outlier extremo)
    *   Mediana: 5.99 (muito menor que a média, confirmando a presença de outliers de alto valor).
*   **`discount_price_num`:**
    *   Média: 46.82
    *   Desvio Padrão: 93.75
    *   Mínimo: 0.0
    *   Máximo: 962.6
    *   Mediana: 19.98 (também menor que a média, sugerindo assimetria).

### 3.3. Frequências Categóricas

*   **`types`:** A vasta maioria das entradas são `app` (38.021), representando jogos individuais. `bundle` (2.572) e `sub` (238) são menos frequentes.
*   **`release_date`:** Há uma quantidade significativa de jogos lançados em "2019" (296), com muitas datas futuras ("Coming Soon": 134, "TBA": 74), indicando que o dataset inclui títulos ainda não lançados.
*   **`developer` e `publisher`:** Há uma concentração de títulos por desenvolvedores e editoras específicas, como "Ubisoft - San Francisco" (1.041 desenvolvedor) e "Degica,Degica" (469 editora), sugerindo players dominantes no mercado Steam.
*   **`popular_tags`:** "Action", "Casual,Simulation" e "Simulation" são as tags mais populares, indicando tendências de gêneros e estilos de jogo.
*   **`recent_reviews` e `all_reviews`:** Estas colunas contêm strings descritivas que precisam ser parseadas para extrair informações numéricas de reviews e sentimentos. Muitos jogos possuem poucas reviews, resultando em "Need more user reviews to generate a score".

---

## 4. Leitura dos Gráficos

*   **Gráfico de Valores Ausentes (`grafico_valores_ausentes.png`):** Este gráfico ilustra visualmente a proporção de valores ausentes por coluna. Ele confirma que `recent_reviews`, `mature_content`, `achievements`, `discount_price` e `discount_price_num` são as colunas mais afetadas, com mais de 60% de seus dados faltando. Isso reforça a necessidade de estratégias de tratamento de dados para essas colunas.

*   **Gráfico de Distribuição de Achievements (`grafico_distribuicao_achievements.png`):** Este gráfico demonstra a distribuição do número de conquistas por jogo. Espera-se que ele mostre uma concentração de jogos com poucas conquistas e uma longa cauda à direita, representando um pequeno número de jogos com um volume excepcionalmente alto de achievements, corroborando a alta média e desvio padrão observados.
    ![Gráfico de Distribuição de Achievements](Z:/Nova pasta (3)/Semana 04/graficos_relatorio/grafico_distribuicao_achievements.png)

*   **Gráfico Top 10 URLs (`grafico_top10_url.png`):** Este gráfico, com base nos dados fornecidos, mostra os 10 URLs mais frequentes. Como cada URL no dataset é única (frequência 1), o gráfico essencialmente ilustra 10 URLs distintas, cada uma com uma ocorrência. Isso reforça que a coluna `url` serve como um identificador único para cada entrada.
    ![Gráfico Top 10 URLs](Z:/Nova pasta (3)/Semana 04/graficos_relatorio/grafico_top10_url.png)

---

## 5. Riscos ou Limitações da Análise

*   **Dados Ausentes:** A alta proporção de valores ausentes em colunas chave pode levar a vieses ou análises incompletas se não forem tratados adequadamente (imputação, remoção ou análise específica).
*   **Outliers de Preço:** A presença de valores extremos e anômalos (`-1.0` e `730.640.0`) em `original_price_num` exige validação e tratamento antes de qualquer análise de precificação.
*   **Formato de Reviews:** As colunas `recent_reviews` e `all_reviews` estão em formato de texto, exigindo processamento de linguagem natural ou extração de padrões para converter em métricas numéricas utilizáveis.
*   **Representatividade:** A concentração de dados em certos desenvolvedores/editoras e tags pode não ser totalmente representativa de todo o universo de jogos Steam, mas sim dos jogos presentes neste dataset específico.
*   **Dados Categóricos Complexos:** Colunas como `popular_tags` e `genre` podem conter múltiplos valores em uma única entrada, exigindo técnicas de one-hot encoding ou similar para análise eficaz.

---

## 6. Recomendações Executivas

1.  **Priorizar a Limpeza de Dados:**
    *   Investigar e tratar os valores anômalos em `original_price_num` (e.g., o valor `-1.0`).
    *   Desenvolver uma estratégia para lidar com os valores ausentes, especialmente em `recent_reviews`, `achievements` e `discount_price_num`, considerando imputação, remoção ou criação de categorias "sem informação".
    *   Implementar um processo de extração de dados numéricos e de sentimento das colunas `recent_reviews` e `all_reviews`.

2.  **Análise de Precificação:**
    *   Aprofundar a análise dos preços originais e de desconto, identificando padrões de precificação, estratégias de desconto e o impacto de outliers.
    *   Segmentar a análise de preços por tipo de jogo (`app`, `bundle`, `sub`) e por desenvolvedor/editora.

3.  **Exploração de Mercado e Tendências:**
    *   Realizar uma análise mais detalhada das `popular_tags` e `genre` para identificar tendências de mercado, nichos promissores e a popularidade de diferentes tipos de jogos.
    *   Analisar a performance de desenvolvedores e editoras com maior número de títulos para entender seus diferenciais e estratégias.

4.  **Engajamento e Conteúdo:**
    *   Investigar a relação entre o número de `achievements` e o engajamento do usuário ou sucesso do jogo, após tratar os valores ausentes.
    *   Analisar a correlação entre a presença de `mature_content` e o desempenho do jogo, se dados suficientes forem recuperados.

Estas recomendações visam aprimorar a qualidade dos dados e direcionar futuras análises para insights mais profundos e acionáveis, suportando decisões estratégicas no ecossistema de jogos Steam.