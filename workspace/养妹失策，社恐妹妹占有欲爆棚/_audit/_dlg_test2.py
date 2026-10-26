import sys
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
import cli
prompt = """【对白 00:09-00:10.5】R02陈诚画外音（画面右后方的门板后、压低地说）：谁啊？
【对白 00:18.5-00:20】R02陈诚（内心独白、嘴唇不动地说）：沈幼怡。这三个字，
【对白 00:20-00:21】陈诚：老格式，冒号：在正文里也要能解析。
"""
d = cli._dialogue_from_prompt(prompt)
print(cli._dialogue_lines({"dialogue": d}, "旁白"))
