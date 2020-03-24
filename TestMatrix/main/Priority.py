import csv
import time

# import numpy as np

from TestMatrix.main.MakeTestMatrix import *


class MatrixPriority:
    def __init__(self):
        pass

    def show_reader(self, reader=None, key=None):
        """
        拆包读取文件的内容
        :param reader: 读取出的字典格式的迭代器
        :param key: 需要取出哪一列
        :return: 返回改列的内容
        """
        _list = []
        for r in reader:
            _list.append(r[key])
        _list = sorted(set(_list), key=_list.index)  # 去重
        return _list

    def open_file(self, target="2_priority.csv", type="matrix"):
        """

        :param target: 需要读取的带系数的表格
        :return: 字典（首行为键，列为值）{key:[],}
        """
        self.target = target

        def get_option_list(reader, key_list):
            option_list = []
            for key in key_list:
                _list = []
                for r in reader:
                    _list.append(r[key])
                if type == "matrix":
                    _list = sorted(set(_list), key=_list.index)  # 去重
                option_list.append(_list)
            return option_list

        if type == "matrix":
            target = CSV_FILE_PATH + (input("请输入需加载的文件名1：") or target)
        elif type == "priority":
            target = CSV_OUTPUT_PATH + target
        else:
            pass
        with open(target, 'r', encoding="UTF-8-sig") as f:
            reader = csv.DictReader(f)
            key_list = reader.fieldnames

            reader = list(reader)
            pri_list = []

            for _key in key_list:
                if "系数" in _key:
                    pri_list.append(_key)
                    key_list.remove(_key)
                else:
                    pass
            option_list = get_option_list(reader, key_list)
            pri_list = get_option_list(reader, pri_list)
        return key_list, option_list, pri_list

    def make_pri_dir(self, key_list=None, option_list=None, pri_list=None):
        """
        制作各配置项优先级字典
        :param option_list:
        :param pri_list:
        :return:
        """
        dir = {}
        for n in range(len(option_list)):
            key_ = key_list[n]
            for i in range(len(option_list[n])):
                key = option_list[n][i]
                if key:
                    dir[key_ + "_" + key] = pri_list[n][i]
        return dir

    def write_file(self, key_list=None, option_list=None):
        """
        生成一个不含优先级的源文件，供生成测试矩阵
        :param key_list: 配置项列表
        :param option_list: 各配置项选项列表
        :return: 保存的文件名称
        """
        fn = self.target.split("_")[:-1:][0]
        file_name = CSV_FILE_PATH + fn + '.csv'
        lines = []
        for n in range(len(key_list)):
            line = []
            for i in range(len(option_list[n])):
                line.append(option_list[i][n])
            lines.append(line)
        with open(file_name, 'w', encoding="UTF-8-sig", newline='') as f:
            write = csv.writer(f)
            write.writerow(key_list)
            write.writerows(lines)
        return fn + ".csv"

    def main(self):
        """
        输出目标测试矩阵的名称，赋值字典
        :return:
        """
        flag = "go"
        while True:
            if not flag:
                break
            else:
                try:
                    key_list, option_list, pri_list = self.open_file()
                    try:
                        pri_dir = self.make_pri_dir(key_list, option_list, pri_list)
                        file_name = self.write_file(key_list, option_list)
                        matrix1 = TestMatrix()
                        matrix1.main(file_name)
                        fn = ''
                        ln = len(key_list)
                        if ln > 3:
                            ln = 3
                        for p in range(0, ln):
                            fn += str(key_list[p])
                            if p < ln - 1:
                                fn += "_"
                        file_name = file_name.split(".")[0] + "_" + fn + ".csv"
                        return file_name, pri_dir
                    except Exception as e:
                        print(e)
                        # 如果输入不含优先级的源文件，询问，并生成无优先级矩阵
                        flag = input("文件不包含优先级，是否使用改文件？\n"
                                     "重新输入请回车, 输入任意字符使用该文件")
                        if not flag:
                            self.main()
                        else:
                            file_name = self.write_file(key_list, option_list)
                            return file_name, None
                except Exception as e:
                    print(e)
                    flag = input("无此文件，重新输入请回车, 输入任意字符退出")
                    if not flag:
                        self.main()
                    else:
                        pass

    def add_score(self, file_name, pri_dir):
        """
        为测试矩阵添加系数
        :param file_name: 文件名称
        :param pri_dir: 优先级字典
        :return: 配置项列表，添加了系数的配置项列表
        """

        def change_way(need_change):
            """
            切换矩阵方向
            :return:
            """
            changed = []
            for x in range(len(need_change[0])):
                change_x = []
                for y in range(len(need_change)):
                    change_x.append(need_change[y][x])
                changed.append(change_x)
            return changed

        def add_priority(key_list, option_list):
            scores = []
            for ops_num in range(len(option_list)):
                key = key_list[ops_num]
                ops = option_list[ops_num]
                for op_num in range(len(ops)):
                    ko = key + "_" + ops[op_num]
                    if len(scores) - 1 >= op_num:
                        scores[op_num] += int(pri_dir[ko])
                    else:
                        scores.insert(op_num, int(pri_dir[ko]))
            option_list.append(scores)
            key_list.append("系数")
            return key_list, option_list

        def add_kind(key_list, option_list):
            score = option_list[-1]
            # mean = max(score)
            # mean = np.median(score)
            # print(mean)
            kind = []
            _ss = 0
            for s in score:
                _ss += int(s)
            mean = _ss / len(score)
            M = 0
            for i in score:
                M += (i - mean) ** 2
            M = (M / len(score)) ** 0.5
            print(M)
            for k in score:
                if int(k) > (M + mean):
                    kind.append('高')
                elif int(k) < (mean - M):
                    kind.append('低')
                else:
                    kind.append("中")
            key_list.append("优先级")
            option_list.append(kind)
            print(score)
            print(mean)
            return key_list, option_list

        target_file = file_name
        key_list, option_list, pri_list = self.open_file(target_file, type="priority")

        key_list, option_list = add_priority(key_list, option_list)

        # 添加标注
        key_list, option_list = add_kind(key_list, option_list)
        print(key_list, option_list)
        option_list = change_way(option_list)
        return key_list, option_list


if __name__ == '__main__':
    matrix = MatrixPriority()
    file_name, pri_dir = matrix.main()
    key_list, option_list = matrix.add_score(file_name, pri_dir)
    matrix1 = TestMatrix()
    matrix1.write_file(key_list, option_list)
