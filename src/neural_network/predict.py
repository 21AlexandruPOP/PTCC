from pathlib import Path
import pandas as pd
import joblib


THIS_FILE = Path(__file__).resolve()
NEURAL_NETWORK_DIR = THIS_FILE.parent  
MODEL_FILE = NEURAL_NETWORK_DIR / "mlp_trip_fuel_model.joblib"

print(f"[DEBUG] Modelul va fi incarcat de la: {MODEL_FILE}")

def make_prediction():

    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Modelul AI nu a fost gasit la: {MODEL_FILE}. Ruleaza intai train_ml_regressor.py!")

    model = joblib.load(MODEL_FILE)
    print("[INFO] Modelul MLP Regressor incarcat cu succes.")


    sample = pd.DataFrame([{
        "distance_km": 170,        
        "city_share_pct": 10,      
        "avg_speed_city": 30,      
        "avg_speed_hwy": 110,       
        "ac_on": 0,                
        "persons_in_car": 2,       
        "tire_pressure_bar": 1.9, 
        "outside_temp_c": 6       
    }])


    predicted_liters = float(model.predict(sample)[0])
    l_per_100 = 100 * predicted_liters / sample["distance_km"].iloc[0]
    estimate_cost = predicted_liters * 7.50  
    print("\n==============================================")
    print(f"[PREDICTIE] Consum Total Estimat: {predicted_liters:.2f} Litri")
    print(f"[PREDICTIE] Consum Mediu Estimat: {l_per_100:.2f} L/100km")
    print(f"[PREDICTIE] Cost Estimat: {estimate_cost:.2f} RON")
    print("==============================================")

if __name__ == "__main__":
    make_prediction()