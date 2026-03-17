import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULE_FILES = ['google-android.yaml', 'bytedance-global.yaml', 'cn-direct.yaml']

def update_readme(file_stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    s_m, e_m = "<" + "!-- STATS_START --" + ">", "<" + "!-- STATS_END --" + ">"
    
    table = "\n### 🛡️ Mihomo 规则库深度审计报告\n\n"
    table += "| 文件名 | 总数 | 域名类 | IP类 | 进程/协议 | 逻辑/高级 | 异常 |\n"
    table += "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n"
    
    for name, s in file_stats.items():
        table += f"| {name} | **{s['total']}** | {s['dns']} | {s['ip']} | {s['app']} | {s['adv']} | {s['err']} |\n"
    
    table += f"\n> **全库去重后的唯一规则总数：{total_unique}**\n"
    table += f"> *最后更新时间: 2026-03-17*\n\n"
    
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
        new_content = "# My Rules\n\n" + new_block

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    # 定义更完备的语法字典
    SYNTAX = {
        'DNS': ['DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'DOMAIN-SET', 'GEOSITE'],
        'IP': ['IP-CIDR', 'IP-CIDR6', 'IP-ASN', 'GEOIP', 'IP-SET', 'SRC-IP-CIDR'],
        'APP': ['PROCESS-NAME', 'PROCESS-PATH', 'PROCESS-NAME-REGEX', 'NETWORK', 'DSCP', 'IN-PORT', 'IN-TYPE', 'IN-USER', 'IN-NAME'],
        'ADV': ['AND', 'OR', 'NOT', 'SUB-RULE', 'MATCH']
    }

    file_stats = {}
    all_unique_rules = set()

    for f_name in RULE_FILES:
        path = os.path.join(BASE_DIR, f_name)
        # 初始化统计项
        stats = {'total': 0, 'dns': 0, 'ip': 0, 'app': 0, 'adv': 0, 'err': 0}
        unique_in_file = set()

        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    clean = line.strip()
                    if not clean.startswith('- '): continue
                    
                    # 提取核心规则部分
                    core = clean.lstrip('- ').split('#')[0].strip().upper()
                    if not core or core == "PAYLOAD:": continue
                    
                    unique_in_file.add(core)
                    all_unique_rules.add(core)
                    
                    # 匹配语法字典
                    matched = False
                    # 提取每行开头的第一个逗号前的单词，作为判断标准
                    prefix = core.split(',')[0].strip()
                    
                    if prefix in SYNTAX['DNS']:
                        stats['dns'] += 1
                        matched = True
                    elif prefix in SYNTAX['IP']:
                        stats['ip'] += 1
                        matched = True
                    elif prefix in SYNTAX['APP']:
                        stats['app'] += 1
                        matched = True
                    elif prefix in SYNTAX['ADV'] or core.startswith('('):
                        stats['adv'] += 1
                        matched = True
                    
                    if not matched:
                        stats['err'] += 1
            
            stats['total'] = len(unique_in_file)
            file_stats[f_name] = stats

    update_readme(file_stats, len(all_unique_rules))
