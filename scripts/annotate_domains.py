#!/usr/bin/env python3
"""
annotate_domains.py
给 cleaned-logs/*/*.yaml 里的域名加业务用途注释。
用法: python3 scripts/annotate_domains.py cleaned-logs domain-notes.yaml

原理:
- domain-notes.yaml 是持久缓存(域名 -> 注释),跨多次运行复用,避免重复调用模型
- clean_mihomo_logs.py 每次都会重写 cleaned-logs(不带注释),所以本脚本必须在它之后运行,
  注释来源始终是缓存文件,不依赖 cleaned-logs 里已有的注释,重复执行是安全的
- 模型判断不了的域名会标"未知",不强行瞎编
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

import yaml

MODEL = "openai/gpt-4o-mini"
API_URL = "https://models.github.ai/inference/chat/completions"
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

    req = urllib.request.Request(API_URL, data=body, method="POST", headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    content = data["choices"][0]["message"]["content"].strip()
    for fence in ("```json", "```"):
        if content.startswith(fence):
            content = content[len(fence):]
    content = content.rstrip("`").strip()
    return json.loads(content)


def load_cache(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def save_cache(path: Path, cache: dict):
    lines = [f'{d}: "{cache[d]}"' for d in sorted(cache)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def collect_domains(cleaned_dir: Path) -> set:
    domains = set()
    for f in cleaned_dir.glob("*/*.yaml"):
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line.startswith("- DOMAIN"):
                domains.add(line.split(",", 1)[1].strip())
    return domains


def annotate_files(cleaned_dir: Path, cache: dict):
    for f in cleaned_dir.glob("*/*.yaml"):
        out_lines = []
        for raw in f.read_text(encoding="utf-8").splitlines():
            line = raw.split("#", 1)[0].rstrip()
            if line.startswith("- DOMAIN"):
                host = line.split(",", 1)[1].strip()
                note = cache.get(host)
                out_lines.append(f"{line}  # {note}" if note else line)
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
                cache.update(call_model(batch, token))
            except (urllib.error.HTTPError, json.JSONDecodeError, KeyError) as e:
                print(f"批次 {i} 标注失败,跳过: {e}")
            time.sleep(1)
        save_cache(cache_path, cache)

    annotate_files(cleaned_dir, cache)
    print(f"已附加注释,缓存共 {len(cache)} 条")


if __name__ == "__main__":
    main()
