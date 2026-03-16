# 🐱 Shilei Rules 定制规则库
简介: 个人维护的 Mihomo (Clash Meta) 专属规则集
功能: 字节跳动海外规则 (TikTok, Lemon8, 关联拉流域名)
更新日期: 不定时更新
说明: 全平台通用，已移除安卓进程名，建议配合 no-resolve 使用

# 使用方法
# rule-providers:
    bytedance_global:
      type: http
      behavior: classical
      url: "RAW链接"
      path: ./ruleset/bytedance_global.yaml
      interval: 86400
# rules:
    - RULE-SET,bytedance_global,Tiktok,no-resolve



### 📊 规则统计详情

| 规则集名称 | 规则数量 |
| :--- | :--- |
| google-android.yaml | 23 |
| bytedance-global.yaml | 22 |
| cn-direct.yaml | 187 |
| **总计** | **232** |


| 规则集名称 | 规则数量 |
| :--- | :--- |
| google-android.yaml | 23 |
| bytedance-global.yaml | 22 |
| cn-direct.yaml | 187 |
| **总计** | **232** |
