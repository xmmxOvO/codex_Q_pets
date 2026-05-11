# Codex Q Pets

把几张真人照片变成「萌系 Q 版 Codex 桌宠」的 Codex Skill。

这个 skill 适合这样的需求：

- 给几张真人照片，让 Codex 生成一个 Q 版桌宠
- 根据真人的发型、眼镜、穿搭、气质，生成 Codex 可用的 animated pet
- 想把朋友、教练、博主、同事、自己做成一个 Codex 桌面小伙伴

它不是普通头像生成器，而是会走完整的 Codex pet 流程：主形象、九行动作、spritesheet、`pet.json`、QA contact sheet、预览视频，最后安装到本机 Codex pets 目录。

## 效果

输入：

- 2-5 张真人照片
- 可选：1 张 Q 版风格参考图
- 可选：人物特征说明，比如「黑色短发、圆框眼镜、白背心、健身教练气质」

输出：

```text
~/.codex/pets/<pet-id>/
  pet.json
  spritesheet.webp
```

同时会生成 QA 文件：

```text
pet-runs/<pet-id>/
  final/spritesheet.webp
  qa/contact-sheet.png
  qa/review.json
  qa/videos/*.mp4
```

## 依赖

使用前需要：

1. Codex / Codex Desktop 可用
2. 已安装 `hatch-pet` skill
3. 当前 Codex 能使用 `$imagegen`

这个 skill 是 `hatch-pet` 的上层封装，负责把「真人照片」转换成适合 `hatch-pet` 的 Q 版桌宠流程；真正的 spritesheet 切帧、校验、打包仍由 `hatch-pet` 完成。

## 安装

把仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/xmmxOvO/codex_Q_pets.git ~/.codex/skills/codex-q-pets
```

如果你设置了 `CODEX_HOME`，可以安装到：

```bash
git clone https://github.com/xmmxOvO/codex_Q_pets.git "$CODEX_HOME/skills/codex-q-pets"
```

安装完成后，重新打开一个 Codex 线程，或者重启 Codex，让 skill 列表重新加载。

## 最简单用法

在 Codex 里上传几张真人照片，然后说：

```text
使用 codex-q-pets，把这些真人照片生成一个萌系 Q 版 Codex 桌宠。
名字叫小蒋。请参照最后一张图的 Q 版风格。
```

或者：

```text
用 codex-q-pets，根据这几张人像照片做一个 Codex 桌宠。
保留黑色短发、圆框眼镜、白背心、健身教练气质。
```

Codex 会按四步执行：

1. 准备 pet run
2. 生成主形象
3. 生成九行动作
4. 合成并打包 Codex pet

## 命令行辅助脚本

这个仓库提供了一个初始化脚本：

```bash
scripts/new_q_pet_run.py \
  --pet-name "小蒋" \
  --reference /absolute/path/photo1.jpg \
  --reference /absolute/path/photo2.jpg \
  --reference /absolute/path/photo3.jpg \
  --style-reference /absolute/path/q-style.jpg \
  --identity-notes "black fluffy hair, round glasses, white tank top, fitness coach energy" \
  --output-dir /absolute/path/pet-runs/xiao-jiang \
  --force
```

脚本会创建一个 `hatch-pet` run，并生成第一步 `base` 任务。之后 Codex 会继续用 `$imagegen` 生成主形象和动作行。

常用参数：

- `--pet-name`：桌宠显示名
- `--reference`：真人照片，可重复传多张
- `--style-reference`：Q 版风格参考图，可选
- `--identity-notes`：希望保留的人物特征，可选
- `--output-dir`：运行目录
- `--force`：覆盖同名 run

## 推荐照片

为了生成效果稳定，建议准备：

- 2-5 张清晰真人照
- 至少一张正脸或半身照
- 至少一张能看清穿搭/配饰/发型的图
- 如果想模仿某种 Q 版画风，再额外给一张风格参考图

不建议：

- 只有远景照
- 脸被挡住太多
- 照片里有多人但没有说明目标人物
- 要求保留非常小的 logo、文字、复杂首饰

## 生成规则

这个 skill 会优先保留「小尺寸下也能读出来」的人物特征：

- 发型和发色
- 眼镜、胡子、帽子等强特征
- 代表性穿搭和色块
- 一个可读的小配饰，比如手表、项链、耳机
- 人物气质，比如健身教练、创作者、程序员、学生感

会主动避免：

- 写实人体
- 性感化表达
- 复杂背景
- 海报感构图
- 漂浮符号、速度线、阴影、文字
- 太小导致桌宠里看不清的细节

## 输出检查

完成后重点看：

```text
qa/contact-sheet.png
final/validation.json
qa/review.json
qa/videos/*.mp4
```

合格标准：

- `validation.json` 没有 errors
- `review.json` 没有 errors
- 每行动作里都还是同一个人物
- 没有裁切、重叠、文字、背景、阴影、漂浮特效
- 未使用的 atlas 格子是透明的

## 常见问题

### 1. Codex 没识别到这个 skill

确认目录是：

```text
~/.codex/skills/codex-q-pets/SKILL.md
```

然后重新打开一个 Codex 线程，或者重启 Codex。

### 2. 提示找不到 hatch-pet

这个 skill 依赖 `hatch-pet`。请先安装 `hatch-pet`，并确认存在：

```text
~/.codex/skills/hatch-pet/SKILL.md
```

### 3. Python 缺少 Pillow

在 Codex Desktop 环境里，优先使用 Codex bundled runtime。脚本会自动尝试：

```text
~/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
```

### 4. 生成物像普通头像，不像桌宠

让 Codex 强化这些约束：

```text
不是头像，不是插画海报。要生成 Codex desktop pet sprite：
全身、小尺寸可读、Q版、粗描边、扁平色块、纯色 chroma-key 背景。
```

### 5. 某一行动作不像本人

只返修那一行，不要重做全部。让 Codex 使用 `qa/contact-sheet.png` 和 `references/canonical-base.png` 作为对照，重新生成失败的 row。

## 隐私提醒

真人照片只应该在你有权使用的情况下上传和生成。不要用没有授权的人像做公开分发的桌宠包。

## 仓库内容

```text
codex_Q_pets/
  SKILL.md
  agents/openai.yaml
  scripts/new_q_pet_run.py
  references/q-pet-prompting.md
```

`pet-runs/`、生成图片、测试素材不会进入仓库。
