
# 🧬 Hope Hub – AI-Powered Cancer Detection Platform

**Hope Hub** is an intelligent web application built with Flask that leverages deep learning models to detect cancer types (Skin, Brain, and Lung) from uploaded medical images. With a clean and accessible user interface, secure login system, and real-time PDF reporting, Hope Hub aims to empower early detection and healthcare awareness through AI.

---

## 💡 Key Features

* 🎯 **Multi-Type Cancer Detection**: Detects:

  * Skin Cancer (Benign / Malignant)
  * Brain Tumors (Glioma, Meningioma, Pituitary, Healthy)
  * Lung Diseases (Opacity, Pneumonia, Normal)

* 📁 **Image Upload & Prediction**: Upload a `.jpg` or `.png` image and get predictions from trained deep learning models.

* 🧾 **PDF Report Generation**: Automatically generate a detailed, downloadable PDF diagnosis report including your name, age, cancer type, and prediction.

* 👤 **User Authentication**: Secure signup/login system with SQLite3 database.

* 🗂 **Real-Time Dataset Logging**: Stores every prediction in a research-friendly CSV file with associated image.

* 📰 **Live Health News**: Fetches and displays the latest healthcare-related headlines via News API.

* 🧠 **Models Powered By**: TensorFlow & Keras trained models (`.h5`) loaded at runtime.

---

## ⚙️ Technologies Used

* **Frontend**: HTML5, CSS, Jinja2 Templates (via Flask)
* **Backend**: Flask (Python), SQLite3 for user management
* **ML Models**: TensorFlow/Keras (`.h5` models)
* **PDF Reports**: ReportLab
* **Health News API**: NewsAPI.org
* **Image Handling**: PIL, NumPy
* **File Storage**: Auto-log of predictions with download options
* **Dataset Management**: ZIP compression + CSV logging

---

## 🛠 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/Dhruv821-oss/Hope-Hub.git
cd Hope-Hub
```

2. **Create Virtual Environment (Optional but Recommended)**

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the App**

```bash
python app.py
```

The app will be available at `http://localhost:5000`.

---

## 🧪 Models & Files

> Large `.h5` files are stored via **Git Large File Storage (Git LFS)** due to GitHub’s 100MB limit.
> Ensure you have Git LFS installed:

```bash
git lfs install
git lfs pull
```

**Model Directory Structure:**

```
models/
├── skin_cancer_binary_model.h5
├── brain_tumor_classifier.h5
└── lung_model.h5
```

---



## 🙏 Credits

Created by [Dhruv](https://github.com/Dhruv821-oss)


