import tensorflow as tf
import numpy as np
import os
import traceback
from datetime import datetime

def check_model_integrity():
    """Comprehensive model integrity checker for the wrist model"""
    
    print("="*60)
    print("WRIST MODEL INTEGRITY CHECKER")
    print("="*60)
    print(f"Timestamp: {datetime.now()}")
    print(f"TensorFlow Version: {tf.__version__}")
    print()
    
    # Check if model file exists
    model_path = "wrist_model.keras"
    if not os.path.exists(model_path):
        print(f"❌ ERROR: Model file '{model_path}' not found!")
        return False
    
    file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
    print(f"📁 Model file found: {model_path}")
    print(f"📊 File size: {file_size:.2f} MB")
    print()
    
    try:
        print("🔄 Loading model...")
        model = tf.keras.models.load_model(model_path, compile=False)
        print("✅ Model loaded successfully!")
        print()
        
        # Basic model information
        print("📋 MODEL SUMMARY:")
        print("-" * 40)
        model.summary()
        print()
        
        # Check model layers in detail
        print("🔍 LAYER ANALYSIS:")
        print("-" * 40)
        problematic_layers = []
        
        for i, layer in enumerate(model.layers):
            layer_info = f"Layer {i}: {layer.name} ({type(layer).__name__})"
            print(layer_info)
            
            # Check input/output shapes
            try:
                if hasattr(layer, 'input_shape'):
                    print(f"  Input shape: {layer.input_shape}")
                if hasattr(layer, 'output_shape'):
                    print(f"  Output shape: {layer.output_shape}")
                    
                # Special check for Flatten layers
                if isinstance(layer, tf.keras.layers.Flatten):
                    print(f"  ⚠️  FLATTEN LAYER DETECTED")
                    if hasattr(layer, 'input_spec') and layer.input_spec:
                        print(f"  Input spec: {layer.input_spec}")
                    else:
                        print(f"  ⚠️  No input spec found for Flatten layer")
                        problematic_layers.append((i, layer))
                        
            except Exception as e:
                print(f"  ❌ Error checking layer properties: {e}")
                problematic_layers.append((i, layer))
            print()
        
        if problematic_layers:
            print("⚠️  PROBLEMATIC LAYERS FOUND:")
            for i, layer in problematic_layers:
                print(f"  - Layer {i}: {layer.name} ({type(layer).__name__})")
            print()
        
        # Test model with dummy input
        print("🧪 TESTING MODEL WITH DUMMY INPUT:")
        print("-" * 40)
        
        # Test different input shapes
        test_shapes = [
            (1, 224, 224, 3),
            (2, 224, 224, 3),  # Batch size 2
            (1, 256, 256, 3),  # Different image size
        ]
        
        for shape in test_shapes:
            try:
                print(f"Testing with shape {shape}...")
                dummy_input = np.random.random(shape).astype(np.float32)
                print(f"  Input type: {type(dummy_input)}")
                print(f"  Input dtype: {dummy_input.dtype}")
                
                # Make prediction
                prediction = model.predict(dummy_input, verbose=0)
                print(f"  ✅ Success! Output shape: {prediction.shape}")
                print(f"  Output type: {type(prediction)}")
                print(f"  Output range: [{prediction.min():.4f}, {prediction.max():.4f}]")
                
            except Exception as e:
                print(f"  ❌ Failed with shape {shape}")
                print(f"  Error: {str(e)}")
                print(f"  Error type: {type(e).__name__}")
                print("  Full traceback:")
                traceback.print_exc()
            print()
        
        # Check model configuration
        print("⚙️  MODEL CONFIGURATION:")
        print("-" * 40)
        try:
            config = model.get_config()
            print(f"Model type: {config.get('name', 'Unknown')}")
            if 'layers' in config:
                print(f"Number of layers in config: {len(config['layers'])}")
                
                # Look for potential issues in config
                for i, layer_config in enumerate(config['layers']):
                    if layer_config.get('class_name') == 'Flatten':
                        print(f"  Flatten layer found in config at position {i}")
                        print(f"  Config: {layer_config}")
                        
        except Exception as e:
            print(f"❌ Could not retrieve model configuration: {e}")
        
        print()
        print("🔧 POTENTIAL FIXES:")
        print("-" * 40)
        if problematic_layers:
            print("1. Try rebuilding the model with correct architecture")
            print("2. Use GlobalAveragePooling2D instead of Flatten")
            print("3. Check if model was saved with different TensorFlow version")
        else:
            print("No obvious issues detected. The error might be in:")
            print("1. Input preprocessing pipeline")
            print("2. Runtime environment differences")
            print("3. Memory/resource constraints")
        
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Failed to load model!")
        print(f"Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print("\nFull traceback:")
        traceback.print_exc()
        
        print("\n🔧 SUGGESTED ACTIONS:")
        print("1. Check if model file is corrupted")
        print("2. Try loading with different TensorFlow version")
        print("3. Recreate model from original training script")
        print("4. Check if model was saved properly")
        
        return False

def compare_with_knee_model():
    """Compare wrist model structure with working knee model"""
    print("\n" + "="*60)
    print("COMPARING WITH WORKING KNEE MODEL")
    print("="*60)
    
    try:
        knee_model = tf.keras.models.load_model("knee.h5", compile=False)
        print("✅ Knee model loaded successfully")
        
        print("\n📋 KNEE MODEL SUMMARY:")
        print("-" * 40)
        knee_model.summary()
        
        # Compare architectures
        print("\n🔍 KNEE MODEL LAYERS:")
        print("-" * 40)
        for i, layer in enumerate(knee_model.layers):
            print(f"Layer {i}: {layer.name} ({type(layer).__name__})")
            if isinstance(layer, tf.keras.layers.Flatten):
                print(f"  ✅ Flatten layer working correctly")
        
    except Exception as e:
        print(f"❌ Could not load knee model for comparison: {e}")

if __name__ == "__main__":
    # Run integrity check
    success = check_model_integrity()
    
    # Compare with working knee model if available
    compare_with_knee_model()
    
    print("\n" + "="*60)
    if success:
        print("✅ Model integrity check completed")
    else:
        print("❌ Model integrity check failed - manual intervention required")
    print("="*60)
