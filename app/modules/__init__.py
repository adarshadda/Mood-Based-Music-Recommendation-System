import os
import time

from modules.emotion import Emotion
from modules.transcription import Transcription

transcription_model = "tiny.en"
emotion_model = "joeddav/distilbert-base-uncased-go-emotions-student"

transcription_obj = Transcription(model_name=transcription_model)
emotion_obj = Emotion(model_name=emotion_model)

class Module:

    def predict(self, audio_path: str) -> str:
        """Loads audio, gets transcription and detects emotion

        Args:
            audio_path (str): path to the audio file

        Returns:
            str: emotion
        """
        print("Getting transcription...")
        start_time = time.time()
        if text := transcription_obj.transcribe(audio_path=audio_path):
            print("Text: ", text, time.time() - start_time)
            
            start_time = time.time()
            emotion = emotion_obj.detect_emotion(text=text)
            print("Emotion: ", emotion, time.time() - start_time)
            return text, emotion
        return None
        
