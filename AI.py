import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# === 1. Ler os arquivos e unir os dados ===
merged_data = pd.read_csv("merged_data.csv")
gpu_specs = pd.read_csv("gpu_specs_v6.csv")

# Padronizar nomes para merge
merged_data["productName"] = merged_data["productName"].str.strip().str.lower()
gpu_specs["productName"] = gpu_specs["productName"].str.strip().str.lower()

# Merge dos datasets
merged_specs = pd.merge(merged_data, gpu_specs, on="productName", how="inner")

# === 2. Tratar dados ausentes e inválidos ===
# Remover valores ausentes críticos
merged_specs = merged_specs.dropna(subset=["Price", "gpuClock", "memSize", "memClock", "releaseYear"])

# Preencher valores ausentes nas colunas numéricas
for col in ["Price", "gpuClock", "memSize", "memClock", "releaseYear"]:
    merged_specs[col] = merged_specs[col].fillna(merged_specs[col].median())

# Remover valores com preço zero ou negativo
merged_specs = merged_specs[merged_specs["Price"] > 0]

# Normalizar preços
scaler = MinMaxScaler()
merged_specs["Price"] = scaler.fit_transform(merged_specs[["Price"]])

# Remover valores infinitos e garantir dados válidos
merged_specs = merged_specs.replace([np.inf, -np.inf], np.nan).dropna()

# === 3. Criar métrica de custo-benefício ===
weights = {"gpuClock": 0.4, "memSize": 0.3, "memClock": 0.2, "releaseYear": 0.1}
merged_specs["performance_score"] = (
    weights["gpuClock"] * merged_specs["gpuClock"] +
    weights["memSize"] * merged_specs["memSize"] +
    weights["memClock"] * merged_specs["memClock"] +
    weights["releaseYear"] * merged_specs["releaseYear"]
)

merged_specs["cost_benefit"] = merged_specs["performance_score"] / merged_specs["Price"]

# Garantir que não há valores inválidos após o cálculo
merged_specs = merged_specs.replace([np.inf, -np.inf], np.nan).dropna(subset=["cost_benefit"])

# Conferir tamanho final
print("Tamanho do dataframe final:", merged_specs.shape)

# === 4. Preparar dados para treinamento ===
features = ["gpuClock", "memSize", "memClock", "releaseYear", "Price"]
target = "cost_benefit"

X = merged_specs[features]
y = merged_specs[target]

# === Verificar integridade dos dados ===
print("Número de registros:", X.shape[0])
print("Valores ausentes nas features:", X.isna().sum())
print("Valores ausentes no target:", y.isna().sum())

# === 5. Dividir os dados ===
if X.shape[0] == 0:
    raise ValueError("Nenhum dado disponível para treinamento. Verifique o processamento dos dados.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === 6. Treinar modelo ===
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Previsões
y_pred = model.predict(X_test)

# Avaliação
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Erro médio quadrático (MSE):", mse)
print("R² (Coeficiente de Determinação):", r2)

# === 7. Classificar GPUs por custo-benefício previsto ===
merged_specs["predicted_cost_benefit"] = model.predict(merged_specs[features])
result = merged_specs.sort_values(by="predicted_cost_benefit", ascending=False)

# Salvar resultado
result.to_csv("gpu_ranking_cost_benefit.csv", index=False)
print("Resultado salvo como 'gpu_ranking_cost_benefit.csv'.")
