# Emotion Detector

A Flask-based emotion detection web application.

## Features

- Emotion detection for anger, disgust, fear, joy and sadness
- Dominant emotion detection
- Flask web interface
- Error handling for blank input
- Unit tests
- Pylint static analysis
- Watson NLP integration
- Offline local mode for development

## Project Structure

```text
EmotionDetection/
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── server.py
├── test_emotion_detection.py
├── requirements.txt
└── README.md
```

## Run locally without the remote Watson endpoint

PowerShell:

```powershell
$env:EMOTION_MODE="local"
python server.py
```

Open:

```text
http://127.0.0.1:5000/
```

## Run with Watson

Remove the local mode variable:

```powershell
Remove-Item Env:EMOTION_MODE -ErrorAction SilentlyContinue
python server.py
```

The Watson endpoint must be reachable from your network/lab environment.

## Run tests

```powershell
python -m unittest test_emotion_detection.py -v
```

## Static analysis

```powershell
pylint server.py
```
