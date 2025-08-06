
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
<img width="1900" height="907" alt="Screenshot 2025-08-07 010907" src="https://github.com/user-attachments/assets/d5b7f0d4-2b26-4f44-9c01-5af6341fba66" />
<img width="1903" height="884" alt="Screenshot 2025-08-07 010920" src="https://github.com/user-attachments/assets/5d7b4a1a-a424-4dcb-8b79-f5facda2e3bf" />
<img width="1824" height="905" alt="Screenshot 2025-08-07 010933" src="https://github.com/user-attachments/assets/bc384c5a-fc6c-45ff-90db-fd985454f22a" />
<img width="1911" height="891" alt="Screenshot 2025-08-07 010952" src="https://github.com/user-attachments/assets/e192b28e-960f-4ee1-9c57-8367df117472" />
<img width="1905" height="864" alt="Screenshot 2025-08-07 011114" src="https://github.com/user-attachments/assets/724f3f67-5e6a-4c3e-b258-8ef175f05347" />
<img width="1914" height="967" alt="Screenshot 2025-08-07 011126" src="https://github.com/user-attachments/assets/3c0d78c3-7761-497d-ad63-4602169098a4" />
<img width="1895" height="931" alt="Screenshot 2025-08-07 011143" src="https://github.com/user-attachments/assets/008d604a-01c9-4946-807f-a237a551c5aa" />
<img width="1905" height="890" alt="Screenshot 2025-08-07 011155" src="https://github.com/user-attachments/assets/343334ed-05a4-414b-87c6-efa9aa73a651" />
## 🙏 Credits

Created by [Dhruv](https://github.com/Dhruv821-oss)


