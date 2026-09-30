#!/usr/bin/env python3
"""
annotate_domains.py
给 cleaned-logs/*/*.yaml 里的域名加业务用途注释:
先用本地关键词匹配处理明显可识别的域名(免费、即时),
剩下真正认不出的再交给 Gemini 判断。
用法: python3 scripts/annotate_domains.py cleaned-logs domain-notes.yaml
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

import yaml

MODEL = "gemini-2.5-flash-lite"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
BATCH_SIZE = 30
MAX_RETRIES = 4

# 本地关键词表:命中直接判定,不消耗模型调用。
# 顺序敏感,越靠前优先级越高。按需扩充。
LOCAL_RULES = [
    (("doubleclick", "adservice", "adjust.com", "pangolin-sdk-toutiao",
      "tagmanager", "mmstat.com"), "疑似广告追踪"),
    (("googleapis.com", "gstatic.com", "google.com"), "谷歌服务"),
    (("tencent.com", "qq.com", "weixin", "wechat"), "腾讯服务"),
    (("alicdn.com", "aliyuncs.com", "taobao.com", "tmall.com"), "阿里服务"),
    (("baidu.com", "bdstatic.com"), "百度服务"),
    (("amazonaws.com", "cloudfront.net"), "AWS云服务"),
    (("cloudflare.com", "cloudflare.net"), "Cloudflare CDN"),
    (("apple.com", "icloud.com"), "苹果服务"),
    (("microsoft.com", "windows.net", "live.com"), "微软服务"),
    (("facebook.com", "fbcdn.net", "instagram.com"), "Meta服务"),
]


def local_match(domain: str):
    d = domain.lower()
    for keywords, label in LOCAL_RULES:
        if any(k in d for k in keywords):
            return label
    return None


SYSTEM_PROMPT = (
    "你是网络流量分析助手。给定一批域名,判断每个域名最可能属于什么业务/服务,"
    "用不超过12个汉字简要说明(例如:抖音短视频CDN、微信推送、谷歌地图API)。"
    "如果域名看起来是随机生成的CDN节点、无法判断具体业务,输出\"未知(CDN节点)\"。"
    "如果看起来像广告/追踪域名,标注\"疑似广告追踪\"。"
    "不要编造你不确定的具体公司名。"
    "严格按JSON对象格式输出,key是域名,value是说明。"
)


def call_model(domains: list, api_key: str) -> dict:
    body = json.dumps({
        "contents": [{
            "parts": [{"text": SYSTEM_PROMPT + "\n\n域名列表:\n" + "\n".join(domains)}]
        }],
        "generationConfig": {
            "temperature": 0,
            "responseMimeType": "application/json",
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{API_URL}?key={api_key}",
        data=body, method="POST",
        headers={"Content-Type": "application/json"},
    )

    delay = 2
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
            content = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            return json.loads(content)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_RETRIES - 1:
                print(f"  触发限流,{delay}秒后重试(第{attempt + 1}次)")
                time.sleep(delay)
                delay *= 2
                continue
            raise


def load_cache(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def save_cache(path: Path, cache: dict):
    lines = [f'{d}: "{cache[d]}"' for d in sorted(cache)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_domain(line: str):
    clean = line.split("#", 1)[0].strip()
    if clean.startswith("- DOMAIN"):
        parts = [p.strip().strip("'\"") for p in clean.split(",")]
        if len(parts) >= 2:
            return parts[1]
    return None


def collect_domains(cleaned_dir: Path) -> set:
    domains = set()
    for f in cleaned_dir.glob("*/*.yaml"):
        for line in f.read_text(encoding="utf-8").splitlines():
            d = parse_domain(line)
            if d:
                domains.add(d)
    return domains


def annotate_files(cleaned_dir: Path, cache: dict):
    for f in cleaned_dir.glob("*/*.yaml"):
        out_lines = []
        for raw in f.read_text(encoding="utf-8").splitlines():
            domain = parse_domain(raw)
            if domain and domain in cache:
                base = raw.split("#", 1)[0].rstrip()
                out_lines.append(f"{base}  # {cache[domain]}")
            else:
                out_lines.append(raw)
        f.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def main():
    cleaned_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "cleaned-logs")
    cache_path = Path(sys.argv[2] if len(sys.argv) > 2 else "domain-notes.yaml")
    api_key = os.environ.get("GEMINI_API_KEY")

    cache = load_cache(cache_path)
    all_unknown = sorted(collect_domains(cleaned_dir) - cache.keys())

    # 第一步:本地关键词能认出来的,直接判定,不消耗模型调用
    still_unknown = []
    local_hits = 0
    for d in all_unknown:
        label = local_match(d)
        if label:
            cache[d] = label
            local_hits += 1
        else:
            still_unknown.append(d)
    if local_hits:
        print(f"本地规则直接识别: {local_hits} 个")

    # 第二步:真正认不出的,交给模型
    if still_unknown and api_key:
        print(f"需要模型判断的域名: {len(still_unknown)} 个")
        failed_batches = 0
        for i in range(0, len(still_unknown), BATCH_SIZE):
            batch = still_unknown[i:i + BATCH_SIZE]
            try:
                cache.update(call_model(batch, api_key))
            except (urllib.error.HTTPError, json.JSONDecodeError, KeyError) as e:
                failed_batches += 1
                print(f"批次 {i} 标注失败,跳过: {e}")
            time.sleep(1)
        if failed_batches:
            print(f"共 {failed_batches} 个批次失败,下次运行会重试(未写入缓存)")
    elif still_unknown and not api_key:
        print(f"缺少 GEMINI_API_KEY,{len(still_unknown)} 个域名暂不标注")

    if local_hits or still_unknown:
        save_cache(cache_path, cache)

    annotate_files(cleaned_dir, cache)
    print(f"已附加注释,缓存共 {len(cache)} 条")


if __name__ == "__main__":
    main()
