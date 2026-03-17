import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULE_FILES = ['google-android.yaml', 'bytedance-global.yaml', 'cn-direct.yaml']

def update_readme(file_stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    s_m, e_m = "<" + "!-- STATS_START --" + ">", "<" + "!-- STATS_END --" + ">"
    
    # 构建更高级的统计表格
    table = "\n### 📊 规则库深度审计\n\n"
    table += "| 规则集文件 | 总计 | Suffix | Domain | IP/ASN | 其他 |\n"
    table += "| :--- | :---: | :---: | :---: | :---: | :---: |\n"
    
    for name, s in file_stats.items():
        table += f"| {name} | **{s['total']}** | {s['suffix']} | {s['domain']} | {s['ip']} | {s['other']} |\n"
    
    table += f"\n> **全库去重后的唯一规则总数：{total_unique}**\n\n"
    new_block = s_m + table + e_m

    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if s_m in content and e_m in content:
            pre, post = content.split(s_m)[0], content.split(e_m)[1]
            new_content = pre + new_block + post
        else:
            new_content = content.strip() + "\n\n" + new_block
    else:
        new_content = "# Mihomo Rules\n\n" + new_block

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    file_stats = {}
    all_unique_rules = set()

    for f_name in RULE_FILES:
        path = os.path.join(BASE_DIR, f_name)
        stats = {'total': 0, 'suffix': 0, 'domain': 0, 'ip': 0, 'other': 0}
        unique_in_file = set()

        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    clean = line.strip()
                    if not clean.startswith('- '): continue
                    
                    # 提取核心规则，去掉前面的 "- " 和后面的注释
                    core = clean.lstrip('- ').split('#')[0].strip().upper()
                    if not core or core == "PAYLOAD:": continue
                    
                    unique_in_file.add(core)
                    all_unique_rules.add(core)
                    
                    # 分类识别逻辑
                    if 'DOMAIN-SUFFIX' in core: stats['suffix'] += 1
                    elif 'DOMAIN' in core and 'SUFFIX' not in core: stats['domain'] += 1
                    elif any(x in core for x in ['IP-CIDR', 'IP-ASN', 'IP6']): stats['ip'] += 1
                    else: stats['other'] += 1
            
            stats['total'] = len(unique_in_file)
            file_stats[f_name] = stats

    update_readme(file_stats, len(all_unique_rules))
