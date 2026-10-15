import base64
import os
import requests as req

from .client import ArkClient


class ImageClient:
    def __init__(self, client: ArkClient):
        self.c = client

    def generate(self, *, model: str, prompt: str, size="2K",
                 n=1, response_format="url", watermark=False,
                 seed: int | None = None,
                 ref_images: list[str] | None = None) -> dict:
        body = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "n": n,
            "response_format": response_format,
            "watermark": watermark,
        }
        if seed is not None:
            body["seed"] = seed
        if ref_images:
            uris = []
            for img_path in ref_images:
                with open(img_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                ext = os.path.splitext(img_path)[1].lstrip(".") or "png"
                mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(ext, "image/png")
                uris.append(f"data:{mime};base64,{b64}")
            body["image"] = uris[0] if len(uris) == 1 else uris
        resp = self.c.request("POST", "/images/generations", json=body)
        return resp.json()

    def generate_to_dir(self, *, model: str, prompt: str,
                        save_dir: str, size="2K", n=1, **kw) -> list[str]:
        data = self.generate(model=model, prompt=prompt, size=size, n=n, **kw)
        os.makedirs(save_dir, exist_ok=True)
        paths = []
        for i, item in enumerate(data.get("data", [])):
            url = item.get("url")
            if not url:
                continue
            path = os.path.join(save_dir, f"img_{i}.png")
            with req.get(url, stream=True) as r:
                r.raise_for_status()
                with open(path, "wb") as f:
                    f.write(r.content)
            paths.append(path)
        return paths
