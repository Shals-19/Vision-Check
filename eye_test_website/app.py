from flask import Flask, render_template, jsonify, request, redirect, url_for, Response
from datetime import datetime
import cv2

app = Flask(__name__, static_folder='static')
app = Flask(__name__)

# Define Node class and questionnaire logic
class Node:
    def __init__(self, question, symptom=None, yes=None, no=None, image = None):
        self.question = question
        self.symptom = symptom
        self.yes = yes
        self.no = no
        self.image = image

# Initialize the decision tree
root = Node(
    question="Are you experiencing blurred vision?",
    yes=Node(
        question="Do you have eye strain?",
        yes=Node(
            question="Do you have frequent head aches?",
            yes=Node(
                question="Do you have blurred vision at all distances?",
                yes=Node(
                    question = "Do headlights of vehicles in the night appear as lines?.",
                    image="linedlights.jpg",
                    yes=Node(
                        question = "Please consult a doctor.",
                        symptom="Astigmatism"
                    )
                ),
                no=Node(
                    question="Blurred vision at only some distances?",
                    yes=Node(
                        question="Are you not able to see far away objects like billboards clearly?",
                        image="static/billboard.jpg",
                        yes=Node(
                            question="When sitting in the back of  lecture halls or classes, do you find it difficult to read what is written on the board?",
                            image="static/lecturehall.jpg",
                            yes=Node(
                                question="Far distances?",
                                symptom="Myopia"
                            )
                        ),
                        no=Node(
                            question="Are you not able to see nearby objects clearly?",
                            yes=Node(
                                question="Do you hold books or newspapers away from you, in order to read comfortably?",
                                image="static/books.jpg",
                                yes=Node(
                                    question="Far distances?",
                                    symptom="Hyperopia"
                                )
                            )
                        )
                    )
                )
            ),
            no=Node(
                question="Do you also face sensitivity towards light?",
                yes=Node(
                    question="Do you experience cloudy vision, wherein blurring happens only at somespots?",
                    yes=Node(
                        question="Do you experience double vision?",
                        yes=Node(
                            question = "Are you above the age of 40-50?.",
                            yes=Node(
                                question = "Please consult a doctor.",
                                symptom="Cataract"
                            )
                        ),
                        no=Node(
                            question="Do you experience any blank or dark spots around your central vision?",
                            image="static/centraldarkspots.jpg",
                            yes=Node(
                                question="Do you find it hard to recognizing faces?",
                                yes=Node(
                                    question = "Please consult a doctor.",
                                    symptom="AMD"
                                )
                            ),
                            no=Node(
                                question="Do you experience any blank or dark spots or blurring in the edges of your vision?",
                                image="static/peripheraldarkspots.jpg",
                                yes=Node(
                                    question="Do you experience difficulty in seeing at night time?",
                                    yes=Node(
                                        question="Consult a doctor",
                                        symptom="Retinitis Pigmentosa"
                                    )
                                )
                            )
                        )
                    ),
                    no = Node(
                        question = "Do you experience any sharp pain in your eyes?",
                        yes=Node(
                            question="Do you experience any blank or dark spots or blurring in the edges of your vision?",
                            image="linedlights.jpg",
                            yes=Node(
                                question = "Please consult a doctor.",
                                symptom = "Glaucoma"
                            ),
                            no=Node(
                                question = "Have you had any eye injuries or eye surgeries recently?",
                                yes=Node(
                                    question = "Please consult a doctor.",
                                    symptom = "Corneal Abrasions"
                                )
                            )
                        ),
                        no=Node(
                            question="Do you get eye fatigue even after short times?",
                            yes=Node(
                                question = "Do you get the feeling that something is there in your eye?",
                                yes=Node(
                                    question = "Please consult a doctor.",
                                    symptom="Dry eye syndrome"
                                )
                            )
                        )
                    )
                ),  
                no=Node(
                    question="Do you get any sensation of pressure in the eyes?",
                    yes=Node(
                        question = "Please consult a doctor.",
                        symptom="Eye Cancer"
                    )
                )
            )
        ),
        no=Node(
            question="Have you experienced Gradual or Sudden vision loss",
            yes=Node(
                question = "Please consult a doctor.",
                symptom="Optical Neuropathy"
            )
        )
    ),
    no=Node(
        question="Do you have trouble distinguishing between colours?",
        yes=Node(
            question = "Please consult a doctor.",
            symptom="Color Blindness"
        )
    )
)
current_node = root

@app.route("/questionnaire", methods=["GET", "POST"])
def diagnose():
    global current_node
    if request.method == "POST":
        response = request.form.get("response")
        if response == "yes" and current_node.yes:
            current_node = current_node.yes
        elif response == "no" and current_node.no:
            current_node = current_node.no

        if not current_node.yes and not current_node.no:
            return render_template("decision.html", symptom=current_node.symptom)

    return render_template("diagnosis.html", question=current_node.question)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/distance")
def distance():
    return render_template("distance.html")

KNOWN_WIDTH = 15.0  # Average width of a human face in cm
KNOWN_DISTANCE = 60.0  # Distance to the object during calibration (cm)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
focal_length = None  # Global focal length variable

def calculate_focal_length(apparent_width):
    return (apparent_width * KNOWN_DISTANCE) / KNOWN_WIDTH

def calculate_distance(apparent_width, focal_length):
    return (KNOWN_WIDTH * focal_length) / apparent_width

def generate_frames():
    global focal_length
    cap = cv2.VideoCapture(0)
    calibrated = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if not calibrated and len(faces) > 0:
            (x, y, w, h) = faces[0]
            focal_length = calculate_focal_length(w)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Calibration Done", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            calibrated = True

        for (x, y, w, h) in faces:
            if focal_length:
                distance = calculate_distance(w, focal_length)
                cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    cap.release()

# @app.route("/distance")
# def distance():
#     return render_template("distance.html")

@app.route("/distance_feed")
def distance_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/visual-acuity')
def visual_acuity():
    return render_template('visual_acuity.html')

@app.route('/color-vision')
def color_vision():
    return render_template('color_vision.html')

@app.route('/astigmatism')
def astigmatism():
    return render_template('astigmatism.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/screentime')
def screentime():
    return render_template('screentime.html')

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/lens-adjustment")
def lens_adjustment():
    return render_template("lens_adjustment.html")

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/reset")
def reset():
    global current_node
    current_node = root
    return redirect(url_for("diagnose"))

# @app.route("/api/save-results", methods=["POST"])
# def save_results():
#     results = request.json
#     return jsonify({
#         "status": "success",
#         "timestamp": datetime.now().isoformat(),
#         "results": results
#     })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
