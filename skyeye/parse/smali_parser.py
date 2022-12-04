# coding=UTF-8
from skyeye.dto import *
from skyeye.result_wirter import ResultWirter
from .invokeline_parser import InvokeLineParser

class SmaliParser:

    #扫描单个类文件
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
            # 解析调用类
            if(line.startswith('.class')):
                className = line[line.index('L')+1:line.index(";")].replace("/",".")
                continue
            # 解析调用方法
            if(line.startswith('.method')):
                 matcherCallerInfo = SmaliParser.parseCallMehtodInfo(line,className)
                 methodBlock = True
                 continue
             
            if(methodBlock):
                if(line.strip().startswith('.line')):
                    matcherCallerInfo.invoke_num = SmaliParser.parseInvokeNum(line)
                    continue
                    
                # 扫描调用方法里面 执行的方法  1.执行的方法 2.成员变量赋值的方法
                copyCallerInfo = InvokeLineParser.matchInvokeLine(matcherCallerInfo,line,scan_strategy_list)
                # TODO 匹配调用方法里面 变量，枚举，引用的常量
                
                if(copyCallerInfo):
                    SmaliParser.toStringScanInfo(copyCallerInfo)
                    matcherCallerInfo.invoke_class = None
                    matcherCallerInfo.invoke_func = None
                    matcherCallerInfo.invoke_num = None
                    ResultWirter.shared().addResultDto(copyCallerInfo)
            # 解析调用方法结束
            if(line.startswith('.end method')):
                methodBlock = False
                matcherCallerInfo = None
        smaliFile.close()
        # print("扫描类 "+className)
        

    #调用者函数
    @classmethod
    def parseCallMehtodInfo(cls,startMethodLine='',className='')->CallerInfo:
        callerInfo = CallerInfo()
        calllMehotdInfoList = startMethodLine.split(' ')
        methodDsec = ''
        for index,item in enumerate(calllMehotdInfoList):
            if(index != 0):
                methodDsec += " "+item.strip().replace("/",".")
        callerInfo.class_name = className
        callerInfo.method_name = methodDsec.strip()
        return callerInfo


    #调用者执行的行数
    @classmethod
    def parseInvokeNum(cls,line:str)->str:
        lineStrip = line.strip()
        lineNumStr = lineStrip[5:]
        return lineNumStr


    @classmethod
    def toStringScanInfo(cls,copyCallerInfo:CallerInfo)->str:
        resultLine = ''
        if len(copyCallerInfo.invoke_func) > 0:
            resultLine ='行数={e} {a}:{b} 调用: {c}:{d}'.format(a=copyCallerInfo.class_name,
                                b=copyCallerInfo.method_name,
                                c=copyCallerInfo.invoke_class,
                                d=copyCallerInfo.invoke_func,
                                e=copyCallerInfo.invoke_num)
        else:
            resultLine ='行数={e} {a}:{b} 调用: {c}.{d}'.format(a=copyCallerInfo.class_name,
                    b=copyCallerInfo.method_name,
                    c=copyCallerInfo.invoke_class,
                    d=copyCallerInfo.ref_filed,
                    e=copyCallerInfo.invoke_num) 
        print("😄😄😄扫描到了"+resultLine)
        
        
        
        