from pathlib import Path
from bs4 import BeautifulSoup
import time
import pandas as pd
import joblib
import streamlit as st
import requests 
import re

from pathlib import Path
MODEL_PATH = Path("models/mlp_trip_fuel_model.joblib")

#Incarcam modelul
@st.cache_resource
def incarcamil(): 
    if not MODEL_PATH.exists():
        print(f" Modelul nu a fost gasit la calea: {MODEL_PATH}")
        raise FileNotFoundError
    
    model = joblib.load(MODEL_PATH)
    print("Modelul a fost incarcat!")
    return model

model = incarcamil()

#incercam sa luam datele de la peco prin doua metode: la_furat si mana_stanga
#daca nu merge, afisam un grafic cu datele introduse manual intr-un csv

# --- LA FURAT (Reparat să nu mai dea NoneType) ---
def la_furat_de_tabel():
    try:
        url = "https://www.peco-online.ro/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            element = soup.find("div", {"id": "pret_mediu_b95"})
            
            # AICI E CHEIA: verificăm dacă EXISTĂ înainte de .text
            if element:
                return float(element.get_text(strip=True).replace(" RON", "").replace(",", "."))
            
            # Dacă nu, căutăm orice preț în pagină
            match = re.search(r"(\d[,\.]\d{2})\s*RON", soup.text)
            if match:
                return float(match.group(1).replace(",", "."))
        return None
    except:
        return None

# --- MANA STANGA (Reparat pentru grafic) ---
def mana_stanga():
    try:
        url = "https://www.peco-online.ro/istoric.php"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        
        # Regex-ul tău din poză, dar mai "elastic"
        pattern = r"\[\'(\d{2}\.\d{2}\.\d{4})\'\s*,\s*(\d+\.\d+)\]"
        matches = re.findall(pattern, response.text)
        
        if matches:
            df = pd.DataFrame(matches, columns=['Data', 'Pret_95'])
            df['Data'] = pd.to_datetime(df['Data'], dayfirst=True) #
            df['Pret_95'] = df['Pret_95'].astype(float)
            return df.sort_values('Data')
        return None
    except:
        return None
    
#Interfata Streamlit
st.title("PTCC (MLP Regressor)")
st.caption("Estimare consum de combustibil bazata pe retea neuronala (MAE 0.47 L)")

st.header("Parametrii Calatoriei")

col1, col2 = st.columns(2)

with col1:
    distance_km = st.slider("Distanta (km)", 10, 500, 180, 10)
    city_share_pct = st.slider("Ponderea drumului urban (%)", 0, 100, 35)
    persons_in_car = st.selectbox("Numar pasageri (+sofer)", [1, 2, 3, 4, 5], index=1)
    
with col2:
    outside_temp_c = st.slider("Temperatura Exterioara (°C)", -10, 40, 15, 1)
    tire_pressure_bar = st.slider("Presiunea medie in pneuri (bar)", 1.7, 2.3, 2.0, 0.05)
    ac_on = st.radio("Aer Conditionat?", ["Da", "Nu"], index=1)
    
st.subheader("Viteze Medii")
col3, col4 = st.columns(2)
with col3:
    avg_speed_city = st.number_input("Viteza medie oras (km/h)", 15, 50, 28)
with col4:
    avg_speed_hwy = st.number_input("Viteza medie extraurban (km/h)", 50, 140, 95)

ac_val = 1 if ac_on == "Da" else 0

st.subheader("Costuri")
fuel_price = st.number_input("Pret combustibil (RON/L)", 5.0, 10.0, 7.5)

# Predictie la apasarea butonului
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

    start_time = time.time()  

    prediction = model.predict(input_data)
    
    end_time = time.time()
    
    inference_time = (end_time - start_time) * 1000

    st.info(f"Timp de raspuns pipeline: {inference_time:.2f} ms")
    
    try:
        predicted_liters = float(model.predict(input_data)[0])
        l_per_100 = 100 * predicted_liters / distance_km
        total_cost = predicted_liters * fuel_price
        
        if predicted_liters <= 0:
            st.error("Eroare de Validare: Consumul prezis este negativ sau zero. Ajusteaza parametrii.")
        else:
    
            st.success("Predictie realizată cu succes!")

            c1, c2 = st.columns(2)
            with c1:
                st.metric(
                    label="Consum Total Estimat", 
                    value=f"{predicted_liters:.2f} Litri", 
                    delta=f"{l_per_100:.2f} L/100km"
                )
            with c2:
                st.metric(
                    label="Cost Estimat Calatorie", 
                    value=f"{total_cost:.2f} RON",
                    delta_color="inverse" 
                )
            st.markdown("---")
            st.markdown(f"**Detalii (Input-ul AI-ului):** Distanta: {distance_km}km, Oras: {city_share_pct}%, Persoane: {persons_in_car}, AC: {ac_on}")

    #Se mai intampla sa si eroare
    except Exception as e:
        st.error(f"Eroare in timpul predictiei: {e}")

# --- SECTIUNE AFISARE DATE PECO ---
st.subheader("Live Data: Monitorizare Peco-Online")

# Incercam sa luam datele de pe site
pret_site = la_furat_de_tabel()
df_istoric_site = mana_stanga()

# Verificam daca avem date live
if pret_site and df_istoric_site is not None:
    st.info(f"Pret actualizat de pe site: {pret_site} RON/L")
    # Sortam si afisam graficul live
    df_grafic = df_istoric_site.copy().sort_values('Data').set_index('Data')
    st.line_chart(df_grafic)
    pret_final = pret_site
else:
    # Daca n-avem date live, intram pe date locale
    st.warning("Conexiunea la serverul extern a esuat. Se folosesc datele locale.")

    cale_fisier = Path("data/raw/petrol_prices.csv") 
    
    if cale_fisier.exists():
        df_local = pd.read_csv(cale_fisier)
        df_local['Data'] = pd.to_datetime(df_local['Data'])

        coloana_pret = " benzin_95" 
        
        st.write("Grafic istoric (date salvate):")
        st.line_chart(df_local.set_index('Data')[coloana_pret])

        pret_final = float(df_local.iloc[-1][coloana_pret])
    else:
        st.error("Fisierul de date locale nu a fost gasit.")
        pret_final = 7.69

# Calculul costului final pentru afisarea metricii
if 'prediction' in locals():
    cost_calatorie = float(prediction[0]) * pret_final
    st.metric(label="Cost Estimativ", value=f"{cost_calatorie:.2f} RON")