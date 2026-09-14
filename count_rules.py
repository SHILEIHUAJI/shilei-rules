import os
import yaml
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IGNORE_FILES = ['config.yaml', 'nodes.yaml', 'requirements.txt', 'clashmi_api.md']

LOGIC_TYPES = {'AND', 'OR', 'NOT'}

VALID_RULE_TYPES = {
    'DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'DOMAIN-REGEX', 'DOMAIN-WILDCARD',
    'GEOSITE', 'GEOIP', 'IP-CIDR', 'IP-CIDR6', 'IP-ASN', 'IP-SUFFIX',
    'SRC-IP-CIDR', 'SRC-IP-ASN', 'SRC-PORT', 'DST-PORT', 'IN-PORT',
    'PROCESS-NAME', 'PROCESS-PATH', 'PROCESS-NAME-REGEX', 'PROCESS-PATH-REGEX',
    'NETWORK', 'RULE-SET', 'SUB-RULE', 'AND', 'OR', 'NOT', 'MATCH',
    'IN-TYPE', 'IN-USER', 'IN-NAME', 'UID',
}

# 按文件用途标注语义类别，用于检测"同一域名出现在语义相反规则集"
# 没列出的文件默认视为 'unknown'，不参与语义冲突检测（避免误报）
FILE_INTENT = {
    'Reject-Manually.yaml': 'reject',
    'vivo-ads.yaml': 'reject',
    'cn-direct.yaml': 'direct',
    'cn-direct-pro.yaml': 'direct',
    'bytedance-global.yaml': 'proxy',
    'claude-ai.yaml': 'proxy',
    'google-android.yaml': 'proxy',
    'international-website.yaml': 'proxy',
    'telegram-ip-pro.yaml': 'proxy',
    'tv-player.yaml': 'proxy',
    'usa.yaml': 'proxy',
}


def split_top_level(s: str, sep: str = ',') -> list:
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
    raw = raw.strip()
    top = split_top_level(raw, ',')
    if not top:
        return raw

    rule_type = top[0].strip().upper()

    if rule_type in LOGIC_TYPES and len(top) >= 2:
        group_str = strip_outer_parens(top[1])
        children = split_top_level(group_str, ',')
        normalized_children = sorted(
            normalize_rule(strip_outer_parens(c)) for c in children
        )
        target_part = ','.join(top[2:])
        return f"{rule_type}({'|'.join(normalized_children)})->{target_part}"

    return raw


def get_rule_type(raw: str) -> str:
    top = split_top_level(raw, ',')
    return top[0].strip().upper() if top else ''


def get_match_key(raw: str):
    """
    提取用于语义冲突检测的"匹配目标"，比如 DOMAIN-SUFFIX,xxx.com 提取 xxx.com。
    非域名类规则（AND/PROCESS-NAME等）返回 None，不参与语义冲突检测。
    """
    top = split_top_level(raw, ',')
    if len(top) < 2:
        return None
    rule_type = top[0].strip().upper()
    if rule_type in {'DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD'}:
        return top[1].strip().lower()
    return None


def load_yaml_data(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"⚠️ 跳过 {os.path.basename(path)}：YAML 解析失败 - {e}")
        return None


def extract_entries(data, filename):
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


def update_readme(stats, type_stats, total_unique, duplicates, unknown_types, conflicts):
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

    if unknown_types:
        table += f"### ❗ 疑似拼写错误的规则类型（共 {len(unknown_types)} 处）\n\n"
        table += "| 未知类型 | 出现位置 | 原始内容 |\n| :--- | :--- | :--- |\n"
        for rtype, source, raw in unknown_types:
            safe_raw = raw.replace('|', '\\|')
            table += f"| `{rtype}` | {source} | `{safe_raw}` |\n"
        table += "\n"

    if conflicts:
        table += f"### 🚨 语义冲突规则（同一域名出现在不同用途规则集，共 {len(conflicts)} 条）\n\n"
        table += "| 域名 | 冲突类别 | 出现位置 |\n| :--- | :--- | :--- |\n"
        for domain, (occ, intents) in sorted(conflicts.items()):
            sources = ', '.join(o[0] for o in occ)
            table += f"| `{domain}` | {' vs '.join(sorted(intents))} | {sources} |\n"
        table += "\n"

    if duplicates:
        table += f"### ⚠️ 跨文件/跨模块重复规则（共 {len(duplicates)} 条，含逻辑等价识别）\n\n"
        table += "| 规则内容 | 出现在 |\n| :--- | :--- |\n"
        for norm_key, occurrences in sorted(duplicates.items()):
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

    norm_to_occurrences = defaultdict(list)
    unknown_types = []  # [(rule_type, source, raw), ...]
    match_key_occurrences = defaultdict(list)  # domain -> [(source, raw), ...]

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
                file_entries = load_text_rules(path)

        file_rule_set = {raw for _, raw in file_entries}
        stats[f_name] = len(file_rule_set)
        all_rules_set.update(file_rule_set)

        for source, raw in file_entries:
            type_stats[categorize(raw)] += 1

            # 类型拼写校验（跳过纯域名/IP的text格式行，它们没有逗号分隔的类型前缀）
            if ',' in raw:
                rtype = get_rule_type(raw)
                if rtype and rtype not in VALID_RULE_TYPES:
                    unknown_types.append((rtype, source, raw))

            norm_key = normalize_rule(raw)
            norm_to_occurrences[norm_key].append((source, raw))

            # 语义冲突检测：只看当前文件（不含 [rules]/[sub-rule:xxx] 后缀）是否登记了 intent
            base_file = source.split('[')[0]
            intent = FILE_INTENT.get(base_file)
            if intent:
                mk = get_match_key(raw)
                if mk:
                    match_key_occurrences[mk].append((source, raw, intent))

    duplicates = {}
    for norm_key, occ in norm_to_occurrences.items():
        sources = {o[0] for o in occ}
        if len(sources) > 1:
            duplicates[norm_key] = occ

    conflicts = {}
    for domain, occ in match_key_occurrences.items():
        intents = {o[2] for o in occ}
        if len(intents) > 1:
            conflicts[domain] = ([(o[0], o[1]) for o in occ], intents)

    update_readme(stats, type_stats, len(all_rules_set), duplicates, unknown_types, conflicts)

    print(f"总计 {len(yaml_files)} 个文件，去重后 {len(all_rules_set)} 条规则")
    if unknown_types:
        print(f"❗ 发现 {len(unknown_types)} 处疑似类型拼写错误")
    if conflicts:
        print(f"🚨 发现 {len(conflicts)} 条语义冲突规则")
    if duplicates:
        print(f"⚠️ 发现 {len(duplicates)} 组跨来源重复规则")
