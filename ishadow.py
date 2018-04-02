import requests
from bs4 import BeautifulSoup
import json
import base64

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}


# baidu 获取百度搜索ishadow的第一个结果（因为ishadow经常变网址来着）
web = requests.get(
    r"https://www.baidu.com/s?ie=UTF-8&wd=ishadow", headers=headers)
soup = BeautifulSoup(web.text, "lxml")
ishadow_url = soup.find(name="h3").find(name="a").attrs["href"]
print("iShadow的地址是：%s" % ishadow_url)


# 用于保存服务器配置
configs = []

class config:
    remarks = ""
    server = ""
    serverport = 0
    password = ""
    method = ""
    protocol = "origin"
    obfs = "plain"


# 从iShadow获取服务器配置
# ishadow_url = "https://get.ishadowx.net/"
# ishadow_url = "isx.yt"
# ishadow_url = "isx.tn"
web = requests.get(ishadow_url, headers=headers)
soup = BeautifulSoup(web.text, "lxml")
ss_list = soup.find(name="div", attrs={"class": "portfolio-items"}).findAll(
    name="div", attrs={"class": "portfolio-item"})  # 找到ss配置列表
i = 1

for ss_item in ss_list:
    ss_infos = ss_item.findAll(name="span")
    ss_method = ss_item.findAll(name="h4")[3]
    ssr_info = ss_item.findAll(name="h4")[4]
    print("----------Number %d----------" % i)
    _config = config()
    
    _config.remarks=ss_infos[0].string.replace("\n", "")
    _config.server = ss_infos[0].string.replace("\n", "")
    print(_config.server)

    _config.serverport = int(ss_infos[2].string.replace("\n", ""))
    print(_config.serverport)
    
    _config.password = ss_infos[4].string.replace("\n", "")
    print(_config.password)
    
    _config.method = ss_method.string[7:]
    print(_config.method)

    if ssr_info.find(name="a") == None:
        _config.protocol,_config.obfs = ssr_info.string.split(" ")
        _config.remarks += " SSR"
        print(_config.protocol)
        print(_config.obfs)

    configs.append(_config)
    i += 1


# 修改SSR配置文件
config_file_path = r"D:\Program Files (x86)\ssr-win\gui-config.json"    # SSR配置文件的地址

config_file = open(config_file_path, "r")
config_obj = json.load(config_file)  # 读取原先的配置内容
config_file.close()

config_obj["configs"]=[]    # 清空服务器列表
for item in configs:
    config_item = {
        "remarks": item.remarks,
        "id": "",
        "server": item.server,
        "server_port": item.serverport,
        "server_udp_port": 0,
        "password": item.password,
        "method": item.method,
        "protocol": item.protocol,
        "protocolparam": "",
        "obfs": item.obfs,
        "obfsparam": "",
        "remarks_base64": bytes.decode(base64.b64encode(item.remarks.encode('utf-8'))), # 将remarks转换为base64编码，不然应用里面无法显示备注
        "group": "",
        "enable": True,
        "udp_over_tcp": False
    }
    config_obj["configs"].append(config_item)   # 写入新的服务器信息

config_file = open(config_file_path, "w")
json.dump(config_obj, config_file)   # 将修改后的配置内容覆盖写入源文件
config_file.close()

print("Done!")
