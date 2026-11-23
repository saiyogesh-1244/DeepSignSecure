# DeepSignSecure – Handwritten Signature Verification

DeepSignSecure is a web-based handwritten signature verification application built using Python, Flask, and Deep Learning. It analyzes uploaded signature images and predicts whether a signature is **Genuine** or **Forged** using a trained Convolutional Neural Network (CNN) model.

## 🌐 Live Demo

**Website:** https://deepsignsecure.onrender.com

## 🚀 Features

- User registration and login authentication.
- Upload handwritten signature images.
- Image preprocessing using OpenCV.
- Deep Learning-based signature verification.
- Predicts whether a signature is Genuine or Forged.
- Displays prediction results through a web interface.
- Responsive interface using HTML, CSS, and JavaScript.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| TensorFlow / Keras | Deep Learning model |
| CNN | Signature classification |
| OpenCV | Image preprocessing |
| NumPy | Numerical operations |
| HTML | Web page structure |
| CSS | Website styling |
| JavaScript | Frontend interactions |
| Flask-SQLAlchemy | Database management |
| SQLite | User data storage |
| Render | Cloud deployment |
| GitHub | Source code management |

## 🧠 Model Information

The project uses a Convolutional Neural Network (CNN) for handwritten signature classification.

**Model files:**
- `model100.json` – Model architecture.
- `model100.weights.h5` – Trained model weights.

**Image preprocessing:**
1. Read the uploaded signature image.
2. Convert the image from BGR to RGB.
3. Resize the image to 64 × 64 pixels.
4. Normalize pixel values.
5. Pass the processed image to the trained CNN model.
6. Display the prediction result.

## 📁 Project Structure

```text
DeepSignSecure/
│
├── app.py
├── requirements.txt
├── README.md
├── .python-version
├── .gitignore
│
├── model/
│   ├── model100.json
│   └── model100.weights.h5
│
├── src/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── ...
│
└── instance/
```

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/saiyogesh-1244/DeepSignSecure.git
```

### 2. Navigate to the project directory

```bash
cd DeepSignSecure
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

For Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Flask application

```bash
python app.py
```

### 7. Open the application

Visit:

```text
http://127.0.0.1:5000
```

## ☁️ Deployment

The Flask application is deployed using **Render**.

- Source code is maintained on GitHub.
- Render connects to the GitHub repository.
- Gunicorn runs the Flask application in production.
- New changes pushed to the `main` branch can trigger automatic deployments.

**Live Application:** https://deepsignsecure.onrender.com

## 🔄 How It Works

1. The user registers or logs in.
2. The user uploads a handwritten signature image.
3. The application preprocesses the image.
4. The CNN model analyzes the processed image.
5. The application displays the prediction as Genuine or Forged.

## 🎯 Project Objective

The main objective of DeepSignSecure is to develop a web-based system that uses Deep Learning techniques to assist in handwritten signature verification and help distinguish genuine signatures from forged signatures.

## 👨‍💻 Author

**Sai Yogesh Gopisetti**

GitHub: https://github.com/saiyogesh-1244

---

*DeepSignSecure – Deep Learning Based Handwritten Signature Verification.*
