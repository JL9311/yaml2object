import yaml
import json


def field(name, required=False):
    """
    字段装饰器，用于标记字段的名称和是否必须
    :param name: 在配置文件中的名称，如果是嵌套的，用.分割
    :param required: 是否必须
    :return: 装饰器
    """

    def decorator(func):
        func.name = name
        func.required = required
        return func

    return decorator


def yaml_to_object(class_name, yaml_config_str):
    """
    将yaml配置转换为对象
    :param class_name: 类
    :param yaml_config_str: yaml配置
    :return: 对象
    """
    config_yaml = yaml.safe_load(yaml_config_str)
    config_obj = class_name()

    def read_yaml(items, config):
        try:
            if len(items) == 1:
                return config[items[0]]
            else:
                return read_yaml(items[1:], config[items[0]])
        except KeyError:
            return None

    for item in config_obj.__dict__:
        attr = getattr(class_name, item)
        name = attr.name
        required = attr.required
        # 读取 yaml，name是yaml的key，按.分割，required是是否必须
        # 读取yaml的值，赋值给application_config
        # 如果required是True，但是yaml中没有这个key，抛出异常
        name_list = name.split('.')
        # 是用递归的方式，一层一层的读取yaml
        value = read_yaml(name_list, config_yaml)
        if required and value is None:
            raise ValueError('yaml中没有这个key:' + name)
        if value is not None:
            config_obj.__setattr__(item, value)

    return config_obj


def json_to_object(class_name, json_str):
    """
    将json配置转换为对象
    :param class_name: 类
    :param json_str: json配置
    :return: 对象
    """
    json_dict = json.loads(json_str)
    json_obj = class_name()

    def read_json(items, json):
        try:
            if len(items) == 1:
                return json[items[0]]
            else:
                return read_json(items[1:], json[items[0]])
        except KeyError:
            return None

    for item in json_obj.__dict__:
        attr = getattr(class_name, item)
        name = attr.name
        required = attr.required
        # 读取 json，name是json的key，按.分割，required是是否必须
        # 读取json的值，赋值给application_config
        # 如果required是True，但是json中没有这个key，抛出异常
        name_list = name.split('.')
        # 是用递归的方式，一层一层的读取json
        value = read_json(name_list, json_dict)
        if required and value is None:
            raise ValueError('json中没有这个key' + name)
        elif value is not None:
            json_obj.__setattr__(item, value)
        else:
            json_obj.__setattr__(item, None)

    return json_obj
