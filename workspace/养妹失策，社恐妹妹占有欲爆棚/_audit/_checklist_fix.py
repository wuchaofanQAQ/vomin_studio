# -*- coding: utf-8 -*-
p = r"skills\drama-asset-generation\references\review-checklist.md"
t = open(p, encoding="utf-8").read()
old = '''| 3 | 背景 | 绿幕或纯白，干净可抠 |
| 4 | 无文字 | 没有文字、水印、logo、价签 |
| 5 | 材质 | 材质与使用痕迹真实（金属、皮质、塑料分得清） |
| 6 | 与描述一致 | 尺寸、颜色、磨损与资产描述一致 |'''
new = '''| 3 | 无人 | 画面里只有道具，没有人物、没有人手、没有支架 |
| 4 | 背景 | 绿幕或纯白，干净可抠 |
| 5 | 无文字 | 没有文字、水印、logo、价签 |
| 6 | 材质 | 材质与使用痕迹真实（金属、皮质、塑料分得清） |
| 7 | 与描述一致 | 尺寸、颜色、磨损与资产描述一致 |'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("checklist updated")
