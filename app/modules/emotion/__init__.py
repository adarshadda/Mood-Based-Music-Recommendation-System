from typing import Any

from modules.utils import Pipeline, load_model


class Emotion:
    task: str = "text-classification"
    
    def __init__(self, model_name: str) -> None:
        # model_name: str = "/models/distilbert-base-uncased-go-emotions-student/"
        print("Loading emotion model...")
        self.emotion_model: Pipeline = load_model(task=self.task, model=model_name)
        print("Loaded emotion model")
    
    def detect_emotion(self, text: str) -> str:
        """Detects emotion of the given text

        Args:
            text (str): text

        Returns:
            str: emotion
        """
        return self.emotion_model(text)[0]['label']