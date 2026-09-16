import unittest
from unittest.mock import patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_joy(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.01,
                    "disgust": 0.01,
                    "fear": 0.01,
                    "joy": 0.95,
                    "sadness": 0.02
                }
            }]
        }

        result = emotion_detector("I am very happy today!")
        self.assertEqual(result["dominant_emotion"], "joy")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_anger(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.95,
                    "disgust": 0.01,
                    "fear": 0.01,
                    "joy": 0.01,
                    "sadness": 0.02
                }
            }]
        }

        result = emotion_detector("I am angry!")
        self.assertEqual(result["dominant_emotion"], "anger")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_sadness(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.01,
                    "disgust": 0.01,
                    "fear": 0.01,
                    "joy": 0.02,
                    "sadness": 0.95
                }
            }]
        }

        result = emotion_detector("I am sad.")
        self.assertEqual(result["dominant_emotion"], "sadness")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_disgust(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.01,
                    "disgust": 0.95,
                    "fear": 0.01,
                    "joy": 0.01,
                    "sadness": 0.02
                }
            }]
        }

        result = emotion_detector("This is disgusting!")
        self.assertEqual(result["dominant_emotion"], "disgust")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_fear(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.01,
                    "disgust": 0.01,
                    "fear": 0.95,
                    "joy": 0.01,
                    "sadness": 0.02
                }
            }]
        }

        result = emotion_detector("I am very scared!")
        self.assertEqual(result["dominant_emotion"], "fear")

    def test_blank_input(self):
        result = emotion_detector("")
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()