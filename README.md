<!-- STATS_START -->
### 📊 规则统计详情

| 规则集名称 | 唯一规则数量 |
| :--- | :--- |
| Reject-Manually.yaml | 80 |
| bytedance-global.yaml | 12 |
| claude-ai.yaml | 6 |
| cn-direct-pro.yaml | 32 |
| cn-direct.yaml | 331 |
| google-android.yaml | 33 |
| international-website.yaml | 25 |
| telegram-ip-pro.yaml | 17 |
| tv-player.yaml | 5 |
| usa.yaml | 1 |
| vivo-ads.yaml | 103 |
| **全库去重总计** | **644** |

### 🏷️ 规则类型分布

| 类型 | 数量 |
| :--- | :--- |
| DOMAIN-SUFFIX | 411 |
| DOMAIN | 115 |
| PROCESS-NAME | 52 |
| IP-CIDR | 20 |
| IP-ASN | 18 |
| DOMAIN-KEYWORD | 11 |
| IP-CIDR6 | 8 |
| DOMAIN-WILDCARD | 6 |
| DST-PORT | 4 |

### ⚠️ 跨文件重复规则（共 1 条）

| 规则内容 | 出现在 |
| :--- | :--- |
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
