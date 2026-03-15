from flask import Flask, render_template, request
from pdfminer.high_level import extract_text
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

skills = [
"python","java","html","css","javascript",
"sql","react","docker","c","flask",
"machine learning","django","node","mongodb"
]

@app.route("/", methods=["GET","POST"])
def index():

    matched = []
    missing = []
    score = 0

    if request.method == "POST":

        job = request.form["job"].lower()

        file = request.files["resume"]

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        resume_text = extract_text(filepath).lower()

        for skill in skills:
            if skill in resume_text and skill in job:
                matched.append(skill)
            elif skill in job:
                missing.append(skill)

        if len(matched)+len(missing) > 0:
            score = int((len(matched)/(len(matched)+len(missing)))*100)

    return render_template("index.html",
                           score=score,
                           matched=matched,
                           missing=missing)

if __name__ == "__main__":
    app.run(debug=True)