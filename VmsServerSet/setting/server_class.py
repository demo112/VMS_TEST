import time
import paramiko
import telnetlib


def make_time():
    pass


class ServerSetCentOS:
    def __init__(self):
        self.hostname = '206.10.0.206'
        self.port = 22
        self.username = 'root'
        self.password = '123456'

    def give_order(self, order, showback=True):
        """
        输入命令文本
        :param showback: 是否将返回值及报错打印出来
        :param order: 需要执行的命令
        :return: 响应的内容
        """
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(order)
        # response_data = stdout.read().decode("utf-8")
        try:
            response_data = stdout.read().decode("utf-8")
        except Exception as e:
            print(e)
            response_data = None
        if response_data and showback:
            print(response_data)
        if stderr and showback:
            # print(stderr.read().decode("utf-8"))
            print(stderr.read().decode("utf-8"))
        time.sleep(0.2)
        # 获取命令结果
        #     result = stdout.read()
        # 关闭连接
        ssh.close()
        return response_data

    def get_init(self):
        pass

    def run_change_time(self, change_to):
        date_time = 'timedatectl set-time "%s"' % change_to
        self.give_order(date_time)
        self.give_order("date")

    def run_restart_server(self):
        restart = "./AttendanceSys/server.sh" + " restart"
        self.give_order(restart)


class ServerSetVMS:
    """
    示例：
    HOST = "localhost"
    user = input("Enter your remote account: ")
    password = getpass.getpass()

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"login: ")
    tn.write(user.encode('uff-8') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('uff-8') + b"\n")

    tn.write(b"ls\n")
    tn.write(b"exit\n")

    print(tn.read_all().decode('uff-8'))
    """

    def __init__(self):
        self.username = 'root'
        self.password = '123456'

    def give_order(self, object, order):
        print(object.read_until("#".encode("ascii"), timeout=2))
        object.write(order.encode("ascii") + "\r\n".encode("ascii"))
        print(object.read_until("Build date".encode("ascii"), timeout=2).decode("ascii"))
        print(object.close())

    def login(self, host: str):
        ob_ = telnetlib.Telnet(host)
        ob_.read_until("login:".encode("ascii"), timeout=2).decode("ascii")
        # print(object.write("root\r\n".encode("ascii")))
        ob_.write(self.username.encode("ascii") + "\r\n".encode("ascii"))
        ob_.read_until("Password:".encode("ascii"), timeout=2).decode("ascii")
        ob_.write(self.password.encode("ascii") + "\r\n".encode("ascii"))
        return ob_


if __name__ == '__main__':
    pass
