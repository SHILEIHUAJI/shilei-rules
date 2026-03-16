import os
import re

def count_rules_in_file(filepath):
    count = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 排除空行、注释行、以及 payload: 这种结构声明行
            if line and not line.startswith('#') and not line.startswith('payload:'):
                count += 1
    return count

def update_readme(rule_count):
    # 读取现有的 README.md
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 用正则替换掉旧的统计数字 (假设你在 README 里预留了 "当前规则数: 1234" 这样的文本)
    new_content = re.sub(r'当前规则数: \d+', f'当前规则数: {rule_count}', content)
    
    # 把新的数量写回 README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    # 假设我们要统计你那个核心的 Google 规则集
    target_file = 'google-android.yaml'
    if os.path.exists(target_file):
        total_rules = count_rules_in_file(target_file)
        print(f"统计完成，共 {total_rules} 条规则。")
        update_readme(total_rules)
