import requests
from bs4 import BeautifulSoup
import csv

# URL base do site
base_url = "https://placasdevideo.com"
page_url_template = "https://placasdevideo.com/page/{page}?hoje=true"
exclude_links = [
    "/",
    "https://www.instagram.com/placasdevideocom",
    "https://twitter.com/Xplacasdevideo",
    "https://t.me/placasdevideo",
    "https://placasdevideo.com/"  # Excluir link vazio ou raiz do site
]

def get_links_from_page(url, exclude_links):
    """Obtém todos os links válidos de uma página específica."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Adiciona base_url a links relativos
            full_link = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")
            # Exclui links indesejados ou vazios
            if full_link not in exclude_links and full_link != base_url + "/":
                links.append(full_link)

        return links
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página {url}: {e}")
        return []

# Percorre todas as páginas
all_links = set()
page_number = 1

while True:
    current_page_url = page_url_template.format(page=page_number)
    print(f"Acessando: {current_page_url}")
    
    # Obtém os links da página atual
    links = get_links_from_page(current_page_url, exclude_links)
    
    # Interrompe se a página não tiver novos links
    if not links:
        print("Fim das páginas alcançado ou página sem links.")
        break
    
    # Adiciona os links encontrados à coleção de todos os links
    initial_size = len(all_links)
    all_links.update(links)
    
    # Se nenhum link novo foi adicionado, encerra o loop
    if len(all_links) == initial_size:
        print("Nenhum link novo encontrado nesta página. Parando a busca.")
        break

    page_number += 1

# Salva os links em um arquivo CSV
csv_file = "links_coletados.csv"
try:
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Links"])  # Cabeçalho do CSV
        for link in sorted(all_links):
            writer.writerow([link])
    print(f"\nLinks salvos com sucesso no arquivo: {csv_file}")
except Exception as e:
    print(f"Erro ao salvar os links no arquivo CSV: {e}")
