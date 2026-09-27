#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from collections import defaultdict

YAML_PATH = "proc-alias.yaml"

# 包名分类正则匹配规则
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
    md.append("# 📊 proc-alias.yaml 分析与检测报告\n")

    # 1. 核心数据统计面板
    md.append("## 📈 核心指标数据")
    md.append("| 统计指标 | 数量 | 校验状态 |")
    md.append("| :--- | :---: | :---: |")
    md.append(f"| 原始解析总条数 | `{total_count}` | - |")
    md.append(f"| 去重后有效包名数 | `{unique_count}` | - |")
    if dup_count > 0:
        md.append(f"| 重复包名数 | `{dup_count}` | ❌ **失败（存在重复）** |")
    else:
        md.append(f"| 重复包名数 | `0` | ✅ **通过（无重复）** |")
    md.append("\n")

    # 2. 重复告警列表（若有重复）
    if dup_count > 0:
        md.append("## ❌ 报错：发现重复包名")
        md.append("| 包名 (Package Name) | 首次出现位置 | 冲突/重复行号 |")
        md.append("| :--- | :---: | :---: |")
        for pkg, items in dup_pkgs.items():
            first_line = seen_pkgs[pkg]['line']
            other_lines = ", ".join([f"`第 {x['line']} 行`" for x in items])
            md.append(f"| `{pkg}` | `第 {first_line} 行` | {other_lines} |")
        md.append("\n> ⚠️ **请尽快修改 `proc-alias.yaml` 删除上述重复行！**\n")

    # 3. 按包名名称分类统计
    md.append("## 📦 包名按类别汇总统计")
    md.append("| 应用分类类别 | 包含应用数 | 占比 |")
    md.append("| :--- | :---: | :---: |")
    for cat, items in sorted(category_map.items(), key=lambda x: len(x[1]), reverse=True):
        ratio = (len(items) / unique_count * 100) if unique_count else 0
        md.append(f"| **{cat}** | `{len(items)}` | `{ratio:.1f}%` |")
    md.append("\n")

    # 4. 可折叠的完整包名分类清单
    md.append("## 📋 包名分类明细")
    for cat, items in sorted(category_map.items(), key=lambda x: len(x[1]), reverse=True):
        md.append(f"<details><summary><b>{cat}</b> （点击展开明细 - 共 {len(items)} 个应用）</summary>\n")
        md.append("| 包名 (Package Name) | 目录别名 (Alias) | 备注说明 |")
        md.append("| :--- | :--- | :--- |")
        for item in sorted(items, key=lambda x: x["pkg"]):
            comment = item['comment'] if item['comment'] else "-"
            md.append(f"| `{item['pkg']}` | `{item['alias']}` | {comment} |")
        md.append("\n</details>\n")

    return "\n".join(md)

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

    # 生成完整 Markdown 报告
    md_content = build_markdown_report(entries, dup_pkgs, seen_pkgs, category_map)

    # 终端打印输出
    print(md_content)

    # 如果运行在 GitHub Actions 环境中，直接写入 GitHub Step Summary
    summary_env = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_env:
        with open(summary_env, "a", encoding="utf-8") as f:
            f.write(md_content + "\n")

    if dup_pkgs:
        sys.exit(1)

if __name__ == "__main__":
    main()
