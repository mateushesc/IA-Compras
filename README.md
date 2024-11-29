# Previsão de Preços de Produtos com Regressão Linear

Este repositório contém um script em Python para realizar análises de séries temporais e prever preços futuros de produtos com base em dados históricos. O código utiliza bibliotecas populares como `pandas`, `numpy`, `sklearn` e `matplotlib`.

## Funcionalidades

- **Carregamento e limpeza de dados:** Carrega um arquivo CSV contendo dados históricos de preços e realiza a limpeza dos dados.
- **Seleção de produtos:** Permite ao usuário selecionar um produto com dados suficientes para análise.
- **Treinamento de modelo de regressão linear:** Treina um modelo usando os dados históricos.
- **Métricas de avaliação:** Calcula e exibe métricas como MAE, RMSE e MAPE para avaliar o modelo.
- **Previsão de preços futuros:** Faz previsões para os próximos quatro meses com base no modelo treinado.
- **Visualização:** Gera gráficos para ilustrar os preços históricos, valores previstos e projeções futuras.

## Requisitos

Antes de executar o script, certifique-se de ter as seguintes bibliotecas instaladas:

- pandas
- numpy
- scikit-learn
- matplotlib

Você pode instalá-las com o comando:

```bash
pip install pandas numpy scikit-learn matplotlib
```

## Estrutura dos Dados

O arquivo CSV deve conter as seguintes colunas:

- **Date:** Data dos registros (formato `YYYY-MM-DD`).
- **Price:** Preço do produto.
- **URL:** Identificador único do produto (por exemplo, link do produto).

## Como Usar

1. Coloque o arquivo CSV com os dados históricos na mesma pasta do script e renomeie-o para `merged_data.csv`.
2. Execute o script.
3. Escolha um produto da lista exibida no console.
4. O script exibirá métricas de avaliação, previsões futuras e um gráfico dos preços.

## Saídas do Script

### Métricas de Avaliação do Modelo

- **Erro Absoluto Médio (MAE):** Média dos erros absolutos.
- **Raiz do Erro Quadrático Médio (RMSE):** Raiz quadrada do erro médio quadrático.
- **Erro Percentual Médio Absoluto (MAPE):** Erro médio percentual em relação aos valores reais.

### Tabela de Previsões Futuras

Mostra os preços previstos para os próximos quatro meses.

### Gráfico

Exibe:
- **Preços históricos.**
- **Valores previstos para os dados de teste.**
- **Projeções de preços futuros.**

(Não será explicado sobre as outras partes do código, pois até esse momento, não são o foco.)
