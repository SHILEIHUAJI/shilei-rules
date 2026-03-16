import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULE_FILES = ['google-android.yaml', 'bytedance-global.yaml', 'cn-direct.yaml']

def process_rules():
    file_stats = {}
    all_unique_rules = set()
    for filename in RULE_FILES:
        filepath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()
        
        header, raw_rules = [], []
        for line in content:
            clean = line.strip()
            if clean.startswith('payload:') or clean.startswith('#') or not clean:
                if not raw_rules: header.append(line)
            else:
                # 统一去掉开头的 - 和空格，方便排序去重
                raw_rules.append(re.sub(r'^-\s*', '', clean))

        unique_raw_rules = sorted(list(set(raw_rules)))
        with open(filepath, 'w', encoding='utf-8') as f:
            for h in header: f.write(h)
            for r in unique_raw_rules: f.write(f"  - {r}\n")

        file_stats[filename] = len(unique_raw_rules)
        all_unique_rules.update(unique_raw_rules)
    return file_stats, len(all_unique_rules)

def update_readme(stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    # 定义占位符标记
    start_marker = ""
    end_marker = ""
    
    table = f"\n### 📊 规则统计详情\n\n| 规则集名称 | 唯一规则数量 |\n| :--- | :--- |\n"
    for name, count in stats.items():
        table += f"| {name} | {count} |\n"
    table += f"| **全库去重总计** | **{total_unique}** |\n"

    new_stats_block = f"{start_marker}{table}{end_marker}"

    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果 README 里已经有占位符，就替换中间的内容
        if start_marker in content and end_marker in content:
            pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
            new_content = re.sub(pattern, new_stats_block, content, flags=re.DOTALL)
        else:
            # 如果没有占位符，直接把旧的“统计详情”连根拔起替换掉，或者追加
            if "### 📊 规则统计详情" in content:
                new_content = re.sub(r"### 📊 规则统计详情.*", new_stats_block, content, flags=re.DOTALL)
            else:
                new_content = content.strip() + "\n\n" + new_stats_block
    else:
        new_content = "# 我的 Mihomo 分流规则库\n\n" + new_stats_block

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    stats_data, unique_total = process_rules()
    update_readme(stats_data, unique_total)
    print(f"处理完成，全库去重总计: {unique_total}")
