import csv
from itertools import product, combinations, permutations


class TestMatrix:
    def __init__(self):
        self.option_list = [
            ["选项11", "选项21"],
            ["选项11", "选项22"],
            ["选项11", "选项23"],
            ["选项12", "选项21"],
            ["选项12", "选项22"],
            ["选项12", "选项23"]
        ]
        self.project_list = ["条件1", "条件2"]

    def make_example(self):
        """生成模版"""
        need_or_not = input("是否需要导出模板:\n"
                            "1、是\n"
                            "2、否\n")
        if need_or_not == ("1" or "是"):
            self.write_file(None, None)
        elif need_or_not == ("2" or "否"):
            self.open_file()
        else:
            self.open_file()
            # print("输入错误，请重新输入")
            # self.make_example()

    def open_file(self):
        """打开文件"""
        target = input("请输入需加载的文件名：")
        with open(target or "1.csv", 'r', encoding="UTF-8") as f:
            reader = csv.DictReader(f)
            self.project_list = reader.fieldnames
            key_list = reader.fieldnames
            self.option_list = []
            reader = list(reader)
            # print(reader)
            for key in key_list:
                _list = []
                for r in reader:
                    _list.append(r[key])
                _list = sorted(set(_list), key=_list.index)  # 去重
                self.option_list.append(_list)

    def be_sure(self, checking_list):
        """集中处理异常数据，优化输出内容"""
        # 1、避免空白行出现
        for op in checking_list:
            if op:
                pass
            else:
                checking_list = []
                break
        return checking_list

    def zhuanyi(self, checking_list):
        # todo 转义特殊字符
        pass

    def huchi(self, checking_list):
        # todo 引入条件互斥过滤
        self.open_file()
        pass

    def youxianji(self, checking_list):
        # todo 引入选项关注度系数，以此计算用例优先级
        pass

    def make_matrix(self, project_list=None, option_list=None):
        """生成矩阵"""
        if option_list is None:
            option_list = self.option_list
        if project_list is None:
            project_list = self.project_list
        self.project_list = project_list

        matrix_way = int(input("请选择生成矩阵的方式\n"
                               "1、多选项多配置项\n"
                               "2、单配置项多选项\n"))
        if matrix_way == 1:
            self.many_many(option_list)
        elif matrix_way == 2:
            self.one_many(option_list)

    def many_many(self, option_list=None):
        """
        输出列表
        形式为：[[],[],[],[],[],[],[],[]]
        """
        all_option = []
        for _list in product(*option_list):  # 生成矩阵
            # print(_list)
            _list = self.be_sure(_list)
            if not _list:
                pass
                # print(_list)
                # print(len(_list))
            else:
                all_option.append(list(_list))
        self.option_list = all_option

    def one_many(self, option_list=None):
        """
        输出列表
        形式为：[[],[],[],[],[],[],[],[]]
        """
        all_option = []
        option_list = option_list[0]
        p = list(permutations(option_list, len(option_list)))
        for _list in p:  # 将每一项中含重复项的内容删除
            dic = {}.fromkeys(_list)
            if len(_list) == len(dic):
                all_option.append(_list)
            else:
                pass
        self.option_list = all_option

    def write_file(self, project_list=None, option_list=None):
        """写入文件"""
        if option_list is None:
            option_list = self.option_list
        if project_list is None:
            project_list = self.project_list

        def make_name():
            fn = ""
            ln = len(project_list)
            if ln > 3:
                ln = 3
            for p in range(0, ln):
                fn += str(project_list[p])
                if p < ln - 1:
                    fn += "_"
            return fn

        file_name = make_name() + '.csv'
        with open(file_name, 'w', encoding='UTF-8', newline='') as f:
            write = csv.writer(f)
            write.writerow(project_list)
            write.writerows(option_list)
            print("测试矩阵生成完毕！")
        # pass

    def main(self):
        self.make_example()
        self.make_matrix()
        self.write_file()


if __name__ == '__main__':
    matrix = TestMatrix()
    matrix.main()
