#!/usr/bin/env python3
"""Validate a Vidu Q3 production prompt document."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED = ("供应商", "系列", "模型", "模式", "用途", "时长", "画幅", "分辨率", "音频")
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
    if not re.search(r"^# G\d+\s+Vidu\s+Q3\s+提示词", text, re.MULTILINE):
        errors.append("标题必须使用 `# G01 Vidu Q3 提示词`")

    values: dict[str, str] = {}
    for name in REQUIRED:
        value = field(text, name)
        if value is None:
            errors.append(f"`{name}：` 必须且只能出现一次")
        else:
            values[name] = value

    if values.get("系列", "").upper() != "Q3":
        errors.append("`系列` 必须是 Q3")

    model = values.get("模型", "").lower()
    mode = values.get("模式", "")
    purpose = values.get("用途", "").lower()
    if "q2" in model:
        errors.append("Q3 文件不得使用 Q2 模型 ID")
    if model and "q3" not in model:
        errors.append("模型 ID 未显示属于 Q3，需核对真实供应商 ID")

    if "pro-fast" in model or "pro_fast" in model or "turbo" in model:
        if "参考" in mode:
            errors.append("Q3 Pro Fast/Turbo 不得冒充 Q3 Reference 多参考模型")
    if "drama" in model and "drama" not in purpose and "漫剧" not in purpose and "短剧" not in purpose:
        errors.append("Q3 Drama 的用途必须明确为 Drama、漫剧或短剧")
    if "-ad" in model or "_ad" in model:
        if "ad" not in purpose and "广告" not in purpose:
            errors.append("Q3 Ad 的用途必须明确为广告")

    if text.count("## 提交正文") != 1:
        errors.append("`## 提交正文` 必须且只能出现一次")
        body = ""
    else:
        body = text.split("## 提交正文", 1)[1].strip()
        if len(body) < 40:
            errors.append("提交正文过短")
        if len(body) > 5000:
            errors.append("未声明更高供应商上限时，Q3 提交正文不得超过 5000 字符")

    for item in SEEDANCE_FIELDS:
        if re.search(rf"^{re.escape(item)}", body, re.MULTILINE):
            errors.append(f"不得使用 Seedance 字段 `{item}`")

    inputs = re.findall(r"^\d+\.\s+.+?\s+[—-]\s+.+$", text, re.MULTILINE)
    if "首尾帧" in mode and len(inputs) != 2:
        errors.append("首尾帧模式必须且只能登记两张输入图")
    if "图生" in mode and "首尾帧" not in mode and len(inputs) != 1:
        errors.append("普通图生模式必须且只能登记一张首帧")
    if "参考" in mode and not 1 <= len(inputs) <= 7:
        errors.append("Q3 参考生模式必须登记 1–7 张真实参考图")

    duration = values.get("时长", "")
    match = re.search(r"(\d+)", duration)
    if match:
        seconds = int(match.group(1))
        if seconds > 16:
            errors.append("Q3 单段时长不得超过 16 秒")
        if "drama" in model and seconds < 2:
            errors.append("Q3 Drama 时长通常不得少于 2 秒")
        if ("-ad" in model or "_ad" in model) and seconds < 3:
            errors.append("Q3 Ad 时长通常不得少于 3 秒")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: Vidu Q3 prompt format")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
