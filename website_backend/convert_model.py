from tensorflow import keras

# Load your existing H5 model
model = keras.models.load_model("wrist79_model.h5", compile=False)

# 1. Save in new native Keras format
model.save("wrist_model.keras")

# 2. Save in legacy H5 format
model.save("wrist_model_legacy.h5")

# 3. Export in TensorFlow SavedModel format (folder)
model.export("wrist_model_saved")

print("✅ Models exported: wrist_model.keras, wrist_model_legacy.h5, wrist_model_saved/")

