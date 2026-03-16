import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULE_FILES = ['google-android.yaml', 'bytedance-global.yaml', 'cn-direct.yaml']

def update_readme(stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    start_marker = ""
    end_marker = ""
    
    table = f"\n### 📊 规则统计详情\n\n| 规则集名称 | 唯一规则数量 |\n| :--- | :--- |\n"
    for name, count in stats.items():
        table += f"| {name} | {count} |\n"
    table += f"| **全库去重总计** | **{total_unique}** |\n\n"

    new_block = f"{start_marker}{table}{end_marker}"

    # 如果文件不存在，直接创建最简版
    if not os.path.exists(readme_path):
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("# Rules\n\n" + new_block)
        return

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if start_marker in content and end_marker in content:
        parts = content.split(start_marker)
        post_parts = parts[1].split(end_marker)
        new_content = parts[0] + new_block + post_parts[1]
    else:
        # 如果找不到标记，为了安全，直接重写整个文件，绝不追加
        new_content = "# Rules\n\n" + new_block

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    # 简单的去重统计逻辑
    res, total_set = {}, set()
    for f_name in RULE_FILES:
        path = os.path.join(BASE_DIR, f_name)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                rules = [l.strip().lstrip('- ') for l in f if l.strip() and not l.strip().startswith(('#', 'payload:'))]
            res[f_name] = len(set(rules))
            total_set.update(rules)
    update_readme(res, len(total_set))
