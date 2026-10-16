#!/usr/bin/env python3
"""Validate a Vidu Q2 production prompt document."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED = ("供应商", "系列", "模型", "模式", "时长", "画幅", "分辨率", "音频")
SEEDANCE_FIELDS = (
    "Objective:",
    "Reference binding:",
    "Immutable locks:",
    "Target duration:",
    "Timeline:",
    "Visual direction:",
    "Audio direction:",
    "Preserve:",
    "Avoid:",
)


def field(text: str, name: str) -> str | None:
    matches = re.findall(rf"^{re.escape(name)}：\s*(.+)$", text, re.MULTILINE)
    return matches[0].strip() if len(matches) == 1 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    args = parser.parse_args()

    try:
        text = args.file.read_text(encoding="utf-8").strip()
    except OSError as exc:
        print(f"FAIL: 读取失败：{exc}")
        return 2

    errors: list[str] = []
    if not re.search(r"^# G\d+\s+Vidu\s+Q2\s+提示词", text, re.MULTILINE):
        errors.append("标题必须使用 `# G01 Vidu Q2 提示词`")

    values: dict[str, str] = {}
    for name in REQUIRED:
        value = field(text, name)
        if value is None:
            errors.append(f"`{name}：` 必须且只能出现一次")
        else:
            values[name] = value

    if values.get("系列", "").upper() != "Q2":
        errors.append("`系列` 必须是 Q2")

    model = values.get("模型", "").lower()
    mode = values.get("模式", "")
    resolution = values.get("分辨率", "").lower()
    if "q3" in model:
        errors.append("Q2 文件不得使用 Q3 模型 ID")
    if model and "q2" not in model:
        errors.append("模型 ID 未显示属于 Q2，需核对真实供应商 ID")

    if "pro-fast" in model or "pro_fast" in model:
        if "参考" in mode:
            errors.append("Q2 Pro Fast 不支持参考生视频，应改用 Q2 Pro Reference")
        if resolution and resolution not in {"720p", "1080p"}:
            errors.append("Q2 Pro Fast 仅允许 720p 或 1080p")

    if text.count("## 提交正文") != 1:
        errors.append("`## 提交正文` 必须且只能出现一次")
        body = ""
    else:
        body = text.split("## 提交正文", 1)[1].strip()
        if len(body) < 40:
            errors.append("提交正文过短")

    for item in SEEDANCE_FIELDS:
        if re.search(rf"^{re.escape(item)}", body, re.MULTILINE):
            errors.append(f"不得使用 Seedance 字段 `{item}`")

    if ("图生" in mode or "img2video" in mode.lower()) and len(body) > 2000:
        errors.append("Q2 图生提交正文超过 2000 字符")
    elif len(body) > 5000:
        errors.append("Q2 提交正文超过 5000 字符")

    is_rec = field(text, "is_rec")
    if "图生" in mode and is_rec is None:
        errors.append("Q2 图生必须明确记录 `is_rec：false` 或真实配置")
    if is_rec and is_rec.lower() == "true" and body:
        errors.append("`is_rec=true` 可能忽略手写正文，正式手写提示词必须设为 false")
    if ("pro-fast" in model or "pro_fast" in model) and (
        re.search(r"图\d+\s*为", body) or "[@" in body
    ):
        errors.append("Q2 Pro Fast 不得使用多参考图片编号或 subject 绑定语法")

    inputs = re.findall(r"^\d+\.\s+.+?\s+[—-]\s+.+$", text, re.MULTILINE)
    if "首尾帧" in mode and len(inputs) != 2:
        errors.append("首尾帧模式必须且只能登记两张输入图")
    if "图生" in mode and "首尾帧" not in mode and len(inputs) != 1:
        errors.append("普通图生模式必须且只能登记一张首帧")
    if "参考" in mode and not inputs:
        errors.append("参考生模式必须登记真实参考素材")

    duration = values.get("时长", "")
    match = re.search(r"(\d+)", duration)
    if match and int(match.group(1)) > 10:
        errors.append("Q2 单段时长不得超过 10 秒")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: Vidu Q2 prompt format")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
