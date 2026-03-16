# 🐱 Shilei Rules 定制规则库
简介：个人维护的 Mihomo (Clash Meta) 规则库
# 专属规则集功能
国内直连,谷歌全家桶,字节跳动海外规则 (TikTok, Lemon8, 关联拉流域名定时更新说明，建议配合no-resolve使用
# 使用方法
    rule-providers:
      bytedance global:
      type:http
      behavior:classical
      url："RAW链接”
      path:./ruleset/bytedance_global.yaml
      interval:86400

    Rules
      - RULE-SET, bytedance_global,Tiktok, no-resolve

### 📊 规则统计详情

| 规则集名称 | 唯一规则数量 |
| :--- | :--- |
| google-android.yaml | 22 |
| bytedance-global.yaml | 22 |
| cn-direct.yaml | 186 |
| **全库去重总计** | **228** |

