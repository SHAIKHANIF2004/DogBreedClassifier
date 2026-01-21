# 🐶 Dog Breed Image Classification

A **Dog Breed Image Classification** project that uses **Deep Learning (EfficientNet)** to identify the breed of a dog from an input image.  
The project covers **data preprocessing**, **model training**, and an **image prediction application** to test the trained model.

---

## 📌 Project Description

This project aims to classify dog breeds from images using a trained deep learning model.  
The workflow includes:

- Cleaning and preprocessing image datasets
- Training a convolutional neural network for breed classification
- Using an image-based interface to upload images and view predictions

---

## 📂 Project Structure

```
DogBreedClassifier/
│
├── DataCleaning/
│   ├── DataPreProcessingCodes/
│   └── DataPreProcessingOutputs/
│
├── TrainingModel/
│   ├── train.py -->trains the model
│   ├── rebuild_model.py
│   ├── debug_predict.py
│   ├── breed_labels.txt
│   ├── efficientnetb3_clean_rgb.h5
│   └── training_log.csv
│
├── Dog-Breed-Classifier-App/
│   ├── backend/
│   ├── frontend/
│   └── outputs/
│
└── README.md
```

## 🚀 How to Run the Project

Follow the steps below to run the **Dog Breed Image Classification** application locally.

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SHAIKHANIF2004/DogBreedClassifier.git
cd DogBreedClassifier
```

---

### 2️⃣ Start the Prediction Server (Backend)

```bash
cd Dog-Breed-Classifier-App/backend
npm install
npm run dev
```

- The prediction server starts on: `http://localhost:5000`
- Keep this terminal running

---

### 3️⃣ Start the Image Upload Interface (Frontend)

Open a **new terminal** and run:

```bash
cd Dog-Breed-Classifier-App/frontend
npm install
npm run dev
```

- The interface starts on: `http://localhost:5173`

---

### 4️⃣ Use the Application

- Open the frontend URL in a browser
- Upload a dog image
- View the predicted dog breed

  ## 🧠 Model Details

- **Task**: Dog breed image classification
- **Model Architecture**: EfficientNetB3
- **Framework**: TensorFlow / Keras
- **Input**: RGB dog images
- **Output**: Predicted dog breed label

---

### 📁 Model Files

- Trained model:
  ```
  TrainingModel/efficientnetb3_clean_rgb.h5
  ```

- Breed labels:
  ```
  TrainingModel/breed_labels.txt
  ```

The trained model is loaded by the prediction server to classify uploaded dog images.

---

## ✨ Key Features

- Dog breed classification from input images  
- Deep learning–based prediction using EfficientNet  
- Supports RGB image inputs  
- Clean separation of data preprocessing, training, and prediction  
- Simple image upload interface for testing predictions  
- Fast and accurate inference using a trained model

---

## 🛠️ Tech Stack

### Deep Learning & Data Processing
- Python
- TensorFlow
- Keras
- NumPy
- OpenCV

### Model Serving & Prediction
- Node.js
- Express.js

### Image Upload Interface
- React
- Vite
- JavaScript
- HTML
- CSS

---

## 📊 Dataset Description

- The dataset consists of labeled dog images belonging to multiple dog breeds  
- Images are organized by breed for supervised learning  
- Raw images are cleaned and preprocessed before training  
- Preprocessing steps include:
  - Image resizing
  - RGB normalization
  - Removal of corrupted images
- The cleaned dataset is used to train the EfficientNet-based classification model

---

## 🔄 Optional: Retrain the Model

If you want to retrain the dog breed classification model, follow these steps.

### 1️⃣ Navigate to TrainingModel directory

```bash
cd TrainingModel
```

### 2️⃣ Run the training script

```bash
python train.py
```

- The model will be trained on the preprocessed dataset  
- Training logs are saved in:
  ```
  training_log.csv
  ```
- The trained model will be saved as:
  ```
  efficientnetb3_clean_rgb.h5
  ```

You can replace the existing model with the newly trained one for updated predictions.

---

## 📄 Project Summary 

Developed a **Dog Breed Image Classification** system using deep learning techniques.  
Implemented data preprocessing, trained an EfficientNet-based model, and enabled image-based predictions through a simple interface.  
The project demonstrates practical experience in **image classification**, **model training**, and **deployment-ready inference workflows**.

---

## 👨‍💻 Author

**Shaik Abdul Hanif**

- Project: Dog Breed Image Classification  
- Focus Area: Deep Learning & Image Classification  

🔗 GitHub: https://github.com/SHAIKHANIF2004








