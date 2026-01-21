# ============================================================
# 🐶 DOG BREED CLASSIFICATION - EfficientNetB3 (Robust Version)
# ============================================================

# ============================================================
# ✅ Mount Google Drive
# ============================================================
from google.colab import drive
drive.mount('/content/drive')

import os
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, Dropout, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import mixed_precision

# ============================================================
# ✅ Enable Mixed Precision (Faster on GPU)
# ============================================================
mixed_precision.set_global_policy('mixed_float16')

# ============================================================
# ✅ Paths
# ============================================================
base_dir = '/content/drive/MyDrive/final_dataset'
train_dir = os.path.join(base_dir, 'train')
val_dir   = os.path.join(base_dir, 'val')
test_dir  = os.path.join(base_dir, 'test')
model_path = os.path.join(base_dir, 'efficientnetb3_best.h5')
final_model_path = os.path.join(base_dir, 'efficientnetb3_final.h5')
log_path = os.path.join(base_dir, 'training_log.csv')

# ============================================================
# ✅ Verify Dataset Folders
# ============================================================
for d in [train_dir, val_dir, test_dir]:
    if not os.path.exists(d):
        raise FileNotFoundError(f"Directory not found: {d}")

print("Dataset folders exist. Train classes:", os.listdir(train_dir))

# ============================================================
# ✅ Detect Number of Classes
# ============================================================
NUM_CLASSES = len(os.listdir(train_dir))
print(f"Detected {NUM_CLASSES} dog breeds.")

# ============================================================
# ✅ Check GPU
# ============================================================
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"✅ GPU detected: {gpus[0]}")
else:
    print("⚠️ No GPU detected. Training will be slower!")

# ============================================================
# ✅ Hyperparameters
# ============================================================
IMG_SIZE = (300, 300)
BATCH_SIZE = 32
EPOCHS = 50
FINE_TUNE_EPOCHS = 20
AUTOTUNE = tf.data.AUTOTUNE

# ============================================================
# ✅ Data Augmentation
# ============================================================
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2),
    tf.keras.layers.RandomTranslation(0.1, 0.1),
    tf.keras.layers.RandomContrast(0.2),
], name="data_augmentation")

# ============================================================
# ✅ Datasets
# ============================================================
train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical',
    shuffle=True
).prefetch(AUTOTUNE)

val_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    val_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical',
    shuffle=False
).prefetch(AUTOTUNE)

test_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    test_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical',
    shuffle=False
).prefetch(AUTOTUNE)

# ============================================================
# ✅ Learning Rate Scheduler
# ============================================================
lr_schedule = tf.keras.optimizers.schedules.CosineDecayRestarts(
    initial_learning_rate=1e-4,
    first_decay_steps=1000,
    t_mul=2.0,
    m_mul=0.9
)
optimizer = Adam(learning_rate=lr_schedule)

# ============================================================
# ✅ Callbacks
# ============================================================
checkpoint_cb = ModelCheckpoint(
    filepath=model_path,
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)
csv_logger = CSVLogger(log_path, append=True)
callbacks = [checkpoint_cb, early_stop, csv_logger]

# ============================================================
# ✅ Model Definition or Resume
# ============================================================
fine_tuning_started = False
if os.path.exists(model_path):
    print("🔄 Resuming from last saved model...")
    model = load_model(model_path)
    fine_tuning_started = any([layer.trainable for layer in model.layers])
else:
    print("🚀 Building new EfficientNetB3 model...")
    base_input = Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = data_augmentation(base_input)

    base_model = tf.keras.applications.EfficientNetB3(
        include_top=False,
        weights='imagenet',
        input_tensor=x
    )
    base_model.trainable = False

    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(1024, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)
    output = Dense(NUM_CLASSES, activation='softmax', dtype='float32')(x)

    model = Model(inputs=base_input, outputs=output)
    model.compile(
        optimizer=optimizer,
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=['accuracy']
    )

# ============================================================
# ✅ Resume from Last Epoch
# ============================================================
initial_epoch = 0
if os.path.exists(log_path):
    import pandas as pd
    log_data = pd.read_csv(log_path)
    if len(log_data) > 0:
        initial_epoch = int(log_data['epoch'].iloc[-1]) + 1
        print(f"⏩ Resuming from epoch {initial_epoch}...")

# ============================================================
# ✅ Stage 1: Initial Training
# ============================================================
if not fine_tuning_started:
    print("\n🔥 Stage 1: Training frozen EfficientNetB3...")
    history_1 = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=EPOCHS,
        initial_epoch=initial_epoch,
        callbacks=callbacks
    )

    # Fine-tune last 100 layers
    print("\n🎯 Stage 2: Fine-tuning last 100 layers...")
    base_model = next(layer for layer in model.layers if isinstance(layer, tf.keras.Model))
    for layer in base_model.layers[:-100]:
        layer.trainable = False
    for layer in base_model.layers[-100:]:
        layer.trainable = True

    model.compile(
        optimizer=Adam(1e-5),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=['accuracy']
    )
else:
    print("\n🎯 Resuming Fine-tuning phase...")

# ============================================================
# ✅ Stage 2: Fine-tuning
# ============================================================
history_2 = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=EPOCHS + FINE_TUNE_EPOCHS,
    initial_epoch=max(initial_epoch, EPOCHS),
    callbacks=callbacks
)

# ============================================================
# ✅ Save Final Model
# ============================================================
model.save(final_model_path)
print(f"✅ Final model saved at {final_model_path}")

# ============================================================
# ✅ Evaluate on Test Set
# ============================================================
print("\n📊 Evaluating on test set...")
test_loss, test_acc = model.evaluate(test_dataset)
print(f"✅ Final Test Accuracy: {test_acc * 100:.2f}%")
