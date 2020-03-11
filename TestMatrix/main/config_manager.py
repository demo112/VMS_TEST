import csv
from TestMatrix.main import *


class GetConfig:
    def __init__(self):
        pass

    def open_file(self):
        """打开文件"""
        target = CSV_FILE_PATH + "时间配置列表.csv"
        print(target)
        # target = input("请输入需加载的文件名：")
        with open(target, 'r', encoding="UTF-8-sig") as f:
            reader = csv.DictReader(f)
            self.project_list = reader.fieldnames
            key_list = reader.fieldnames
            self.option_list = []
            reader = list(reader)
            print(reader)
            return key_list, reader


if __name__ == '__main__':
    cfg = GetConfig()
    cfg.open_file()
