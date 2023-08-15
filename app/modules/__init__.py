from modules.audio import Audio
from modules.emotion import Emotion
from modules.transcription import Transcription


class Module:
    @classmethod
    def predict(cls, audio_path: str) -> str:
        """Loads audio, gets transcription and detects emotion

        Args:
            audio_path (str): path to the audio file

        Returns:
            str: emotion
        """
        audio_data = Audio.load_audio(audio_path=audio_path)
        text = Transcription.transcribe(audio_data=audio_data)
        return Emotion.detect_emotion(text=text)
        
