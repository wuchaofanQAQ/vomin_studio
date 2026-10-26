import yaml
d = yaml.safe_load(open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\workspace.yaml", encoding="utf-8"))
print(d["feishu"]["tables"].get("道具库"))
print(sorted(d["feishu"]["tables"].keys()))
