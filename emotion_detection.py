import os
import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)

WATSON_HEADERS = {
    "grpc-metadata-mm-model-id":
        "emotion_aggregated-workflow_lang_en_stock"
}


def _empty_result():
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None
    }


def _local_detector(text):
    """Small offline fallback so the complete Flask app can run locally."""
    groups = {
        "anger": [
            "angry", "anger", "furious", "mad", "hate", "annoyed",
            "irritated", "rage"
        ],
        "disgust": [
            "disgust", "disgusted", "gross", "awful", "nasty", "revolting"
        ],
        "fear": [
            "afraid", "fear", "scared", "terrified", "worried", "anxious"
        ],
        "joy": [
            "happy", "happiness", "joy", "great", "excellent", "love",
            "excited", "wonderful", "good", "fantastic"
        ],
        "sadness": [
            "sad", "sadness", "unhappy", "depressed", "cry", "lonely",
            "bad", "sorry"
        ]
    }

    lower_text = text.lower()
    scores = {}

    for emotion, words in groups.items():
        score = 0
        for word in words:
            if word in lower_text:
                score += 1
        scores[emotion] = score

    maximum = max(scores.values())

    if maximum == 0:
        dominant = "joy"
        scores["joy"] = 1
        maximum = 1
    else:
        dominant = max(scores, key=scores.get)

    total = sum(scores.values())

    result = {}
    for emotion in scores:
        result[emotion] = round(scores[emotion] / total, 4)

    result["dominant_emotion"] = dominant
    return result


def emotion_detector(text_to_analyse):
    """
    Detect emotions.

    Default mode is Watson. Set EMOTION_MODE=local to run the
    complete application without depending on the remote lab endpoint.
    """
    if not text_to_analyse or not text_to_analyse.strip():
        return _empty_result()

    mode = os.getenv("EMOTION_MODE", "watson").lower()

    if mode == "local":
        return _local_detector(text_to_analyse)

    input_json = {
        "raw_document": {
            "text": text_to_analyse
        }
    }

    response = requests.post(
        WATSON_URL,
        json=input_json,
        headers=WATSON_HEADERS,
        timeout=30
    )

    if response.status_code == 400:
        return _empty_result()

    response.raise_for_status()

    result = response.json()
    emotions = result["emotionPredictions"][0]["emotion"]

    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
        "dominant_emotion": dominant_emotion
    }