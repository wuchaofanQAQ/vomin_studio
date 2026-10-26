# CLI 命令速查表

harness 通过以下 CLI 命令与飞书表格和本地 workspace 交互。

> **权限分类**
> - 🔍 **只读**：随时可执行，不需要用户确认。
> - ✏️ **写入/消费**：会改变飞书数据或消耗生成预算，**必须在确认点向用户列出清单并得到明确确认后执行**。

## 初始化

**项目路径**：一个剧本一个文件夹，默认根目录 `C:\Users\Heart\PycharmProjects\vomin_studio\workspace`，即默认路径为 `workspace\{剧名}`；用户可指定任意路径。

```bash
# 从飞书链接创建 workspace（自动发现/补全表结构，绑定已有表格）
#   路径省略 → 自动用 项目根/workspace/剧名
python cli.py init-from-url "<飞书URL>" --name "剧名"
python cli.py init-from-url "<飞书URL>" "D:\my_dramas\剧名" --name "剧名"

# 从零创建（自动建飞书多维表格 + 本地 workspace）
python cli.py init --name "剧名"
python cli.py init "D:\my_dramas\剧名" --name "剧名"
```

- 两个命令完成后都会**自动写入飞书「系统设置」表**：`项目路径`、`剧名`、`创建时间`
- `init-from-url` 不写业务数据（仅绑定 + 拉取 + 写系统设置引导项），用户主动提供链接即可在启动时执行
- `init` 会新建飞书多维表格，必须在确认点 1 用户确认后执行
- 剧名含非法路径字符（`\ / : * ? " < > |`）时 CLI 自动替换为 `_`
- 本地目录迁移后用 `python cli.py set-path <workspace>` 更新系统设置中的项目路径

## 读数据（🔍 只读）

```bash
# 读取指定表当前数据（JSON 输出到 stdout）
python cli.py read <workspace> --table 剧本设定
python cli.py read <workspace> --table 资产库
python cli.py read <workspace> --table 角色档案
python cli.py read <workspace> --table 资产库

# 剧本表/分镜表按集过滤：拆分镜只读 当前集 ± 1 集（共3集），禁止全量读剧本
# 剧本表默认剔除「小说内容」(novel_text)，避免撑爆上下文；仅需要原文时才加 --with-novel
python cli.py read <workspace> --table 剧本表 --episode 5 --context 1   # 第4/5/6集（不含小说原文）
python cli.py read <workspace> --table 剧本表 --episode 5 --with-novel   # 仅第5集，连同小说原文
python cli.py read <workspace> --table 剧本分镜表 --episode 5           # 仅第5集已有分镜
python cli.py read <workspace> --table 生图工作台
python cli.py read <workspace> --table 素材库
# 全量读剧本表仅用于总览/检查，不得作为分镜生成/场景抽取的输入
python cli.py read <workspace> --table 剧本表
```

## 写数据（✏️ 需确认）

```bash
# JSON 字符串直接写入（upsert：按 match key 更新已有/插入新增）
python cli.py write <workspace> --table 资产库 --data '[{"name":"林砚","gen_prompt":"..."}]'

# 从文件读取 JSON 写入
python cli.py write <workspace> --table 剧本设定 --data @settings.json
```

各表 match key：

| 表名 | match key | 说明 |
|---|---|---|
| 剧本设定 | `name` | 设定项名 |
| 剧本表 | `episode` | 集号（数字） |
| 资产库 | `name` | 角色名 |
| 角色档案 | `name` | 角色名 |
| 资产库 | `name` | 场景名（= 场景ID；一个场景一行一张图） |
| 剧本分镜表 | `shot_id` | 段ID（`ep{集号两位}_p{段序两位}`，一段一行） |
| 生图工作台 | `name` | 任务名 |
| 素材库 | `name` | 素材ID |

## 生成素材（✏️ 需确认，花预算）

```bash
# 生成指定角色/场景/分镜/工作台任务的素材
python cli.py generate <workspace> --target 资产库:林砚
python cli.py generate <workspace> --target 资产库:写字楼大堂
python cli.py generate <workspace> --target 剧本分镜表:ep01_p01
python cli.py generate <workspace> --target 生图工作台:任务名

# 批量生成所有"待生成"状态的分镜
python cli.py generate <workspace>

# 仅生成配音（本项目已关闭 TTS，tts.enabled=false 时此命令为空操作）
python cli.py generate <workspace> --tts-only
```

提示词【参考素材锚点】块中的 `{资产库：张三} 图1：【张三】，男主角，…` / `{资产库：出租屋} 图2：…` / `{sheetName:rowId} 视频N：…` 引用会在生成时自动解析：标记移除、图N/视频N 的身份说明保留，对应图片/视频按编号顺序作为参考素材随 API 传递。正文（资产锁定、整体基准、逐镜头等）只用【资产名】，不写 `{}`。

## 同步（🔍 pull 只读 / ✏️ push 需确认）

```bash
# 推送本地数据到飞书（✏️）
python cli.py push <workspace>

# 从飞书拉取到本地缓存（🔍）
python cli.py pull <workspace>
```

## 辅助（🔍 只读）

```bash
# 查看 workspace 状态、预算
python cli.py status <workspace>

# 预览提示词模板展开结果（引用解析后的最终文本 + 参考图/参考视频清单）
python cli.py expand <workspace>
python cli.py expand <workspace> --shot ep01_p01
```

`expand` 是写入前的只读预检：确认所有引用可解析、素材已就绪，再向用户发起确认。

## 表结构迁移（存量飞书表）

```bash
# 🔍 只读：打印迁移计划（表改名 / 新增字段 / 受影响行数），不做任何写入
python cli.py migrate-schema <workspace> --dry-run

# ✏️ 需确认：执行迁移（剧集表→剧本表；补 小说章节/小说内容；资产库补 参考场景/作用关联；
#            旧「完整剧本」内容复制到「小说内容」后清空，状态置「待转剧本」；改写本地 workspace.yaml）
python cli.py migrate-schema <workspace>
```

幂等：已完成的步骤自动跳过。执行前须先列清单并拿到用户明确确认。
