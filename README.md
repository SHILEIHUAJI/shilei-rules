<!-- STATS_START -->
### 🛡️ Mihomo 规则库深度审计报告

| 文件名 | 总数 | 域名类 | IP类 | 应用/协议 | 逻辑/高级 | 异常 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| google-android.yaml | **0** | 0 | 0 | 0 | 0 | 0 |
| bytedance-global.yaml | **0** | 0 | 0 | 0 | 0 | 0 |
| cn-direct.yaml | **0** | 0 | 0 | 0 | 0 | 0 |

> **全库去重后的唯一规则总数：0**

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
