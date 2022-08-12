# coding=UTF-8
import os
from skyeye.dto import *
import json
class ResultWirter:
    
    callerInfoList = []
    
    callerResultMap = {}
    
    @classmethod
    def initialize(cls):
        ResultWirter.shared()

    @classmethod
    def shared(cls):
        if not hasattr(ResultWirter, "_instance"):
            ResultWirter._instance = ResultWirter()
        return ResultWirter._instance

    def __init__(self):
        if os.path.exists('out/result.txt'):
           os.remove('out/result.txt')

    
    def addResultDto(self,callerInfo):
        self.callerInfoList.append(callerInfo)
    
    def wirte(self,resultDir):
        self.groupCaller()
        jsonStr = json.dumps(self.callerResultMap,indent=4, ensure_ascii=False)
        realOutputPath = os.path.join(os.getcwd(),"result.json")
        if(resultDir):
            realOutputPath = os.path.join(os.getcwd(),resultDir,"result.json")
        with open(realOutputPath,"w+") as file:
             file.writelines(jsonStr)
        return realOutputPath   

    def groupCaller(self):
        for callerInfo in self.callerInfoList:
            key ='{a}:{b}'.format(a=callerInfo.invoke_class,
                                  b=callerInfo.invoke_func)
            callerList = self.callerResultMap.get(key)
            if callerList != None :
                callerList.append(CallerInfo.toResultJsonMap(callerInfo))
                continue
            callerList = []
            callerList.append(CallerInfo.toResultJsonMap(callerInfo))
            self.callerResultMap[key] = callerList