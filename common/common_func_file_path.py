import os
from common.common_func_read_yaml import  readyaml

# cur_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# yaml_path = os.path.join(cur_path, "data", "data.yaml")
# merchantPriKey = readyaml(yaml_path)["Api_merchantPriKey"]["merchantPriKey"]
#
#
#
# #curpath = os.path.dirname(os.path.realpath(__file__))
# # yaml文件的路径
# # yamlpath = os.path.join('../data/data.yaml')
# # data = readyaml(yamlpath)['login_username_data']
#
# print(cur_path)
# print(yaml_path)
# print(type(merchantPriKey))

cur_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
yaml_path = os.path.join(cur_path, "data", "6.png")
f = open(yaml_path, "rb")
print(f.read())
print(yaml_path)