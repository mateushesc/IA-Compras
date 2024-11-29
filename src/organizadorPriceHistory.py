import pandas as pd
import json

def extract_prices(data):
    rows = []
    for _, row in data.iterrows():
        url = row['URL']
        try:
            prices_list = json.loads(row['Prices'].replace("'", '"'))  # Corrigir aspas para JSON válido
            for entry in prices_list:
                rows.append({
                    'URL': url,
                    'Date': entry['date'],
                    'Price': entry['price']
                })
        except (json.JSONDecodeError, TypeError):
            continue  # Ignorar linhas com erros de parsing
    return pd.DataFrame(rows)

# Carregar o arquivo original
file_path = 'data/priceHistoryBruto.csv'  # Substitua pelo caminho correto
data = pd.read_csv(file_path)

# Extrair e organizar os dados
structured_data = extract_prices(data)

# Salvar o resultado em um arquivo CSV
output_path = 'data/priceHistoryOrganizado.csv'
structured_data.to_csv(output_path, index=False)

print(f"Arquivo organizado salvo em: {output_path}")
