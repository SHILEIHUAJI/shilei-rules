<!-- STATS_START -->
### 📊 规则统计详情

| 规则集名称 | 唯一规则数量 |
| :--- | :--- |
| Reject-Manually.yaml | 85 |
| bytedance-global.yaml | 12 |
| claude-ai.yaml | 6 |
| cn-direct-pro.yaml | 32 |
| cn-direct.yaml | 331 |
| google-android.yaml | 33 |
| international-website.yaml | 27 |
| requirements.txt | 1 |
| telegram-ip-pro.yaml | 17 |
| tv-player.yaml | 5 |
| usa.yaml | 1 |
| vivo-ads.yaml | 103 |
| **全库去重总计** | **645** |

### 🏷️ 规则类型分布

| 类型 | 数量 |
| :--- | :--- |
| DOMAIN-SUFFIX | 416 |
| DOMAIN | 117 |
| PROCESS-NAME | 52 |
| IP-CIDR | 20 |
| IP-ASN | 18 |
| DOMAIN-KEYWORD | 11 |
| IP-CIDR6 | 8 |
| DOMAIN-WILDCARD | 6 |
| DST-PORT | 4 |
| DOMAIN(text) | 1 |

### ⚠️ 跨文件重复规则（共 8 条）

| 规则内容 | 出现在 |
| :--- | :--- |
| `DOMAIN,lookup.api.bsb.baidu.com` | Reject-Manually.yaml, vivo-ads.yaml |
| `DOMAIN,vcode-or.vivo.com.-` | Reject-Manually.yaml, vivo-ads.yaml |
| `DOMAIN-SUFFIX,ip.cn` | Reject-Manually.yaml, cn-direct.yaml |
| `DOMAIN-SUFFIX,liquidlink.cn` | Reject-Manually.yaml, cn-direct.yaml |
| `DOMAIN-SUFFIX,nekogram.app` | Reject-Manually.yaml, telegram-ip-pro.yaml |
| `DOMAIN-SUFFIX,t.me` | international-website.yaml, telegram-ip-pro.yaml |
| `DOMAIN-SUFFIX,telegram.org` | international-website.yaml, telegram-ip-pro.yaml |
| `PROCESS-NAME,com.android.mms.service` | Reject-Manually.yaml, vivo-ads.yaml |

<!-- STATS_END -->

# 🐱 Shilei Rules 极致分流
简介：个人维护的 Mihomo (Clash Meta) 规则库

# 专属规则集功能
建议配合no-resolv

## 配置示例 
    rule-providers:
      bytedance-global:
        type:http
        behavior:classical
        url："”
        path:./ruleset/bytedance_global.yaml
        interval:86400

    rules
      - RULE-SET,bytedance-global,Tiktok,no-resolve

## 仅Linux内核检验会遇到如下Warn⚠️请忽略警告。其他客户端无提醒可以正常使用。如果在意,请放弃使用此规则。
    provider is Classical, only matching it contain domain rule

### 关于规则集的详细配置，请参考 [Mihomo 官方文档](https://wiki.metacubex.one/config/rule-providers/)


# 状态
规则集维护中,欢迎贡献。
