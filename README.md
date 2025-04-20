## 👁️ Eye Test Website

A smart, web-based application designed to help users perform basic eye tests at home. From visual acuity, lens adjustment test and color blindness checks to astigmatism detection and symptom-based questionnaires, this site combines accessibility with healthcare awareness — all in one interactive platform!

## 📌 Features

- Visual Acuity Test (reading distance-based test)
- Astigmatism Detection (radial blur-based patterns)
- Color Blindness Test (Ishihara plates)
- Vision Symptom Questionnaire (powered by Python logic)
- Lens Adjustment Test: Users adjust a blur slider to match their vision clarity, and the system estimates the range of eye power.
- Measures User Distance from Screen
- Maps Integration for Nearby Clinics
- Responsive UI with intuitive controls

## 🧠 Core Components

### Python Backend ###
- **app.py:** Flask backend for routing and page handling
- **Questionnaire.py:** Handles processing of vision symptom questionnaire

### JavaScript Integration ###
- **script.js:** Handles user interaction, distance measurement, and lens blur slider behavior

### Web Pages ###
- **index.html:** Homepage with access to all tests
- **page2.html:** Results or additional test page

## ⚙️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask), Node.js (optional backend with server.js)
- **UI Assets:** Static images, CSS styling, and test visuals

## 📂 Folder Structure

```
📁 eye_test_website
├── app.py
├── server.js
├── Questionnaire.py
├── index1.html
├── page2.html
├── styles.css
├── script.js
├── static/
│   ├── images/
│   ├── css/
│   └── test_assets/
├── package.json
├── package-lock.json
└── README.md
```

## ▶️ How to Run

1. **Install Python Dependencies**
   ```bash
   pip install flask
   ```
2. **Run the Backend Server**
   ```bash
   python app.py
   ```
3. **Open `index.html`** in the browser and begin testing
      
