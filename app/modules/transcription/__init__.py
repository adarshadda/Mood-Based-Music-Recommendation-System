import torch
from faster_whisper import WhisperModel


class Transcription:

    def __init__(self, model_name: str) -> None:
        print("Loading whisper model...")
        self.whisper_model = self.load_whisper(model_id=model_name)
        print("Loaded whisper model")
    
    def load_whisper(self, model_id: str):

        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = "float16" if torch.cuda.is_available() else "float32"

        return WhisperModel(model_id, device=device, compute_type=torch_dtype)
    
    def transcribe(self, audio_path: str) -> str:
        """Transcribes the given audio data

        Args:
            audio_path (str): audio path

        Returns:
            str: text
        """
        segments, info = self.whisper_model.transcribe(audio_path, language="en")
        return "".join(segment.text for segment in segments)
        
