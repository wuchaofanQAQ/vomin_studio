p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_script_v2.md"
t = open(p, encoding="utf-8").read()
t = t.replace("陈诚（OS）：沈幼怡。这三个字，是他捂了六年的旧疤。",
              "陈诚（OS）：沈幼怡。这三个字，是他亲手捂了六年的旧疤。")
open(p, "w", encoding="utf-8").write(t)
print("fixed 亲手")
