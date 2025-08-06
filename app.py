from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from werkzeug.utils import secure_filename
import os
import numpy as np
import requests
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from reportlab.pdfgen import canvas
import sqlite3
import shutil
from flask import send_file
import zipfile



# Initialize app
app = Flask(__name__)
app.secret_key = "dhruv_super_secret_key_723#@!"
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('reports', exist_ok=True)

# Load ML models
skin_model = load_model('models/skin_cancer_binary_model.h5')
brain_model = load_model('models/brain_tumor_classifier.h5')
lung_model = load_model('models/lung_model.h5')

# Class labels
skin_classes = ['Benign', 'Malignant']
brain_classes = ['Glioma', 'Healthy', 'Meningioma', 'Pituitary']
lung_classes = ['Lung Opacity', 'Normal', 'Pneumonia']

# Prepare image for model
def prepare_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array / 255.0

# Generate PDF report
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os

def generate_report(prediction, cancer_type, filename_base, user_info, image_path):
    report_path = f"reports/{filename_base}_report.pdf"
    c = canvas.Canvas(report_path, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height-20,"Hope Hub")
    c.drawString(50, height - 50, "Cancer Detection Report")

    # Date
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # User Info
    c.drawString(50, height - 110, f"Name: {user_info['name']}")
    c.drawString(50, height - 130, f"Email: {user_info['email']}")
    c.drawString(50, height - 150, f"Age: {user_info['age']}")

    # Prediction Info
    c.drawString(50, height - 180, f"Cancer Type: {cancer_type}")
    c.drawString(50, height - 200, f"Prediction Result: {prediction}")
    c.drawString(50, height - 220, "Recommendation: Please consult a certified oncologist.")

    # Insert uploaded image
    if os.path.exists(image_path):
        try:
            img = ImageReader(image_path)
            img_width, img_height = img.getSize()
            aspect = img_height / img_width

            display_width = 300
            display_height = display_width * aspect

            # Place image lower on the page
            c.drawImage(img, 50, height - 500, width=display_width, height=display_height)
        except Exception as e:
            c.drawString(50, height - 250, f"[Error displaying image in PDF: {str(e)}]")

    # Footer
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 100, "Thank you for using our service.")

    c.save()
    return report_path


# Fetch health news
NEWS_API_KEY = "61bc51da11e2429dbd460e912b816d50"
NEWS_URL = f"https://newsapi.org/v2/top-headlines?category=health&language=en&apiKey={NEWS_API_KEY}"

def fetch_news():
    try:
        response = requests.get(NEWS_URL)
        articles = response.json().get("articles", [])[:5]
        return articles
    except Exception as e:
        print("News API Error:", e)
        return []

# Routes
@app.route('/')
def index():
    news_items = fetch_news()
    return render_template('index.html', news=news_items)

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if 'user_id' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for('login'))
    return render_template('detect.html')

import csv
from datetime import datetime

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files or request.files['image'].filename == '':
        return render_template("detect.html", error="Please upload an image.")

    file = request.files['image']
    cancer_type = request.form.get('cancer_type')
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    img = prepare_image(filepath)

    try:
        if cancer_type == 'Skin':
            preds = skin_model.predict(img)
            prediction = skin_classes[np.argmax(preds)]
        elif cancer_type == 'Brain':
            preds = brain_model.predict(img)
            prediction = brain_classes[np.argmax(preds)]
        elif cancer_type == 'Lung':
            preds = lung_model.predict(img)
            prediction = lung_classes[np.argmax(preds)]
        else:
            return render_template("detect.html", error="Invalid cancer type selected.")

        filename_base = os.path.splitext(filename)[0]

        # Generate PDF Report
        report_path = generate_report(
            prediction=prediction,
            cancer_type=cancer_type,
            filename_base=filename_base,
            user_info={
                "name": session.get("name"),
                "email": session.get("email"),
                "age": session.get("age")
            },
            image_path=filepath
        )

        # Save image & metadata to research dataset
        dataset_dir = os.path.join("static", "dataset")
        os.makedirs(dataset_dir, exist_ok=True)
        dataset_image_path = os.path.join(dataset_dir, filename)
        shutil.copyfile(filepath, dataset_image_path)  # Save image to dataset folder

        log_file = os.path.join(dataset_dir, "dataset_log.csv")
        user_info = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": session.get("name"),
            "email": session.get("email"),
            "age": session.get("age"),
            "cancer_type": cancer_type,
            "prediction": prediction,
            "image_filename": filename
        }

        # Log metadata to CSV
        file_exists = os.path.isfile(log_file)
        with open(log_file, mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=user_info.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(user_info)

        # News fetch (optional)
        news_items = fetch_news()

        return render_template("detect.html",
                               prediction=prediction,
                               report_url=url_for("download_report", filename=filename_base),
                               news=news_items)

    except Exception as e:
        return render_template("detect.html", error=f"Prediction failed: {str(e)}")


@app.route('/download/<filename>')
def download_report(filename):
    path = f'reports/{filename}_report.pdf'
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Report not found", 404

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        age = request.form.get("age")
        password = request.form.get("password")

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            # Ensure table exists
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                phone TEXT,
                age INTEGER,
                password TEXT
            )''')
            cursor.execute("INSERT INTO users (name, email, phone, age, password) VALUES (?, ?, ?, ?, ?)",
                           (name, email, phone, age, password))
            conn.commit()
            flash("Signup successful. Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already registered.", "error")
        finally:
            conn.close()
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            
            session["email"] = user[2]  # email
            session["name"] = user[1]   # name
            session["age"] = user[4]   
            flash("Login successful!", "success")
            return redirect(url_for('detect'))
        else:
            flash("Invalid credentials!", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))
@app.route('/awareness')
def awareness():
    return render_template("awareness.html")

@app.route('/dataset')
def view_dataset():
    dataset_dir = os.path.join('static', 'dataset')
    log_file = os.path.join(dataset_dir, 'dataset_log.csv')

    entries = []

    if os.path.exists(log_file):
        with open(log_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['image_path'] = url_for('static', filename=f'dataset/{row["image_filename"]}')
                entries.append(row)

    return render_template('dataset.html', entries=entries)


@app.route('/download_dataset')
def download_dataset():
    dataset_folder = os.path.join('static', 'uploads')
    zip_filename = 'cancer_dataset.zip'
    zip_path = os.path.join('static', zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(dataset_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dataset_folder)
                zipf.write(file_path, arcname)

    return send_file(zip_path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
