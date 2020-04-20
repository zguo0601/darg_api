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
    test_data = readyaml('test_data.yaml')["invoiceApplyCategoryDTOJson"][0]
    # print(type(test_data))
    print(test_data)
    # print(test_data['merchant_accountName_data'])
    # print(type(test_data['merchant_accountName_data'][1]))
    # print(test_data['merchant_accountName_data'][1])
    # print(test_data['merchant_accountName_data'][1][1]['success'])
    # print(test_data['merchant_accountName_data'][1][1]['message'])
    # print(test_data['merchant_accountName_data'][1][1]['message']['code'])
    # print(test_data['merchant_accountName_data'][1][1]['message']['content'])