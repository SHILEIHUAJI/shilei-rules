import os
import re

# 获取脚本所在的当前目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 定义需要处理的规则文件
RULE_FILES = [
    'google-android.yaml',
    'bytedance-global.yaml',
    'cn-direct.yaml'
]

def process_rules():
    file_stats = {}
    all_unique_rules = set()

    for filename in RULE_FILES:
        filepath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(filepath):
            print(f"警告: 找不到文件 {filename}")
            continue

        rules_in_this_file = []
        with open(filepath, 'r', encoding='utf-8') as f:
            # 这里的逻辑：保留 payload: 这一行，但对其下的规则进行去重排序
            content = f.readlines()

        header = []
        raw_rules = []
        for line in content:
            clean_line = line.strip()
            # 识别 payload 声明行或注释行，这些不参与排序去重
            if clean_line.startswith('payload:') or clean_line.startswith('#') or not clean_line:
                if not raw_rules: # 只记录规则出现之前的注释和 header
                    header.append(line)
            else:
                raw_rules.append(clean_line)

        # 1. 内部去重并排序
        unique_raw_rules = sorted(list(set(raw_rules)))
        
        # 2. 写回原文件（实现自动清理）
        with open(filepath, 'w', encoding='utf-8') as f:
            for h in header:
                f.write(h)
            for r in unique_raw_rules:
                f.write(f"  - {r.lstrip('- ')}\n") # 统一格式化为 Mihomo 标准格式

        # 3. 统计数据
        file_stats[filename] = len(unique_raw_rules)
        for r in unique_raw_rules:
            all_unique_rules.add(r)

    return file_stats, len(all_unique_rules)

def update_readme(stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    
    # 如果 README 不存在则创建
    if not os.path.exists(readme_path):
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("# 我的 Mihomo 分流规则库\n\n## 自动化统计\n")

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 构建统计表格
    table_content = "### 📊 规则统计详情\n\n"
    table_content += "| 规则集名称 | 唯一规则数量 |\n"
    table_content += "| :--- | :--- |\n"
    for name, count in stats.items():
        table_content += f"| {name} | {count} |\n"
    table_content += f"| **全库去重总计** | **{total_unique}** |\n"

    # 正则替换旧表格。如果没有找到表格标记，就在文末追加
    marker = "### 📊 规则统计详情"
    if marker in content:
        # 匹配从标记开始到下一个双换行或文件末尾的内容
        new_content = re.sub(r'### 📊 规则统计详情.*?(?=\n\n|$)', table_content, content, flags=re.DOTALL)
    else:
        new_content = content.strip() + "\n\n" + table_content

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    print("开始处理规则文件...")
    stats_data, unique_total = process_rules()
    print(f"去重排序完成！全库唯一规则总数: {unique_total}")
    
    update_readme(stats_data, unique_total)
    print("README.md 更新完成。")
