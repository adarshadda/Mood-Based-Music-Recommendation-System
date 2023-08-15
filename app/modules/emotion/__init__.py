from typing import Any

from modules.utils import Pipeline, load_model


class Emotion:
    task: str = "text-classification"
    model_name: str = "joeddav/distilbert-base-uncased-go-emotions-student"
    emotion_model: Pipeline = load_model(
        task=task,
        model=model_name
    )
    
    @classmethod
    def detect_emotion(cls, text: str) -> str:
        """Detects emotion of the given text

        Args:
            text (str): text

        Returns:
            str: emotion
        """
        return cls.emotion_model(text)[0]['label']