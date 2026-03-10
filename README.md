# 🚀 Shilei Rules 定制规则库

这里是我个人维护的 Mihomo (Clash Meta) 专属规则集，旨在实现更精准的流量控制与分流。

## 📦 规则列表
| **Bytedance Global** | 字节跳动海外规则 | `classical` | TikTok, Lemon8, 关联拉流域名 |
| **CN Direct** | 国内直连增强 | `classical` | 针对特定环境优化的国内 IP 与域名 |

## 🛠️ 使用方法

在你的主配置文件 `config.yaml` 中添加以下代码：

```yaml
rule-providers:
  bytedance_global:
    type: http
    behavior: classical
    url: "Raw链接"
    path: ./ruleset/bytedance_global.yaml
    interval: 86400

rules:
  - RULE-SET,bytedance_global,Tiktok,no-resolve

