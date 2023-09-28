# coding=UTF-8
import copy
from skyeye.dto import *
from .class_context_center import ClassContextCenter
import re
from skyeye.utils import *

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
    #构造方法里面有对 变量or静态变量 赋值 这里匹配的是构造方法or普通方法里面get的值
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
            targetMethod = strategy.method_name
        
            getClassContext = ClassContextCenter.shared().getClassContext(getClass)
            # InvokeLineParser.printClassContextLined(getClassContext)              
            cur = getClassContext
            while(cur):
                curGetClass = cur.class_name
                if(targetClass in curGetClass and matcherCallerInfo.caller_class not in curGetClass):
                    # 匹配构造方法里面所有get目标类所有的成员变量
                    if(isEmpty(targetFiled) and isEmpty(targetMethod)):
                        matcherCallerInfo.target_class = targetClass
                        matcherCallerInfo.target_ref_filed = getFiled
                        return copy.copy(matcherCallerInfo)
                    elif(not isEmpty(targetFiled)):
                        # 匹配指定类和字段 需要将自己的父类对应的字段也匹配一遍
                        if getFiled in targetFiled and curGetClass in targetClass:
                            matcherCallerInfo.target_class = targetClass
                            matcherCallerInfo.target_ref_filed = getFiled
                            return copy.copy(matcherCallerInfo)   
                cur = cur.parent
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
        # 寻找superClass链
        invokeClassContext = ClassContextCenter.shared().getClassContext(invokeClass)
        # InvokeLineParser.printClassContextLined(invokeClassContext)
        
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
            currentInvokeClassHead= invokeClassContext
            while(currentInvokeClassHead):
                currentInvokeClass = currentInvokeClassHead.class_name
                # 执行方法的类包含扫描的类&& 不包括自生的调用
                if(targetClass in currentInvokeClass and matcherCallerInfo.caller_class not in currentInvokeClass):
                    # 匹配所有调用到目标类的invoke line
                    if(isEmpty(targetMethod)):
                        if (isEmpty(targetFiled)):
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
                currentInvokeClassHead = currentInvokeClassHead.parent

        return None
    
    @classmethod
    def printClassContextLined(cls,classContext:ClassContext):
        currentInvokeClassHead = classContext
        classContextStr = ''
        while(currentInvokeClassHead):
             classContextStr += currentInvokeClassHead.class_name + "->"
             currentInvokeClassHead = currentInvokeClassHead.parent
        print(classContextStr[0:len(classContextStr)-2])