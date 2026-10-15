# V8 格式结构模板（12 子段标准）

> 每次写 CLIP 提示词，必须包含全部 12 子段，缺一不可。

## STYLE LOCK 段（8 子段）

### ①一句话风格锁定
Ultra-detailed cinematic film。画幅（如 2.35:1 anamorphic）。4K。运镜方式概述。BGM 状态。

### ②色调
色卡融入叙述一段压完。写明 primary/cold 比例、光源类型。冷色调场景 100%冷色零暖色；暖色调有冷色平衡。CLIP 中不写色号，用描述性语言。

### ③质感
Kodak 胶片模拟。室内低光用 500T 5219（tungsten），室外日光用 250D 5207（daylight）。Fine organic grain, no digital noise。Anamorphic oval bokeh。DARK AREAS not pure black。

### ④电影质感锁定
Live action not animation/CGI/game。Physical camera + anamorphic lens。Real film stock characteristics。Camera movement description。

### ⑤物理照明锁定
光源数量/位置/角度。光衰减物理。表面反射类型。阴影特性（never pure black + ambient bounce）。大气条件。
**2.5 必写**：光源-角色皮肤交互（详见 `seedance-25-execution-model.md` 第四节）。

### ⑥人物运动物理锁定
站立重心链（feet→knees→hips→spine）。气流/风对衣物的影响。所有运动有惯性和重量。
**2.5 必写**：全身动力学链（详见 `seedance-25-execution-model.md` 第二节）。
**2.5 必写**：情绪→物理分解（详见 `seedance-25-execution-model.md` 第一节）。
**2.5 必写**：环境动态（详见 `seedance-25-execution-model.md` 第三节）。

### ⑦场景特定物理规则
视场景而定：暗金能量物理/水流物理/管道侵蚀物理等。纯物理描述，no magic。

### ⑧严格 N 人声明
角色数量锁定。如"画面中严格只有 3 个人类角色，禁止角色复制"。

## CLIP 段（3 子段）

### ⑨首帧声明
场景。时间。光线。人物位置/状态。色调。一句话设定画面。

### ⑩逐秒拆解
`[0-1s] [1-2s] [2-3s]` 格式。每秒写明：主体动作 + 镜头运动 + 光影变化 + 物理细节。上一段结束状态=下一段起始状态。
**2.5 必写**：四层画面枚举——前景层/中景层/背景层/空气层（详见 `seedance-25-execution-model.md` 第五节）。

### ⑪微动作全程
按阶段总结关键动作链，每阶段一句话。

## 结尾（1 子段）

### ⑫[NEGATIVE]
场景特定否定指令。3-8 项精准限制，不堆通用词。每个否定对应本场景可能出现的具体错误。

## STYLE LOCK 标准模板示例

```
Cinematic film。Low Key Lighting。冷灰蓝黑为绝对主色调（90%+）。
光源体系（所有光源必须有真实物理来源，禁止凭空出现暖光）：
①主光源描述；②辅助光源描述；③反射光源描述；④大气光效描述。
Anamorphic 2.35:1。4K, cinematic film rendering, fine organic grain, 
no digital noise, smooth gradient in dark areas。
Consistent motion blur on all movement, natural depth of field。
画面中严格只有[N]个人物角色，禁止角色复制。

材质系统：[场景材质描述]。所有物体接地有 contact shadow。
禁止塑料质感/泥泞噪点/无序反光。
```

## 参考图全局锁定写法

```
@Image1 角色：identity/outfit/关键特征
@Image2 角色：identity/outfit/关键特征
以上各图均为唯一参考，禁止偏离。每张图只控制上述指定属性。
全局锁定，后续不再重复@声明。
```

## 负面限制选题库（从中选 3-8 项最相关的）

```
no character identity drift, no extra characters, no blue-purple glow, 
no neon, no plastic skin, no muddy texture, no blur on focused subject, 
no silent footsteps, no eye color, no static posing, no overexposed whites, 
no crushed blacks, no floating objects without contact shadow, 
no sourceless warm light, no independent subject lighting, 
no frame skipping, no stutter, no choppy motion, 
no character duplication, no cloned characters
```

## CLIP 完整文件结构

```
## 使用方式
（上传参考图顺序 + 复制粘贴说明）

## 导演推理（不复制此部分给 Seedance）
（时间铰链/Shot Function/张力机制/演出弧线/站位/质检）

## [STYLE LOCK]
（8 个子段）

## [参考图锚定]
（@Image 锁定）

## CLIP — 标题（时长·N 镜）
### Shot N（镜头类型·景别·运镜）
【0s-3s】起始状态 + 主体动作 + 镜头拍法 + 结束状态

## [BGM & 声音设计]
（BGM/对白/关键音效独立段）

## [限制]
（3-8 项精准限制）
```
