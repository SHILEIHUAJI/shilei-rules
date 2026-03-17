import os

# 基础配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULE_FILES = ['google-android.yaml', 'bytedance-global.yaml', 'cn-direct.yaml']

def update_readme(stats, total_unique):
    readme_path = os.path.join(BASE_DIR, 'README.md')
    
    # 彻底拆分，确保不被任何编辑器或聊天软件拦截
    s_m = "<" + "!-- STATS_START --" + ">"
    e_m = "<" + "!-- STATS_END --" + ">"
    
    table_head = "\n### 📊 规则统计详情\n\n| 规则集名称 | 唯一规则数量 |\n| :--- | :--- |\n"
    table_body = ""
    for name, count in stats.items():
        table_body += f"| {name} | {count} |\n"
    table_footer = f"| **全库去重总计** | **{total_unique}** |\n\n"

    new_block = s_m + table_head + table_body + table_footer + e_m

    # 逻辑：读取、替换或创建
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if s_m in content and e_m in content:
            # 精准切片替换
            pre = content.split(s_m)[0]
            post = content.split(e_m)[1]
            new_content = pre + new_block + post
        else:
            # 没找到标记就追加
            new_content = content.strip() + "\n\n" + new_block
    else:
        new_content = "# Rules\n\n" + new_block

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    res, total_set = {}, set()
    for f_name in RULE_FILES:
        path = os.path.join(BASE_DIR, f_name)
        if os.path.exists(path):
            current_rules = []
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    c = line.strip().lstrip('- ')
                    if c and not c.startswith(('#', 'payload:')):
                        current_rules.append(c)
            
            # 去重、排序并写回文件
            unique_list = sorted(list(set(current_rules)))
            with open(path, 'w', encoding='utf-8') as f:
                f.write("payload:\n")
                for r in unique_list:
                    f.write(f"  - {r}\n")
            
            res[f_name] = len(unique_list)
            total_set.update(unique_list)
            
    update_readme(res, len(total_set))
