import os
import re

# 获取脚本所在的当前目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RULE_FILES = [
    'google-android.yaml',
    'bytedance-global.yaml',
    'cn-direct.yaml'
]

def count_rules_in_file(filename):
    # 使用绝对路径拼接，确保万无一失
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"警告: 找不到文件 {filename}")
        return 0
    count = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('payload:'):
                count += 1
    return count

# ... 后面保持 update_readme 逻辑一致，但读取 README.md 也要用 os.path.join(BASE_DIR, 'README.md')
