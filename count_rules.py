import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 如果有不想统计的 YAML（如订阅配置），填在这里
IGNORE_FILES = ['config.yaml', 'nodes.yaml']

def update_readme(stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    # 物理拼接，确保暗号不被任何环境拦截
    s_m = "<" + "!-- STATS_START --" + ">"
    e_m = "<" + "!-- STATS_END --" + ">"
    
    table = f"\n### 📊 规则统计详情\n\n| 规则集名称 | 唯一规则数量 |\n| :--- | :--- |\n"
    # 按文件名排序，让表格看起来更整齐
    for name in sorted(stats.keys()):
        table += f"| {name} | {stats[name]} |\n"
    table += f"| **全库去重总计** | **{total_unique}** |\n\n"

    new_block = s_m + table + e_m

    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if s_m in content and e_m in content:
            parts_pre = content.split(s_m)[0]
            parts_post = content.split(e_m)[1]
            new_content = parts_pre + new_block + parts_post
        else:
            new_content = content.strip() + "\n\n" + new_block
    else:
        new_content = "# Rules\n\n" + new_block

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    res, all_rules_set = {}, set()
    
    # --- 自动化扫描：获取目录下所有 .yaml 文件 ---
    yaml_files = [f for f in os.listdir(BASE_DIR) 
                  if f.endswith('.yaml') and f not in IGNORE_FILES]
    
    for f_name in yaml_files:
        path = os.path.join(BASE_DIR, f_name)
        if os.path.exists(path):
            file_rules = set()
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    clean = line.strip()
                    # 核心逻辑：只读取以 "- " 开头的行，保留你的原汁原味
                    if clean.startswith('- '):
                        # 剔除注释部分再进行统计计数
                        rule_content = clean.lstrip('- ').split(' #')[0].strip()
                        if rule_content and rule_content.lower() != "payload:":
                            file_rules.add(rule_content)
            
            res[f_name] = len(file_rules)
            all_rules_set.update(file_rules)
    
    # 仅更新 README，绝对不碰你的规则文件
    update_readme(res, len(all_rules_set))
