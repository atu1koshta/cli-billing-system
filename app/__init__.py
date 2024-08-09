import logging.config
import yaml
import os

# Determine the path to logging.yml dynamically
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, '../logging.yml')

with open(config_path, 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
