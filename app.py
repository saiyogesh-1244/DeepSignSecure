
import os
import cv2
import numpy as np
import uuid

from flask import Flask, request, render_template, redirect, url_for, flash
from tensorflow.keras.models import model_from_json

# Authentication & Database Libraries
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)

# Initialize Flask Application
app = Flask(__name__)
app.secret_key = "super_cool_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create Upload Directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Database & Security
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# User Database Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Load Deep Learning Model
MODEL_DIR = 'model'
json_path = os.path.join(MODEL_DIR, 'model100.json')
weights_path = os.path.join(MODEL_DIR, 'model100.weights.h5')

with open(json_path, 'r') as json_file:
    loaded_model_json = json_file.read()

model = model_from_json(loaded_model_json)
model.load_weights(weights_path)

print("System Initialized: Colab CNN Model loaded successfully!")


# OpenCV Preprocessing Pipeline
def preprocess_signature(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Unable to read uploaded image.")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(img_rgb, (64, 64))
    normalized = resized / 255.0

    return np.expand_dims(normalized, axis=0)


# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'warning')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))

        flash('Login Unsuccessful. Please check username and password.', 'danger')

    return render_template('login.html')


# Logout Route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# Team Route
@app.route('/team')
def team():
    return render_template('team.html')


# About Route
@app.route('/about')
def about():
    return render_template('about.html')


# Home Route
@app.route('/')
@login_required
def index():
    return render_template('index.html')


# Contact Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        print(name, email, message)

        flash("Message sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')


# Signature Upload & Verification Route
@app.route('/upload', methods=['POST'])
@login_required
def upload_signature():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    ext = file.filename.rsplit('.', 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        processed_img = preprocess_signature(filepath)

        prediction = model.predict(processed_img)
        score = float(prediction[0][0])

        # Check uncertain predictions
        if 0.4 < score < 0.6:
            flash("Please upload a clearer signature image!", "danger")
            return redirect(url_for('index'))

        # Classification
        if score > 0.5:
            result = "Genuine"
            confidence = round(score * 100, 2)
        else:
            result = "Forgery"
            confidence = round((1 - score) * 100, 2)

        return render_template(
            'result.html',
            result=result,
            confidence=confidence,
            image_url=filename
        )

    except Exception as e:
        print("Signature verification error:", e)
        flash("Unable to process this image. Please try again.", "danger")
        return redirect(url_for('index'))


# Run Flask Application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)
