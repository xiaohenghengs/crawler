import os
import yaml

parent_path = os.path.dirname(os.path.realpath(__file__))  # 父文件夹的绝对路径
with open(os.path.join(parent_path, 'database.yaml'), 'r') as f:
    database = yaml.safe_load(f)
