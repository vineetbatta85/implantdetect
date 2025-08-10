from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
import tensorflow as tf
import numpy as np
from model import get_model, preprocess_image, CLASS_NAMES

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://lakshayy10.github.io",
        "*"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# Load PyTorch Model (General)
# =============================
pytorch_model = get_model(num_classes=len(CLASS_NAMES))
pytorch_model.load_state_dict(torch.load("efficientnet_b3_best_model.pth", map_location=torch.device("cpu")))
pytorch_model.eval()

# =============================
# Load TensorFlow Knee Model
# =============================
knee_model = tf.keras.models.load_model("knee.h5")
KNEE_CLASS_LABELS = [
    'Aesculap Columbus',
    'Anika unicap',
    'BIOIMPIANTI K mod',
    'Biomet AGC',
    'Depuy AMK',
    'Depuy Attune',
    'Depuy COORDINATE',
    'Depuy LCS',
    'Depuy PFC SIGMA',
    'DJO 3D Knee',
    'Exatech Optera',
    'Howmedica DURACON TS',
    'Implantcast ACS PS fixed bearing',
    'INTERMEDICS Natural Knee',
    'Kyocera ACTIYAS',
    'Kyocera INITIA PS',
    'Kyocera TRIBRID',
    'link endomodel',
    'Link Gemini SL',
    'Meril life FREEDOM KNEE',
    'Microport MEDIAPIVOT',
    'Smith and Nephew ANTHEM',
    'Smith and Nephew GENESIS II',
    'Smith and Nephew Gensis PS',
    'Smith and Nephew JOURNEY',
    'Smith and Nephew LEGION',
    'Smith and Nephew TC PLUS SOLUTION',
    'Stryker NRG',
    'Stryker SCORPIO',
    'Stryker TRIATHLON',
    'TTK Healthcare BUCHEL PAPPAS',
    'Zimmer INSALL BURSTEINI',
    'Zimmer LPS Flex Knee GSF',
    'Zimmer Natural Knee II',
    'Zimmer NEXGEN',
    'Zimmer NK II',
    'Zimmer Oxford',
    'Zimmer UKS (ZUK)',
    'Zimmer Vanguard',
    'Zimmer biomet LCCK',
    'Zimmer persona'
]

# =============================
# Load TensorFlow Wrist Model
# =============================
wrist_model = tf.keras.models.load_model("wrist79_model.h5")
WRIST_CLASS_LABELS = [
    "Depuy Bias", "Depuy total modular wrist system", "Fischer Medical Universal 2",
    "Pyrodisk", "Swemac Motec", "Tornier-Bioprofile APSI", "Tornier-Bioprofile Amandys",
    "Tornier-Bioprofile Eclypse", "Wright Medical-Tornier STPI", "Zimmer Biomet Maestro", "RCPI"
]

# =============================
# Preprocessing Helper
# =============================
def preprocess_tf_image(image: Image.Image, target_size=(224, 224)):
    image = image.resize(target_size)
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# =============================
# Prediction Endpoints
# =============================
@app.post("/predict/")
async def predict_pytorch(file: UploadFile = File(...)):
    """Predict using PyTorch model"""
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = preprocess_image(image)
        with torch.no_grad():
            output = pytorch_model(input_tensor)
            probs = torch.nn.functional.softmax(output, dim=1)
            pred_index = torch.argmax(probs, dim=1).item()
            confidence = torch.max(probs).item()
        return {
            "prediction": CLASS_NAMES[pred_index],
            "confidence": round(confidence, 4)
        }
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

@app.post("/predict/knee")
async def predict_knee(file: UploadFile = File(...)):
    """Predict knee implant using TensorFlow model"""
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = preprocess_tf_image(image)
        prediction = knee_model.predict(input_tensor)
        pred_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction))
        predicted_label = KNEE_CLASS_LABELS[pred_index]
        return {
            "prediction": predicted_label,
            "confidence": round(confidence, 4)
        }
    except Exception as e:
        return {"error": f"Knee prediction failed: {str(e)}"}

@app.post("/predict/wrist")
async def predict_wrist(file: UploadFile = File(...)):
    """Predict wrist implant using TensorFlow model"""
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = preprocess_tf_image(image)
        prediction = wrist_model.predict(input_tensor)
        pred_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction))
        predicted_label = WRIST_CLASS_LABELS[pred_index]
        return {
            "prediction": predicted_label,
            "confidence": round(confidence, 4)
        }
    except Exception as e:
        return {"error": f"Wrist prediction failed: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "API is running"}

