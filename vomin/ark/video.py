import os
import requests as req

from .client import ArkClient


class VideoClient:
    def __init__(self, client: ArkClient):
        self.c = client

    def create(self, *, model: str, content: list[dict],
               resolution="720p", ratio="9:16", duration=5,
               generate_audio=True, watermark=False,
               seed: int | None = None, draft: bool = False) -> str:
        body = {
            "model": model,
            "content": content,
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "generate_audio": generate_audio,
            "watermark": watermark,
        }
        if seed is not None:
            body["seed"] = seed
        if draft:
            body["draft"] = True
        resp = self.c.request("POST", "/contents/generations/tasks", json=body)
        return resp.json()["id"]

    def get(self, task_id: str) -> dict:
        return self.c.request("GET", f"/contents/generations/tasks/{task_id}").json()

    def cancel(self, task_id: str) -> dict:
        return self.c.request("DELETE", f"/contents/generations/tasks/{task_id}").json()

    def create_and_download(self, *, model: str, content: list[dict],
                            save_path: str, **kwargs) -> dict:
        task_id = self.create(model=model, content=content, **kwargs)
        print(f"  视频任务已提交: {task_id}")
        task = self.c.poll_task(task_id)
        if task["status"] != "succeeded":
            raise RuntimeError(f"视频任务失败: {task.get('error')}")
        video_url = task["content"]["video_url"]
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        with req.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
        print(f"  视频已下载: {save_path}")
        return {**task, "local_path": save_path}
