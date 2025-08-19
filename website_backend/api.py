from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
import tensorflow as tf
import numpy as np
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Force CPU-only execution for TensorFlow
os.environ["CUDA_VISIBLE_DEVICES"] = ""
tf.config.set_visible_devices([], 'GPU')

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
# Global Model Variables
# =============================
pytorch_model = None
preprocess_image = None
knee_model = None
wrist_model = None

# Class labels (same for both general and knee models)
CLASS_NAMES = [
    'Aesculap Columbus', 'Anika unicap', 'BIOIMPIANTI K mod', 'Biomet AGC',
    'Depuy AMK', 'Depuy Attune', 'Depuy COORDINATE', 'Depuy LCS', 'Depuy PFC SIGMA',
    'DJO 3D Knee', 'Exatech Optera', 'Howmedica DURACON TS', 'Implantcast ACS PS fixed bearing',
    'INTERMEDICS Natural Knee', 'Kyocera ACTIYAS', 'Kyocera INITIA PS', 'Kyocera TRIBRID',
    'link endomodel', 'Link Gemini SL', 'Meril life FREEDOM KNEE', 'Microport MEDIAPIVOT',
    'Smith and Nephew ANTHEM', 'Smith and Nephew GENESIS II', 'Smith and Nephew Gensis PS',
    'Smith and Nephew JOURNEY', 'Smith and Nephew LEGION', 'Smith and Nephew TC PLUS SOLUTION',
    'Stryker NRG', 'Stryker SCORPIO', 'Stryker TRIATHLON', 'TTK Healthcare BUCHEL PAPPAS',
    'Zimmer INSALL BURSTEINI', 'Zimmer LPS Flex Knee GSF', 'Zimmer Natural Knee II',
    'Zimmer NEXGEN', 'Zimmer NK II', 'Zimmer Oxford', 'Zimmer UKS (ZUK)',
    'Zimmer Vanguard', 'Zimmer biomet LCCK', 'Zimmer persona'
]

WRIST_CLASS_LABELS = [
    "Depuy Bias", "Depuy total modular wrist system", "Fischer Medical Universal 2",
    "Pyrodisk", "Swemac Motec", "Tornier-Bioprofile APSI", "Tornier-Bioprofile Amandys",
    "Tornier-Bioprofile Eclypse", "Wright Medical-Tornier STPI", "Zimmer Biomet Maestro", "RCPI"
]

# =============================
# Model Loading Functions
# =============================
def load_pytorch_model():
    global pytorch_model, preprocess_image
    if pytorch_model is None:
        try:
            from model import get_model, preprocess_image as preprocess_func
            pytorch_model = get_model(num_classes=len(CLASS_NAMES))
            pytorch_model.load_state_dict(torch.load("efficientnet_b3_best_model.pth", map_location=torch.device("cpu")))
            pytorch_model.eval()
            preprocess_image = preprocess_func
            logger.info("PyTorch model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load PyTorch model: {str(e)}")

def load_knee_model():
    global knee_model
    if knee_model is None:
        try:
            knee_model = tf.keras.models.load_model("knee.h5", compile=False)
            logger.info("Knee model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load knee model: {str(e)}")

def load_wrist_model():
    global wrist_model
    if wrist_model is None:
        try:
            # Create custom objects to handle the Flatten layer issue
            def fixed_flatten_layer(*args, **kwargs):
                # Create a Flatten layer
                flatten_layer = tf.keras.layers.Flatten(*args, **kwargs)
                
                # Override the call method
                original_call = flatten_layer.call
                
                def call(inputs, **call_kwargs):
                    # Handle list input
                    if isinstance(inputs, list) and len(inputs) == 1:
                        inputs = inputs[0]
                    return original_call(inputs, **call_kwargs)
                
                flatten_layer.call = call
                return flatten_layer
            
            # Load model with custom Flatten
            custom_objects = {'Flatten': fixed_flatten_layer}
            wrist_model = tf.keras.models.load_model(
                "wrist_model.keras", 
                compile=False, 
                custom_objects=custom_objects
            )
            
            logger.info("✅ Wrist model loaded with fixed Flatten layer")
            
        except Exception as e:
            logger.error(f"Failed to load wrist model: {str(e)}")# Helper Functions
# =============================
def preprocess_tf_image(image: Image.Image, target_size=(224, 224)):
    image = image.resize(target_size)
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# =============================
# Endpoints
# =============================
@app.get("/")
def read_root():
    return {"message": "Medical Implant Classifier API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": {
            "pytorch": pytorch_model is not None,
            "knee": knee_model is not None,
            "wrist": wrist_model is not None
        }
    }

@app.post("/predict/")
async def predict_pytorch(file: UploadFile = File(...)):
    load_pytorch_model()
    
    if pytorch_model is None or preprocess_image is None:
        raise HTTPException(status_code=503, detail="PyTorch model not available")
    
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
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/knee")
async def predict_knee(file: UploadFile = File(...)):
    load_knee_model()
    
    if knee_model is None:
        raise HTTPException(status_code=503, detail="Knee model not available")
    
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = preprocess_tf_image(image)
        
        prediction = knee_model.predict(input_tensor, verbose=0)
        pred_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction))
        predicted_label = CLASS_NAMES[pred_index]
        
        return {
            "prediction": predicted_label,
            "confidence": round(confidence, 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knee prediction failed: {str(e)}")

@app.post("/predict/wrist")
async def predict_wrist(file: UploadFile = File(...)):
    load_wrist_model()
    
    if wrist_model is None:
        raise HTTPException(status_code=503, detail="Wrist model not available")
    
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = preprocess_tf_image(image)
        
        prediction = wrist_model.predict(input_tensor, verbose=0)
        pred_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction))
        predicted_label = WRIST_CLASS_LABELS[pred_index]
        
        return {
            "prediction": predicted_label,
            "confidence": round(confidence, 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wrist prediction failed: {str(e)}")
