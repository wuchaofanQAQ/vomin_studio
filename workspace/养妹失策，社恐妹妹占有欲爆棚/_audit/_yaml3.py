import yaml
d = yaml.safe_load(open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\workspace.yaml", encoding="utf-8"))
print("top:", list(d.keys()))
print("ark:", d.get("ark"))
print("budget:", d.get("budget"))
print("tts:", d.get("tts"))
print("url:", d["feishu"].get("url"))
print("app_token:", d["feishu"].get("app_token"))
print("drama_name:", d.get("drama_name"))
