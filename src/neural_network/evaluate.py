import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from pathlib import Path

MODEL_PATH = Path("models/mlp_trip_fuel_model.joblib")
HISTORY_PATH = Path("training_history.csv")
TEST_DATA = Path("data/test/test_samples.csv")

#Date despre model 
def evalueazamil():
    print("Evaluare Model Predictie Consum")
    
    if HISTORY_PATH.exists():
        history = pd.read_csv(HISTORY_PATH)
        epochs_run = len(history)
        final_loss = history['loss'].iloc[-1]
        print(f"-> Modelul s-a antrenat timp de {epochs_run} epoci.")
        print(f"-> Loss final (MSE): {final_loss:.6f}")
    else:
        print("Nu s-a gasit training_history.csv!")


    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)

        print(f"-> Arhitectura straturi: {model.hidden_layer_sizes}")
        print(f"-> Functie activare: {model.activation}")
        print(f"-> Batch size: {model.batch_size}")
    else:
        print("Nu s-a gasit modelul salvat!")

    #Top 5 erori
    df_test = pd.read_csv(TEST_DATA)
    X_test = df_test.iloc[:, :-1]
    y_true = df_test.iloc[:, -1]

    y_pred = model.predict(X_test)

    analysis_df = X_test.copy()
    analysis_df['Real'] = y_true
    analysis_df['Prezis'] = y_pred
    analysis_df['Eroare Absoluta'] = abs(y_true - y_pred)

    top_5 = analysis_df.sort_values(by='Eroare Absoluta', ascending=False).head(5)

    print("\n" + "="*50)
    print("ANALIZA TOP 5 ERORI PENTRU DOCUMENTATIE")
    print("="*50)
    print(top_5[['Real', 'Prezis', 'Eroare Absoluta']])
    print("="*50)
    
    top_5.to_csv('data/top_5_errors_analysis.csv', index=True)

if __name__ == "__main__":
    evalueazamil()