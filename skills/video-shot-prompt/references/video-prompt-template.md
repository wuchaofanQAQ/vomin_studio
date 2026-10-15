# CLIP 完整输出模板

## 输出结构（每个 CLIP 一份完整文件）

```
## 使用方式
（上传参考图的顺序 + 复制粘贴说明）

## 导演推理（❌ 不复制此部分给 Seedance）
- 时间铰链：镜头间连续关系
- Shot Function：每 Shot 叙事功能
- 张力机制：景别/运镜/节奏如何服务张力
- 演出弧线：角色本 CLIP 演出变化
- 站位：角色画面位置
- 质检：演出→人设匹配？角色分化？

## [STYLE LOCK]
①一句话风格锁定
②色调
③质感
④电影质感锁定
⑤物理照明锁定（含光照-皮肤交互）
⑥人物运动物理锁定（含全身动力学链+情绪物理分解+环境动态）
⑦场景特定物理规则
⑧严格 N 人声明

## [参考图锚定]
@Image1 角色：identity/outfit/关键特征
@Image2 角色：identity/outfit/关键特征
（全局锁定，后续不重复）

## CLIP — 标题（时长·N 镜）
### Shot 1（镜头类型·景别·运镜）
【首帧声明】场景/时间/光线/人物状态/色调
【0s-2s】主体动作 + 镜头运动 + 光影变化 + 物理细节
  → 四层：前景/中景/背景/空气
【2s-4s】上一段结束状态 = 本段起始状态 + ...
【微动作】关键动作链一句话总结

### Shot 2（镜头类型·景别·运镜）
...

## [BGM & 声音设计]
- BGM 风格/调性
- 对白（如有）
- 关键音效

## [限制]
no character identity drift, no extra characters, ...（3-8 项精准限制）
```

## 完整示例

### 导演推理

```
时间铰链：Shot1→Shot2 连续（站起→走向门口）
Shot Function：Shot1=建立孤独感，Shot2=转折期待
张力机制：Shot1 近景固定→压迫；Shot2 中景跟拍→释放
演出弧线：从低沉→微微振作
站位：Shot1 人物偏画面右，左侧留白=孤独；Shot2 人物居中前行
质检：角色人设=内敛沉默→不应有大表情，同场无第二角色对比
```

### STYLE LOCK

```
①Ultra-detailed cinematic film. Anamorphic 2.35:1. 4K. Slow dolly and static shots.
No BGM, ambient sound only.

②Cold blue-grey dominates (90%+). Single warm source from desk lamp (10%).
Shadows lean cool-grey, no warm ambient bounce. Low saturation.

③Kodak 500T 5219 tungsten stock. Fine organic grain, no digital noise.
Anamorphic oval bokeh on background lights. DARK AREAS smooth gradient,
not pure black.

④Live action, not animation/CGI/game. Physical camera with anamorphic lens.
Real film stock grain and color science. Slow dolly forward.

⑤Desk lamp 45° camera-right, warm tungsten 3200K, illuminates right side
of face and right hand. Window behind subject: cold blue-grey 6500K skylight
backfills left shoulder and hair edge. Floor reflects dim cold grey upward
onto jaw. Shadow under brow ridge and chin — never pure black, ambient
bounce from desk surface fills at 15%.
角色光照交互：desk lamp warm orange on right cheek+right hand; skylight
cold rim on left shoulder+hair; floor bounce dim grey under chin. Skin
reads warm-right, cold-left, grey-below.

⑥Standing-to-walking physics. Weight on right foot, left foot externally
rotated 15°. Breathing: chest rises 3mm every 3s. Blink every 4s.
Body micro-sway 2mm. When walking: left foot steps 40cm (primary),
right foot pushes off core tightens (stabilizer), right arm swings 30°
left arm back torso leans 3° forward (compensator), coat hem sways
with stride (involuntary).
情绪物理分解："失落"→ eyelids droop, corners of mouth pull down 2mm,
shoulders roll inward 5°, exhale through nose.

⑦Room dust particles drift in desk lamp beam. Paper on desk edge
curls slightly from age. Glass surface has fingerprint smudges
catching lamp light.

⑧画面中严格只有 1 个人类角色，禁止角色复制。
```

### 参考图锚定

```
@Image1 角色：林砚 — 黑色外套、短发、30岁男性
以上为唯一参考，禁止偏离。每张图只控制上述指定属性。
全局锁定，后续不再重复@声明。
```

### CLIP — 独处（5s·2 镜）

```
### Shot 1（情绪建立·近景·固定）
【首帧】深夜出租屋。冷蓝调。林砚坐在桌前，桌灯投暖橙光。
【0s-1s】林砚坐桌前，重心落右臀，左手撑桌面（主动）。右脚
平放地面稳定（稳定）。右肩微沉5°头微低（补偿）。胸腔随
呼吸起伏3mm，眨眼一次（不自主）。镜头固定近景。
前景：桌面杯子水面微颤+纸张边缘卷曲。中景：林砚上半身。
背景：窗外冷蓝光穿百叶窗形成水平条纹。空气：灯光光柱中
灰尘粒子缓慢飘动。
【1s-2.5s】eyelids droop, corners of mouth pull down 2mm.
左手从桌面收回垂到身侧（主动）。重心微移到左臀（稳定）。
肩膀同时下沉3mm（补偿）。呼吸变浅胸腔起伏减小（不自主）。
窗外有车灯扫过，光条从左向右移动越过背景墙。

### Shot 2（转折·中景·缓推）
【2.5s-3s】林砚视线从桌面抬起看向手机屏幕（主动）。
双脚不动重心微前移（稳定）。颈椎前倾10°右手伸向手机（补偿）。
眨眼一次呼吸微停（不自主）。镜头缓推从中景向近景。
手机屏幕冷白光照亮下巴和鼻尖，与桌灯暖光在脸颊形成冷暖分界。
【3s-5s】右手拿起手机举到眼前高度（主动）。左脚蹬地
身体微前倾3°（稳定）。左手扶桌边脊柱挺直5°（补偿）。
瞳孔微放大但不写眼色，嘴唇微张1mm（不自主）。
前景：桌角+杯子虚化。中景：林砚上半身+手机。背景：百叶窗
条纹光+墙面。空气：灰尘在手机冷白光中更明显。
```

### BGM & 声音设计

```
无 BGM，纯环境音。窗外远处车流低频。桌灯电流微弱嗡声。
手机震动嗡嗡声（3s处）。
```

### 限制

```
no character identity drift, no extra characters, no plastic skin,
no sourceless warm light, no overexposed whites, no crushed blacks,
no static posing, no eye color description
```

## 修正规则

- 用户改某镜头 → 只重出该 Shot 及受影响的连续性段，其余不变
- 迭代修复 → 参考 `iteration-manual.md`，一次只改 1-2 个变量
- Preflight 不通过 → 修改后重新过检，不可跳过
