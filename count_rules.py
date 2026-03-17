import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULE_FILES = ['google-android.yaml', 'bytedance-global.yaml', 'cn-direct.yaml']

def update_readme(file_stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    s_m, e_m = "<" + "!-- STATS_START --" + ">", "<" + "!-- STATS_END --" + ">"
    
    table = "\n### 🛡️ Mihomo 规则库深度审计报告\n\n"
    table += "| 文件名 | 总数 | 域名类 | IP类 | 应用/协议 | 逻辑/高级 | 异常 |\n"
    table += "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n"
    for name, s in file_stats.items():
        table += f"| {name} | **{s['total']}** | {s['dns']} | {s['ip']} | {s['app']} | {s['adv']} | {s['err']} |\n"
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
        new_content = "# Rules\n\n" + new_block

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    # 采用正则匹配，容错率更高
    patterns = {
        'dns': re.compile(r'^(DOMAIN|GEOSITE)', re.I),
        'ip': re.compile(r'^(IP-|GEOIP)', re.I),
        'app': re.compile(r'^(PROCESS-|NETWORK|DSCP|IN-|USER-AGENT)', re.I),
        'adv': re.compile(r'^(AND|OR|NOT|SUB-RULE|MATCH)', re.I)
    }

    file_stats = {}
    all_unique_rules = set()

    for f_name in RULE_FILES:
        path = os.path.join(BASE_DIR, f_name)
        stats = {'total': 0, 'dns': 0, 'ip': 0, 'app': 0, 'adv': 0, 'err': 0}
        unique_in_file = set()

        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    # 匹配 - 开头的行
                    match = re.search(r'^\s*-\s+([A-Z0-9\-\(\)]+)', line, re.I)
                    if not match: continue
                    
                    raw_rule = line.strip().lstrip('- ').split('#')[0].strip()
                    if not raw_rule or raw_rule.lower() == "payload:": continue
                    
                    unique_in_file.add(raw_rule.upper())
                    all_unique_rules.add(raw_rule.upper())
                    
                    key = match.group(1).upper()
                    
                    # 分类逻辑
                    if patterns['dns'].match(key): stats['dns'] += 1
                    elif patterns['ip'].match(key): stats['ip'] += 1
                    elif patterns['app'].match(key): stats['app'] += 1
                    elif patterns['adv'].match(key) or key.startswith('('): stats['adv'] += 1
                    else: stats['err'] += 1
            
            stats['total'] = len(unique_in_file)
            file_stats[f_name] = stats

    update_readme(file_stats, len(all_unique_rules))
