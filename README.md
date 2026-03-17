<!-- STATS_START -->
### 📊 规则统计详情

| 规则集名称 | 唯一规则数量 |
| :--- | :--- |
| bytedance-global.yaml | 21 |
| cn-direct.yaml | 186 |
| google-android.yaml | 22 |
| **全库去重总计** | **229** |

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

    rules
      - RULE-SET,bytedance-global,Tiktok,no-resolve

## 关于规则集的详细配置，请参考 [Mihomo 官方文档](https://wiki.metacubex.one/config/rule-providers/)


# 状态
规则集维护中
