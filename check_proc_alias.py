#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from collections import defaultdict

YAML_PATH = "proc-alias.yaml"
README_PATH = "README.md"

# README 中的自动插入锚点
START_MARKER = "<!-- STATS_START -->"
END_MARKER = "<!-- STATS_END -->"

# 包名分类正则规则
CLASSIFICATION_RULES = [
    (r"^com\.google\.", "Google 系应用与服务"),
    (r"^com\.android\.", "Android 系统核心组件"),
    (r"^(com\.ss\.android|com\.bytedance)", "字节跳动系 (ByteDance)"),
    (r"^com\.tencent\.", "腾讯系 (Tencent)"),
    (r"^com\.baidu\.", "百度系 (Baidu)"),
    (r"^(com\.taobao|com\.eg\.android|com\.xunmeng|com\.sankuai)", "主流电商与服务 (阿里/拼多多/美团)"),
    (r"^com\.vivo\.", "vivo 厂商应用"),
    (r"^com\.microsoft\.", "微软系 (Microsoft)"),
    (r"^(io\.github|com\.github|org\.fdroid|moe\.shizuku|li\.songe|bin\.mt)", "GitHub / 开源与极客工具"),
    (r"^org\.", "开源软件组织 (org.*)"),
]

def classify_package(pkg):
    for pattern, category in CLASSIFICATION_RULES:
        if re.search(pattern, pkg, re.IGNORECASE):
            return category
    return "其他第三方应用"

def parse_yaml_file(filepath):
    if not os.path.exists(filepath):
        print(f"❌ 错误: 未在根目录下找到文件 '{filepath}'")
        sys.exit(1)

    entries = []
    line_num = 0

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line_num += 1
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            
            match = re.match(r"^([a-zA-Z0-9_\.]+):\s*([^\s#]+)(?:\s*#\s*(.*))?$", stripped)
            if match:
                pkg, alias, comment = match.groups()
                entries.append({
                    "line": line_num,
                    "pkg": pkg,
                    "alias": alias,
                    "comment": comment.strip() if comment else ""
                })

    return entries

def build_markdown_report(entries, dup_pkgs, seen_pkgs, category_map):
    total_count = len(entries)
    unique_count = len(seen_pkgs)
    dup_count = len(dup_pkgs)

    md = []
    md.append(f"{START_MARKER}")
    md.append("## 📊 实时数据统计大屏\n")

    # 1. 核心数据指标
    md.append("### 📈 核心指标")
    md.append("| 统计指标 | 数量 | 校验状态 |")
    md.append("| :--- | :---: | :---: |")
    md.append(f"| 原始配置条数 | `{total_count}` | - |")
    md.append(f"| 去重后有效应用数 | `{unique_count}` | - |")
    if dup_count > 0:
        md.append(f"| 重复包名冲突 | `{dup_count}` | ❌ **存在冲突（请清理）** |")
    else:
        md.append(f"| 重复包名冲突 | `0` | ✅ **无重复（正常）** |")
    md.append("\n")

    # 2. 重复告警列表
    if dup_count > 0:
        md.append("### ❌ 重复包名警报")
        md.append("| 包名 (Package Name) | 首次出现行号 | 重复冲突行号 |")
        md.append("| :--- | :---: | :---: |")
        for pkg, items in dup_pkgs.items():
            first_line = seen_pkgs[pkg]['line']
            other_lines = ", ".join([f"`第 {x['line']} 行`" for x in items])
            md.append(f"| `{pkg}` | `第 {first_line} 行` | {other_lines} |")
        md.append("\n> ⚠️ **请尽快在 `proc-alias.yaml` 中清理上述重复项！**\n")

    # 3. 按包名名称分类汇总
    md.append("### 📦 按分类汇总统计")
    md.append("| 应用分类类别 | 包含应用数 | 占比 |")
    md.append("| :--- | :---: | :---: |")
    for cat, items in sorted(category_map.items(), key=lambda x: len(x[1]), reverse=True):
        ratio = (len(items) / unique_count * 100) if unique_count else 0
        md.append(f"| **{cat}** | `{len(items)}` | `{ratio:.1f}%` |")
    md.append("\n")

    # 4. 可折叠分类明细表
    md.append("### 📋 详细分类清单")
    for cat, items in sorted(category_map.items(), key=lambda x: len(x[1]), reverse=True):
        md.append(f"<details><summary><b>{cat}</b> （包含 {len(items)} 个应用，点击展开）</summary>\n")
        md.append("| 包名 (Package Name) | 目录别名 (Alias) | 备注说明 |")
        md.append("| :--- | :--- | :--- |")
        for item in sorted(items, key=lambda x: x["pkg"]):
            comment = item['comment'] if item['comment'] else "-"
            md.append(f"| `{item['pkg']}` | `{item['alias']}` | {comment} |")
        md.append("\n</details>\n")

    md.append(f"{END_MARKER}")
    return "\n".join(md)

def update_readme(stats_md):
    if not os.path.exists(README_PATH):
        readme_content = "# Proc Alias 映射表管理与自动校验\n\n"
    else:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme_content = f.read()

    # 如果存在锚点，替换锚点中间的内容；如果不存在，直接追加到末尾
    if START_MARKER in readme_content and END_MARKER in readme_content:
        pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
        new_content = re.sub(pattern, stats_md, readme_content, flags=re.DOTALL)
    else:
        new_content = readme_content.rstrip() + f"\n\n{stats_md}\n"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ 已将最新统计数据写回 README.md！")

def main():
    entries = parse_yaml_file(YAML_PATH)

    seen_pkgs = {}
    dup_pkgs = defaultdict(list)

    for item in entries:
        pkg = item["pkg"]
        if pkg in seen_pkgs:
            dup_pkgs[pkg].append(item)
        else:
            seen_pkgs[pkg] = item

    unique_entries = list(seen_pkgs.values())

    category_map = defaultdict(list)
    for item in unique_entries:
        cat = classify_package(item["pkg"])
        category_map[cat].append(item)

    # 1. 生成 Markdown 统计文本
    stats_md = build_markdown_report(entries, dup_pkgs, seen_pkgs, category_map)

    # 2. 直接写回 README.md 页面
    update_readme(stats_md)

    if dup_pkgs:
        print(f"❌ 检测到 {len(dup_pkgs)} 个重复包名，请前往 README.md 查看详细行号并清理！")
        sys.exit(1)

if __name__ == "__main__":
    main()
