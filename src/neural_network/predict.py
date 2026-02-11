from pathlib import Path
import pandas as pd
import joblib

THIS_FILE = Path(__file__).resolve()
NEURAL_NETWORK_DIR = THIS_FILE.parent  
MODEL_FILE = NEURAL_NETWORK_DIR / "mlp_trip_fuel_model.joblib"

print(f"[DEBUG] Modelul va fi incarcat de la: {MODEL_FILE}")

#Aici are loc magia
def prezicemil():

    model = joblib.load(MODEL_FILE)
    print("Modelul a fost incarcat cu succes.")

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

    litrii_prezisi = float(model.predict(sample)[0])
    lper100 = 100 * litrii_prezisi / sample["distance_km"].iloc[0]
    costEstimat = litrii_prezisi * 7.50  
    print("\n----------------------------------------------")
    print(f"Consum Total Estimat: {litrii_prezisi:.2f} Litri")
    print(f"Consum Mediu Estimat: {lper100:.2f} L/100km")
    print(f"Cost Estimat: {costEstimat:.2f} RON")
    print("-----------------------------------------------\n")

if __name__ == "__main__":
    prezicemil()