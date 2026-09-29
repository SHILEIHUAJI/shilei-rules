#!/usr/bin/env python3
"""
annotate_domains.py
给 cleaned-logs/*/*.yaml 里的域名加业务用途注释。
用法: python3 scripts/annotate_domains.py cleaned-logs domain-notes.yaml
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

import yaml

MODEL = "gpt-4o-mini"
API_URL = "https://models.inference.ai.azure.com/chat/completions"
BATCH_SIZE = 25

SYSTEM_PROMPT = (
    "你是网络流量分析助手。给定一批域名,判断每个域名最可能属于什么业务/服务,"
    "用不超过12个汉字简要说明(例如:抖音短视频CDN、微信推送、谷歌地图API)。"
    "如果域名看起来是随机生成的CDN节点、无法判断具体业务,输出\"未知(CDN节点)\"。"
    "如果看起来像广告/追踪域名,标注\"疑似广告追踪\"。"
    "不要编造你不确定的具体公司名。"
    "严格按JSON对象格式输出,key是域名,value是说明,不要输出其他任何文字。"
)


def call_model(domains: list, token: str) -> dict:
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "\n".join(domains)},
        ],
        "temperature": 0,
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "GitHubActions-Annotator/1.0",
    }

    req = urllib.request.Request(API_URL, data=body, method="POST", headers=headers)
    content = ""
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw_data = resp.read().decode("utf-8")
            data = json.loads(raw_data)
            content = data["choices"][0]["message"]["content"].strip()
            
            # 使用正则表达式精准匹配 JSON 对象部分 {...}
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                json_str = match.group(0)
                res = json.loads(json_str)
                return res if isinstance(res, dict) else {}
            else:
                print(f"模型未返回有效 JSON 结构，原始输出:\n{content}")
                return {}
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        print(f"API 请求失败 HTTP {e.code}: {error_body}")
        raise
    except Exception as e:
        print(f"解析模型输出失败: {e}\n模型原始返回内容 content 为:\n{content}")
        raise


def load_cache(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def save_cache(path: Path, cache: dict):
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(cache, f, allow_unicode=True, sort_keys=True)


def parse_domain(line: str) -> str | None:
    """去除缩进后准确解析规则行中的域名，兼容 DOMAIN 及 DOMAIN-SUFFIX"""
    clean_line = line.split("#", 1)[0].strip()
    if clean_line.startswith("- DOMAIN"):
        parts = [p.strip().strip("'\"") for p in clean_line.split(",")]
        if len(parts) >= 2:
            return parts[1]
    return None


def collect_domains(cleaned_dir: Path) -> set:
    domains = set()
    for f in cleaned_dir.glob("*/*.yaml"):
        for line in f.read_text(encoding="utf-8").splitlines():
            domain = parse_domain(line)
            if domain:
                domains.add(domain)
    return domains


def annotate_files(cleaned_dir: Path, cache: dict):
    for f in cleaned_dir.glob("*/*.yaml"):
        out_lines = []
        for raw in f.read_text(encoding="utf-8").splitlines():
            clean_code = raw.split("#", 1)[0].strip()
            domain = parse_domain(raw)
            
            if clean_code.startswith("- DOMAIN") and domain and domain in cache:
                note = cache[domain]
                base_code = raw.split("#", 1)[0].rstrip()
                out_lines.append(f"{base_code}  # {note}")
            else:
                out_lines.append(raw)
        f.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def main():
    cleaned_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "cleaned-logs")
    cache_path = Path(sys.argv[2] if len(sys.argv) > 2 else "domain-notes.yaml")
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("缺少 GITHUB_TOKEN,跳过标注")
        return

    cache = load_cache(cache_path)
    unknown = sorted(collect_domains(cleaned_dir) - cache.keys())

    if unknown:
        print(f"需要标注的新域名: {len(unknown)} 个")
        for i in range(0, len(unknown), BATCH_SIZE):
            batch = unknown[i:i + BATCH_SIZE]
            try:
                result = call_model(batch, token)
                cache.update(result)
            except Exception as e:
                print(f"批次 {i} 标注失败: {e}")
            time.sleep(1)
        save_cache(cache_path, cache)

    annotate_files(cleaned_dir, cache)
    print(f"已附加注释,缓存共 {len(cache)} 条")


if __name__ == "__main__":
    main()
