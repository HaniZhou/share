import psutil
import configparser
import socket
import time
import threading
import json


def getConfig() -> dict:
    """to get the serve config file and to check the config is right"""
    config = dict()  # 存储读取的配置信息
    int_tuple = ("port",)  # 配置的值必须为int类型的键
    str_tuple = ("destination_ip",)  # 配置的值必须为str类型的键
    float_tuple = ("send_info_interval",)  # 配置的值必须为float类型的键
    conf = configparser.ConfigParser()
    try:
        # 读取配置信息，并且进行类型转换
        conf.read('./serve.conf', encoding="UTF-8")
        for (key) in int_tuple:
            config[key] = int(conf.get("main", key))
        for (key) in float_tuple:
            config[key] = float(conf.get("main", key))
        for (key) in str_tuple:
            config[key] = conf.get("main", key)
    except ValueError:
        print("A worry type in the config file!")
        exit(-1)
    except FileNotFoundError:
        print("there aren't the config file")
        exit(-1)
    except Exception as e:
        print("You are missing some configuration!")
        exit(-1)
    return config


def connectServe():
    """测试和连接服务器,并且发送数据"""
    tcp_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    while True:
        try:
            tcp_sock.connect((config["destination_ip"], config["port"]))
            while True:
                time.sleep(config["send_info_interval"])
                if data:
                    try:
                        json_data = json.dumps(data.pop(0))
                        # request = "POST / HTTP/1.1\r\nHost: {}\r\nContent-Type: application/json\r\nContent-Length: {}\r\n\r\n{}".format(
                        #     config["destination_ip"], len(json_data), json_data)
                        tcp_sock.sendall(json_data.encode("UTF-8"))
                    except Exception as e:
                        print("Send failed: {}".format(e))
        except Exception as e:
            print("can't connect to serve: {} :{} [{}]".format(config["destination_ip"], config["port"], e))


def getSystemInfo():
    """获取系统的信息，并且将信息压入data[]中"""
    disk = psutil.disk_usage('/')
    memory = psutil.virtual_memory()
    operation = 1024 ** 3
    while True:
        processes = psutil.process_iter()
        d = {"CPU": {}, "memory": {}, "disk": {}, "processes": []}
        d["CPU"]["cpu_percent"] = psutil.cpu_percent(interval=config["send_info_interval"])  # 与发送时间同步更新
        d["memory"] = {"memory_total": round(memory.total / operation, 2),
                       "memory_used": round(memory.used / operation, 2),
                       "memory_percent": memory.percent}
        d["disk"] = {"disk_total": round(disk.total / operation, 2), "disk_used": round(disk.used / operation, 2),
                     "disk_percent": disk.percent}
        for process in processes:
            d["processes"].append({"pid": process.pid, "name": process.name(), "status": process.status()})
        data.append(d)


if __name__ == "__main__":
    data = []
    config = getConfig()
    threading.Thread(target=getSystemInfo, daemon=True).start()
    # while True:
    #     if data:
    #         print(data.pop(0))
    connectServe()
