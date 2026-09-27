# Proc Alias 映射表管理与自动校验

维护 Android 应用包名（`Package Name`）到目录别名（`Alias`）的映射关系文件 `proc-alias.yaml`。

<!-- STATS_START -->
<!-- 运行脚本后，最新包名去重、计数与分类统计表格将由脚本自动更新并填充在此处 -->
<!-- STATS_END -->

## 📄 文件结构说明

* `proc-alias.yaml`: 核心配置文件（包名与别名映射表）。
* `check_proc_alias.py`: 自动化检测与统计脚本（运行后会自动更新本文档）。
* `.github/workflows/check-alias.yml`: GitHub Actions 自动触发并更新 README 的工作流配置。

---

## 🛠️ 本地运行与更新

提交代码前或修改包名后，可以在本地终端运行：

```bash
python check_proc_alias.py
