from VmsServerSet.setting.server_class import *
from TestMatrix.main.config_manager import *


def run_update_centos_server():
    """
    自动升级
    :return:
    """
    cent = ServerSetCentOS()
    print("【请确保安装包已上传至服务器】")
    ls_list = cent.give_order("ls", showback=False).split('\n')

    num = 1
    for file in ls_list:
        if file:
            print(str(num) + "、" + file)
            num += 1
    pg_num = input("请选择安装包：")
    pg = ls_list[int(pg_num) - 1]
    path1 = pg.split('.')[0]

    print("正在解压：%s" % pg)

    cent.give_order("unzip -u " + pg)
    time.sleep(3)
    cent.give_order("cd /root/%s/attendance/;pwd;chmod 777 *;./AttendanceInstall.sh" % path1)
    cent.give_order("cd /root/AttendanceSys/;./server.sh status")


def change_all_time(time=None):
    """
    time-> 2008-08-08 08:08:08
    :param time: 需要修改的目标时间，修改对象包括，一体机、人脸速通门、考勤服务器
    :return: None
    """
    if not time:
        time = input("请输入修改时间：\n"
                     "【格式：2000-1-1 08:08:08】")
    time_list = [
        time,
    ]

    def t2t(date_time):
        date_, time_ = date_time.split(" ")
        y, m, d = date_.split("-")
        date_time = y + "." + m + "." + d + "-" + time_
        return date_time

    def vms_():
        """
        修改一体机时间
        :return:
        """
        vms = ServerSetVMS()
        ob_vms = vms.login('206.10.30.1')
        vms.give_order(ob_vms, "date '%s'" % t)
        return "一体机"

    def face_1():
        """
        修改人脸速通门时间
        :return:
        """
        et = ServerSetVMS()
        ob_et = et.login("206.10.0.199")
        et.give_order(ob_et, "date -s %s" % t2t(t))
        return "人脸速通门(206.10.0.199)"

    def face_2():
        """
        修改人脸速通门时间
        :return:
        """
        et = ServerSetVMS()
        ob_et = et.login("206.10.25.3")
        et.give_order(ob_et, "date -s %s" % t2t(t))
        return "人脸速通门(206.10.25.3)"

    def cent_():
        """
        修改考勤服务时间
        :return:
        """
        cent = ServerSetCentOS()
        cent.run_change_time(t)
        cent.run_restart_server()
        return "考勤服务器"

    def for_while(target_device, ts=3):
        """
        循环调用一个程序，直至成功或超过尝试次数ts
        :param target_device: 目标程序
        :param ts: 尝试次数
        :return:
        """
        while True:
            if ts == 0:
                break
            try:
                device = target_device
                print("修改%s时间为：%s" % (device, t))
                break
            except Exception as e:
                print("没有修改成功： %s" % t)
                print(e)
                ts -= 1
                for_while(target_device, ts=ts)
                print("retry:%d times" % ts)

    for t in time_list:
        flag = input("是否修改时间为：%s"
                     "\n【按任意键+回车取消】" % t)
        if flag:
            break
        for_while(vms_(), 3)
        for_while(face_1(), 3)
        for_while(face_2(), 3)
        for_while(cent_(), 3)


def set_time_while(keys: list, cfgs):
    """
    根据用例设置服务器、一体机、人脸速通门的时间，配合测试
    :param keys: 配置项列表
    :param cfgs: 各配置项选项字典迭代器
    :return: None
    """

    def effective(date):
        """
        在每条用例执行修改生效以后，对服务器进行过12点并重启
        :param date:需要生成数据的考勤日期
        :return:None
        """
        date_list = date.split(" ")[0].split("-")
        date_list[2] = str(int(date_list[2]) + 1)
        sc = ServerSetCentOS()
        sc.run_change_time("%s-%s-%s 11:59:55" % (date_list[0], date_list[1], date_list[2]))
        print("Waiting...")
        time.sleep(10)
        sc.run_restart_server()

    for o in cfgs:
        for k in keys:
            # 展示用例配置信息
            case = o[k].replace("/", "-")
            print("%s为: %s" % (k, case))

        for k in keys:
            case = o[k].replace("/", "-")
            if "用例" in k:
                print("-" * 88)
                time.sleep(0.38)

            # 修改为上下班时间进行打卡
            if "上班" in k or "下班" in k:
                flag_1 = input("是否将服务器时间修改为%s: %s" % (k, case))
                flag_2 = input("请再次确认")
                print("+" * 88)
                if not flag_1 and not flag_2:
                    change_all_time(case)
            # 生效当日数据
            if "生效" in k and case:
                effective(case)


if __name__ == '__main__':
    # 修改所有设备时间，要求联通并打开对应设备的Telnet
    change_all_time()
    # 自动升级考勤服务，要求，安装包上传至服务器，并尽量删除老版本服务
    # run_updateCentOS_server()
    # 循环修改设定好时间
    # cfg = GetConfig()
    # (key, config_list) = cfg.open_file()
    # set_time_while(key, config_list)
