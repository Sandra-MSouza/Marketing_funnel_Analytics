import pandas as pd

# 1. Carregar o arquivo CSV de forma robusta, tratando a formatação com aspas
try:
    # Passo A: Ler o arquivo como se tivesse uma única coluna, sem cabeçalho
    df_raw = pd.read_csv('marketing_funnel.csv', header=None)
    print("Arquivo 'marketing_funnel.csv' carregado em modo bruto.")

    # Passo B: Pegar a primeira linha (índice 0) e quebrar a string do cabeçalho pela vírgula
    column_names = df_raw.iloc[0, 0].split(',')

    # Passo C: Pegar apenas os dados (da segunda linha em diante)
    data = df_raw.iloc[1:].copy()

    # Passo D: Dividir a única coluna de dados em múltiplas colunas
    df_split = data[0].str.split(',', expand=True)

    # Passo E: Criar o DataFrame final, juntando os dados separados com os nomes das colunas
    df = pd.DataFrame(df_split.values, columns=column_names)

    print("Dados separados em colunas com sucesso!")

except FileNotFoundError:
    print("Erro: O arquivo 'marketing_funnel.csv' não foi encontrado.")
    exit()
except Exception as e:
    print(f"Ocorreu um erro inesperado ao processar o CSV: {e}")
    exit()


# 2. DIAGNÓSTICO E LIMPEZA DOS NOMES DAS COLUNAS
print("Nomes das colunas lidas:", df.columns.tolist())
df.columns = df.columns.str.strip() # Remove espaços em branco (boa prática)


# 3. Limpeza e Transformação dos Dados (Esta parte permanece a mesma)

# Converter a coluna 'date' para o formato de data (datetime)
# Agora esta linha VAI funcionar!
df['date'] = pd.to_datetime(df['date'])

# Garantir que as colunas numéricas tenham o tipo de dado correto
numeric_cols = ['impressions', 'clicks', 'cost', 'leads', 'mql', 'sql', 'customers', 'revenue']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.fillna(0, inplace=True)


# 4. Engenharia de Features: Criar novas métricas (KPIs)
df['cpc'] = df.apply(lambda row: row['cost'] / row['clicks'] if row['clicks'] > 0 else 0, axis=1)
df['ctr'] = df.apply(lambda row: row['clicks'] / row['impressions'] if row['impressions'] > 0 else 0, axis=1)
df['cpl'] = df.apply(lambda row: row['cost'] / row['leads'] if row['leads'] > 0 else 0, axis=1)
df['conversion_rate'] = df.apply(lambda row: row['leads'] / row['clicks'] if row['clicks'] > 0 else 0, axis=1)


# 5. Exibir as primeiras linhas do DataFrame transformado
print("\nTabela de dados após a limpeza e com as novas métricas:")
print(df.head())

# 6. Salvar o resultado em um novo arquivo CSV
output_filename = 'marketing_funnel_analyzed.csv'
df.to_csv(output_filename, index=False, decimal='.')
print(f"\nDados processados foram salvos com sucesso no arquivo: '{output_filename}'")
