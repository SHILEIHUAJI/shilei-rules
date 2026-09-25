<!-- STATS_START -->
### 📊 规则统计详情

| 规则集名称 | 唯一规则数量 |
| :--- | :--- |
| Reject-Manually.yaml | 81 |
| bytedance-global.yaml | 12 |
| claude-ai.yaml | 6 |
| cn-direct.yaml | 331 |
| google-android.yaml | 33 |
| international-website.yaml | 25 |
| my-rules.yaml | 202 |
| tv-player.yaml | 5 |
| usa.yaml | 1 |
| vivo-ads.yaml | 103 |
| **全库去重总计** | **799** |

### 🏷️ 规则类型分布

| 类型 | 数量 |
| :--- | :--- |
| DOMAIN-SUFFIX | 551 |
| DOMAIN | 125 |
| PROCESS-NAME | 92 |
| RULE-SET | 22 |
| AND | 22 |
| DOMAIN-KEYWORD | 16 |
| IP-CIDR | 8 |
| DOMAIN-WILDCARD | 6 |
| DST-PORT | 5 |
| MATCH | 3 |
| SRC-IP-CIDR | 2 |
| SUB-RULE | 2 |
| DOMAIN-REGEX | 1 |

### ✅ 未发现跨文件重复规则

<!-- STATS_END -->

# 🐱 Shilei Rules 极致分流

简介：个人维护的 Mihomo (Clash Meta) 规则库

## 专属规则集功能

建议配合 `no-resolve` 使用（IP 类规则无需二次 DNS 解析，减少不必要的查询开销）。

## 配置示例

```yaml
rule-providers:
  bytedance-global:
    type: http
    behavior: classical
    url: "https://example.com/bytedance-global.yaml"
    path: ./ruleset/bytedance-global.yaml
    interval: 86400

rules:
  - RULE-SET,bytedance-global,Tiktok,no-resolve
```

## 仅 Linux 内核检验会遇到如下 Warn ⚠️，请忽略警告。其他客户端无提醒，可以正常使用。如果在意，请放弃使用此规则。

```
provider is Classical, only matching it contain domain rule
```

---

## 📋 本仓库的自动化检测说明

每次 push 后，GitHub Action 会自动扫描全部规则文件并生成上方统计报告，包含四个部分：

- **规则统计详情 / 规则类型分布**：单纯的数量统计，方便掌握规则库规模。
- **❗ 疑似拼写错误的规则类型**：检测规则类型前缀（如 `DOMAIN-SUFFIX`）是否在 mihomo 官方支持的类型列表里，防止手滑打错字导致某条规则静默失效（mihomo 遇到无法识别的类型不会报错，只会跳过该条规则，非常难排查）。**这张表不出现，说明本次没有发现拼写问题**，不是没检测。
- **🚨 语义冲突规则**：检测同一个域名是否同时出现在"用途相反"的规则集里（比如同时出现在拦截类和直连类文件中）。如果出现，说明这个域名的实际生效结果取决于你主配置里 `RULE-SET` 引用的先后顺序，很可能不是你想要的效果，需要人工核对处理。**这张表不出现，说明没有检测到冲突。**
- **⚠️ 跨文件/跨模块重复规则**：检测完全相同或逻辑等价（`AND`/`OR` 条件顺序不同但含义相同）的规则是否在多个文件中重复出现，包括藏在 `sub-rules:` 里的条件。**显示"✅ 未发现跨文件重复规则"就是真的没有重复**，可以放心。

> 语义冲突检测依赖脚本里手动维护的 `FILE_INTENT` 分类表（哪个文件是"拦截用途"、哪个是"直连用途"、哪个是"代理用途"）。新增规则文件后记得同步更新脚本里这张表，否则新文件不会被纳入语义冲突检测范围。

## 关于 `my-rules.yaml`

这个文件是主配置文件里 `rules:` / `sub-rules:` 主列表的副本，专门放进仓库参与上述自动检测（查重、类型校验、语义冲突），本身不作为独立的 rule-provider 被 mihomo 引用。每次修改主配置的 `rules` 列表后，记得同步更新这份副本，保证检测结果反映的是线上实际生效的规则。

## 关于规则集的详细配置，请参考 [Mihomo 官方文档](https://wiki.metacubex.one/config/rule-providers/)

## 状态

规则集维护中，欢迎贡献。
