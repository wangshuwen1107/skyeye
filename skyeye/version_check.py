# coding=UTF-8
import requests
from skyeye.config import VERSION

def version_tuple(v):
    # 将版本号转换为可比较的元组 (处理简单数字版本)
    return tuple(map(int, (v.split('.') + ['0', '0', '0'])[:3]))

def checkVersions():
    url = "https://pypi.python.org/pypi/skyeye/json"
    versions = []
    try:
        data = requests.get(url).json()
        if(data == None):
            return
        releases = data["releases"]
        if(releases == None):
            return
        versions = sorted(list(releases.keys()), key=version_tuple, reverse=True)
    except:
        pass
    if(versions and len(versions)>0):
        hasNewVersion = version_tuple(versions[0]) > version_tuple(VERSION)
        if hasNewVersion:
           print('🔥🔥🔥 版本升级提示，最新版本：'+versions[0]+" \n🔥🔥🔥请用该命令升级： pip3 install --upgrade skyeye")
