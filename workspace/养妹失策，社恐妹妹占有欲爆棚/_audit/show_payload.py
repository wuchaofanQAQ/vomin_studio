# -*- coding: utf-8 -*-
import sys, os, json, base64
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
shots = ws.load_storyboard()
shot = next(s for s in shots if s.get("shot_id") == "ep01_p01")

final_prompt, ref_images, chars, scenes, ref_videos = ws.expand_prompt(shot["prompt"])
cfg = ws.config
ark = cfg.get("ark", {})
model = shot.get("model") or ark.get("video_model")
dur = 30

print("=== 请求体（base64 已折叠） ===")
print("model:", model)
print("resolution:", ark.get("default_resolution"), "| ratio:", ark.get("default_ratio"),
      "| duration:", dur, "| generate_audio:", bool(ark.get("generate_audio", True)),
      "| watermark: False")
print("content 条数:", 1 + len(ref_images))
print()
print("[0] type=text, len=%d" % len(final_prompt))
print("    开头:", final_prompt[:60].replace("\n", " "))
print()
total = len(final_prompt)
for i, p in enumerate(ref_images, start=1):
    b = os.path.getsize(p)
    total += int(b * 4 / 3)
    print(f"[{i}] type=image_url, role=reference_image, {b/1024:.0f} KB, {ws.rel(p)}")
print()
print("估算 JSON 体积: %.1f MB" % (total / 1024 / 1024))
print()
print("=== 提示词全文 ===")
print(final_prompt)
