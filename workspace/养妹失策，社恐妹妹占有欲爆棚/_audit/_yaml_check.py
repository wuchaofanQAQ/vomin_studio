import yaml, io
p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\workspace.yaml"
d = yaml.safe_load(open(p, encoding="utf-8"))
print(list(d["feishu"]["tables"].keys()))
print(d["feishu"]["tables"].get("场景库"))
