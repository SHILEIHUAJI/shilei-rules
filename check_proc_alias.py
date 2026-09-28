#!/usr/bin/env python3
"""
proc_alias_stats.py
校验 proc-alias.yaml 并把统计写入 README.md 的 STATS 标记区间。

分类来源: yaml 里被 === 或 --- 夹住的注释行(如 "# ===== VIVO系应用 ====="),
          标题下面的条目都归入该分类,没有标题的归"未分组"。
校验项:   重复包名 / 别名能否安全用作目录名 / 无法解析的行 -> 退出码 1
警告项:   多个包名共用同一别名(可能是有意合并目录,只提示不失败)
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

YAML_PATH = Path("proc-alias.yaml")
README_PATH = Path("README.md")
START_MARKER = "<!-- STATS_START -->"
END_MARKER = "<!-- STATS_END -->"
DEFAULT_CATEGORY = "未分组"

# 不用 yaml.safe_load:PyYAML 遇到重复键会静默保留最后一个,检测不到重复
ENTRY_RE = re.compile(
    r"""^["']?(?P<pkg>[A-Za-z0-9_.]+)["']?\s*:\s*["']?(?P<alias>[^\s#"']+)["']?\s*(?:#\s*(?P<comment>.*))?$"""
)
# 分组标题: "# ===== 名称 =====";名称首字符不能是 = - 或空白,避免纯分隔线被当成标题
HEADER_RE = re.compile(r"^#\s*[=\-]{3,}\s*(?P<name>[^=\-\s].*?)\s*[=\-]{3,}\s*$")

# 别名会变成 cleaned-logs/<别名>/ 目录,只允许安全的单层目录名
ALIAS_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
RESERVED_ALIASES = {"unknown-process"}  # 清洗脚本给"无进程名"连接保留的目录


def eprint(*args):
    print(*args, file=sys.stderr)


def parse_yaml_file(path: Path):
    if not path.exists():
        eprint(f"❌ 未找到 {path}")
        sys.exit(1)

    entries, malformed = [], []
    category = DEFAULT_CATEGORY
    text = path.read_text(encoding="utf-8")
    for line_num, raw in enumerate(text.splitlines(), 1):
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            h = HEADER_RE.match(stripped)
            if h:
                category = h["name"].strip()
            continue
        m = ENTRY_RE.match(stripped)
        if not m:
            malformed.append((line_num, stripped))
            continue
        entries.append({
            "line": line_num,
            "pkg": m["pkg"],
            "alias": m["alias"],
            "comment": (m["comment"] or "").strip(),
            "category": category,
        })
    return entries, malformed


def validate(entries):
    """返回 (每个包名首次出现的条目, 重复项{包名: 全部出现位置}, 非法别名列表, 共用别名{别名: 包名列表})"""
    first_seen = {}
    occurrences = defaultdict(list)
    bad_aliases = []
    for e in entries:
        occurrences[e["pkg"]].append(e)
        first_seen.setdefault(e["pkg"], e)
        if not ALIAS_RE.match(e["alias"]) or e["alias"] in RESERVED_ALIASES:
            bad_aliases.append(e)
    dups = {p: v for p, v in occurrences.items() if len(v) > 1}

    alias_owners = defaultdict(list)
    for pkg, e in first_seen.items():
        alias_owners[e["alias"]].append(pkg)
    shared = {a: pkgs for a, pkgs in alias_owners.items() if len(pkgs) > 1}
    return first_seen, dups, bad_aliases, shared


def esc(text: str) -> str:
    """转义表格里的竖线,避免撑坏 Markdown 表格"""
    return text.replace("|", "\\|")


def build_report(entries, first_seen, dups, bad_aliases, malformed, category_map):
    problems = len(dups) + len(bad_aliases) + len(malformed)
    md = [START_MARKER, "## 📊 包名映射统计\n"]

    md.append("### 📈 概览")
    md.append(f"- **配置总条数**: `{len(entries)}` 条")
    md.append(f"- **独立应用数**: `{len(first_seen)}` 个")
    md.append(f"- **分类数**: `{len(category_map)}` 个")
    md.append("- **校验状态**: " + ("✅ 通过" if not problems else f"❌ 发现 {problems} 个问题"))
    md.append("")

    cats = list(category_map.items())  # 保持 yaml 里的出现顺序

    if cats:  # 空数据时不生成空饼图,否则 Mermaid 会报错
        md.append("### 🎨 应用分类分布\n")
        md.append("```mermaid")
        md.append("pie title 包名分类占比统计")
        for cat, items in cats:
            md.append(f'    "{cat.replace(chr(34), chr(39))}" : {len(items)}')
        md.append("```\n")

    if dups:
        md.append("### ❌ 重复包名")
        md.append("| 包名 | 出现位置 → 别名 | 别名是否冲突 |")
        md.append("| :--- | :--- | :---: |")
        for pkg, items in dups.items():
            where = ", ".join(f"第{e['line']}行→`{esc(e['alias'])}`" for e in items)
            conflict = "⚠️ 冲突" if len({e["alias"] for e in items}) > 1 else "相同"
            md.append(f"| `{pkg}` | {where} | {conflict} |")
        md.append("")

    if bad_aliases:
        md.append("### ❌ 非法别名(会被用作目录名)")
        md.append("| 行号 | 包名 | 别名 |")
        md.append("| :---: | :--- | :--- |")
        for e in bad_aliases:
            md.append(f"| {e['line']} | `{e['pkg']}` | `{esc(e['alias'])}` |")
        md.append("")

    if malformed:
        md.append("### ❌ 无法解析的行")
        for line_num, content in malformed:
            md.append(f"- 第 {line_num} 行: `{esc(content)}`")
        md.append("")

    md.append("### 📋 分类明细")
    for cat, items in cats:
        md.append(f"<details><summary><b>{cat}</b>(包含 {len(items)} 个应用)</summary>\n")
        md.append("| 包名 | 目录别名 | 备注 |")
        md.append("| :--- | :--- | :--- |")
        for item in sorted(items, key=lambda x: x["pkg"]):
            comment = esc(item["comment"]) if item["comment"] else "-"
            md.append(f"| `{item['pkg']}` | `{esc(item['alias'])}` | {comment} |")
        md.append("\n</details>\n")

    md.append(END_MARKER)
    return "\n".join(md)


def update_readme(stats_md: str):
    if README_PATH.exists():
        content = README_PATH.read_text(encoding="utf-8")
    else:
        content = "# Proc Alias 映射表管理\n\n"

    if START_MARKER in content and END_MARKER in content:
        pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
        # 用 lambda 避免 stats_md 里的反斜杠被当成替换模板转义
        content = re.sub(pattern, lambda m: stats_md, content, flags=re.DOTALL)
    else:
        content = content.rstrip() + f"\n\n{stats_md}\n"

    README_PATH.write_text(content, encoding="utf-8")


def report_problems(dups, bad_aliases, malformed, shared) -> bool:
    """问题打印到 stderr(Action 日志可见);有失败项返回 True,共用别名只警告"""
    for pkg, items in dups.items():
        where = ", ".join(f"第{e['line']}行→{e['alias']}" for e in items)
        conflict = "别名冲突" if len({e["alias"] for e in items}) > 1 else "别名相同"
        eprint(f"❌ 重复包名 {pkg} ({conflict}): {where}")
    for e in bad_aliases:
        eprint(f"❌ 第{e['line']}行 非法别名 '{e['alias']}' (包名 {e['pkg']})")
    for line_num, content in malformed:
        eprint(f"❌ 第{line_num}行 无法解析: {content}")
    for alias, pkgs in shared.items():
        eprint(f"⚠️ 别名 '{alias}' 被 {len(pkgs)} 个包名共用(日志会合并到同一目录): {', '.join(pkgs)}")
    return bool(dups or bad_aliases or malformed)


def main():
    entries, malformed = parse_yaml_file(YAML_PATH)
    first_seen, dups, bad_aliases, shared = validate(entries)

    category_map = defaultdict(list)
    for item in first_seen.values():
        category_map[item["category"]].append(item)

    update_readme(build_report(entries, first_seen, dups, bad_aliases, malformed, category_map))

    if report_problems(dups, bad_aliases, malformed, shared):
        sys.exit(1)


if __name__ == "__main__":
    main()
