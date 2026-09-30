#!/usr/bin/env python3
"""
annotate_domains.py
给 cleaned-logs/*/*.yaml 里的域名加业务用途注释。
不依赖 AI，不需要 Token，使用本地规则自动识别域名用途。
"""

import json
import os
import re
import sys
import time
from pathlib import Path
import yaml


# ============================
# 本地规则引擎（自动识别域名业务）
# ============================

def local_annotate(domain: str) -> str:
    d = domain.lower()

    # 广告 / 追踪
    if any(k in d for k in [
        "ads", "adservice", "doubleclick", "tracking", "analytics",
        "advert", "measure", "pixel", "tagmanager"
    ]):
        return "疑似广告追踪"

    # CDN / 随机节点
    if any(k in d for k in [
        "cdn", "cloudfront", "edgekey", "akamai", "cache", "llnwd",
        "fastly", "cloudflare", "hwcdn", "alicdn"
    ]):
        return "CDN节点"

    # 国内大厂
    if any(k in d for k in ["qq.com", "tencent", "weixin", "wechat"]):
        return "腾讯服务"
    if any(k in d for k in ["alibaba", "alicdn", "taobao", "tmall"]):
        return "阿里服务"
    if any(k in d for k in ["baidu", "bdstatic"]):
        return "百度服务"
    if any(k in d for k in ["bytedance", "douyin", "tiktokcdn"]):
        return "字节跳动服务"

    # 国外大厂
    if "google" in d or "gstatic" in d:
        return "谷歌服务"
    if "facebook" in d or "fbcdn" in d:
        return "Meta服务"
    if "apple" in d or "icloud" in d:
        return "苹果服务"
    if "microsoft" in d or "msn" in d or "office" in d:
        return "微软服务"
    if "amazonaws" in d:
        return "AWS云服务"

    # 视频 / 音乐 / 游戏
    if any(k in d for k in ["youtube", "ytimg"]):
        return "YouTube视频"
    if "spotify" in d:
        return "Spotify音乐"
    if any(k in d for k in ["steam", "valve"]):
        return "Steam游戏平台"

    # 邮件服务
    if any(k in d for k in ["smtp", "mail", "mx"]):
        return "邮件服务"

    # 安全 / 反作弊
    if any(k in d for k in ["anticheat", "safebrowsing"]):
        return "安全/反作弊"

    # IoT / 智能设备
    if any(k in d for k in ["miio", "tuya", "smartdevice"]):
        return "智能设备服务"

    # 金融 / 支付
    if any(k in d for k in ["alipay", "paypal", "stripe"]):
        return "支付服务"

    # 电商
    if any(k in d for k in ["amazon", "jd.com", "rakuten"]):
        return "电商服务"

    # 社交
    if any(k in d for k in ["twitter", "x.com"]):
        return "社交平台"

    # AI / 模型服务
    if any(k in d for k in ["openai", "anthropic", "ai"]):
        return "AI服务"

    # 运营商 / DNS
    if any(k in d for k in ["dns", "resolver", "carrier"]):
        return "DNS/运营商服务"

    # 默认
    return "未知"


# ============================
# YAML 处理逻辑（保持你的原逻辑）
# ============================

def load_cache(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def save_cache(path: Path, cache: dict):
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(cache, f, allow_unicode=True, sort_keys=True)


def parse_domain(line: str) -> str | None:
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

    cache = load_cache(cache_path)
    unknown = sorted(collect_domains(cleaned_dir) - cache.keys())

    if unknown:
        print(f"需要标注的新域名: {len(unknown)} 个")
        for d in unknown:
            cache[d] = local_annotate(d)
        save_cache(cache_path, cache)

    annotate_files(cleaned_dir, cache)
    print(f"已附加注释,缓存共 {len(cache)} 条")


if __name__ == "__main__":
    main()
