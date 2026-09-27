# Proc Alias 映射表管理与自动校验

维护 Android 应用包名（`Package Name`）到目录别名（`Alias`）的映射关系文件 `proc-alias.yaml`。

## 📄 文件结构

* `proc-alias.yaml`: 核心配置文件（包名与别名映射表）。
* `check_proc_alias.py`: 自动化检测与统计脚本。
* `.github/workflows/check-alias.yml`: GitHub Actions 自动触发配置文件。

---

## 📊 统计与校验逻辑说明

脚本 `check_proc_alias.py` 执行时将自动按以下规则解析并处理 `proc-alias.yaml`：

### 1. 语法解析与去重计数
* **原始解析总数**：统计配置文件中所有有效的 `包名: 别名` 配置项。
* **重复检测与定位**：自动判断包名唯一性。若出现重复包名，会**高亮报错指出首次出现行号与重复行号**，并中断工作流。
* **有效总数统计**：计算去重后的实际独立包名数量。

### 2. 包名按类别自动归类
根据 Android 包名命名规则，自动按以下分类归纳并计算数量占比：
* **Google 系应用与服务** (`com.google.*`)
* **Android 系统核心组件** (`com.android.*`)
* **字节跳动系** (`com.ss.android.*`, `com.bytedance.*`)
* **腾讯系** (`com.tencent.*`)
* **百度系** (`com.baidu.*`)
* **主流电商与服务** (阿里/拼多多/美团等)
* **vivo 厂商应用** (`com.vivo.*`)
* **微软系** (`com.microsoft.*`)
* **GitHub / 开源与极客工具** (`io.github.*`, `moe.shizuku.*`, `bin.mt.*` 等)
* **其他第三方应用**

---

## 🖥️ GitHub Actions 可视化大屏

每次 `push` 提交或发起 `Pull Request` 时，GitHub Actions 将自动运行检测脚本，并**在 Actions Run Summary 首页直接渲染 Markdown 统计大屏**：

无需翻阅控制台运行日志，直接在 GitHub Actions 页面即可直观看到：
1. **数据概览卡片**（总数、有效独立数、重复状态）
2. **重复报错面板**（准确提示冲突行数）
3. **分类汇总表格与占比**
4. **可折叠展开的应用明细表**

---

## 🛠️ 本地运行

提交前可在本地终端手动执行检测：

```bash
python check_proc_alias.py
