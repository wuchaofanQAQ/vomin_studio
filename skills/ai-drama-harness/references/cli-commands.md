# CLI 命令速查表

harness 通过以下 CLI 命令与飞书表格和本地 workspace 交互。

## 初始化

```bash
# 从飞书链接创建 workspace（自动发现/补全 6 张表）
python cli.py init-from-url "<飞书URL>" <workspace路径> --name "剧名"

# 从零创建（自动建飞书多维表格 + 本地 workspace）
python cli.py init <workspace路径> --name "剧名"
```

## 读数据

```bash
# 读取指定表当前数据（JSON 输出到 stdout）
python cli.py read <workspace> --table 角色库
python cli.py read <workspace> --table 场景库
python cli.py read <workspace> --table 剧本设定
python cli.py read <workspace> --table 剧本分镜表
python cli.py read <workspace> --table 生图工作台
python cli.py read <workspace> --table 素材库
python cli.py read <workspace> --table 角色档案
```

## 写数据

```bash
# JSON 字符串直接写入（upsert：按 match key 更新已有/插入新增）
python cli.py write <workspace> --table 角色库 --data '[{"name":"林砚","gen_prompt":"..."}]'

# 从文件读取 JSON 写入
python cli.py write <workspace> --table 剧本设定 --data @settings.json
```

各表 match key：
| 表名 | match key | 说明 |
|---|---|---|
| 角色库 | `name` | 角色名 |
| 场景库 | `name` | 场景名 |
| 剧本设定 | `name` | 设定项名 |
| 剧本分镜表 | `shot_id` | 镜头ID |
| 生图工作台 | `name` | 任务名 |
| 素材库 | `name` | 素材ID |
| 角色档案 | `name` | 角色名 |

## 生成素材

```bash
# 生成指定角色/场景/分镜/工作台任务的素材
python cli.py generate <workspace> --target 角色库:林砚
python cli.py generate <workspace> --target 场景库:写字楼大堂
python cli.py generate <workspace> --target 剧本分镜表:ep01_s01
python cli.py generate <workspace> --target 生图工作台:任务名

# 批量生成所有"待生成"状态的分镜
python cli.py generate <workspace>

# 仅生成配音（不出视频，省钱）
python cli.py generate <workspace> --tts-only
```

## 同步

```bash
# 推送本地数据到飞书
python cli.py push <workspace>

# 从飞书拉取到本地缓存
python cli.py pull <workspace>
```

## 辅助

```bash
# 查看 workspace 状态、预算
python cli.py status <workspace>

# 预览提示词模板展开结果
python cli.py expand <workspace>
python cli.py expand <workspace> --shot ep01_s01
```
