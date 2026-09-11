#!/usr/bin/env python3
"""构建并校验可分发的「去 AI 腔（中文版）」插件包。

改造自 Peter Yang 的 no-ai-slop（MIT）中的同名脚本，仅做路径与命名适配。
"""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
DIST = ROOT / "dist"
PLUGIN_NAME = "no-ai-slop-zh"
SKILL_ROOT = ROOT / "skills" / PLUGIN_NAME
ICON = ROOT / "assets" / f"{PLUGIN_NAME}.png"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="只校验，不保留构建产物")
    return parser.parse_args()


def validate_source(manifest: dict) -> None:
    required = ("name", "version", "description", "author", "skills", "interface")
    missing = [key for key in required if not manifest.get(key)]
    if missing:
        raise SystemExit(f"插件清单缺少字段: {', '.join(missing)}")

    interface = manifest["interface"]
    interface_required = (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "defaultPrompt",
    )
    missing_interface = [key for key in interface_required if not interface.get(key)]
    if missing_interface:
        raise SystemExit(f"界面信息缺少字段: {', '.join(missing_interface)}")

    prompts = interface["defaultPrompt"]
    if len(prompts) > 3 or any(len(prompt) > 128 for prompt in prompts):
        raise SystemExit("起始提示词最多三条，每条不超过 128 个字符")

    for source in (SKILL_ROOT / "SKILL.md", SKILL_ROOT / "eval.md", ICON):
        if not source.is_file():
            raise SystemExit(f"缺少打包源文件: {source.relative_to(ROOT)}")


def build_plugin(manifest: dict) -> tuple[Path, Path]:
    plugin_root = DIST / PLUGIN_NAME
    if plugin_root.exists():
        shutil.rmtree(plugin_root)

    skill_root = plugin_root / "skills" / PLUGIN_NAME
    (plugin_root / ".codex-plugin").mkdir(parents=True)
    (plugin_root / "assets").mkdir(parents=True)
    skill_root.mkdir(parents=True)

    shutil.copy2(MANIFEST, plugin_root / ".codex-plugin" / "plugin.json")
    shutil.copy2(SKILL_ROOT / "SKILL.md", skill_root / "SKILL.md")
    shutil.copy2(SKILL_ROOT / "eval.md", skill_root / "eval.md")
    shutil.copy2(ICON, plugin_root / "assets" / ICON.name)
    shutil.copy2(ROOT / "LICENSE", plugin_root / "LICENSE")
    shutil.copy2(ROOT / "PRIVACY.md", plugin_root / "PRIVACY.md")
    shutil.copy2(ROOT / "TERMS.md", plugin_root / "TERMS.md")

    archive = DIST / f"{PLUGIN_NAME}-plugin-{manifest['version']}.zip"
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as output:
        for path in sorted(plugin_root.rglob("*")):
            if path.is_file():
                output.write(path, path.relative_to(DIST))
    return plugin_root, archive


def validate_build(plugin_root: Path, archive: Path) -> None:
    expected = {
        ".codex-plugin/plugin.json",
        f"assets/{PLUGIN_NAME}.png",
        f"skills/{PLUGIN_NAME}/SKILL.md",
        f"skills/{PLUGIN_NAME}/eval.md",
        "LICENSE",
        "PRIVACY.md",
        "TERMS.md",
    }
    actual = {
        path.relative_to(plugin_root).as_posix()
        for path in plugin_root.rglob("*")
        if path.is_file()
    }
    if expected != actual:
        raise SystemExit(f"打包文件不一致: 期望 {sorted(expected)}，实际 {sorted(actual)}")

    packaged_skill = plugin_root / "skills" / PLUGIN_NAME / "SKILL.md"
    packaged_eval = plugin_root / "skills" / PLUGIN_NAME / "eval.md"
    if packaged_skill.read_bytes() != (SKILL_ROOT / "SKILL.md").read_bytes():
        raise SystemExit("打包后的 SKILL.md 与源文件不一致")
    if packaged_eval.read_bytes() != (SKILL_ROOT / "eval.md").read_bytes():
        raise SystemExit("打包后的 eval.md 与源文件不一致")
    if not zipfile.is_zipfile(archive):
        raise SystemExit("插件包不是合法的 ZIP 文件")


def main() -> None:
    args = parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate_source(manifest)
    plugin_root, archive = build_plugin(manifest)
    validate_build(plugin_root, archive)
    print(f"已构建 {archive.relative_to(ROOT)}")
    if args.check:
        shutil.rmtree(plugin_root)
        archive.unlink()
        try:
            DIST.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    main()
