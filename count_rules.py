import os
import re
import yaml
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 不参与规则统计的文件（配置文件、脚本自身依赖等）
IGNORE_FILES = ['config.yaml', 'nodes.yaml', 'requirements.txt', 'clashmi_api.md']

LOGIC_TYPES = {'AND', 'OR', 'NOT'}


def split_top_level(s: str, sep: str = ',') -> list:
    """按顶层逗号切分，忽略括号内部的逗号"""
    parts, depth, current = [], 0, ''
    for ch in s:
        if ch == '(':
            depth += 1
            current += ch
        elif ch == ')':
            depth -= 1
            current += ch
        elif ch == sep and depth == 0:
            parts.append(current)
            current = ''
        else:
            current += ch
    parts.append(current)
    return [p.strip() for p in parts if p.strip()]


def strip_outer_parens(s: str) -> str:
    s = s.strip()
    if s.startswith('(') and s.endswith(')'):
        return s[1:-1].strip()
    return s


def normalize_rule(raw: str) -> str:
    """
    把规则归一化，让"逻辑等价但书写顺序不同"的 AND/OR 复合规则
    在比较时被视为相同。简单规则（DOMAIN、PROCESS-NAME等）原样返回。
    """
    raw = raw.strip()
    top = split_top_level(raw, ',')
    if not top:
        return raw

    rule_type = top[0].strip().upper()

    if rule_type in LOGIC_TYPES and len(top) >= 2:
        # top[1] 形如 "((a),(b),(c))"，去掉最外层括号后按顶层逗号切分
        group_str = strip_outer_parens(top[1])
        children = split_top_level(group_str, ',')
        normalized_children = sorted(
            normalize_rule(strip_outer_parens(c)) for c in children
        )
        target_part = ','.join(top[2:])  # 保留目标策略/no-resolve等后续参数
        return f"{rule_type}({'|'.join(normalized_children)})->{target_part}"

    # 非逻辑规则，原样返回（大小写、空格已在 split_top_level 里 strip 过）
    return raw


def load_yaml_data(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"⚠️ 跳过 {os.path.basename(path)}：YAML 解析失败 - {e}")
        return None


def extract_entries(data, filename):
    """
    从解析后的 yaml 数据里提取所有规则条目，返回 [(来源标签, 原始规则文本), ...]
    支持三种结构：
      - payload: [...]                标准 rule-provider
      - rules: [...]                  主配置文件的顶层规则列表
      - sub-rules: {组名: [...], ...} 子规则定义
    """
    entries = []
    if not data or not isinstance(data, dict):
        return entries

    if 'payload' in data and data['payload']:
        for r in data['payload']:
            entries.append((filename, str(r).strip()))

    if 'rules' in data and data['rules']:
        for r in data['rules']:
            entries.append((f"{filename}[rules]", str(r).strip()))

    if 'sub-rules' in data and data['sub-rules']:
        for group_name, conditions in data['sub-rules'].items():
            if not conditions:
                continue
            for r in conditions:
                entries.append((f"{filename}[sub-rule:{group_name}]", str(r).strip()))

    return entries


def load_text_rules(path):
    entries = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            clean = line.strip()
            if clean and not clean.startswith('#'):
                entries.append((os.path.basename(path), clean))
    return entries


def categorize(rule: str) -> str:
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
        table += f"### ⚠️ 跨文件/跨模块重复规则（共 {len(duplicates)} 条，含逻辑等价识别）\n\n"
        table += "| 规则内容 | 出现在 |\n| :--- | :--- |\n"
        for norm_key, occurrences in sorted(duplicates.items()):
            # occurrences: list of (source, raw_text)
            display_raw = occurrences[0][1]
            sources = ', '.join(o[0] for o in occurrences)
            safe_raw = display_raw.replace('|', '\\|')
            table += f"| `{safe_raw}` | {sources} |\n"
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

    # normalized_key -> [(source, raw_text), ...]
    norm_to_occurrences = defaultdict(list)

    yaml_files = [f for f in os.listdir(BASE_DIR)
                  if f.endswith(('.yaml', '.yml', '.txt', '.list'))
                  and f not in IGNORE_FILES]

    for f_name in yaml_files:
        path = os.path.join(BASE_DIR, f_name)
        if not os.path.exists(path):
            continue

        if f_name.endswith(('.txt', '.list')):
            file_entries = load_text_rules(path)
        else:
            data = load_yaml_data(path)
            file_entries = extract_entries(data, f_name)
            if not file_entries:
                # 兼容非标准结构：退回按行读取
                file_entries = load_text_rules(path)

        # 按"文件"维度去重计数（同文件内重复的规则只算一次）
        file_rule_set = {raw for _, raw in file_entries}
        stats[f_name] = len(file_rule_set)
        all_rules_set.update(file_rule_set)

        for source, raw in file_entries:
            type_stats[categorize(raw)] += 1
            norm_key = normalize_rule(raw)
            norm_to_occurrences[norm_key].append((source, raw))

    # 只保留真正出现在"不同来源"里的重复（同一文件内部重复不算跨文件问题）
    duplicates = {}
    for norm_key, occ in norm_to_occurrences.items():
        sources = {o[0] for o in occ}
        if len(sources) > 1:
            duplicates[norm_key] = occ

    update_readme(stats, type_stats, len(all_rules_set), duplicates)

    print(f"总计 {len(yaml_files)} 个文件，去重后 {len(all_rules_set)} 条规则")
    if duplicates:
        print(f"⚠️ 发现 {len(duplicates)} 组跨来源重复规则（含逻辑等价识别），已写入 README")
