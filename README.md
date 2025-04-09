# Desafio: Expansão Estratégica de Laboratórios

## Objetivo

Identificar as **3 regiões mais promissoras** para a instalação de novos laboratórios, com base em dados:
- Econômicos
- Demográficos
- Geocodificados
- Transacionais
- Dos exames


## Estrutura do Projeto

```
desafio/
│
├── data/                    # Bases de dados originais, tratadas e analíticas
│   ├── transactional_treated.csv
│   ├── ...
│   └── .csv
│
├── notebooks/               # Notebooks de sanity check e análise exploratória
│   ├── 01_demographic_sanity.ipynb
│   ├── 02_geocode_sanity.ipynb
│   ├── 03_economic_sanity.ipynb
│   ├── 04_exams_sanity.ipynb
│   ├── 05_transactional_sanity.ipynb
│   └── 06_final_analysis.ipynb
│
├── presentation/            # Slides de apresentação
│   └── .pdf
│
├── scripts/                 # Scripts do projeto
│   └── pipeline.py
│
├── README.md                # Este guia
│
└── requirements.txt         # Bibliotecas necessárias
```


## Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Oleari19/desafio.git
cd desafio
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

> Inclui bibliotecas como `pandas`, `matplotlib`, `seaborn`, `jupyter`.

### 3. Dados

Dois arquivos de dados utilizados neste projeto são muito grandes para serem armazenados no GitHub. Por isso, **não estão inclusos no repositório**.

Você pode baixar os dados manualmente pelos links abaixo e colocá-los na pasta `data/` do projeto:

- [`transactional_data.csv`](https://drive.google.com/drive/folders/1kxSRQKKmgQ-6XDxC0c87J0SMR9TFpTY3?usp=drive_link)
- [`transactional_treated.csv`](https://drive.google.com/drive/folders/1kxSRQKKmgQ-6XDxC0c87J0SMR9TFpTY3?usp=drive_link)
  

### 4. Execute os notebooks

Abra os notebooks em `notebooks/` com Jupyter ou VS Code para rodar os sanity checks e a análise final na ordem enumerada.

Veja um resumo do que cada um faz:

- **01_demographic_sanity.ipynb**
  Analisa a composição etária da população por região, incluindo indicadores como:
  - População total e por faixa etária;
  - Mediana da idade;
  - Proporção de homens para cada 100 mulheres;
  - Indicadores de envelhecimento populacional e concentração de jovens.

- **02_geocode_sanity.ipynb**  
  Verifica a integridade dos dados de localização e geocodificação. Filtra valores inconsistentes ou ausentes.

- **03_economic_sanity.ipynb**  
  Analisa a receita líquida por região (ZCTA), identifica outliers e consolida a base econômica.

- **04_exams_sanity.ipynb**  
  Trata e verifica a consistência nos dados de exames, separando tipos, volumes e datas.

- **05_transactional_sanity.ipynb**  
  Realiza análise dos dados transacionais, relacionando-os com exames, receitas e padrões de utilização.

> Antes de executar o notebook 06 execute o passo 4

- **06_final_analysis.ipynb**  
  Consolida todas as bases tratadas (econômica, exames, demográfica e transacional), realiza cruzamentos e gera os **insights finais**, incluindo a seleção das **3 regiões mais promissoras**.


### 5. Execute o pipeline completo

```bash
cd scripts
python pipeline.py
```

O script irá:
- Ler dados tratados: Importa dados transacionais, de exames e demográficos (arquivos CSV).
- Calcular receita líquida: Une os dados de transações e exames, e calcula a receita líquida por exame.
- Gerar resumo: Produz um resumo por exame com métricas como custo médio, preço médio, receita líquida média e total.
- Analisar idade: Para os 30 exames mais lucrativos, identifica as 3 idades mais frequentes entre os pacientes.
- Analisar a parte demográfica: Para cada área geográfica (ZCTA), calcula a porcentagem de três faixas etárias específicas na população.
- Exportar os resultados: Os resultados são salvos como arquivos CSV na pasta data.


Na pasta `data/`, serão salvos:

- `final_analytical_exams.csv` – Base analítica com dados transacionais e de exames.
- `final_analytical_demographic.csv` – Base analítica com dados demográficos enxutos.

> Após o salvamento das bases analíticas execute o notebook 06_final_analysis.ipynb


## Etapas Realizadas

1. Carregamento das 5 bases de dados fornecidas
2. Criação do notebook 01
    - Entendimento da base de dados demográficos
    - Tratamento dos dados nulos da base
    - Análises exploratórias
    - Hipótese individual sobre a base em questão
3. Criação do notebook 02
    - Entendimento da base de dados geográficos
    - Tratamento dos dados nulos da base
    - Análises exploratórias
    - Hipótese individual sobre a base em questão
4. Criação do notebook 03
    - Entendimento da base de dados econômicos
    - Análises exploratórias
    - Hipótese individual sobre a base em questão
5. Criação do notebook 04
    - Entendimento da base de dados dos exames
    - Análises exploratórias
    - Hipótese individual sobre a base em questão
6. Criação do notebook 05
    - Entendimento da base de dados transacionais
    - Tratamento dos dados separando-os em colunas
    - Qualidade
    - Análises exploratórias
    - Hipótese individual sobre a base em questão
7. Criação do pipeline e das bases analíticas
8. Criação do notebook 06
    - Confirmação da base analítica
    - Todas as hipóteses levantadas
    - Hipótese escolhida
    - Passo a passo explicativo até chegar a conclusão final
    - Conclusão final e justificativa
9. Requirements.txt
10. README.md
11. Apresentação final no Canva 
- Introdução e objetivo
- Metodologia utilizada e limitações
- Análises exploratórias que auxiliaram na decisão final
- Hipótese final com destaque das 3 ZCTAs escolhidas.
- Justificativa clara e direta para apoio à **expansão estratégica dos laboratórios**.


## Recomendação Final

As **3 ZCTAs ideais para expansão** foram:

- **77449** – Essa região tem a maior população dentre as filtradas, o que representa um grande potencial de demanda. Além disso, 14,9% da população está na faixa de 25 a 34 anos, que é a mais recorrente nos exames que geram maior receita líquida. Ou seja, tem volume e perfil demográfico alinhado com os exames mais lucrativos.

- **79936** – Com mais de 110 mil habitantes e 15,1% da população na faixa de 25 a 34 anos, essa região une alto volume populacional com uma forte presença da faixa etária que mais realiza os exames de maior rentabilidade. É uma região estratégica por ter um perfil populacional muito alinhado com o público-alvo dos exames mais lucrativos.

- **11385** – Apesar de ter uma população um pouco menor que as outras duas, se destaca por ter a maior concentração proporcional da faixa etária 25–34 anos. Como essa é a faixa que mais consome os exames com maior lucro, essa ZCTA é altamente qualificada em termos de público-alvo, representando um ótimo retorno em potencial.
