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


def change_all_time(time):
    """
    time-> 2008-08-08 08:08:08
    :param time:
    :return:
    """
    time_list = [
        time,
    ]

    def t2t(date_time):
        date_, time_ = date_time.split(" ")
        y, m, d = date_.split("-")
        date_time = y + "." + m + "." + d + "-" + time_
        return date_time

    for t in time_list:
        flag = input("是否修改时间为：%s"
                     "\n【按任意键+回车取消】" % t)
        print("")
        if flag:
            break
        try:
            vms = ServerSetVMS()
            ob_vms = vms.login('206.10.30.1')
            vms.give_order(ob_vms, "date '%s'" % t)
        except Exception as e:
            print("一体机没有修改成功： %s" % t)
            print(e)

        try:
            et = ServerSetVMS()
            ob_et = et.login("206.10.0.199")
            et.give_order(ob_et, "date -s %s" % t2t(t))
        except Exception as e:
            print("人脸速通门没有修改成功： %s" % t)
            print(e)

        try:
            cent = ServerSetCentOS()
            cent.run_change_time(t)
            cent.run_restart_server()
        except Exception as e:
            print("考勤服务没有修改成功： %s" % t)
            print(e)


def set_time_while(key: list, cfg):
    for o in cfg:
        for k in key:
            case = o[k].replace("/", "-")
            print("%s为: %s" % (k, case))
        for k in key:
            case = o[k].replace("/", "-")
            if "用例" in k:
                print("-" * 88)
            time.sleep(0.38)
            if "上班" in k or "下班" in k:
                flag_1 = input("是否将服务器时间修改为%s: %s" % (k, case))
                flag_2 = input("请再次确认")
                print("+" * 88)
                if not flag_1 and not flag_2:
                    # change_all_time(case)
                    pass




if __name__ == '__main__':
    # 修改所有设备时间，要求联通并打开对应设备的Telnet
    # change_all_time()
    # 自动升级考勤服务，要求，安装包上传至服务器，并尽量删除老版本服务
    # run_updateCentOS_server()
    # 循环修改设定好时间
    cfg = GetConfig()
    (a, b) = cfg.open_file()
    set_time_while(a, b)
