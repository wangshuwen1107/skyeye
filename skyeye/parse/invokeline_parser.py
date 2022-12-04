# coding=UTF-8
import copy
from skyeye.dto import *
import re

class InvokeLineParser:

    @classmethod
    def upperFirstChar(cls,str)->str:
        return str[0:1].upper()+ str[1:]
        
    @classmethod
    def matchInvokeLine(cls,matcherCallerInfo:CallerInfo,line:str,scan_strategy_list=[ScanVO])->CallerInfo:
        if None == matcherCallerInfo:
            return None
        lineStrip = line.strip()
        if(not lineStrip.startswith('invoke')):
            return None
        # invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;
        # 解析完成之后 invokeClass = java.lang.Runtime
        classMatch = re.compile(r"},{1}\s\S+;->{1}").search(lineStrip)
        if not classMatch:
            return None
        tempClassStr = classMatch.group()
        invokeClass = tempClassStr[4:len(tempClassStr)-3].replace('/','.')
        #解析完成之后 invokeMethod = getRuntime()
        methodMatch = re.compile(r"->{1}[\s\S]+").search(lineStrip)
        if not methodMatch:
            return None
        invokeMethod = methodMatch.group()[2:].replace('/','.')
        # print ("matchInvokeLine invokeClass="+invokeClass+" invokeMethod="+invokeMethod)
        for strategy in scan_strategy_list:
            targetClass:str = strategy.class_name
            targetMethod:str = strategy.method_name
            targetFiled:str = strategy.filed_name
            
            # 执行方法的类包含扫描的类&& 不包括自生的调用
            if(targetClass in invokeClass and matcherCallerInfo.class_name not in invokeClass):
                # 匹配所有调用到目标类的invoke line
                if(targetMethod == None or len(targetMethod) == 0):
                    if (targetFiled == None or len(targetFiled) == 0):
                        matcherCallerInfo.invoke_class = targetClass
                        matcherCallerInfo.invoke_func = invokeMethod
                        return copy.copy(matcherCallerInfo)
                    else:
                        # 初始字段的set和get方法
                        unperFirstCharFiled = InvokeLineParser.upperFirstChar(targetFiled)
                        targetFiledToSetFunc = 'set'+unperFirstCharFiled
                        targetFiledToGetFunc = 'get'+unperFirstCharFiled
                        if(targetFiledToSetFunc in invokeMethod or targetFiledToGetFunc in invokeMethod):
                            matcherCallerInfo.invoke_class = targetClass
                            matcherCallerInfo.ref_filed = targetFiled
                            return copy.copy(matcherCallerInfo)
                # 匹配调用到目标类和目标方法的invoke line
                elif(targetMethod in invokeMethod):
                    matcherCallerInfo.invoke_class = targetClass
                    matcherCallerInfo.invoke_func = targetMethod
                    return copy.copy(matcherCallerInfo)
        return None
    
