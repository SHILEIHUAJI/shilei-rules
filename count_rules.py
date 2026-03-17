import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 你的规则文件列表
RULE_FILES = ['google-android.yaml', 'bytedance-global.yaml', 'cn-direct.yaml']

def update_readme(stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    # 物理拼接标记，防止被屏蔽
    s_m = "<" + "!-- STATS_START --" + ">"
    e_m = "<" + "!-- STATS_END --" + ">"
    
    table = f"\n### 📊 规则统计详情\n\n| 规则集名称 | 唯一规则数量 |\n| :--- | :--- |\n"
    for name, count in stats.items():
        table += f"| {name} | {count} |\n"
    table += f"| **全库去重总计** | **{total_unique}** |\n\n"

    new_block = s_m + table + e_m

    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if s_m in content and e_m in content:
            pre = content.split(s_m)[0]
            post = content.split(e_m)[1]
            new_content = pre + new_block + post
        else:
            new_content = content.strip() + "\n\n" + new_block
    else:
        new_content = "# Rules\n\n" + new_block

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    res, all_rules_set = {}, set()
    
    for f_name in RULE_FILES:
        path = os.path.join(BASE_DIR, f_name)
        if os.path.exists(path):
            file_rules = set()
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    clean = line.strip()
                    # 仅仅统计以 "- " 开头的行，但不修改原文件
                    if clean.startswith('- '):
                        rule_content = clean.lstrip('- ').split(' #')[0].strip()
                        if rule_content and rule_content != "payload:":
                            file_rules.add(rule_content)
            
            res[f_name] = len(file_rules)
            all_rules_set.update(file_rules)
    
    # 这里只更新 README，不再 open(path, 'w') 你的 YAML 文件
    update_readme(res, len(all_rules_set))

