import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def train_model(data):
    """
    Entrena un modelo Isolation Forest y devuelve el modelo junto con el escalador.
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(scaled_data)

    return model, scaler

def detect_anomalies(model, scaler, data):
    """
    Detecta anomalías usando el modelo Y el escalador correspondientes.
    """
    # CORRECCIÓN: Ahora recibimos 'scaler' como argumento
    scaled_data = scaler.transform(data)
    predictions = model.predict(scaled_data)

    return predictions

def process_transactions(transactions):
    """
    Orquestador del flujo de datos.
    """
    # Definimos nombres de columnas para evitar warnings
    df = pd.DataFrame(transactions, columns=['monto', 'latencia'])

    # Obtenemos ambos objetos
    model, scaler = train_model(df)

    # Pasamos ambos objetos a la función de detección
    predictions = detect_anomalies(model, scaler, df)

    return predictions

# --- EJECUCIÓN ---
if __name__ == "__main__":
    transactions_data = [
        [100.5, 200.3],
        [98.4, 197.6],
        [5000.0, 10.1], # Posible anomalía
    ]

    print("🚀 Procesando transacciones en Vertex Services...")
    predictions = process_transactions(transactions_data)

    for i, prediction in enumerate(predictions):
        estado = "ANÓMALA ⚠️" if prediction == -1 else "NORMAL ✅"
        print(f"Transacción {i+1}: {estado}")