# coding=UTF-8
import copy
from skyeye.dto import *

import re

class InvokeLineParser:

    @classmethod
    def upperFirstChar(cls,str)->str:
        return str[0:1].upper()+ str[1:]
        
    @classmethod
    def matchMethodBlock(cls,matcherCallerInfo:CallerInfo,line:str,scan_strategy_list=[ScanVO])->CallerInfo:
        if None == matcherCallerInfo:
            return None
        lineStrip = line.strip()
        if(lineStrip.startswith('invoke')):
            return InvokeLineParser.matchInvoekLine(matcherCallerInfo,lineStrip,scan_strategy_list)
        if(lineStrip.startswith('iget-object') or lineStrip.startswith('sget-object')):
            return InvokeLineParser.matchFiled(matcherCallerInfo,lineStrip,scan_strategy_list)
        else:
            return  None

    #解析 静态变量引用(sget-object) 变量引用(iget-object)
    @classmethod
    def matchFiled(cls,matcherCallerInfo:CallerInfo,lineStrip,scan_strategy_list=[ScanVO])->CallerInfo:
        # sget-object v1, Lcn/cheney/picker/app/Test;->staticString:Ljava/lang/String;
        classMatch = re.compile(r",{1}\s\S+;->{1}").search(lineStrip)
        if not classMatch:
            return None
        tempClassStr = classMatch.group()
        getClass = tempClassStr[3:len(tempClassStr)-3].replace('/','.')

        filedMatch = re.compile(r"->{1}[\s\S]+:{1}").search(lineStrip)
        if not filedMatch:
            return None
        tempFiledStr = filedMatch.group()
        getFiled = tempFiledStr[2:len(tempFiledStr)-1].replace('/','.')
        for strategy in scan_strategy_list:
            targetClass = strategy.class_name
            targetFiled = strategy.filed_name
            if(targetClass in getClass and matcherCallerInfo.caller_class not in getClass):
                if(targetFiled == None or len(targetFiled) == 0):
                    matcherCallerInfo.target_class = getClass
                    matcherCallerInfo.target_ref_filed = getFiled
                    return copy.copy(matcherCallerInfo)
                else:
                    if getFiled in targetFiled and getClass in targetClass:
                         matcherCallerInfo.target_class = getClass
                         matcherCallerInfo.target_ref_filed = getFiled
                         return copy.copy(matcherCallerInfo)   
            else:
                return None
                
    
    #解析invoke里面的调用
    @classmethod
    def matchInvoekLine(cls,matcherCallerInfo:CallerInfo,lineStrip,scan_strategy_list=[])->CallerInfo:
        # invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;
        # 解析完成之后 invokeClass = java.lang.Runtime
        classMatch = re.compile(r"},{1}\s\S+;->{1}").search(lineStrip)
        if not classMatch:
            return None
        tempClassStr = classMatch.group()
        invokeClass = tempClassStr[4:len(tempClassStr)-3].replace('/','.')
        methodMatch = re.compile(r"->{1}[\s\S]+").search(lineStrip)
        if not methodMatch:
            return None
        #invokeMethod = getRuntime()Ljava.lang.Runtime
        invokeMethod = methodMatch.group()[2:].replace('/','.')
        #invokeMethodName = getRuntime
        invokeMethodName =invokeMethod[0:invokeMethod.index('(')] 
        # print ("matchInvokeLine invokeClass="+invokeClass+" invokeMethod="+invokeMethod)
        for strategy in scan_strategy_list:
            targetClass = strategy.class_name
            targetMethod = strategy.method_name
            targetFiled = strategy.filed_name
            
            # 执行方法的类包含扫描的类&& 不包括自生的调用
            if(targetClass in invokeClass and matcherCallerInfo.caller_class not in invokeClass):
                # 匹配所有调用到目标类的invoke line
                if(targetMethod == None or len(targetMethod) == 0):
                    if (targetFiled == None or len(targetFiled) == 0):
                        matcherCallerInfo.target_class = targetClass
                        matcherCallerInfo.target_method = invokeMethod
                        return copy.copy(matcherCallerInfo)
                    else:
                        # 初始字段的set和get方法
                        unperFirstCharFiled = InvokeLineParser.upperFirstChar(targetFiled)
                        targetFiledToSetFunc = 'set'+unperFirstCharFiled
                        targetFiledToGetFunc = 'get'+unperFirstCharFiled
                        if(targetFiledToSetFunc == invokeMethodName or targetFiledToGetFunc == invokeMethodName):
                            matcherCallerInfo.target_class = targetClass
                            matcherCallerInfo.target_ref_filed = targetFiled
                            return copy.copy(matcherCallerInfo)
                # 匹配调用到目标类和目标方法的invoke line
                elif(targetMethod == invokeMethodName):
                    matcherCallerInfo.target_class = targetClass
                    matcherCallerInfo.target_method = targetMethod
                    return copy.copy(matcherCallerInfo)
        return None
