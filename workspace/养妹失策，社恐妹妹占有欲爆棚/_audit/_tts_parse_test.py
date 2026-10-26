import sys, os
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
import cli
prompt = """【资产锁定】
【镜头06｜00:08.5-00:11｜门缝】
……
【对白 00:09-00:10.5】R02陈诚画外音（画右门板后、压低地说）：谁啊？
【对白 00:18.5-00:20】R02陈诚（内心独白、嘴唇不动地说）：沈幼怡。这三个字，
【对白 0-2s】陈诚：老格式也要能解析。
"""
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
d = cli._dialogue_from_prompt(prompt)
print("RAW:\n" + d)
print("LINES:", cli._dialogue_lines({"dialogue": d}, "旁白"))
