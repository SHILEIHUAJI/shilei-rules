<!-- STATS_START -->
### 📊 规则库深度审计

| 规则集文件 | 总计 | Suffix | Domain | IP/ASN | 其他 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| google-android.yaml | **22** | 7 | 2 | 1 | 12 |
| bytedance-global.yaml | **21** | 11 | 7 | 0 | 3 |
| cn-direct.yaml | **185** | 181 | 4 | 0 | 0 |

> **全库去重后的唯一规则总数：228**

<!-- STATS_END -->

# 🐱 Shilei Rules 定制规则库
简介：个人维护的 Mihomo (Clash Meta) 规则库
# 专属规则集功能
国内直连,谷歌全家桶,字节跳动海外规则 (TikTok, Lemon8, 关联拉流域名，建议配合no-resolve使用
# 使用方法
    rule-providers:
      bytedance-global:
        type:http
        behavior:classical
        url："RAW链接”
        path:./ruleset/bytedance_global.yaml
        interval:86400

    Rules
      - RULE-SET,bytedance-global,Tiktok,no-resolve

# 状态
规则集维护中
