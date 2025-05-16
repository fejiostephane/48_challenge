from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from fastapi.middleware.cors import CORSMiddleware

# ========== FastAPI + CORS ==========
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pour le dev local. En prod, mets l'URL exacte de ton front Vue.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Modèle et encodeurs ==========
model = joblib.load("mon_model.pkl")

le_quartier = LabelEncoder()
le_quartier.fit(["zone 1", "zone 2", "zone 3", "zone 4", "zone 5"])

le_catastrophe = LabelEncoder()
le_catastrophe.fit(["aucun", "inondation", "seisme"])

# ========== Stockage temporaire ==========
last_prediction = None

# ========== Structure d'entrée attendue ==========
class PredictionInput(BaseModel):
    temperature: float
    humidite: float
    pluie_totale: float
    pluie_intensite_max: float
    force_moyenne_du_vecteur_de_vent: float
    sismicite: float
    concentration_gaz: float
    jour: int
    mois: int
    quartier: str

# ========== POST /predict ==========
@app.post("/predict")
def predict(data: PredictionInput):
    global last_prediction

    quartier_input = data.quartier.lower().strip()
    if quartier_input not in le_quartier.classes_:
        return {
            "error": f"Quartier inconnu : '{data.quartier}'. Choisis parmi : {list(le_quartier.classes_)}"
        }

    quartier_encoded = le_quartier.transform([quartier_input])[0]

    features = pd.DataFrame([[data.temperature, data.humidite, data.pluie_totale,
                              data.pluie_intensite_max, data.force_moyenne_du_vecteur_de_vent,
                              data.sismicite, data.concentration_gaz, data.jour, data.mois,
                              quartier_encoded]],
                            columns=[
                                "temperature", "humidite", "pluie_totale", "pluie_intensite_max",
                                "force_moyenne_du_vecteur_de_vent", "sismicite", "concentration_gaz",
                                "jour", "mois", "quartier_encoded"
                            ])

    pred_index = model.predict(features)[0]
    catastrophe_label = le_catastrophe.inverse_transform([pred_index])[0]

    last_prediction = {
        "quartier": quartier_input,
        "catastrophe_predite": catastrophe_label
    }

    return last_prediction

# ========== GET /last-prediction ==========
@app.get("/last-prediction")
def get_last_prediction():
    if last_prediction is None:
        return {"message": "Aucune prédiction n'a encore été effectuée."}
    return last_prediction
