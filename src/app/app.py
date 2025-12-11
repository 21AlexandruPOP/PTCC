from pathlib import Path
import pandas as pd
import joblib
import streamlit as st


MODEL_PATH = Path(r"C:/Users/AlexFix/OneDrive/Desktop/PTCC/src/neural_network/mlp_trip_fuel_model.joblib")
print(f"[DEBUG] Incarc modelul de la: {MODEL_PATH}")


@st.cache_resource
def load_model():
    print("DEBUG 1: Incarc modelul...") # <---- MODIFICARE
    if not MODEL_PATH.exists():
        # Aici nu mai poti folosi st.error, deci lasa Python sa dea eroare
        print(f"FATAL ERROR: Modelul nu a fost gasit la calea: {MODEL_PATH}")
        # Nu folosim st.stop() aici, lasam scriptul sa se blocheze
        raise FileNotFoundError
    
    model = joblib.load(MODEL_PATH)
    print("DEBUG 2: Modelul a fost incarcat!") # <---- MODIFICARE
    return model

model = load_model()

st.title("PTCC (MLP Regressor)")
st.caption("Estimare consum de combustibil bazata pe retea neuronala (MAE 0.47 L)")

st.header("Parametrii Calatoriei")

col1, col2 = st.columns(2)

with col1:
    distance_km = st.slider("Distanta (km)", 10, 500, 180, 10)
    city_share_pct = st.slider("Ponderea drumului urban (%)", 0, 100, 35)
    persons_in_car = st.selectbox("Numar de persoane in masina", [1, 2, 3], index=1)
    
with col2:
    outside_temp_c = st.slider("Temperatura Exterioara (°C)", -10, 40, 15, 1)
    tire_pressure_bar = st.slider("Presiunea medie in pneuri (bar)", 1.7, 2.3, 2.0, 0.05)
    ac_on = st.radio("Aer Conditionat PORNIT?", ["Da", "Nu"], index=1)
    
st.subheader("Viteze Medii")
col3, col4 = st.columns(2)
with col3:
    avg_speed_city = st.number_input("Viteza medie oras (km/h)", 15, 50, 28)
with col4:
    avg_speed_hwy = st.number_input("Viteza medie extraurban (km/h)", 50, 140, 95)

ac_val = 1 if ac_on == "Da" else 0

if st.button("Estimeaza Consumul"):

    input_data = pd.DataFrame([{
        "distance_km": distance_km,
        "city_share_pct": city_share_pct,
        "avg_speed_city": avg_speed_city,
        "avg_speed_hwy": avg_speed_hwy,
        "ac_on": ac_val,
        "persons_in_car": persons_in_car,
        "tire_pressure_bar": tire_pressure_bar,
        "outside_temp_c": outside_temp_c,
    }])
    
    try:
        predicted_liters = float(model.predict(input_data)[0])
        l_per_100 = 100 * predicted_liters / distance_km
        
        
        if predicted_liters <= 0:
            st.error("Eroare de Validare: Consumul prezis este negativ sau zero. Ajusteaza parametrii.")
        else:
    
            st.success("Predicție realizata cu succes!")
            
            st.metric(
                label="Consum Total Estimat", 
                value=f"{predicted_liters:.2f} Litri", 
                delta=f"{l_per_100:.2f} L/100km (Mediu)"
            )
            st.markdown("---")
            st.markdown(f"**Detalii (Input-ul AI-ului):** Distanta: {distance_km}km, Oras: {city_share_pct}%, Persoane: {persons_in_car}, AC: {ac_on}")

    except Exception as e:
        st.error(f"Eroare in timpul predictiei: {e}")
        st.caption("Verifica daca setul de date de training a avut aceleasi coloane si daca modelul este compatibil.")