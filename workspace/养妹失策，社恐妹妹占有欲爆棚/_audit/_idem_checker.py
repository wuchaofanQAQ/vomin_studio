# -*- coding: utf-8 -*-
p = r"skills\script-asset-extraction\scripts\check_assets.py"
t = open(p, encoding="utf-8").read()

# 参数
t = t.replace('''    ap.add_argument("--max-desc", type=int, default=50)''',
'''    ap.add_argument("--max-desc", type=int, default=50)
    ap.add_argument("--library", default="", help="workspace 目录（含 characters.json / scenes.json / props.json），用于幂等检查")''')

# 归一化 + 读库
t = t.replace('''def clen(s: str) -> int:''',
'''def norm_name(s: str) -> str:
    """名字归一：去空白、半角括号统一成全角、英文小写，用于跨次幂等比对。"""
    n = re.sub(r"\\s+", "", s or "")
    n = n.replace("(", "（").replace(")", "）")
    return n.lower()


def load_library(path: str) -> dict[str, set[str]]:
    """读 workspace 里的三张资产表缓存，返回 {type: {归一化名字}}。"""
    lib = {"角色": set(), "场景": set(), "道具": set()}
    if not path:
        return lib
    base = Path(path)
    for kind, fname in (("角色", "characters.json"), ("场景", "scenes.json"), ("道具", "props.json")):
        fp = base / fname
        if not fp.exists():
            continue
        try:
            rows = json.loads(fp.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        for r in rows:
            if r.get("name"):
                lib[kind].add(norm_name(r["name"]))
    return lib


def clen(s: str) -> int:''')

# check 签名 + 逻辑
t = t.replace("def check(doc: dict, limit: int) -> tuple[list[tuple[str, bool, str]], list[str]]:",
              "def check(doc: dict, limit: int, lib: dict[str, set[str]] | None = None) -> tuple[list[tuple[str, bool, str]], list[str]]:")
t = t.replace('''    reused = doc.get("reused") or []
    missing = doc.get("missing") or []''',
'''    reused = doc.get("reused") or []
    missing = doc.get("missing") or []
    lib = lib or {"角色": set(), "场景": set(), "道具": set()}''')

t = t.replace('''        names = [r.get("name", "").strip() for r in rows]
        dup = {n for n in names if n and names.count(n) > 1}''',
'''        names = [norm_name(r.get("name", "")) for r in rows]
        dup = {n for n in names if n and names.count(n) > 1}''')

t = t.replace('''            status = r.get("status")
            if status not in ("新建", "复用"):
                errors.append(f"{who} status 必须是 新建/复用，当前 {status!r}")
            if status == "复用":
                continue''',
'''            status = r.get("status")
            if status not in ("新建", "复用"):
                errors.append(f"{who} status 必须是 新建/复用，当前 {status!r}")
            key = norm_name(name)
            if status == "复用":
                if key not in lib[label]:
                    errors.append(f"{who} 标了复用，但库里没有同名资产")
                continue
            if key in lib[label]:
                errors.append(f"{who} 库里已有同名资产（多次提取会重复插入）；标复用或改名区分")''')

t = t.replace('''    checks, errors = check(doc, args.max_desc)''',
'''    lib = load_library(args.library)
    checks, errors = check(doc, args.max_desc, lib)''')

open(p, "w", encoding="utf-8").write(t)
print("checker idempotency added")
