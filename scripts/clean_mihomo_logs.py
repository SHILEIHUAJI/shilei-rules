#!/usr/bin/env python3
"""
clean_mihomo_logs.py
解析 mihomo INFO 级别日志(.log / .txt),按进程名分组、按策略分类,
与已有 cleaned-logs/<proc>/*.yaml 合并去重后覆盖写回。
处理完的原始日志文件会被删除,避免仓库堆积。

用法:
    python3 scripts/clean_mihomo_logs.py logs cleaned-logs
"""

import re
import sys
import ipaddress
from pathlib import Path
from collections import defaultdict

# ---------- 正则 ----------

LINE_RE = re.compile(
    r'^\s*\d+\s+\d{2}:\d{2}:\d{2}\s+(?P<level>\w+)\s+\S+\s+(?P<msg>.*)$'
)
CORE_RE = re.compile(
    r'^\[(?P<proto>TCP|UDP)\]\s+(?P<src>\S+)\s+-->\s+(?P<dst>\S+)'
)
ACTION_RE = re.compile(r'\[(?P<action>[A-Z\-]+)\]\s*$')
PROC_RE = re.compile(r'\((?P<proc>[\w.]+)\)')

# ---------- 可按需扩充的收敛表 ----------

# 域名后缀收敛表:命中后写成 DOMAIN-SUFFIX,避免随机子域名无限膨胀
KNOWN_SUFFIXES = [
    "douyinvod.com", "douyinstatic.com", "douyinpic.com", "douyincdn.com",
    "amemv.com", "zijieapi.com", "ndcpp.com", "bytegecko.com",
    "byteeffecttos.com", "qishui.com", "starrydyn.com", "sjxydc.com",
    "comfylink.com", "ydycdn.com", "qrstuvwxyzab.com", "qtaeixd.com",
    "cjjd14.com", "smtcdns.com", "snssdk.com", "bdurl.net",
    "toutiao.com", "app-measurement.com", "jspcdn.cn", "ctydoh.cn",
    "0kkkkkt.com", "xdrtc.com",
]

# 包名 -> 可读目录名,未命中的直接用原始包名建目录
PROC_ALIAS = {
    'com.ss.android.ugc.aweme': 'aweme',
    'com.luna.music': 'luna-music',
    'com.tencent.mm': 'wechat',
    'com.google.android.gms': 'google-gms',
    'com.vivo.gallery': 'vivo-gallery',
    'mark.via.gp': 'via-browser',
}

# 无进程标注的连接(mihomo自身、纯IP握手等)归到这里
UNKNOWN_PROC = 'unknown-process'

CAT_FILES = {
    'reject': 'reject-domains.yaml',
    'direct': 'direct-domains.yaml',
    'other': 'other-domains.yaml',
}

# 支持的原始日志文件后缀
SUPPORTED_EXTS = ('.log', '.txt')


# ---------- 工具函数 ----------

def is_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def extract_host(dst: str):
    """从 host:port 或 [ipv6]:port 中取出host,过滤纯IP"""
    if dst.startswith('['):
        m = re.match(r'^\[(.+)\]:\d+$', dst)
        return m.group(1) if m else None
    if ':' in dst:
        host, _, _ = dst.rpartition(':')
        return host
    return dst


def collapse_suffix(host: str) -> str:
    for suf in KNOWN_SUFFIXES:
        if host == suf or host.endswith('.' + suf):
            return suf
    return host


def extract_process(src: str, dst: str) -> str:
    for s in (src, dst):
        m = PROC_RE.search(s)
        if m:
            return m.group('proc')
    return UNKNOWN_PROC


def classify(policy: str) -> str:
    am = ACTION_RE.search(policy)
    action = am.group('action') if am else policy.strip()
    if action in ('REJECT', 'REJECT-DROP'):
        return 'reject'
    if action == 'DIRECT':
        return 'direct'
    return 'other'


def parse_message(msg: str):
    """返回 (src, dst, policy) 或 None"""
    if ' using ' not in msg:
        return None
    core, _, policy = msg.rpartition(' using ')
    cm = CORE_RE.match(core)
    if not cm:
        return None
    return cm.group('src'), cm.group('dst'), policy


# ---------- 主流程 ----------

def find_log_files(log_dir: Path):
    files = []
    for ext in SUPPORTED_EXTS:
        files.extend(log_dir.glob(f'*{ext}'))
    return sorted(files)


def parse_new_logs(log_dir: Path):
    """返回 { (proc_alias, cat): set(hosts) }, 已处理的文件列表"""
    buckets = defaultdict(set)
    log_files = find_log_files(log_dir)

    for f in log_files:
        text = f.read_text(encoding='utf-8', errors='ignore')
        for raw in text.splitlines():
            lm = LINE_RE.match(raw)
            if not lm or lm.group('level') != 'info':
                continue

            parsed = parse_message(lm.group('msg'))
            if not parsed:
                continue
            src, dst, policy = parsed

            host = extract_host(dst)
            if not host or is_ip(host):
                continue

            proc = extract_process(src, dst)
            proc_alias = PROC_ALIAS.get(proc, proc)
            cat = classify(policy)
            buckets[(proc_alias, cat)].add(collapse_suffix(host))

    return buckets, log_files


def load_existing_yaml(path: Path) -> set:
    if not path.exists():
        return set()
    hosts = set()
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line.startswith('- DOMAIN-SUFFIX,'):
            hosts.add(line.split(',', 1)[1])
        elif line.startswith('- DOMAIN,'):
            hosts.add(line.split(',', 1)[1])
    return hosts


def to_rule_line(host: str) -> str:
    if host in KNOWN_SUFFIXES:
        return f"  - DOMAIN-SUFFIX,{host}"
    return f"  - DOMAIN,{host}"


def write_merged(out_dir: Path, buckets):
    summary = []
    for (proc_alias, cat), new_hosts in buckets.items():
        proc_dir = out_dir / proc_alias
        proc_dir.mkdir(parents=True, exist_ok=True)
        out_path = proc_dir / CAT_FILES[cat]

        existing = load_existing_yaml(out_path)
        merged = existing | new_hosts
        if not merged:
            continue

        lines = ["payload:"] + [to_rule_line(h) for h in sorted(merged)]
        out_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

        added = len(new_hosts - existing)
        summary.append(
            f"{proc_alias}/{CAT_FILES[cat]}: 合计 {len(merged)} 条 (新增 {added})"
        )
    return summary


def main():
    log_dir = Path(sys.argv[1] if len(sys.argv) > 1 else 'logs')
    out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else 'cleaned-logs')

    if not log_dir.exists():
        print(f"日志目录不存在: {log_dir}")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    buckets, log_files = parse_new_logs(log_dir)

    if not buckets:
        print("未发现可处理的 info 级别记录(或没有新日志文件)。")
    else:
        summary = write_merged(out_dir, buckets)
        for line in summary:
            print(line)

    # 处理完清空原始日志,避免仓库堆积
    for f in log_files:
        f.unlink()
        print(f"已删除已处理日志: {f}")


if __name__ == '__main__':
    main()
