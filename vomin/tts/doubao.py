import os
import base64
import requests


TTS_URL = "https://openspeech.bytedance.com/api/v3/tts/create"


class DoubaoTTS:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("DOUBAO_TTS_API_KEY", "")
        if not self.api_key:
            raise ValueError("缺少 DOUBAO_TTS_API_KEY")

    def create(self, text_prompt: str, *,
               speaker: str | None = None,
               model: str = "seed-audio-1.0",
               fmt: str = "mp3", sample_rate: int = 48000,
               speech_rate: int = 0, pitch_rate: int = 0,
               enable_subtitle: bool = False) -> dict:
        body = {
            "model": model,
            "text_prompt": text_prompt,
            "audio_config": {
                "format": fmt,
                "sample_rate": sample_rate,
                "speech_rate": speech_rate,
                "pitch_rate": pitch_rate,
                "enable_subtitle": enable_subtitle,
            },
            "watermark": {},
        }
        if speaker:
            body["references"] = [{"speaker": speaker}]

        resp = requests.post(
            TTS_URL,
            headers={
                "Content-Type": "application/json",
                "X-Api-Key": self.api_key,
            },
            json=body,
            timeout=300,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("code", 0) != 0:
            raise RuntimeError(f"TTS 失败: code={data.get('code')}, message={data.get('message')}")
        return data

    def create_to_file(self, text_prompt: str, save_path: str, **kwargs) -> dict:
        data = self.create(text_prompt, **kwargs)
        if data.get("audio"):
            os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(base64.b64decode(data["audio"]))
        return data
