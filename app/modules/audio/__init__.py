from typing import Any

import whisper


class Audio:
    @classmethod
    def load_audio(cls, audio_path: str) -> Any:
        """Loads audio file from the disk

        Args:
            audio_path (str): path of the audio file

        Returns:
            Any: loaded audio file in numbers
        """
        return whisper.load_audio(audio_path)
    