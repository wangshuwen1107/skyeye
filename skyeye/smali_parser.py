# coding=UTF-8
from turtle import st
from skyeye.dto import *
import re
from skyeye.result_wirter import ResultWirter

class SmaliParser:

    @classmethod
    def scanSingleSmali(cls,smaliFilePath='',scan_strategy_list=[]): 
        if(smaliFilePath.endswith(".smali") == False):
            return
        smaliFile = open(smaliFilePath)
        lines = smaliFile.readlines() 
  
        className = ""
        methodBlock = False
        matcherCallerInfo:CallerInfo = None
        for line in lines:
            if(line.startswith('.class')):
                className = line[line.index('L')+1:line.index(";")].replace("/",".")
            
            # 解析调用方法
            if(line.startswith('.method') | methodBlock):
                if(line.startswith('.method')):
                    matcherCallerInfo = SmaliParser.parseCallMehtodInfo(line,className)
                    methodBlock = True
                 # 解析调用方法执行的函数
                if(SmaliParser.matchInvokeLine(matcherCallerInfo,line,scan_strategy_list)):
                    resultLine ='{a}:{b} 调用: {c}:{d}'.format(a=matcherCallerInfo.class_name,
                                                  b=matcherCallerInfo.method_name,
                                                  c = matcherCallerInfo.invoke_class,
                                                  d=matcherCallerInfo.invoke_func)
                    ResultWirter.shared().addResultDto(matcherCallerInfo)
                    # print("扫描到了"+resultLine)
            # 解析调用方法结束
            if(line.startswith('.end method')):
                methodBlock = False
                matcherCallerInfo = None
        smaliFile.close()
        # print("扫描类 "+className)
       
 
    @classmethod
    def parseCallMehtodInfo(cls,startMethodLine='',className=''):
        callerInfo = CallerInfo()
        calllMehotdInfoList = startMethodLine.split(' ')
        methodDsec = ''
        for index,item in enumerate(calllMehotdInfoList):
            if(index != 0):
                methodDsec += " "+item.strip().replace("/",".")
        callerInfo.class_name = className
        callerInfo.method_name = methodDsec.strip()
        return callerInfo

    @classmethod
    def matchInvokeLine(cls,matcherCallerInfo:CallerInfo,line:str,scan_strategy_list=[]):
        lineStrip = line.strip()
        if(not lineStrip.startswith('invoke')):
            return False
        # invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;
        # 解析完成之后 invokeClass = java.lang.Runtime
        classMatch = re.compile(r"},{1}\s\S+;->{1}").search(lineStrip)
        if not classMatch:
            return
        tempClassStr = classMatch.group()
        invokeClass = tempClassStr[4:len(tempClassStr)-3].replace('/','.')
        #解析完成之后 invokeMethod = getRuntime()
        methodMatch = re.compile(r"->{1}[\s\S]+").search(lineStrip)
        if not methodMatch:
            return
        invokeMethod = methodMatch.group()[2:].replace('/','.')
        # print ("matchInvokeLine invokeClass="+invokeClass+" invokeMethod="+invokeMethod)
        for strategy in scan_strategy_list:
            targetClass = strategy.class_name
            targetMethod = strategy.method_name
            # 执行方法的类包含扫描的类&& 不包括自生的调用
            if(targetClass in invokeClass and matcherCallerInfo.class_name not in invokeClass):
                # 匹配所有调用到目标类的invoke line
                if(len(targetMethod) == 0):
                    matcherCallerInfo.invoke_class = targetClass
                    matcherCallerInfo.invoke_func = invokeMethod
                    return True
                # 匹配调用到目标类和目标方法的invoke line
                if(targetMethod in invokeMethod):
                    matcherCallerInfo.invoke_class = targetClass
                    matcherCallerInfo.invoke_func = targetMethod
                    return True
        return False
        
        
        