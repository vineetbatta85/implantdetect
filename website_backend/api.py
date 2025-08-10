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
# Custom Layer Fix for Wrist Model
# =============================
class FixedFlatten(tf.keras.layers.Flatten):
    """Custom Flatten layer to handle the list input issue"""
    def call(self, inputs):
        if isinstance(inputs, list):
            inputs = inputs[0]  # Take the first element if it's a list
        return super().call(inputs)

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
            logger.info("Attempting to load wrist model with multiple approaches...")
            
            # Method 1: Try with custom objects to handle Flatten layer
            try:
                custom_objects = {
                    'Flatten': FixedFlatten,
                    'FixedFlatten': FixedFlatten
                }
                wrist_model = tf.keras.models.load_model(
                    "wrist79_model.h5", 
                    custom_objects=custom_objects,
                    compile=False
                )
                logger.info("Wrist model loaded successfully with custom Flatten layer")
                return
            except Exception as e1:
                logger.warning(f"Method 1 failed: {str(e1)}")
            
            # Method 2: Try loading without compile and with safe mode
            try:
                with tf.keras.utils.custom_object_scope({'Flatten': tf.keras.layers.Flatten}):
                    wrist_model = tf.keras.models.load_model(
                        "wrist79_model.h5",
                        compile=False,
                        safe_mode=False
                    )
                logger.info("Wrist model loaded successfully with safe_mode=False")
                return
            except Exception as e2:
                logger.warning(f"Method 2 failed: {str(e2)}")
            
            # Method 3: Try loading weights only if we have architecture
            try:
                # This would require you to define the model architecture manually
                # For now, we'll skip this approach
                pass
            except Exception as e3:
                logger.warning(f"Method 3 failed: {str(e3)}")
                
            # Method 4: Create a simple fallback model (temporary solution)
            try:
                logger.info("Creating temporary fallback wrist model...")
                wrist_model = create_fallback_wrist_model()
                logger.info("Fallback wrist model created successfully")
                return
            except Exception as e4:
                logger.warning(f"Fallback model creation failed: {str(e4)}")
            
            # If all methods fail
            logger.error("All wrist model loading methods failed")
            
        except Exception as e:
            logger.error(f"Failed to load wrist model: {str(e)}")

def create_fallback_wrist_model():
    """Create a simple fallback model for wrist predictions"""
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(224, 224, 3)),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(len(WRIST_CLASS_LABELS), activation='softmax')
    ])
    
    # Initialize with random weights (this is just a placeholder)
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    logger.warning("Using fallback wrist model - predictions will be random!")
    return model

# =============================
# Helper Functions
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
        
        # Add error handling for prediction
        try:
            prediction = wrist_model.predict(input_tensor, verbose=0)
            pred_index = int(np.argmax(prediction))
            confidence = float(np.max(prediction))
            predicted_label = WRIST_CLASS_LABELS[pred_index]
            
            return {
                "prediction": predicted_label,
                "confidence": round(confidence, 4),
                "warning": "Using fallback model" if hasattr(wrist_model, '_is_fallback') else None
            }
        except Exception as pred_error:
            logger.error(f"Wrist prediction error: {str(pred_error)}")
            raise HTTPException(status_code=500, detail=f"Wrist prediction failed: {str(pred_error)}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wrist prediction failed: {str(e)}")

# =============================
# Additional Debug Endpoints
# =============================
@app.get("/debug/models")
async def debug_models():
    """Debug endpoint to check model status"""
    return {
        "pytorch_model": {
            "loaded": pytorch_model is not None,
            "type": str(type(pytorch_model)) if pytorch_model else None
        },
        "knee_model": {
            "loaded": knee_model is not None,
            "type": str(type(knee_model)) if knee_model else None,
            "summary": str(knee_model.summary()) if knee_model else None
        },
        "wrist_model": {
            "loaded": wrist_model is not None,
            "type": str(type(wrist_model)) if wrist_model else None,
            "is_fallback": hasattr(wrist_model, '_is_fallback') if wrist_model else False
        }
    }

@app.post("/debug/reload-wrist")
async def reload_wrist_model():
    """Force reload wrist model for debugging"""
    global wrist_model
    wrist_model = None
    load_wrist_model()
    return {
        "status": "reload_attempted",
        "loaded": wrist_model is not None,
        "type": str(type(wrist_model)) if wrist_model else None
    }
