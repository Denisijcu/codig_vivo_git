from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

app = Flask(__name__)


def create_model():
    """
    Define y compila el modelo de aprendizaje automático.
    """
    model = Sequential([
        Dense(128, activation='relu', input_shape=(50,)),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    return model


# Crear modelo
model = create_model()


@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint de predicción.
    Espera JSON con formato:
    {
        "features": [50 valores numéricos]
    }
    """
    try:
        data = request.get_json()

        if not data or "features" not in data:
            return jsonify({"error": "Debe enviar 'features' con 50 valores"}), 400

        features = data["features"]

        if not isinstance(features, list) or len(features) != 50:
            return jsonify({"error": "La lista debe contener exactamente 50 valores"}), 400

        # Convertir a numpy
        input_array = np.array(features, dtype=np.float32).reshape(1, 50)

        prediction = model.predict(input_array)

        return jsonify({
            "prediction": float(prediction[0][0])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)