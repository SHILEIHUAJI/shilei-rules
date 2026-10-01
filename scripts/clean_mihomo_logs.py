#!/usr/bin/env python3
"""
clean_mihomo_logs.py
解析 mihomo INFO 级别日志(.log / .txt),按进程名分组、按策略分类,
与已有 cleaned-logs/<proc>/*.yaml 合并去重,并自动发现可收敛的域名后缀。
处理完的原始日志文件会被删除,避免仓库堆积。

用法:
    python3 scripts/clean_mihomo_logs.py logs cleaned-logs

依赖:
    pip install pyyaml
"""

import re
import sys
import ipaddress
import yaml
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

# ---------- 配置 ----------

PROC_ALIAS_FILE = Path('proc-alias.yaml')
UNKNOWN_PROC = 'unknown-process'
SUPPORTED_EXTS = ('.log', '.txt')

CAT_FILES = {
    'reject': 'reject-domains.yaml',
    'direct': 'direct-domains.yaml',
    'other': 'other-domains.yaml',
}

# 手动兜底后缀表:自动发现覆盖不到、或者你想强制指定的域名放这里
KNOWN_SUFFIXES = [
    "douyinvod.com", "douyinstatic.com", "douyinpic.com", "douyincdn.com",
    "amemv.com", "zijieapi.com", "ndcpp.com", "bytegecko.com",
    "byteeffecttos.com", "qishui.com", "starrydyn.com", "sjxydc.com",
    "comfylink.com", "ydycdn.com", "qrstuvwxyzab.com", "qtaeixd.com",
    "cjjd14.com", "smtcdns.com", "snssdk.com", "bdurl.net",
    "toutiao.com", "app-measurement.com", "jspcdn.cn", "ctydoh.cn",
    "0kkkkkt.com", "xdrtc.com",
]

# 多段公共后缀:命中时要多算一段,否则会把 co.jp / com.cn 这种
# 公共后缀本身当成"可收敛域名",引发大范围误伤。按需扩充。
MULTI_PART_TLDS = {
    'co.jp', 'or.jp', 'ne.jp', 'com.cn', 'net.cn', 'org.cn', 'gov.cn',
    'co.uk', 'org.uk', 'co.kr', 'co.in', 'com.hk', 'com.tw', 'com.sg',
    'com.au', 'com.br',
}

# 共享云托管/CDN域名:哪怕子域名再多也不能自动收敛,
# 因为背后是无数互不相关的租户,收敛=大范围误伤。按需扩充。
SHARED_HOSTING_DENYLIST = {
    'amazonaws.com', 'cloudfront.net', 'azureedge.net', 'akamaized.net',
    'edgekey.net', 'edgesuite.net', 'herokuapp.com', 'github.io',
    'googleusercontent.com', 'cdn77.org', 'aliyuncs.com', 'myqcloud.com',
}

# 同一可收敛后缀下,累计出现的不同子域名数达到这个值就自动收敛
AUTO_SUFFIX_THRESHOLD = 5


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


def load_proc_alias(path: Path = PROC_ALIAS_FILE) -> dict:
    """从独立配置文件读取包名→别名映射,文件不存在就用空字典。"""
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    return data or {}


def registrable_suffix(host: str):
    """
    取候选的"可收敛后缀"。
    - 命中多段公共TLD(如 co.jp)时自动多算一段,避免收敛到公共后缀本身
    - 命中共享托管黑名单时返回 None,禁止自动收敛
    """
    parts = host.split('.')
    if len(parts) < 2:
        return None
    two = '.'.join(parts[-2:])
    if two in MULTI_PART_TLDS and len(parts) >= 3:
        candidate = '.'.join(parts[-3:])
    else:
        candidate = two
    if candidate in SHARED_HOSTING_DENYLIST:
        return None
    return candidate


def discover_auto_suffixes(all_hosts: set) -> dict:
    """
    在完整域名池(历史+新增)上统计每个候选后缀下的不同子域名数,
    返回达到阈值的 {后缀: 子域名数}。
    """
    suffix_children = defaultdict(set)
    for host in all_hosts:
        suf = registrable_suffix(host)
        if suf is None or host == suf:
            continue
        suffix_children[suf].add(host)
    return {
        s: len(children)
        for s, children in suffix_children.items()
        if len(children) >= AUTO_SUFFIX_THRESHOLD
    }


def collapse_hosts(hosts: set, all_suffixes: set) -> set:
    """把命中收敛后缀的子域名合并为该后缀本身,其余精确域名原样保留。"""
    collapsed = set()
    for host in hosts:
        if host in all_suffixes:
            collapsed.add(host)
            continue
        suf = registrable_suffix(host)
        collapsed.add(suf if suf in all_suffixes else host)
    return collapsed


def to_rule_line(host: str, all_suffixes: set) -> str:
    if host in all_suffixes:
        return f"  - DOMAIN-SUFFIX,{host}"
    return f"  - DOMAIN,{host}"


# ---------- 主流程 ----------

def find_log_files(log_dir: Path):
    files = []
    for ext in SUPPORTED_EXTS:
        files.extend(log_dir.glob(f'*{ext}'))
    return sorted(files)


def parse_new_logs(log_dir: Path, proc_alias: dict):
    """返回 { (proc_alias, cat): set(hosts) }(host未收敛,原始域名), 已处理文件列表"""
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
            proc_name = proc_alias.get(proc, proc)
            cat = classify(policy)
            buckets[(proc_name, cat)].add(host)

    return buckets, log_files


def load_existing_yaml(path: Path) -> set:
    if not path.exists():
        return set()
    hosts = set()
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.split('#', 1)[0].strip()  # 先去掉注释,再解析
        if line.startswith('- DOMAIN-SUFFIX,') or line.startswith('- DOMAIN,'):
            hosts.add(line.split(',', 1)[1].strip())
    return hosts


def gather_merged_buckets(out_dir: Path, new_buckets: dict) -> dict:
    """把新日志的域名和已有yaml里的历史域名合并成完整域名池,
    覆盖「本轮没有新日志但历史已有数据」的 (proc, cat) 组合,
    确保后缀自动发现是基于全量数据,而不是只看当天新增。"""
    merged = {}
    for key, new_hosts in new_buckets.items():
        proc_name, cat = key
        out_path = out_dir / proc_name / CAT_FILES[cat]
        merged[key] = load_existing_yaml(out_path) | new_hosts

    for existing_file in out_dir.glob('*/*.yaml'):
        proc_name = existing_file.parent.name
        cat = next((c for c, fname in CAT_FILES.items() if fname == existing_file.name), None)
        if cat is None:
            continue
        key = (proc_name, cat)
        if key not in merged:
            merged[key] = load_existing_yaml(existing_file)

    return merged


def write_merged(out_dir: Path, merged_buckets: dict, all_suffixes: set):
    summary = []
    for (proc_name, cat), hosts in merged_buckets.items():
        if not hosts:
            continue
        proc_dir = out_dir / proc_name
        proc_dir.mkdir(parents=True, exist_ok=True)
        out_path = proc_dir / CAT_FILES[cat]

        before_count = len(load_existing_yaml(out_path))
        collapsed = collapse_hosts(hosts, all_suffixes)

        lines = ["payload:"] + [to_rule_line(h, all_suffixes) for h in sorted(collapsed)]
        out_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

        summary.append(f"{proc_name}/{CAT_FILES[cat]}: {before_count} → {len(collapsed)} 条")
    return summary


def main():
    log_dir = Path(sys.argv[1] if len(sys.argv) > 1 else 'logs')
    out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else 'cleaned-logs')

    if not log_dir.exists():
        print(f"日志目录不存在: {log_dir}")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    proc_alias = load_proc_alias()
    new_buckets, log_files = parse_new_logs(log_dir, proc_alias)

    if not new_buckets and not log_files:
        print("未发现可处理的 info 级别记录(或没有新日志文件)。")
        return

    merged_buckets = gather_merged_buckets(out_dir, new_buckets)

    all_hosts = set()
    for hosts in merged_buckets.values():
        all_hosts |= hosts

    auto_suffixes = discover_auto_suffixes(all_hosts)
    all_suffixes = set(KNOWN_SUFFIXES) | set(auto_suffixes.keys())

    if auto_suffixes:
        print("自动发现并收敛后缀:")
        for suf, count in sorted(auto_suffixes.items(), key=lambda x: -x[1]):
            tag = " (已在手动表中)" if suf in KNOWN_SUFFIXES else ""
            print(f"  - {suf} ({count}个子域名){tag}")

    summary = write_merged(out_dir, merged_buckets, all_suffixes)
    for line in summary:
        print(line)

    for f in log_files:
        f.unlink()
        print(f"已删除已处理日志: {f}")


if __name__ == '__main__':
    main()
