#!/usr/bin/env python3
"""Prepare a hatch-pet run for a Q-version Codex pet from portrait photos."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


DEFAULT_CHROMA_KEY = "#00FFFF"


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "q-pet"


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or "~/.codex").expanduser().resolve()


def find_hatch_pet_dir() -> Path:
    candidates = [
        codex_home() / "skills" / "hatch-pet",
        Path.home() / ".codex" / "skills" / "hatch-pet",
    ]
    for path in candidates:
        if (path / "scripts" / "prepare_pet_run.py").is_file():
            return path
    raise SystemExit("hatch-pet skill not found. Install hatch-pet before using codex-q-pets.")


def find_python() -> str:
    env_python = os.environ.get("CODEX_PYTHON")
    if env_python and Path(env_python).is_file():
        return env_python

    bundled = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "python"
        / "bin"
        / "python3"
    )
    if bundled.is_file():
        return str(bundled)

    return sys.executable or "python3"


def existing_file(path: str) -> str:
    resolved = Path(path).expanduser().resolve()
    if not resolved.is_file():
        raise argparse.ArgumentTypeError(f"file not found: {resolved}")
    return str(resolved)


def build_pet_notes(args: argparse.Namespace) -> str:
    parts = [
        "Q-version chibi Codex desktop pet based on the attached real portrait photos.",
        "Preserve the person's strongest readable identity markers: hair shape, glasses or signature accessories, outfit color blocks, posture, and overall energy.",
        "Simplify into a cute small digital pet, not a realistic portrait.",
    ]
    if args.style_reference:
        parts.append("Use the style reference only for Q-version cuteness and composition; do not copy unrelated characters.")
    if args.identity_notes:
        parts.append(f"User identity notes: {args.identity_notes}")
    return " ".join(parts)


def build_style_notes(args: argparse.Namespace) -> str:
    return (
        "Codex digital pet sprite style: chibi/Q-version human mascot, compact body, oversized expressive head, "
        "thick dark 1-2 px pixel-style outline, visible stepped edges, limited palette, flat cel shading, clean silhouette, "
        "fully visible full-body sprite on chroma-key background. Avoid realistic anatomy, painterly rendering, glossy 3D, "
        "poster art, scenery, shadows, labels, text, detached effects, and tiny unreadable accessories."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pet-name", required=True, help="Display name for the pet.")
    parser.add_argument("--pet-id", help="Stable slug. Defaults to a slugified pet name.")
    parser.add_argument("--description", help="One sentence package description.")
    parser.add_argument("--reference", action="append", type=existing_file, required=True, help="Portrait photo. Repeat for multiple photos.")
    parser.add_argument("--style-reference", action="append", type=existing_file, help="Optional Q/chibi style reference image. Repeat if needed.")
    parser.add_argument("--identity-notes", help="Important user constraints: outfit, accessory, temperament, or likeness markers.")
    parser.add_argument("--output-dir", required=True, help="Run directory to create.")
    parser.add_argument("--chroma-key", default=DEFAULT_CHROMA_KEY)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    hatch_pet = find_hatch_pet_dir()
    python = find_python()
    pet_id = args.pet_id or slugify(args.pet_name)
    description = args.description or f"A Q-version Codex desktop pet based on portrait photos of {args.pet_name}."

    command = [
        python,
        str(hatch_pet / "scripts" / "prepare_pet_run.py"),
        "--pet-name",
        args.pet_name,
        "--pet-id",
        pet_id,
        "--display-name",
        args.pet_name,
        "--description",
        description,
        "--output-dir",
        str(Path(args.output_dir).expanduser().resolve()),
        "--pet-notes",
        build_pet_notes(args),
        "--style-notes",
        build_style_notes(args),
        "--chroma-key",
        args.chroma_key,
    ]

    for reference in args.reference:
        command.extend(["--reference", reference])
    for reference in args.style_reference or []:
        command.extend(["--reference", reference])
    if args.force:
        command.append("--force")

    subprocess.run(command, check=True)

    run_dir = Path(args.output_dir).expanduser().resolve()
    status_cmd = [
        python,
        str(hatch_pet / "scripts" / "pet_job_status.py"),
        "--run-dir",
        str(run_dir),
    ]
    result = subprocess.run(status_cmd, check=True, text=True, capture_output=True)
    print(result.stdout)

    request_path = run_dir / "pet_request.json"
    if request_path.is_file():
        request = json.loads(request_path.read_text(encoding="utf-8"))
        request["codex_q_pets"] = {
            "portrait_references": len(args.reference),
            "style_references": len(args.style_reference or []),
            "helper": "scripts/new_q_pet_run.py",
        }
        request_path.write_text(json.dumps(request, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Prepared Q-pet run: {run_dir}")
    print(f"Next prompt: {run_dir / 'prompts' / 'base-pet.md'}")


if __name__ == "__main__":
    main()
