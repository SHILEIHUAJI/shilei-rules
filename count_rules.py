import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULE_FILES = ['google-android.yaml', 'bytedance-global.yaml', 'cn-direct.yaml']

def process_rules():
    file_stats = {}
    all_unique_rules = set()
    for filename in RULE_FILES:
        filepath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(filepath): continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        header, raw_rules = [], []
        for line in lines:
            clean = line.strip()
            if clean.startswith('payload:') or clean.startswith('#') or not clean:
                if not raw_rules: header.append(line)
            else:
                # 提取规则内容
                rule_content = clean.lstrip('- ').strip()
                if rule_content: raw_rules.append(rule_content)

        # 去重排序
        unique_raw_rules = sorted(list(set(raw_rules)))
        
        # 写回文件（保持整洁）
        with open(filepath, 'w', encoding='utf-8') as f:
            for h in header: f.write(h)
            for r in unique_raw_rules: f.write(f"  - {r}\n")

        file_stats[filename] = len(unique_raw_rules)
        all_unique_rules.update(unique_raw_rules)
    return file_stats, len(all_unique_rules)

def update_readme(stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    start_marker = ""
    end_marker = ""
    
    # 生成新表格
    table = f"\n### 📊 规则统计详情\n\n| 规则集名称 | 唯一规则数量 |\n| :--- | :--- |\n"
    for name, count in stats.items():
        table += f"| {name} | {count} |\n"
    table += f"| **全库去重总计** | **{total_unique}** |\n\n"

    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 寻找标记位置
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            # 只替换两个标记之间的部分，其余不动
            new_content = content[:start_idx + len(start_marker)] + table + content[end_idx:]
        else:
            # 如果没找到标记，清空所有旧的统计，重新格式化
            print("未找到标记，正在重新初始化 README...")
            new_content = "# 我的 Mihomo 分流规则库\n\n" + start_marker + table + end_marker
    else:
        new_content = "# 我的 Mihomo 分流规则库\n\n" + start_marker + table + end_marker

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    stats, total = process_rules()
    update_readme(stats, total)
