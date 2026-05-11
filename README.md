# Codex Q Pets

把几张真人照片变成「萌系 Q 版 Codex 桌宠」的 Codex Skill。

它会生成完整的 Codex pet：主形象、九行动作、`spritesheet.webp`、`pet.json`、QA 总图和预览视频。适合把自己、朋友、教练、博主、同事做成 Codex 桌面小伙伴。

## 1. 安装和使用

先把这个仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/xmmxOvO/codex_Q_pets.git ~/.codex/skills/codex-q-pets
```

如果你设置了 `CODEX_HOME`，用这个：

```bash
git clone https://github.com/xmmxOvO/codex_Q_pets.git "$CODEX_HOME/skills/codex-q-pets"
```

安装后，重新打开一个 Codex 线程，或者重启 Codex，让 skill 列表重新加载。

然后在 Codex 里上传几张真人照片，直接说：

```text
使用 codex-q-pets，把这些真人照片生成一个萌系 Q 版 Codex 桌宠。
名字叫小蒋。请参照最后一张图的 Q 版风格。
```

也可以这样说：

```text
用 codex-q-pets，根据这几张人像照片做一个 Codex 桌宠。
保留黑色短发、圆框眼镜、白背心、健身教练气质。
```

Codex 会自动按这个流程做：

1. 准备 pet run
2. 生成 Q 版主形象
3. 生成九行动作
4. 合成并安装 Codex pet

## 2. 使用前确认

你需要：

- Codex / Codex Desktop 可用
- 已安装 `hatch-pet` skill
- 当前 Codex 能使用 `$imagegen`

这个 skill 是 `hatch-pet` 的上层封装。它负责把真人照片整理成 Q 版桌宠流程；真正的切帧、校验、打包由 `hatch-pet` 完成。

## 3. 照片怎么准备

推荐上传：

- 2-5 张清晰真人照
- 至少一张正脸或半身照
- 至少一张能看清发型、穿搭、配饰的图
- 如果想模仿某种 Q 版画风，再额外给一张风格参考图

最好同时告诉 Codex 你最想保留什么：

```text
保留黑色短发、圆框眼镜、白背心、手表、健身教练气质。
```

不太适合的照片：

- 只有远景照
- 脸被挡住太多
- 一张图里有很多人但没说明目标人物
- 想保留很小的 logo、文字、复杂首饰

## 4. 生成后看哪里

最终安装位置：

```text
~/.codex/pets/<pet-id>/
  pet.json
  spritesheet.webp
```

过程和检查文件：

```text
pet-runs/<pet-id>/
  final/spritesheet.webp
  qa/contact-sheet.png
  qa/review.json
  qa/videos/*.mp4
```

重点看 `qa/contact-sheet.png`。如果九行动作里都还是同一个人、没有裁切、没有乱七八糟的背景或文字，就基本可以用。

## 5. 常见问题

### Codex 没识别到这个 skill

确认这里存在：

```text
~/.codex/skills/codex-q-pets/SKILL.md
```

然后重新打开一个 Codex 线程，或者重启 Codex。

### 提示找不到 hatch-pet

先安装 `hatch-pet`，并确认这里存在：

```text
~/.codex/skills/hatch-pet/SKILL.md
```

### 生成物像头像，不像桌宠

让 Codex 强化这句话：

```text
不是头像，不是插画海报。要生成 Codex desktop pet sprite：
全身、小尺寸可读、Q版、粗描边、扁平色块、纯色 chroma-key 背景。
```

### 某一行动作不像本人

只返修那一行，不要全部重做。让 Codex 对照 `qa/contact-sheet.png` 和 `references/canonical-base.png`，重新生成失败的 row。

## 6. 命令行辅助脚本

普通用户不需要手动跑这个脚本。它主要给熟悉命令行的人用，用来先创建一个 `hatch-pet` run：

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

常用参数：

- `--pet-name`：桌宠显示名
- `--reference`：真人照片，可重复传多张
- `--style-reference`：Q 版风格参考图，可选
- `--identity-notes`：希望保留的人物特征，可选
- `--output-dir`：运行目录
- `--force`：覆盖同名 run

## 7. 隐私提醒

真人照片只应该在你有权使用的情况下上传和生成。不要用没有授权的人像做公开分发的桌宠包。
