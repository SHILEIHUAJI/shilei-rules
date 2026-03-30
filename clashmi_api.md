# linux 安装命令
    pkg install curl
    
## 安装jq
    pkg install jq
    
## 加上 -s (silent) 参数隐藏 curl 的进度条，并通过管道 | 交给 jq 处理
    curl -s -H "Authorization: Bearer 你的密钥" http://127.0.0.1:9090/version | jq

# 获取当前运行的 Clash 版本
    curl -H "Authorization: Bearer 你的密钥" http://127.0.0.1:9090/version

# ​查看当前的配置信息
    curl -H "Authorization: Bearer 你的密钥" http://127.0.0.1:9090/configs

