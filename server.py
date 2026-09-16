"""Flask web server for the Emotion Detector application."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def home():
    """Render the Emotion Detector home page."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    """Analyze submitted text and render the detected emotions."""
    if request.method == "POST":
        text_to_analyse = request.form.get("text", "")
    else:
        text_to_analyse = request.args.get("text", "")

    if not text_to_analyse.strip():
        return render_template(
            "index.html",
            error="Please enter some text to analyse."
        )

    result = emotion_detector(text_to_analyse)

    if result["dominant_emotion"] is None:
        return render_template(
            "index.html",
            error="Unable to detect emotions."
        )

    return render_template(
        "index.html",
        text=text_to_analyse,
        anger=result["anger"],
        disgust=result["disgust"],
        fear=result["fear"],
        joy=result["joy"],
        sadness=result["sadness"],
        dominant_emotion=result["dominant_emotion"]
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
