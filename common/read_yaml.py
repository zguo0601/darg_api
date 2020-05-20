import os
import yaml


def readyaml(yamlpath):
    if not os.path.isfile(yamlpath):
        raise FileNotFoundError("文件路径不存在，请检查文件路径")
    f = open(yamlpath,"r",encoding='utf-8')
    cfg = f.read()
    d = yaml.load(cfg,Loader=yaml.FullLoader)
    #print("读取测试文件数据:%s"%d)
    return d

if __name__ == '__main__':
    yamlpath = ("../data/data.yaml")
    r = readyaml(yamlpath)["merchant_name"]
    print(r)

