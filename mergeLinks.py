import pandas as pd

# Caminhos dos arquivos
price_history_path = 'priceHistoryOrganizado.csv'
links_coletados_path = 'links_coletados_mais_placas.csv'

# Ler os arquivos CSV
price_history_df = pd.read_csv(price_history_path)
links_coletados_df = pd.read_csv(links_coletados_path)

# Renomear a coluna 'Links' no segundo DataFrame para 'URL' para facilitar a união
links_coletados_df.rename(columns={'Links': 'URL'}, inplace=True)

# Realizar a junção dos DataFrames com base na coluna 'URL'
merged_df = pd.merge(price_history_df, links_coletados_df, on='URL', how='inner')

# Salvar o resultado em um novo arquivo CSV
merged_df.to_csv('merged_data.csv', index=False)

print("Os dados foram unidos e salvos no arquivo 'merged_data.csv'.")
