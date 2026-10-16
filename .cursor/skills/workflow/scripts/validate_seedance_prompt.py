#!/usr/bin/env python3
"""Validate one final Seedance segment prompt against workflow A9."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HEADER = re.compile(
    r"^G\d+\｜Batch\s+.+?\s*/\s*段\s+\d+\s*"
    r"\｜目标模型：Seedance\s+(2\.[05])\s*"
    r"\｜本段时长：\d+(?:\.\d+)?s\s*"
    r"\｜全局时间：\d{2}:\d{2}–\d{2}:\d{2}$",
    re.MULTILINE,
)


def validate_header(text: str, model: str, errors: list[str]) -> None:
    matches = HEADER.findall(text)
    if len(matches) != 1:
        errors.append("必须且只能包含一个符合 A9 的 G0N 段头")
    elif matches[0] != model:
        errors.append(f"段头模型是 {matches[0]}，命令指定的是 {model}")


def validate_20(text: str, errors: list[str]) -> None:
    required = [
        "## 资产标识",
        "### 涉及角色",
        "### 涉及场景",
        "### 关键道具",
        "【正式提示词】",
        "## 人物空间关系",
        "## 光线",
        "## 声音",
        "## 正向锁",
        "## 文字锁",
    ]
    for field in required:
        if text.count(field) != 1:
            errors.append(f"`{field}` 必须且只能出现一次")
    if not re.search(
        r"^## 镜头\s+.+?｜\d{2}:\d{2}–\d{2}:\d{2}｜"
        r"\d+(?:\.\d+)?s｜.+$",
        text,
        re.MULTILINE,
    ):
        errors.append("缺少符合 A9.1 的镜头标题")
    if "## 文字锁" in text and not re.search(
        r"## 文字锁\s*\n[^\n]*无字幕、无额外屏幕文字、无后期叠字",
        text,
    ):
        errors.append("文字锁必须包含 A9.1 的无字幕固定句")


def field_positions(text: str) -> list[tuple[str, int, int]]:
    pattern = re.compile(
        r"^(Objective|Reference binding|Immutable locks|Target duration|"
        r"Timeline|Visual direction|Audio direction|Preserve|Avoid):"
        r"(?:[ \t]*(.*))?$",
        re.MULTILINE,
    )
    return [(m.group(1), m.start(), m.end()) for m in pattern.finditer(text)]


def validate_25(text: str, errors: list[str]) -> None:
    required = [
        "Objective",
        "Immutable locks",
        "Target duration",
        "Timeline",
        "Visual direction",
        "Audio direction",
        "Preserve",
        "Avoid",
    ]
    allowed = [
        "Objective",
        "Reference binding",
        "Immutable locks",
        "Target duration",
        "Timeline",
        "Visual direction",
        "Audio direction",
        "Preserve",
        "Avoid",
    ]

    fields = field_positions(text)
    names = [name for name, _, _ in fields]
    for field in required:
        if names.count(field) != 1:
            errors.append(f"`{field}` 必须且只能出现一次")
    if names.count("Reference binding") > 1:
        errors.append("`Reference binding` 最多出现一次")

    expected = [name for name in allowed if name in names]
    if names != expected:
        errors.append("A9.2 顶层字段顺序错误或存在重复字段")

    unknown = re.findall(r"^([A-Za-z][A-Za-z ]+):(?:\s|$)", text, re.MULTILINE)
    unknown = [name for name in unknown if name not in allowed]
    if unknown:
        errors.append("存在 A9.2 白名单外字段：" + "、".join(sorted(set(unknown))))
    if re.search(r"^#{1,6}\s+", text, re.MULTILINE):
        errors.append("A9.2 最终正文不得使用 Markdown 标题或编号式分镜章节")
    if re.search(r"^镜头\s*\d+|^##\s*镜头", text, re.MULTILINE):
        errors.append("A9.2 不得另立镜头编号体系")
    if "同上" in text or "沿用上一段参考" in text:
        errors.append("A9.2 每段必须自包含，禁止使用“同上/沿用上一段参考”")
    if not re.search(r"^Target duration:\s*\d+(?:\.\d+)?\s*seconds\s*$", text, re.MULTILINE):
        errors.append("`Target duration` 必须使用 `X seconds`")
    if not re.search(r"【0:\d{2}-0:\d{2}】", text):
        errors.append("`Timeline` 缺少 `【0:00-0:XX】` 时间块")

    for index, (name, _, end) in enumerate(fields):
        next_start = fields[index + 1][1] if index + 1 < len(fields) else len(text)
        body = text[end:next_start].strip()
        if not body and name != "Target duration":
            errors.append(f"`{name}` 内容为空")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--model", required=True, choices=("2.0", "2.5"))
    args = parser.parse_args()

    try:
        text = args.file.read_text(encoding="utf-8").strip()
    except OSError as exc:
        print(f"读取失败：{exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    validate_header(text, args.model, errors)
    if args.model == "2.0":
        validate_20(text, errors)
    else:
        validate_25(text, errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: Seedance {args.model} A9 format")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
