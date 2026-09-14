import os
import yaml
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 不想统计的文件
IGNORE_FILES = ['config.yaml', 'nodes.yaml']

# 纯 text 格式的规则文件（一行一条，没有 payload: 包裹）单独列出
TEXT_FORMAT_FILES = []  # 例如 ['my-adblock.txt']


def load_yaml_rules(path):
    """解析标准 clash yaml 规则文件（带 payload: 结构）"""
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not data or 'payload' not in data:
        return set()
    return {str(r).strip() for r in data['payload'] if str(r).strip()}


def load_text_rules(path):
    """解析纯 text 格式（一行一条，# 开头是注释）"""
    rules = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            clean = line.strip()
            if clean and not clean.startswith('#'):
                rules.add(clean)
    return rules


def categorize(rule: str) -> str:
    """按规则类型分类，纯域名/IP格式（没有逗号）归为 DOMAIN 或 IP-CIDR"""
    if ',' in rule:
        return rule.split(',', 1)[0].strip().upper()
    if rule.startswith('+.'):
        return 'DOMAIN-SUFFIX(text)'
    if '/' in rule or rule.replace('.', '').replace(':', '').isdigit():
        return 'IP-CIDR(text)'
    return 'DOMAIN(text)'


def update_readme(stats, type_stats, total_unique, duplicates):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    s_m = "<" + "!-- STATS_START --" + ">"
    e_m = "<" + "!-- STATS_END --" + ">"

    table = "\n### 📊 规则统计详情\n\n"
    table += "| 规则集名称 | 唯一规则数量 |\n| :--- | :--- |\n"
    for name in sorted(stats.keys()):
        table += f"| {name} | {stats[name]} |\n"
    table += f"| **全库去重总计** | **{total_unique}** |\n\n"

    table += "### 🏷️ 规则类型分布\n\n"
    table += "| 类型 | 数量 |\n| :--- | :--- |\n"
    for rtype, count in sorted(type_stats.items(), key=lambda x: -x[1]):
        table += f"| {rtype} | {count} |\n"
    table += "\n"

    if duplicates:
        table += f"### ⚠️ 跨文件重复规则（共 {len(duplicates)} 条）\n\n"
        table += "| 规则内容 | 出现在 |\n| :--- | :--- |\n"
        for rule, files in sorted(duplicates.items()):
            table += f"| `{rule}` | {', '.join(files)} |\n"
        table += "\n"
    else:
        table += "### ✅ 未发现跨文件重复规则\n\n"

    new_block = s_m + table + e_m

    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if s_m in content and e_m in content:
            new_content = content.split(s_m)[0] + new_block + content.split(e_m)[1]
        else:
            new_content = content.strip() + "\n\n" + new_block
    else:
        new_content = "# Rules\n\n" + new_block

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


if __name__ == '__main__':
    stats = {}
    type_stats = Counter()
    all_rules_set = set()
    # 记录每条规则出现在哪些文件里，用于查重
    rule_to_files = defaultdict(list)

    yaml_files = [f for f in os.listdir(BASE_DIR)
                  if f.endswith(('.yaml', '.yml', '.txt', '.list'))
                  and f not in IGNORE_FILES]

    for f_name in yaml_files:
        path = os.path.join(BASE_DIR, f_name)
        if not os.path.exists(path):
            continue

        if f_name in TEXT_FORMAT_FILES or f_name.endswith(('.txt', '.list')):
            file_rules = load_text_rules(path)
        else:
            file_rules = load_yaml_rules(path)
            # 兼容：万一 yaml 文件其实没有 payload 结构，退回按行读取
            if not file_rules:
                file_rules = load_text_rules(path)

        stats[f_name] = len(file_rules)
        all_rules_set.update(file_rules)

        for rule in file_rules:
            type_stats[categorize(rule)] += 1
            rule_to_files[rule].append(f_name)

    # 找出跨文件重复的规则
    duplicates = {r: files for r, files in rule_to_files.items() if len(files) > 1}

    update_readme(stats, type_stats, len(all_rules_set), duplicates)

    print(f"总计 {len(yaml_files)} 个文件，去重后 {len(all_rules_set)} 条规则")
    if duplicates:
        print(f"⚠️ 发现 {len(duplicates)} 条跨文件重复规则，已写入 README")
