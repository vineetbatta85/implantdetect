import numpy as np
from tensorflow import keras
from PIL import Image
import io

model = keras.models.load_model("knee.h5")
print(model.output_shape)  # See how many classes it predicts

