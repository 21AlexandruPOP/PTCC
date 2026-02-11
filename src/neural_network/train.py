
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import joblib
from pathlib import Path
import matplotlib.pyplot as plt

THIS_FILE = Path(__file__).resolve()              
NEURAL_NETWORK_DIR = THIS_FILE.parent            
PROJECT_ROOT = NEURAL_NETWORK_DIR.parent.parent  
DATA_DIR = PROJECT_ROOT / "data" / "generated"

#Fisierele cu date
fisiereDate = [
    DATA_DIR / "generated_trips.csv",
    DATA_DIR / "generated_trips2.csv",
    DATA_DIR / "generated_trips3.csv",
    DATA_DIR / "generated_trips4.csv",
]

print("Script location:", THIS_FILE)
print("Data dir:", DATA_DIR)

for f in fisiereDate:
    print(f"Exista {f.name}? ->", f.exists())

def main():
    dfs = []
    for f in fisiereDate:
        if not f.exists():
            raise FileNotFoundError(f"NOT FOUND: {f}")
        dfs.append(pd.read_csv(f))

    df = pd.concat(dfs, ignore_index=True)
    print(f"Numar total de inregistrari: {len(df)}")
    print("Primele randuri din setul combinat:")
    print(df.head(), "\n")

    coloane = ["distance_km",
                    "city_share_pct",
                    "avg_speed_city",
                    "avg_speed_hwy",
                    "ac_on",
                    "persons_in_car",
                    "tire_pressure_bar",
                    "outside_temp_c",
                    ]   
    
    for col in coloane + ["fuel_used_l"]:
        df_shuffle = df.sample(frac=1, random_state=42).reset_index(drop=True)  
        X = df_shuffle[coloane]
        y = df_shuffle["fuel_used_l"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

    print (f"Numar de inregistrari pentru antrenare: {len(X_train)}, pentru testare: {len(X_test)}")

    model = MLPRegressor(hidden_layer_sizes=(64, 32),
                            activation='relu',
                            solver='adam',
                            learning_rate='adaptive',
                            learning_rate_init=0.001,
                            batch_size=32,
                            max_iter=2000,
                            random_state=21,
                            early_stopping=True,       
                            validation_fraction=0.15,   
                            n_iter_no_change=10
                            )
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"MAE pe setul de testare: {mae:.2f} litri")

    history_df = pd.DataFrame(model.loss_curve_, columns=['loss'])
    history_df.index.name = 'epoch'
    history_df.to_csv('data/training_history.csv')

    r2 = r2_score(y_test, y_pred)
    acuratete = (1 - (mae / y_test.mean())) * 100

    print(f"R2_score(echivalent F1 pentru regresie): {r2:.2f}")
    print(f"Acuratete Estimata: {acuratete:.2f}%")

    model_filename = "models/mlp_trip_fuel_model.joblib"

    joblib.dump(model, model_filename)
    print(f"Model salvat in fisierul: {model_filename}")

    test_dataset = X_test.copy()
    test_dataset['fuel_consumed'] = y_test
    test_dataset.to_csv('data/test_samples.csv', index=False)
    print("Setul de testare a fost salvat in data/test_samples.csv")

    plt.figure(figsize=(10, 5))
    plt.plot(model.loss_curve_)
    plt.title('Curba de Invatare (Model Loss)')
    plt.xlabel('Epoci')
    plt.ylabel('MSE (Eroare)')
    plt.grid(True)
    plt.savefig('docs/learning_curve.png') 

    plt.figure(figsize=(10, 5))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.title('Predictie vs Valori Reale')
    plt.xlabel('Consum Real (Litri)')
    plt.ylabel('Consum Prezis (Litri)')
    plt.savefig('docs/prediction_accuracy.png')

if __name__ == "__main__":
    main()  