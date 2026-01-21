import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.applications import EfficientNetB3

# ============================================================
# 🧩 Rebuilds EfficientNetB3 architecture for Dog Breed Classifier
# ============================================================

def build_model(num_classes=120, input_shape=(300, 300, 3)):
    base_input = Input(shape=input_shape)
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.2),
        tf.keras.layers.RandomTranslation(0.1, 0.1),
        tf.keras.layers.RandomContrast(0.2),
    ], name="data_augmentation")

    x = data_augmentation(base_input)

    base_model = EfficientNetB3(
        include_top=False,
        weights=None,        # ← we'll load weights manually
        input_tensor=x
    )

    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(1024, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)
    outputs = Dense(num_classes, activation='softmax', dtype='float32')(x)

    model = Model(inputs=base_input, outputs=outputs)
    return model


# ============================================================
# 🧩 Load weights safely from your saved file
# ============================================================

SOURCE_PATH = "efficientnetb3_final.h5"       # or efficientnetb3_best.h5
TARGET_PATH = "efficientnetb3_clean_rgb.h5"   # new RGB-safe version

try:
    print("🔍 Rebuilding architecture...")
    model = build_model(num_classes=120)
    model.load_weights(SOURCE_PATH, by_name=True, skip_mismatch=True)
    model.save(TARGET_PATH)
    print(f"✅ Model rebuilt and saved to {TARGET_PATH}")
    print(f"Input shape: {model.input_shape}")
except Exception as e:
    print(f"❌ Failed to rebuild: {e}")
