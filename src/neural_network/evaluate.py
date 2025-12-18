import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from pathlib import Path

MODEL_PATH = Path("neural_network/mlp_trip_fuel_model.joblib")
HISTORY_PATH = Path("training_history.csv")

def evaluate_project():
    print("--- Evaluare Model Predictie Consum ---")
    
    if HISTORY_PATH.exists():
        history = pd.read_csv(HISTORY_PATH)
        epochs_run = len(history)
        final_loss = history['loss'].iloc[-1]
        print(f"-> Modelul s-a antrenat timp de {epochs_run} epoci.")
        print(f"-> Loss final (MSE): {final_loss:.6f}")
    else:
        print("Nu s-a găsit training_history.csv!")


    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)

        print(f"-> Arhitectura straturi: {model.hidden_layer_sizes}")
        print(f"-> Functie activare: {model.activation}")
        print(f"-> Batch size: {model.batch_size}")
    else:
        print("Nu s-a găsit modelul salvat!")

if __name__ == "__main__":
    evaluate_project()