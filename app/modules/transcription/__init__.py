from typing import Any

from modules.utils import Pipeline, load_model


class Transcription:
    task: str = "automatic-speech-recognition"
    model_name: str = "openai/whisper-medium"
    whisper_model: Pipeline = load_model(
        task=task,
        model=model_name
    )
    
    @classmethod
    def transcribe(cls, audio_data: Any) -> str:
        """Transcribes the given audio data

        Args:
            audio_data (Any): audio data

        Returns:
            str: text
        """
        return cls.whisper_model(audio_data)["text"]

