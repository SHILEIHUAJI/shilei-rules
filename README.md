# Proc Alias 映射表管理

本项目用于维护 Android 应用包名（`Package Name`）到目录别名（`Alias`）的映射关系文件 `proc-alias.yaml`。

## 📁 目录说明

* `proc-alias.yaml`: 核心配置文件，保存包名与目录别名的映射。
* `check_proc_alias.py`: 根目录检测脚本，负责自动校验重复项、统计总数与分类显示。
* `.github/workflows/check-alias.yml`: GitHub Actions 配置文件，提交修改时自动触发校验。

## 🚀 本地运行检测

在提交代码前，建议先在本地运行检测脚本：

```bash
python check_proc_alias.py
