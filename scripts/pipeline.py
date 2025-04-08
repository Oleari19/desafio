import pandas as pd
from collections import Counter
import os

# ----------------------------
# Função: carregar_dados
# Objetivo: Carrega os três arquivos CSV de entrada contendo os dados já tratados
# Parâmetros:
#   - transactional_path: caminho para o arquivo de dados transacionais tratados
#   - exams_path: caminho para o arquivo de dados de exames tratados
#   - demographic_path: caminho para o arquivo de dados demográficos tratados
# Retorno:
#   - três DataFrames (transacional, exames, demográfico)
# ----------------------------
def carregar_dados(transactional_path, exams_path, demographic_path):
    df_transactional = pd.read_csv(transactional_path)
    df_exams = pd.read_csv(exams_path)
    df_demographic = pd.read_csv(demographic_path)
    return df_transactional, df_exams, df_demographic


# ----------------------------
# Função: tratar_dados
# Objetivo: Realiza a junção dos dados transacionais e de exames, calculando a receita líquida por transação
# Parâmetros:
#   - df_transactional: DataFrame com dados transacionais
#   - df_exams: DataFrame com dados de exames
# Retorno:
#   - df_merge: DataFrame mesclado contendo informações de custo e receita líquida
# ----------------------------
def tratar_dados(df_transactional, df_exams):
    df_transactional['Testing Cost'] = df_transactional['Testing Cost'].astype(float)
    df_exams['Testing Cost'] = df_exams['Testing Cost'].astype(float)

    df_transactional = df_transactional.rename(columns={'Testing Cost': 'Patient_Price'})
    df_exams = df_exams.rename(columns={'Testing Cost': 'Exam_Cost'})

    df_merge = pd.merge(
        df_transactional,
        df_exams[['CodItem', 'Desc Item', 'Exam_Cost']],
        on='CodItem',
        how='inner'
    )

    df_merge['Net_Revenue'] = df_merge['Patient_Price'] - df_merge['Exam_Cost']
    return df_merge


# ----------------------------
# Função: gerar_resumo
# Objetivo: Agrupa os dados por exame e calcula métricas resumidas como média de preço e receita líquida
# Parâmetros:
#   - df_merge: DataFrame mesclado com dados de transações e exames
# Retorno:
#   - df_summary: DataFrame com resumo estatístico por CodItem
# ----------------------------
def gerar_resumo(df_merge):
    df_summary = df_merge.groupby('CodItem').agg(
        Exam_Cost=('Exam_Cost', 'mean'),
        Patient_Price=('Patient_Price', 'mean'),
        Net_Revenue=('Net_Revenue', 'mean'),
        Total_Transactions=('Net_Revenue', 'count'),
        Total_Net_Revenue=('Net_Revenue', 'sum')
    ).reset_index()

    df_summary[['Exam_Cost', 'Patient_Price', 'Net_Revenue', 'Total_Net_Revenue']] = df_summary[[
        'Exam_Cost', 'Patient_Price', 'Net_Revenue', 'Total_Net_Revenue'
    ]].round(2)

    return df_summary


# ----------------------------
# Função auxiliar: top_3_ages
# Objetivo: Retorna as 3 idades mais frequentes de um conjunto de valores
# Parâmetros:
#   - age_series: coluna de idades
# Retorno:
#   - string com as 3 idades mais comuns separadas por vírgula
# ----------------------------
def top_3_ages(age_series):
    counter = Counter(age_series.dropna())
    top3 = counter.most_common(3)
    return ', '.join([f'{int(age)}' for age, _ in top3])


# ----------------------------
# Função: analisar_idades
# Objetivo: Gera as 3 idades mais comuns por exame para os 30 com maior receita líquida
# Parâmetros:
#   - df_merge: DataFrame com dados mesclados de exames
#   - df_summary: DataFrame com resumo estatístico
#   - top_n: número de exames a considerar (padrão: 30)
# Retorno:
#   - df_final_exams: DataFrame contendo resumo + top 3 idades para os exames mais lucrativos
# ----------------------------
def analisar_idades(df_merge, df_summary, top_n=30):
    top_coditems = df_summary.sort_values(by='Total_Net_Revenue', ascending=False)['CodItem'].head(top_n)
    df_top = df_merge[df_merge['CodItem'].isin(top_coditems)]

    df_ages = df_top.groupby('CodItem').agg(
        Top_3_Ages=('Age at service', top_3_ages)
    ).reset_index()

    df_final_exams = pd.merge(
        df_summary[df_summary['CodItem'].isin(top_coditems)],
        df_ages,
        on='CodItem',
        how='inner'
    )

    return df_final_exams


# ----------------------------
# Função: analisar_demografia
# Objetivo: Calcula a porcentagem de 3 faixas etárias específicas com base na população total
# Parâmetros:
#   - df_demographic: DataFrame com dados demográficos
# Retorno:
#   - df_faixas: DataFrame com as porcentagens calculadas e arredondadas
# ----------------------------
def analisar_demografia(df_demographic):
    faixas_desejadas = [
        'Population_25to34Years',
        'Population_55to59Years',
        'Population_45to54Years'
    ]
    colunas_necessarias = ['GeographicAreaName', 'TotalPopulation'] + faixas_desejadas
    df_faixas = df_demographic[colunas_necessarias].copy()

    for faixa in faixas_desejadas:
        df_faixas[faixa + '_%'] = (df_faixas[faixa] / df_faixas['TotalPopulation']) * 100

    df_faixas = df_faixas.rename(columns={
        'GeographicAreaName': 'ZCTA',
        'Population_25to34Years_%': '25to34Years (%)',
        'Population_55to59Years_%': '55to59Years (%)',
        'Population_45to54Years_%': '45to54Years (%)'
    })

    df_faixas[['25to34Years (%)', '55to59Years (%)', '45to54Years (%)']] = df_faixas[
        ['25to34Years (%)', '55to59Years (%)', '45to54Years (%)']
    ].round(1)

    return df_faixas


# ----------------------------
# Função: salvar_saidas
# Objetivo: Exporta os resultados finais em arquivos CSV
# Parâmetros:
#   - df_final_exams: DataFrame com análises por exame
#   - df_faixas: DataFrame com análises demográficas
#   - output_dir: pasta de saída (padrão: ../data)
# ----------------------------
def salvar_saidas(df_final_exams, df_faixas, output_dir='../data'):
    os.makedirs(output_dir, exist_ok=True)
    df_final_exams.to_csv(os.path.join(output_dir, 'final_analytical_exams.csv'), index=False)
    df_faixas.to_csv(os.path.join(output_dir, 'final_analytical_demographic.csv'), index=False)


# ----------------------------
# Função principal do pipeline
# Objetivo: Executa todo o fluxo de ETL (extração, transformação e carga)
# ----------------------------
def main():
    transactional_path = '../data/transactional_treated.csv'
    exams_path = '../data/exams_treated.csv'
    demographic_path = '../data/demographic_treated.csv'

    df_transactional, df_exams, df_demographic = carregar_dados(transactional_path, exams_path, demographic_path)
    df_merge = tratar_dados(df_transactional, df_exams)
    df_summary = gerar_resumo(df_merge)
    df_final_exams = analisar_idades(df_merge, df_summary)
    df_faixas = analisar_demografia(df_demographic)
    salvar_saidas(df_final_exams, df_faixas)


# Permite rodar o script diretamente (automatização)
if __name__ == "__main__":
    main()
