# coding=UTF-8
import requests
from distutils.version import StrictVersion
from skyeye.config import VERSION

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
        versions = sorted(list(releases.keys()), key=StrictVersion, reverse=True)
    except:
        pass
    if(versions and len(versions)>0):
        hasNewVersion = StrictVersion(versions[0]) > StrictVersion(VERSION)
        if hasNewVersion:
           print('🔥🔥🔥 版本升级提示，最新版本：'+versions[0]+" \n🔥🔥🔥请用该命令升级： pip3 install --upgrade skyeye")
