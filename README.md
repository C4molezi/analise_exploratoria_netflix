# Data Analysis & Exploratory Insights: Netflix Titles Dataset

Este repositório contém uma análise exploratória de dados (EDA) minuciosa do conjunto de dados de títulos da Netflix, cobrindo o acervo histórico até setembro de 2021. O estudo investiga padrões de aquisição de conteúdo, composição de catálogo, distribuição geográfica e tendências temporais por meio de métricas estatísticas calculadas em Python.

---

## Stack Tecnológica & Métodos
* **Python 3.x**
* **Pandas**: Manipulação de *dataframes*, parsing de datas, vetorização de operações e explosão de listas contidas em dados não estruturados (`explode()`).
* **NumPy**: Separação de arrays, operações aritméticas e cômputo de estatísticas descritivas (média e mediana).
* **Matplotlib & Seaborn**: Construção do *pipeline* de visualização estatística e gráficos descritivos.

---

## Relatório Técnico de Insights Extraídos

### 1. Composição e Proporção Mídia (Filmes vs. Séries)
* **Dataset Size:** 8.807 registros totais (`Movie`: 6.131; `TV Show`: 2.676).
* **Distribuição:** O catálogo é predominantemente composto por **Filmes (69,62%)**, enquanto **Séries de TV representam 30,38%**.
* **Diagnóstico:** Indica uma estratégia baseada no alto volume de obras autocontidas (*long-tail content*), equilibrada por séries voltadas à retenção e *engagement* continuado do usuário (*recurring retention assets*).

### 2. Concentração Geográfica de Produções
* **Top Produtores Solos/Principais:** Estados Unidos (3.689), Índia (1.046), Reino Unido (804), Canadá (445) e França (393).
* **Análise:** Observa-se uma assimetria severa e dominância da indústria audiovisual anglófona/norte-americana, acompanhada por um ecossistema expressivo da Índia (foco em *Bollywood*) para atendimento a mercados regionais específicos.

### 3. Dinâmica Temporal de Incorporação ao Catálogo
* **Janela Temporal Relevante:** Aceleração substancial a partir de **2016** (429 adições), atingindo o ápice em **2019** (2.016 adições) e mantendo patamares elevados nos anos subsequentes (2020: 1.879; 2021: 1.498).
* **Análise de Tendência:** Evidencia o período de investimentos massivos em expansão global de infraestrutura e catalogação para fortalecimento do modelo de streaming por assinatura (SVOD).

### 4. *Lag* de Ingestão de Conteúdo (*Release-to-Platform Latency*)
* **Média Movel de Diferença (`year_added` - `release_year`):** 4,70 anos.
* **Mediana:** 1,00 ano.
* **Diagnóstico de Assimetria (*Skewness*):** A assimetria à direita (Média > Mediana) demonstra que, enquanto a maioria esmagadora do conteúdo entra no catálogo no ano de lançamento ou até 1 ano após, o cálculo médio é puxado por um volume residual de conteúdos clássicos/históricos adicionados tardiamente.

### 5. Taxonomia e Granularidade por Gênero
* **Gêneros Liderança:** *International Movies* (2.752), *Dramas* (2.427), *Comedies* (1.674) e *International TV Shows* (1.351).
* **Insight:** A forte presença da tag *International* reflete o investimento na regionalização e localização do conteúdo (*globalization through local IP*), crucial para a penetração em mercados fora do eixo Anglo-Americano.

### 6. Perfil Demográfico da Audiência (*Rating Mapping*)
* **Dominância:** A classificação **TV-MA** (*Mature Audience*) lidera de forma destacada com 3.207 títulos (~36,4%), seguida por **TV-14** (2.160 títulos) e **TV-PG** (863 títulos).
* **Conclusão:** O portfólio da plataforma tem como foco principal o público jovem-adulto e adulto, direcionando estratégias de aquisição para narrativas de complexidade temática elevada.

### 7. Tendência Volumétrica de Duração Cinematográfica
* **Duração Média dos Filmes:** 99,58 minutos (DP reduzido em produções recentes).
* **Evolução Histórica:** Filmes do século XX demonstram variações mais acentuadas de duração por limitação técnica e formatos de exibição clássicos. Filmes pós-2000 convergentemente estabilizam-se na faixa entre 90 e 105 minutos.

### 8. Estrutura de Temporadas e Ciclo de Vida de Séries
* **Média de Temporadas:** 1,76 temporadas por série.
* **Taxa de Renovação:** **67,00%** das séries de TV possuem apenas **1 temporada** registrada no catálogo.
* **Diagnóstico:** Reflete um alto volume de minisséries (*limited series*) ou um *turnover* agressivo no cancelamento de produções originais não performáticas na métrica de retenção inicial.

### 9. Concentração por Direção Cinematográfica
* **Maior Densidade:** Diretores como *Rajiv Chilaka* (22 títulos), *Jan Suter* (21 títulos) e *Raúl Campos* (19 títulos) figuram no topo.
* **Análise de Portfólio:** A presença no topo é impulsionada por coleções/franquias de filmes animados infantis ou especiais de comédia (*stand-ups*), que possuem produção recorrente de baixo custo relativo.

### 10. Topologia de Coproduções Transnacionais
* **Padrões de Parceria:** Estados Unidos & Reino Unido (75), Estados Unidos & Canadá (73), França & Bélgica (27).
* **Diagnóstico Econômico:** Evidencia o uso de incentivos fiscais internacionais, *hubs* de efeitos visuais/pós-produção e alianças estratégicas de financiamento transfronteiriço no audiovisual.

---

## Como Executar o Script de Análise

1. Certifique-se de possuir o arquivo `netflix_titles.csv` no diretório raiz do projeto.
2. Instale as dependências requeridas:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```
3. Execute o script Python contendo o código de análise:
   ```bash
   python main.py
   ```
