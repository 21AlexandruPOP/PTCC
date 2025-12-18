
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import joblib
from pathlib import Path

THIS_FILE = Path(__file__).resolve()              
NEURAL_NETWORK_DIR = THIS_FILE.parent            
PROJECT_ROOT = NEURAL_NETWORK_DIR.parent.parent  
DATA_DIR = PROJECT_ROOT / "data" / "generated"


CSV_FILES = [
    DATA_DIR / "generated_trips.csv",
    DATA_DIR / "generated_trips2.csv",
    DATA_DIR / "generated_trips3.csv",
    DATA_DIR / "generated_trips4.csv",
]

print("[DEBUG] Script location:", THIS_FILE)
print("[DEBUG] Data dir:", DATA_DIR)

for f in CSV_FILES:
    print(f"[DEBUG] Exista {f.name}? ->", f.exists())


def main():
    dfs = []
    for f in CSV_FILES:
        if not f.exists():
            raise FileNotFoundError(f"NOT FOUND: {f}")
        print(f"[INFO] Loading {f} ...")
        dfs.append(pd.read_csv(f))

    df = pd.concat(dfs, ignore_index=True)
    print(f"[INFO] Numar total de inregistrari (combinat): {len(df)}")
    print("[INFO] Primele randuri din setul combinat:")
    print(df.head(), "\n")

    feature_cols = ["distance_km",
                    "city_share_pct",
                    "avg_speed_city",
                    "avg_speed_hwy",
                    "ac_on",
                    "persons_in_car",
                    "tire_pressure_bar",
                    "outside_temp_c",
                    ]   
    
    for col in feature_cols + ["fuel_used_l"]:
        if col not in df.columns:
            raise ValueError(f"Coloana lipsa in CSV: {col}")
        
        df_shuffle = df.sample(frac=1, random_state=42).reset_index(drop=True)  
        X = df_shuffle[feature_cols]
        y = df_shuffle["fuel_used_l"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print (f"[INFO] Numar de inregistrari pentru antrenare: {len(X_train)}, pentru testare: {len(X_test)}")

    model = MLPRegressor(hidden_layer_sizes=(32, 16),
                            activation='relu',
                            solver='adam',
                            learning_rate='adaptive',
                            learning_rate_init=0.001,
                            batch_size=32,
                            max_iter=2000,
                            random_state=21,
                            early_stopping=True,       
                            validation_fraction=0.1,   
                            n_iter_no_change=5
                            )
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"[INFO] Mean Absolute Error pe setul de testare: {mae:.2f} litri")

    history_df = pd.DataFrame(model.loss_curve_, columns=['loss'])
    history_df.index.name = 'epoch'
    history_df.to_csv('training_history.csv')
    print("training_history.csv a fost generat!")

    r2 = r2_score(y_test, y_pred)
    accuracy_pct = (1 - (mae / y_test.mean())) * 100

    print(f"R2 Score (Echivalent F1 pentru Regresie): {r2:.2f}")
    print(f"Acuratete Estimata: {accuracy_pct:.2f}%")

    model_filename = "mlp_trip_fuel_model.joblib"

    joblib.dump(model, model_filename)
    print(f"[INFO] Model salvat in fisierul: {model_filename}")

if __name__ == "__main__":
    main()  