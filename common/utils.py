"""
@File ：utils.py
@Auth ： wanliang
@Description：存放公共方法：如日志记录、发送邮件、数据库操作、获取路径等
"""
import yaml
import json
import logging
import logging.config


class config:
    config_path = './config/config.yaml'


def get_yaml_file_content(filepath):
    with open(filepath, 'r', encoding='UTF-8') as f:
        return yaml.safe_load(f)


def set_yaml_file_content(yamlpath, data):
    with open(yamlpath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)


def get_config_data():
    return get_yaml_file_content(config.config_path)


config_data = get_config_data()


# 【日志配置】
def get_logger():
    """捕获日志"""
    logging.config.fileConfig(config_data['log_config']['log_config_file_path'])
    logger = logging.getLogger(config_data['log_config']['log_output_type'])
    return logger


def get_page_data(page):
    return get_yaml_file_content(config_data['page_data_path'][page])


def get_test_page_data(page):
    return get_yaml_file_content(config_data['page_test_data_path'][page])


def yaml_content_param_replace(yaml_content, param_dict={}):
    raw = json.dumps(yaml_content)
    for key, value in param_dict.items():
        raw = raw.replace('${' + key + '}', value)
    return json.loads(raw)
