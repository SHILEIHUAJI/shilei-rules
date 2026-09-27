#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from collections import defaultdict

YAML_PATH = "proc-alias.yaml"

# 分类规则：正则匹配前缀 -> 分类标签
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
            # 过滤空行和纯注释行
            if not stripped or stripped.startswith("#"):
                continue
            
            # 解析格式: package.name: alias # 注释
            match = re.match(r"^([a-zA-Z0-9_\.]+):\s*([^\s#]+)(?:\s*#\s*(.*))?$", stripped)
            if match:
                pkg, alias, comment = match.groups()
                entries.append({
                    "line": line_num,
                    "pkg": pkg,
                    "alias": alias,
                    "comment": comment.strip() if comment else ""
                })
            else:
                print(f"⚠️  第 {line_num} 行语法解析跳过: {stripped}")

    return entries

def main():
    entries = parse_yaml_file(YAML_PATH)
    
    # 1. 检测重复项
    seen_pkgs = {}
    dup_pkgs = defaultdict(list)
    
    for item in entries:
        pkg = item["pkg"]
        if pkg in seen_pkgs:
            dup_pkgs[pkg].append(item)
        else:
            seen_pkgs[pkg] = item

    unique_entries = list(seen_pkgs.values())

    print("=" * 60)
    print("📊 proc-alias.yaml 检测与分析报告")
    print("=" * 60)
    
    print(f"📈 原始总解析数 : {len(entries)} 条")
    print(f"✨ 去重后有效数 : {len(unique_entries)} 条")

    # 2. 输出重复警报
    has_duplicates = False
    if dup_pkgs:
        has_duplicates = True
        print(f"\n❌ 发现 {len(dup_pkgs)} 个重复的包名:")
        for pkg, items in dup_pkgs.items():
            first_line = seen_pkgs[pkg]['line']
            other_lines = ", ".join([str(x['line']) for x in items])
            print(f"   • {pkg}")
            print(f"     - 首次出现: 第 {first_line} 行")
            print(f"     - 重复出现: 第 {other_lines} 行")
    else:
        print("\n✅ 包名唯一性校验通过（未发现重复项）")

    # 3. 按包名规则归类统计
    category_map = defaultdict(list)
    for item in unique_entries:
        cat = classify_package(item["pkg"])
        category_map[cat].append(item)

    print("\n📦 包名分类汇总统计:")
    print("-" * 40)
    for cat, items in sorted(category_map.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  • {cat:<25}: {len(items):>3} 个应用")

    # 4. 输出各分类下的详细清单
    print("\n📋 各分类明细列表:")
    print("-" * 40)
    for cat, items in sorted(category_map.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n【{cat}】(共 {len(items)} 个):")
        for item in sorted(items, key=lambda x: x["pkg"]):
            comment_info = f" ({item['comment']})" if item['comment'] else ""
            print(f"  - {item['pkg']} => {item['alias']}{comment_info}")

    print("\n" + "=" * 60)

    # 如果有重复，让 CI 运行失败并退出
    if has_duplicates:
        print("❌ 校验未通过：请删除或合并 `proc-alias.yaml` 中的重复包名。")
        sys.exit(1)
    else:
        print("🎉 校验成功完成！")

if __name__ == "__main__":
    main()
