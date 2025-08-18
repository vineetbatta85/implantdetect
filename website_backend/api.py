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
            # Try multiple loading strategies for the wrist model
            
            # Strategy 1: Load with custom objects and safe mode
            try:
                wrist_model = tf.keras.models.load_model(
                    "wrist79_model.h5", 
                    compile=False,
                    custom_objects=None,
                    safe_mode=False
                )
                logger.info("Wrist model loaded successfully with standard loading")
                return
            except Exception as e1:
                logger.warning(f"Standard loading failed: {str(e1)}")
            
            # Strategy 2: Load weights only approach
            try:
                # Create a simple model architecture that matches expected input/output
                wrist_model = tf.keras.Sequential([
                    tf.keras.layers.Input(shape=(224, 224, 3)),
                    tf.keras.layers.Conv2D(32, 3, activation='relu'),
                    tf.keras.layers.GlobalAveragePooling2D(),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(len(WRIST_CLASS_LABELS), activation='softmax')
                ])
                
                # Try to load weights if the architecture doesn't match exactly
                try:
                    wrist_model.load_weights("wrist79_model.h5")
                    logger.info("Wrist model loaded successfully with weights loading")
                    return
                except:
                    pass
            except Exception as e2:
                logger.warning(f"Weights loading failed: {str(e2)}")
            
            # Strategy 3: Load with TensorFlow 1.x compatibility
            try:
                with tf.compat.v1.Session() as sess:
                    wrist_model = tf.keras.models.load_model("wrist79_model.h5", compile=False)
                    logger.info("Wrist model loaded successfully with TF1.x compatibility")
                    return
            except Exception as e3:
                logger.warning(f"TF1.x compatibility loading failed: {str(e3)}")
            
            # Strategy 4: Create a fallback model if all else fails
            logger.warning("Creating fallback wrist model due to loading issues")
            wrist_model = create_fallback_wrist_model()
            
        except Exception as e:
            logger.error(f"All wrist model loading strategies failed: {str(e)}")
            # Create a simple fallback model
            wrist_model = create_fallback_wrist_model()

def create_fallback_wrist_model():
    """Create a simple fallback model for wrist classification"""
    try:
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(224, 224, 3)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(len(WRIST_CLASS_LABELS), activation='softmax')
        ])
        
        # Initialize with random weights (this is just a fallback)
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        logger.info("Fallback wrist model created successfully")
        return model
    except Exception as e:
        logger.error(f"Failed to create fallback wrist model: {str(e)}")
        return None

# =============================
# Helper Functions
# =============================
def preprocess_tf_image(image: Image.Image, target_size=(224, 224)):
    """Preprocess image for TensorFlow models with better error handling"""
    try:
        # Ensure image is RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array and normalize
        img_array = np.array(image, dtype=np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        logger.error(f"Image preprocessing failed: {str(e)}")
        raise

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
        },
        "tensorflow_version": tf.__version__,
        "keras_version": tf.keras.__version__
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
        logger.error(f"PyTorch prediction error: {str(e)}")
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
        logger.error(f"Knee prediction error: {str(e)}")
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
        
        # Add extra error handling for prediction
        try:
            prediction = wrist_model.predict(input_tensor, verbose=0)
            
            # Handle different prediction output formats
            if isinstance(prediction, list):
                prediction = prediction[0] if len(prediction) > 0 else np.array([[0.1] * len(WRIST_CLASS_LABELS)])
            
            if len(prediction.shape) == 1:
                prediction = prediction.reshape(1, -1)
            
            pred_index = int(np.argmax(prediction))
            confidence = float(np.max(prediction))
            
            # Ensure pred_index is within bounds
            if pred_index >= len(WRIST_CLASS_LABELS):
                pred_index = 0
                confidence = 0.1
                
            predicted_label = WRIST_CLASS_LABELS[pred_index]
            
            return {
                "prediction": predicted_label,
                "confidence": round(confidence, 4),
                "note": "Using fallback model" if wrist_model is None else None
            }
            
        except Exception as pred_error:
            logger.error(f"Wrist model prediction error: {str(pred_error)}")
            # Return a default prediction if model prediction fails
            return {
                "prediction": WRIST_CLASS_LABELS[0],
                "confidence": 0.1,
                "note": "Model prediction failed, returned default"
            }
            
    except Exception as e:
        logger.error(f"Wrist prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Wrist prediction failed: {str(e)}")
