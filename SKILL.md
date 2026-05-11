---
name: codex-q-pets
description: Create Codex-compatible chibi/Q-version desktop pets from several real portrait photos. Use when the user provides human photos and asks for a cute Q版 Codex pet, avatar pet, desktop companion, animated pet, or hatch-pet workflow based on that person's appearance.
---

# Codex Q Pets

## Overview

Turn a few real human portrait photos into a Codex-compatible animated Q-version desktop pet. This skill is an adapter on top of the installed `hatch-pet` skill: it adds portrait identity extraction, chibi character direction, run setup, and a streamlined generation checklist.

Use this skill when the user says things like:

- "根据这几张真人照片生成一个 Q 版 Codex 桌宠"
- "用这个男生/女生的照片做一个萌系宠物"
- "把这些头像变成 hatch-pet / Codex pet"
- "参照某张图里的 Q 版形象，但身份来自真人照片"

## Dependencies

This skill composes:

- `hatch-pet` for atlas geometry, row prompts, validation, preview videos, and packaging.
- `$imagegen` for all generated visuals.
- The bundled Codex Python runtime when available, because local `python3` may not have Pillow.

If `hatch-pet` is not installed, stop and tell the user to install it first. Do not hand-draw, tile, or synthesize pet visuals with local code.

## Quick Workflow

Keep this visible checklist for every run:

1. Getting `<Pet>` ready.
2. Imagining `<Pet>`'s main look.
3. Picturing `<Pet>`'s poses.
4. Hatching `<Pet>`.

### 1. Getting Ready

Infer a short pet name from the person, folder, or user wording. If a name is obvious, do not ask.

Create a run with the helper:

```bash
python scripts/new_q_pet_run.py \
  --pet-name "<Name>" \
  --reference /absolute/path/photo1.jpg \
  --reference /absolute/path/photo2.jpg \
  --reference /absolute/path/photo3.jpg \
  --output-dir /absolute/path/pet-runs/<slug>
```

Add `--style-reference /absolute/path/q-style.jpg` when the user points to an existing Q-version style image. Add `--identity-notes` for user constraints such as outfit, glasses, hair, or temperament.

The helper calls `hatch-pet/scripts/prepare_pet_run.py`, writes a concise Q-pet portrait brief into `pet_request.json`, and prints the first ready job.

### 2. Main Look

Open the generated `prompts/base-pet.md` and use `$imagegen` to generate the canonical base. Attach all listed input images:

- real portrait photos as identity references
- optional Q-style reference as style reference

The base prompt must preserve recognizable identity markers while simplifying into a small digital-pet sprite:

- hair shape and color
- glasses or face-defining accessories
- iconic outfit or color block
- posture/energy implied by the photos
- one or two small accessories only if readable at `192x208`

Record only the original `$CODEX_HOME/generated_images/.../ig_*.png` file:

```bash
python "$CODEX_HOME/skills/hatch-pet/scripts/record_imagegen_result.py" \
  --run-dir /absolute/path/to/run \
  --job-id base \
  --source /absolute/path/to/$CODEX_HOME/generated_images/.../ig_*.png
```

Do not record copied files from the run directory.

### 3. Poses

After the base is recorded, run:

```bash
python "$CODEX_HOME/skills/hatch-pet/scripts/pet_job_status.py" \
  --run-dir /absolute/path/to/run
```

Generate the rows in this order:

1. `idle`
2. `running-right`
3. `running-left`
4. `waving`
5. `jumping`
6. `failed`
7. `waiting`
8. `running`
9. `review`

Use the row prompt and every input image listed in `imagegen-jobs.json`, including `references/canonical-base.png`, `decoded/base.png`, and the row layout guide. If subagents are available, use them according to `hatch-pet`; if the user explicitly requests sequential generation, generate rows one by one in the parent thread.

For portrait-based pets, prefer generating `running-left` separately unless a mirror is clearly safe. Watches, hair parting, asymmetrical accessories, text, and side-specific outfit details usually make mirroring a poor choice.

### 4. Hatch

When every visual job is complete, finalize:

```bash
python "$CODEX_HOME/skills/hatch-pet/scripts/finalize_pet_run.py" \
  --run-dir /absolute/path/to/run
```

Then visually inspect:

- `qa/contact-sheet.png`
- `qa/review.json`
- `final/validation.json`
- `qa/videos/*.mp4`

Accept only if:

- `review.json` has no errors.
- `validation.json` has no errors.
- identity remains consistent across all rows.
- unused atlas cells are transparent.
- no row contains guide boxes, labels, shadows, detached effects, scenery, or cropped body parts.

The packaged pet should appear under:

```text
${CODEX_HOME:-$HOME/.codex}/pets/<pet-id>/
  pet.json
  spritesheet.webp
```

## Portrait-To-Q Rules

Read `references/q-pet-prompting.md` when writing or refining prompts for a specific person.

Default style:

- chibi/Q-version human desktop pet
- compact head and body
- friendly expressive face
- thick dark pixel-style outline
- flat cel shading
- clean chroma-key background
- no realistic anatomy, glamour, sexiness, painterly polish, or poster composition

Keep the pet readable as a tiny sprite. A correct result feels like a small Codex companion, not a portrait illustration.

## Failure Handling

If a row drifts away from the base identity, regenerate only that row with stronger identity wording and the contact sheet as review context.

If finalization fails, run:

```bash
python "$CODEX_HOME/skills/hatch-pet/scripts/queue_pet_repairs.py" \
  --run-dir /absolute/path/to/run
```

Then regenerate only the queued repair rows.

If the only issue is the user's taste in likeness or cuteness, generate a new base first, then rerun rows from that approved base.
