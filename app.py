import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

file_path = 'data/merged_data.csv'
data = pd.read_csv(file_path)

data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
data_cleaned = data.dropna(subset=['Date', 'Price']).sort_values(by='Date')

min_data_points = 10
valid_links = [
    link for link in data_cleaned['URL'].unique()
    if len(data_cleaned[data_cleaned['URL'] == link]) >= min_data_points
]

if not valid_links:
    print("Nenhum produto com dados suficientes foi encontrado.")
else:
    print("Escolha um produto pelo número correspondente ao link:")
    for i, link in enumerate(valid_links):
        print(f"{i}: {link}")

    selected_index = int(input("Digite o número do produto: "))
    selected_link = valid_links[selected_index]
    print(f"Produto selecionado: {selected_link}")

    product_data = data_cleaned[data_cleaned['URL'] == selected_link]

    product_data['Year'] = product_data['Date'].dt.year
    product_data['Month'] = product_data['Date'].dt.month
    product_data['Day'] = product_data['Date'].dt.day

    model_data = product_data[['Year', 'Month', 'Day', 'Price']]

    X = model_data[['Year', 'Month', 'Day']]
    y = model_data['Price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    print(f"\nErro Absoluto Médio (MAE): {mae:.2f}")
    print(f"Raiz do Erro Quadrático Médio (RMSE): {rmse:.2f}")
    print(f"Erro Percentual Médio Absoluto (MAPE): {mape:.2f}%")

    last_date = product_data['Date'].max()
    future_dates = pd.date_range(start=last_date, periods=5, freq='MS')[1:]

    future_data = pd.DataFrame({
        'Year': future_dates.year,
        'Month': future_dates.month,
        'Day': future_dates.day
    })

    future_data['Predicted_Price'] = model.predict(future_data)

    print("\nPrevisões para os próximos 4 meses:")
    print(future_data[['Year', 'Month', 'Predicted_Price']])

    # Conectando as datas dos testes com os valores reais e previstos
    test_dates = pd.to_datetime({
        'year': X_test['Year'],
        'month': X_test['Month'],
        'day': X_test['Day']
    })

    plt.figure(figsize=(10, 6))
    plt.plot(product_data['Date'], product_data['Price'], label='Preços Históricos', marker='o')
    plt.scatter(test_dates, y_test, label='Valores Reais (Teste)', color='blue', marker='o')
    plt.scatter(test_dates, y_pred, label='Valores Previstos (Teste)', color='orange', marker='x')
    plt.plot(future_dates, future_data['Predicted_Price'], label='Previsões Futuras', marker='x', linestyle='--', color='red')
    plt.title(f'Previsões de Preços - Produto: {selected_link}')
    plt.xlabel('Data')
    plt.ylabel('Preço')
    plt.legend()
    plt.grid()
    plt.show()
