import os
import yaml

parent_path = os.path.dirname(os.path.realpath(__file__))  # 父文件夹的绝对路径
with open(os.path.join(parent_path, 'config.yaml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    currency = config['CCY']
