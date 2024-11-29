import csv
from selenium import webdriver
import json
import time

# Configurando o WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Para rodar sem abrir o navegador
options.add_argument("--no-sandbox")  # Evita problemas de sandbox
driver = webdriver.Chrome(options=options)

# Caminho para o arquivo CSV de entrada
input_csv_file = 'data/links_coletados.csv'
# Caminho para o arquivo CSV de saída
output_csv_file = 'data/priceHistoryBruto.csv'

# Lista para armazenar os resultados
results = []

try:
    # Lê os links do arquivo CSV de entrada
    with open(input_csv_file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Pula o cabeçalho
        for row in csv_reader:
            if row:  # Ignora linhas vazias
                url = row[0].strip()  # Remove espaços em branco
                print(f"Processando URL: {url}")

                # Valida a URL
                if not (url.startswith("http://") or url.startswith("https://")):
                    print(f"URL inválida: {url}")
                    results.append({"url": url, "prices": None, "error": "Invalid URL"})
                    continue

                # Acessa a página
                driver.get(url)

                # Aguarda o carregamento da página
                time.sleep(5)

                # Extrai o conteúdo da página
                page_source = driver.page_source

                # Busca pela seção "prices" na página
                if "prices" in page_source:
                    start_index = page_source.find('"prices":') + len('"prices":')
                    end_index = page_source.find(']', start_index) + 1
                    prices_data = page_source[start_index:end_index]

                    # Converte o conteúdo para JSON se possível
                    try:
                        prices = json.loads(prices_data)
                        results.append({"url": url, "prices": prices, "error": None})
                        print(f"Preços encontrados para {url}: {prices}")
                    except json.JSONDecodeError:
                        print(f"Erro ao decodificar os preços em {url}: {prices_data}")
                        results.append({"url": url, "prices": None, "error": "JSONDecodeError"})
                else:
                    print(f"A seção 'prices' não foi encontrada na página: {url}")
                    results.append({"url": url, "prices": None, "error": "Prices not found"})

finally:
    # Encerra o WebDriver
    driver.quit()

# Salva os resultados em um arquivo CSV organizado
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['URL', 'Prices', 'Error']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Escreve o cabeçalho
    writer.writeheader()

    # Escreve os dados
    for result in results:
        writer.writerow({
            'URL': result['url'],
            'Prices': json.dumps(result['prices'], ensure_ascii=False) if result['prices'] else '',
            'Error': result['error'] if result['error'] else ''
        })

print(f"Resultados salvos em {output_csv_file}")
