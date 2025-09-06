from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
import numpy as np
import logging
import os
from datetime import datetime

# Torch / torchvision imports
import torch.nn as nn
from torchvision.models import efficientnet_b3, EfficientNet_B3_Weights
from torchvision import transforms

# ======================================
# CONFIG
# ======================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://lakshayy10.github.io", "*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IMAGE_SIZE = 300  # EfficientNet-B3 default

# ======================================
# CLASS LABELS
# ======================================
KNEE_CLASS_LABELS = [
    'Biomet AGC', 'Depuy Attune', 'Exatech Opterak Logic',
    'Smith and Nephew LEGION', 'Smith and Nephew ANTHEM',
    'Stryker SCORPIO', 'Zimmer LPS Flex Knee GSF', 'Zimmer NEXGEN',
    'Zimmer Natural Knee II', 'Zimmer Oxford', 'Zimmer Vanguard', 'Zimmer persona'
]

WRIST_CLASS_LABELS = [
    "Depuy Bias", "Depuy total modular wrist system", "Fischer Medical Universal 2",
    "Pyrodisk", "Swemac Motec", "Tornier-Bioprofile APSI", "Tornier-Bioprofile Amandys",
    "Tornier-Bioprofile Eclypse", "Wright Medical-Tornier STPI",
    "Zimmer Biomet Maestro", "RCPI"
]

SHOULDER_CLASS_LABELS = [
    "Accumed Polarus", "Arthex Inverse", "Arthex universe", "Biomet Bio-Angular",
    "Biomet Comprehensive", "Biomet verso", "DJO Encore Reverse",
    "DePuy Global Advantage CTA Head", "Depuy Delta", "Depuy Global",
    "EXATECH Equinox", "Evolutis UNIC", "Exatech Interspace", "Stryker O leary",
    "Stryker solar", "Tornier Aequalis Modular", "Tornier Press Fit", "Zimmer Bigliani",
    "Zimmer Biomet Sidus", "Zimmer Fenlin total shoulder system", "simth and nephew promos"
]

# ======================================
# MODELS
# ======================================
knee_model = None
shoulder_model = None

def get_efficientnet_b3(num_classes: int):
    weights = EfficientNet_B3_Weights.DEFAULT
    model = efficientnet_b3(weights=weights)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    return model

def preprocess_image(image: Image.Image):
    preprocess = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    return preprocess(image).unsqueeze(0).to(DEVICE)

# ======================================
# LOAD FUNCTIONS
# ======================================
def load_knee_model():
    global knee_model
    if knee_model is None:
        try:
            knee_model = get_efficientnet_b3(num_classes=len(KNEE_CLASS_LABELS))
            knee_model.load_state_dict(torch.load("knee.pth", map_location=DEVICE))
            knee_model.to(DEVICE)
            knee_model.eval()
            logger.info("✅ Knee model loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load knee model: {e}")


def load_shoulder_model():
    global shoulder_model
    if shoulder_model is None:
        try:
            shoulder_model = get_efficientnet_b3(num_classes=len(SHOULDER_CLASS_LABELS))
            shoulder_model.load_state_dict(torch.load("./efficientnet_b3_best_model.pth", map_location=DEVICE))
            shoulder_model.to(DEVICE)
            shoulder_model.eval()
            logger.info("✅ Shoulder model loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load shoulder model: {e}")

# ======================================
# ENDPOINTS
# ======================================
@app.get("/")
def read_root():
    return {"message": "Medical Implant Classifier API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": {
            "knee": knee_model is not None,
            "shoulder": shoulder_model is not None
        }
    }

@app.post("/predict/knee")
async def predict_knee(file: UploadFile = File(...)):
    load_knee_model()
    if knee_model is None:
        raise HTTPException(status_code=503, detail="Knee model not available")
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = preprocess_image(image)
        with torch.no_grad():
            output = knee_model(input_tensor)
            probs = torch.nn.functional.softmax(output, dim=1)
            pred_index = torch.argmax(probs, dim=1).item()
            confidence = torch.max(probs).item()
        return {"prediction": KNEE_CLASS_LABELS[pred_index], "confidence": round(confidence, 4)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knee prediction failed: {e}")


@app.post("/predict/shoulder")
async def predict_shoulder(file: UploadFile = File(...)):
    load_shoulder_model()
    if shoulder_model is None:
        raise HTTPException(status_code=503, detail="Shoulder model not available")
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = preprocess_image(image)
        with torch.no_grad():
            output = shoulder_model(input_tensor)
            probs = torch.nn.functional.softmax(output, dim=1)
            pred_index = torch.argmax(probs, dim=1).item()
            confidence = torch.max(probs).item()
        return {"prediction": SHOULDER_CLASS_LABELS[pred_index], "confidence": round(confidence, 4)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Shoulder prediction failed: {e}")

