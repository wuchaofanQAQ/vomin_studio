# Seedance 2.5 执行模型 — 写 CLIP 前必读

> 核心区别：2.0 会推理、会加戏、写大概它帮你补。2.5 不推理——你写什么它给什么，你不写=画面里没有。

## 一、情绪→物理分解

**问题**：2.5 对情绪词字面执行且过度——"笑"→真笑，"愤怒"→暴怒，"悲伤"→痛哭。

**规律**：所有情绪词、抽象状态词、感受词都必须替换为 2-3 个可见肌肉动作+身体动作。

### 禁用词（遇到同类一律替换）

笑、微笑、怒、愤怒、悲伤、犹豫、轻蔑、紧张、恐惧、惊讶、疑惑、不屑、欣慰、失落、痛苦、得意、尴尬、满足、疲惫、期待、失望、警惕、放松、困惑、厌恶

### 替换写法

| 禁用 | 替换（英文提示词） |
|------|------|
| 微微一笑 | corners of mouth lift 2mm, then settle back; immediately followed by [next action] |
| 愤怒 | brow bones press downward, jaw clenches, neck muscles tense visibly, fists curl at sides |
| 悲伤 | eyelids droop, corners of mouth pull down slightly, throat swallows, shoulders roll inward |
| 犹豫 | eyes dart left then right for 0.5s, lips part without sound, right foot half-steps then stops |
| 紧张 | Adam's apple bobs, fingers curl into fist then release, weight shifts to left foot |
| 恐惧 | eyes widen, nostrils flare, torso leans back 3cm, hands freeze mid-gesture |
| 惊讶 | eyebrows shoot up, mouth opens 1cm, body rocks back slightly |
| 疲惫 | shoulders drop, eyelids at half-mast, exhale through mouth, spine curves forward slightly |
| 警惕 | head turns sharply toward sound source, shoulders square, breathing shallow and rapid |

### 铁律

1. 提示词正文中不出现任何情绪/感受/抽象状态词
2. 替换为可见的肌肉+身体动作
3. 动作后面紧跟下一个动作，不留情绪空白
4. 导演推理段可以写情绪词（该段不复制给 Seedance）

---

## 二、全身动力学链

**问题**：2.5 只执行你写的部位。写"转头"只转头身体不动——像恐怖片。

**规律**：每个动作必须写全四层面。

### 动力学链模板

1. **主动件** — 做核心动作的身体部位
2. **稳定件** — 维持平衡的身体部位（重心腿、核心肌群）
3. **补偿件** — 配合主动件的自然联动（肩膀跟转、手臂摆动）
4. **不自主反应** — 呼吸、眨眼、重心微移、衣物随动

### 常见动作完整写法

**转头看**：颈椎向右旋转30度（主动），双脚不动重心微移到左脚（稳定），右肩跟转5度下巴微抬（补偿），呼吸不变眨眼一次（不自主）

**走路**：左脚前迈40cm（主动），右脚蹬地核心收紧（稳定），右臂前摆30度左臂后摆躯干微前倾3度（补偿），衣角随步伐轻微摆动（不自主）

**站立不动**：无主动动作（但必须写！），重心在右脚左脚微外撇15度（稳定），双手自然垂身侧（补偿），胸腔随呼吸起伏、每3-4秒眨眼、身体2-3mm自然微晃（不自主）

### 铁律

1. 每个角色每个时间段都有全身描写——即使"站着不动"
2. 不能只写一个身体部位——至少主动件+1补偿件+1不自主反应
3. 不自主反应（呼吸/眨眼/微晃）贯穿整个 Shot

---

## 三、环境动态系统

**问题**：2.5 不自动补环境运动。不写=死画面=假。

**规律**：每个 Shot 至少 3-4 个环境动态元素。

### 环境动态清单（每 Shot 至少选 3-4 项）

**空气类**：风（方向+强度+影响对象）、灰尘悬浮/被脚步带起、雾气/蒸汽从缝隙飘出、烟从火源上升随气流飘散

**水类**：水面涟漪扩散/倒影扭曲、水滴从管道滴落溅起水花、积水被脚步踩出波纹

**光类**：火焰摇曳/光斑跳动、影子随光源摆动、丁达尔光柱内粒子流动、水面反射光斑晃动

**物体类**：布料/旗帜被风吹动、松动物件被震动微颤、灰尘碎屑从接触表面脱落

**生物类**：飞虫绕灯光、远处人影走动

**温度可视物**：冷天呼吸雾气、食物热气蒸汽、皮肤凝结水珠

### 铁律

1. 每 Shot 至少 3-4 个环境动态：空气类1+光类1+物体/水/生物类1-2
2. 环境动态融入角色动作时间线（"脚步带起灰尘，灰尘在火光中飘散"）
3. 有时间维度——"风从左侧吹来，强度使衣角每秒摆动2次"
4. 有光源+有粒子的场景必须有丁达尔光柱

---

## 四、光照-表面交互

**问题**：2.5 不自动让环境光影响角色肤色。不写=角色像在影棚独立打光。

### 每个可见角色必须写明

1. **主光源来自哪里** — 天空冷光从上方/火把暖光从右侧
2. **照到角色哪个部位** — 头顶和右肩偏冷蓝灰/左脸偏暖橙
3. **反射光从哪来** — 地面反射光打在下巴上/墙壁反射光从左侧补
4. **阴影落在哪** — 眉骨在眼窝投出阴影/下巴下方暗
5. **色温混合** — 冷天光+暖火光=头顶冷蓝灰、侧面暖橙、下颌暗灰
6. **边缘光** — 天空冷光在肩膀和头顶勾勒出冷灰轮廓

### 写法示例

```
Cold blue-grey sky-light filters from above, casting the top of his head, 
shoulders, and upper chest in dim cold tones. A torch 2 meters to camera-right 
throws warm orange light onto the right side of his face, right arm, and 
right shoulder. Ground moisture reflects dim cold grey light upward onto 
his jaw and under-chin. Skin reads cold grey-pale on top, warm orange on 
the right side, dim grey below — three temperature zones blending on his 
face and hands.
```

### 铁律

1. 每个可见角色必须写光照-皮肤交互
2. 多光源=多色温区，写明哪个部位偏冷、偏暖
3. 反射光必须写（地面/墙壁/水面）
4. 材质决定反射——湿石头反光强、干石头哑光、金属 specular

---

## 五、四层画面枚举

**问题**：2.5 你写多少给多少。不写某层=画面里空白。

### 每个 Shot 逐层检查

**前景层（0-2m）**：物体/碎片/障碍物的材质+光照+运动状态+表面细节（水渍/灰尘/裂纹）

**中景层（2-8m，角色层）**：角色全身动力学链+情绪物理分解+光照-皮肤交互+与环境接触面物理+随动元素（头发/衣角/配饰）

**背景层（8m+）**：建筑/人群/远处光源+背景动态+大气透视（雾使远处偏冷模糊）

**空气层（贯穿全画面）**：灰尘/雾/烟/蒸汽/风+光在空气中传播（丁达尔/散射）+温度可视效果

### 铁律

1. 四层都要写——缺一层画面就"空"
2. 每个元素都有材质+光照+运动状态
3. 角色与环境接触面必须写（脚踩地面的水被挤开、手扶墙的灰尘被带起）
4. 空气永远有内容——至少灰尘和温度效果

---

## 六、禁止事项（不变）

1. 禁止比喻——"像XX""如XX"全删，直接写视觉事实
2. 禁止衣物描写——服装由@Image锚定，除特写外不重复（衣物随动可以写）
3. 禁止瞳孔/虹膜颜色——统一写"视线看向XX"
4. 禁止情绪词——用物理分解替代
5. 禁止剧情原因——不写"因为她想起了过去"
6. 禁止暗示性描述——Seedance 不需要知道的不写

## 七、字数与结构

- 2.5 支持 50 个参考素材，提示词长度不是限制
- 每个字必须描述画面中可见或可听的内容
- 一个 5s Shot 可能 300-500 字描述，一个 CLIP 总量 5000-8000 字
- 不要为控制字数省略细节——2.5 不会帮你补
