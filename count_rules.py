import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULE_FILES = ['google-android.yaml', 'bytedance-global.yaml', 'cn-direct.yaml']

def update_readme(stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    # 1. 这里必须填入具体的标记，绝对不能留空
    start_marker = ""
    end_marker = ""
    
    table = f"\n### 📊 规则统计详情\n\n| 规则集名称 | 唯一规则数量 |\n| :--- | :--- |\n"
    for name, count in stats.items():
        table += f"| {name} | {count} |\n"
    table += f"| **全库去重总计** | **{total_unique}** |\n\n"

    new_block = f"{start_marker}{table}{end_marker}"

    # 2. 读取并替换逻辑
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if start_marker in content and end_marker in content:
            parts = content.split(start_marker)
            post_parts = parts[1].split(end_marker)
            new_content = parts[0] + new_block + post_parts[1]
        else:
            # 如果 README 里没标记，就直接在最前面加上，防止脚本报错
            new_content = new_block + "\n\n" + content
    else:
        new_content = "# 我的规则库\n\n" + new_block

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    res, total_set = {}, set()
    for f_name in RULE_FILES:
        path = os.path.join(BASE_DIR, f_name)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                # 纯净去重统计，不搞任何大小写干扰
                rules = [l.strip().lstrip('- ') for l in f if l.strip() and not l.strip().startswith(('#', 'payload:'))]
            
            unique_list = sorted(list(set(rules)))
            
            # 写回 YAML 文件，让你的规则列表也变整齐
            with open(path, 'w', encoding='utf-8') as f:
                f.write("payload:\n")
                for r in unique_list:
                    f.write(f"  - {r}\n")
            
            res[f_name] = len(unique_list)
            total_set.update(unique_list)
            
    update_readme(res, len(total_set))
