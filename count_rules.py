import os
import re

# 定义你要统计的三个文件
RULE_FILES = [
    'google-android.yaml',
    'bytedance-global.yaml',
    'cn-direct.yaml'
]

def count_rules_in_file(filepath):
    if not os.path.exists(filepath):
        return 0
    count = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 过滤掉空行、注释、yaml 结构头
            if line and not line.startswith('#') and not line.startswith('payload:'):
                count += 1
    return count

def update_readme(stats):
    readme_path = 'README.md'
    # 如果文件不存在，先创建一个基础模板
    if not os.path.exists(readme_path):
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("# 我的 Mihomo 分流规则库\n\n## 规则统计\n")

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 构建统计表格
    table_content = "### 📊 规则统计详情\n\n| 规则集名称 | 规则数量 |\n| :--- | :--- |\n"
    total = 0
    for name, count in stats.items():
        table_content += f"| {name} | {count} |\n"
        total += count
    table_content += f"| **总计** | **{total}** |\n"

    # 使用正则定位并替换。如果 README 里还没这部分，就直接追加在最后
    marker = "### 📊 规则统计详情"
    if marker in content:
        # 这种正则比较暴力，直接定位到表格末尾（假设表格后面没有重要内容）
        new_content = re.sub(r'### 📊 规则统计详情.*?(?=\n\n|$)', table_content, content, flags=re.DOTALL)
    else:
        new_content = content + "\n\n" + table_content

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    results = {}
    for file in RULE_FILES:
        count = count_rules_in_file(file)
        results[file] = count
        print(f"文件 {file}: 统计到 {count} 条规则")
    
    update_readme(results)
