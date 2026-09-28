#!/usr/bin/env python3
"""
proc_alias_stats.py
校验 proc-alias.yaml 并把统计写入 README.md 的 STATS 标记区间。

校验项: 重复包名 / 别名能否安全用作目录名 / 无法解析的行
任何一项不通过 -> 原因打印到 stderr,退出码 1。
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

YAML_PATH = Path("proc-alias.yaml")
README_PATH = Path("README.md")
START_MARKER = "<!-- STATS_START -->"
END_MARKER = "<!-- STATS_END -->"

# 不用 yaml.safe_load:PyYAML 遇到重复键会静默保留最后一个,检测不到重复
ENTRY_RE = re.compile(
    r"""^["']?(?P<pkg>[A-Za-z0-9_.]+)["']?\s*:\s*["']?(?P<alias>[^\s#"']+)["']?\s*(?:#\s*(?P<comment>.*))?$"""
)

# 别名会变成 cleaned-logs/<别名>/ 目录,只允许安全的单层目录名
ALIAS_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
RESERVED_ALIASES = {"unknown-process"}  # 清洗脚本给"无进程名"连接保留的目录

# 顺序敏感,先匹配先生效。前缀按"段边界"匹配:
# "com.ss.android" 匹配 com.ss.android.ugc.aweme,但不会误中 com.ss.androidx
CLASSIFICATION_RULES = [
    # 国际版必须排在国内版前面,否则 com.ss.android.ugc.trill 会被国内版吞掉
    ("字节跳动系(国际版)", [
        "com.zhiliaoapp.musically", "com.ss.android.ugc.trill",
        "com.lemon.lvoverseas", "com.bd.nproject",
        "com.moonvideo.android.resso", "com.ss.android.ugc.boom",
    ]),
    # 部分包名凭记忆整理,以日志里实际抓到的为准
    ("字节跳动系(国内)", [
        "com.ss.android", "com.bytedance", "com.luna", "com.dragon",
        "com.xs.fm", "com.phoenix.read", "com.larus", "com.lemon.lv",
        "com.lemon.faceu", "com.vega", "com.xt.retouch", "com.gorgeous.lite",
        "com.sup.android", "com.f100.android", "com.larksuite",
        "com.pangle", "com.picovr",
    ]),
    ("Google 系应用", ["com.google"]),
    ("Android 系统组件", ["com.android"]),
    ("腾讯系", ["com.tencent"]),
    ("百度系", ["com.baidu"]),
    ("主流电商与服务", ["com.taobao", "com.eg.android", "com.xunmeng", "com.sankuai"]),
    ("vivo 厂商应用", ["com.vivo"]),
    ("微软系", ["com.microsoft"]),
    ("GitHub/开源极客工具", [
        "io.github", "com.github", "org.fdroid",
        "moe.shizuku", "li.songe", "bin.mt",
    ]),
    ("开源组织应用", ["org"]),
]


def eprint(*args):
    print(*args, file=sys.stderr)


def classify_package(pkg: str) -> str:
    low = pkg.lower()
    for category, prefixes in CLASSIFICATION_RULES:
        if any(low == p or low.startswith(p + ".") for p in prefixes):
            return category
    return "其他第三方应用"


def parse_yaml_file(path: Path):
    if not path.exists():
        eprint(f"❌ 未找到 {path}")
        sys.exit(1)

    entries, malformed = [], []
    text = path.read_text(encoding="utf-8")
    for line_num, raw in enumerate(text.splitlines(), 1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
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
        })
    return entries, malformed


def validate(entries):
    """返回 (每个包名首次出现的条目, 重复项{包名: 全部出现位置}, 非法别名列表)"""
    first_seen = {}
    occurrences = defaultdict(list)
    bad_aliases = []
    for e in entries:
        occurrences[e["pkg"]].append(e)
        first_seen.setdefault(e["pkg"], e)
        if not ALIAS_RE.match(e["alias"]) or e["alias"] in RESERVED_ALIASES:
            bad_aliases.append(e)
    dups = {p: v for p, v in occurrences.items() if len(v) > 1}
    return first_seen, dups, bad_aliases


def esc(text: str) -> str:
    """转义表格里的竖线,避免撑坏 Markdown 表格"""
    return text.replace("|", "\\|")


def build_report(entries, first_seen, dups, bad_aliases, malformed, category_map):
    problems = len(dups) + len(bad_aliases) + len(malformed)
    md = [START_MARKER, "## 📊 包名映射统计\n"]

    md.append("### 📈 概览")
    md.append(f"- **配置总条数**: `{len(entries)}` 条")
    md.append(f"- **独立应用数**: `{len(first_seen)}` 个")
    md.append("- **校验状态**: " + ("✅ 通过" if not problems else f"❌ 发现 {problems} 个问题"))
    md.append("")

    sorted_cats = sorted(category_map.items(), key=lambda kv: (-len(kv[1]), kv[0]))

    if sorted_cats:  # 空数据时不生成空饼图,否则 Mermaid 会报错
        md.append("### 🎨 应用分类分布\n")
        md.append("```mermaid")
        md.append("pie title 包名分类占比统计")
        for cat, items in sorted_cats:
            md.append(f'    "{cat}" : {len(items)}')
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
    for cat, items in sorted_cats:
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


def report_problems(dups, bad_aliases, malformed) -> bool:
    """把问题打印到 stderr(Action 日志可见),有问题返回 True"""
    for pkg, items in dups.items():
        where = ", ".join(f"第{e['line']}行→{e['alias']}" for e in items)
        conflict = "别名冲突" if len({e["alias"] for e in items}) > 1 else "别名相同"
        eprint(f"❌ 重复包名 {pkg} ({conflict}): {where}")
    for e in bad_aliases:
        eprint(f"❌ 第{e['line']}行 非法别名 '{e['alias']}' (包名 {e['pkg']})")
    for line_num, content in malformed:
        eprint(f"❌ 第{line_num}行 无法解析: {content}")
    return bool(dups or bad_aliases or malformed)


def main():
    entries, malformed = parse_yaml_file(YAML_PATH)
    first_seen, dups, bad_aliases = validate(entries)

    category_map = defaultdict(list)
    for item in first_seen.values():
        category_map[classify_package(item["pkg"])].append(item)

    update_readme(build_report(entries, first_seen, dups, bad_aliases, malformed, category_map))

    if report_problems(dups, bad_aliases, malformed):
        sys.exit(1)


if __name__ == "__main__":
    main()
