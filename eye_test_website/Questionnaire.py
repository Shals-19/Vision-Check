from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Node:
    def __init__(self, question, symptom=None, yes=None, no=None):
        self.question = question
        self.symptom = symptom
        self.yes = yes
        self.no = no

@app.route("/", methods=["GET", "POST"])
def diagnose():
    # Keep track of the current node using session or simple routing
    global current_node  # Simulating session for simplicity
    if "current_node" not in globals():
        current_node = root

    if request.method == "POST":
        response = request.form.get("response")
        if response == "yes" and current_node.yes:
            current_node = current_node.yes
        elif response == "no" and current_node.no:
            current_node = current_node.no

        # If it's a leaf node, render the diagnosis
        if not current_node.yes and not current_node.no:
            return render_template("decision.html", symptom=current_node.symptom)

    return render_template("diagnosis.html", question=current_node.question)

@app.route("/reset")
def reset():
    global current_node
    current_node = root
    return redirect(url_for("diagnose"))

root = Node(
    question="Are you experiencing blurred vision?",
    yes=Node(
        question="Do you have eye strain?",
        yes=Node(
            question="Do you have frequent head aches?",
            yes=Node(
                question="Do you have blurred vision at all distances?",
                yes=Node(
                    question = "Please consult a doctor.",
                    symptom="Astigmatism"
                ),
                no=Node(
                    question="Blurred vision at only some distances?",
                    yes=Node(
                        question="Are you not able to see far away objects like billboards or classroom boards clearly?",
                        yes=Node(
                            question="Far distances?",
                            symptom="Myopia"
                        ),
                        no=Node(
                            question="Are you not able to see nearby objects clearly? - like holding books farther away for comfort, etc.",
                            yes=Node(
                                question="Far distances?",
                                symptom="Myopia"
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
                            question = "Please consult a doctor.",
                            symptom="Cataract"
                        ),
                        no=Node(
                            question="Do you experience any blank or dark spots around your central vision?",
                            yes=Node(
                                question="Do you find it hard to recognizing faces?",
                                yes=Node(
                                    question = "Please consult a doctor.",
                                    symptom="AMD"
                                )
                            ),
                            no=Node(
                                question="Do you experience any blank or dark spots or blurring in the edges of your vision?",
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
                            yes=Node(
                                question = "Please consult a doctor.",
                                symptom="Glaucoma"
                            ),
                            no=Node(
                                question = "Please consult a doctor.",
                                symptom="Corneal Abrasions"
                            )
                        ),
                        no=Node(
                            question="Do you get eye fatigue even after short times?",
                            yes=Node(
                                question = "Please consult a doctor.",
                                symptom="Dry eye syndrome"
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

if __name__ == "__main__":
    app.run(debug=True)