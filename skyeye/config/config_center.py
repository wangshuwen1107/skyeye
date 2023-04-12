# coding=UTF-8
import yaml
from skyeye.dto import *
import os

# 配置中心
class ConfigCenter:
    
    scan_config = []

    @classmethod
    def initialize(cls,configFilePath):
        ConfigCenter.shared().parseConfig(configFilePath)

    @classmethod
    def shared(cls):
        if not hasattr(ConfigCenter, "_instance"):
            ConfigCenter._instance = ConfigCenter()
        return ConfigCenter._instance

    def __init__(self):
        pass

    def parseConfig(self,configFilePath):
        realPath = os.path.join(os.getcwd(),configFilePath)
        f=open(realPath, 'r', encoding='utf-8')
        config_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        for strategy in config_data:
            scanVo = ScanVO.from_json(strategy)
            self.scan_config.append(scanVo)