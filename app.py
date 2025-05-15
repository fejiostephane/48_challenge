import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Charger le modèle
model = joblib.load("mon_model.pkl")

# Encoder les quartiers et catastrophes
le_quartier = LabelEncoder()
le_quartier.fit(["zone 1", "zone 2", "zone 3", "zone 4", "zone 5"])

le_catastrophe = LabelEncoder()
le_catastrophe.fit(["aucun", "inondation", "seisme"])

st.title("🌦️ Prédiction de Catastrophes Climatiques")

# Saisie utilisateur
temperature = st.number_input("🌡️ Température", value=20.0)
humidite = st.number_input("💧 Humidité (%)", value=60.0)
pluie_totale = st.number_input("☔ Pluie totale (mm)", value=5.0)
pluie_intensite_max = st.number_input("🌧️ Pluie max (mm/h)", value=2.0)
vent_moyen = st.number_input("💨 Vent moyen", value=3.0)
sismicite = st.number_input("🌍 Sismicité", value=0.5)
gaz = st.number_input("🧪 Concentration gaz", value=100.0)

jour = st.number_input("📆 Jour", value=1, min_value=1, max_value=31)
mois = st.number_input("🗓️ Mois", value=1, min_value=1, max_value=12)

quartier_nom = st.selectbox("🏘️ Quartier", le_quartier.classes_)
quartier_encoded = le_quartier.transform([quartier_nom])[0]

# Créer les features avec les bons noms
features = pd.DataFrame([[
    temperature, humidite, pluie_totale, pluie_intensite_max,
    vent_moyen, sismicite, gaz, jour, mois, quartier_encoded
]], columns=[
    "temperature", "humidite", "pluie_totale", "pluie_intensite_max",
    "force_moyenne_du_vecteur_de_vent", "sismicite", "concentration_gaz",
    "jour", "mois", "quartier_encoded"
])

# Prédiction
if st.button("🔍 Prédire"):
    prediction = model.predict(features)[0]
    label = le_catastrophe.inverse_transform([prediction])[0]
    st.success(f"🌪️ Catastrophe prédite : **{label.upper()}**")
