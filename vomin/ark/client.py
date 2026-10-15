import os
import time
import requests

ARK_BASE = "https://ark.cn-beijing.volces.com/api/v3"


class ArkError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 0, request_id: str = ""):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.request_id = request_id
        super().__init__(f"[{code}] {message}")


class ArkClient:
    def __init__(self, api_key: str | None = None, timeout: int = 300):
        self.api_key = api_key or os.environ.get("ARK_API_KEY", "")
        if not self.api_key:
            raise ValueError("缺少 ARK_API_KEY，请设置环境变量或写入 .env")
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {self.api_key}"
        self.timeout = timeout

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{ARK_BASE}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)
        resp = self.session.request(method, url, **kwargs)
        if resp.status_code >= 400:
            try:
                err = resp.json().get("error", resp.json())
            except Exception:
                err = {"code": "Unknown", "message": resp.text[:200]}
            raise ArkError(
                code=err.get("code", "Unknown"),
                message=err.get("message", str(err)),
                status_code=resp.status_code,
                request_id=resp.headers.get("x-request-id", ""),
            )
        return resp

    def poll_task(self, task_id: str, *, timeout_sec=600, interval=10) -> dict:
        deadline = time.time() + timeout_sec
        while time.time() < deadline:
            resp = self.request("GET", f"/contents/generations/tasks/{task_id}")
            task = resp.json()
            status = task["status"]
            if status in ("succeeded", "failed", "cancelled"):
                return task
            print(f"  任务 {task_id} 状态: {status}，等待 {interval}s...")
            time.sleep(interval)
        raise TimeoutError(f"任务 {task_id} 轮询超时 ({timeout_sec}s)")
