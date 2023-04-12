# coding=UTF-8
from operator import methodcaller
from skyeye.dto import *
from skyeye.result_wirter import ResultWirter
from .method_block_parser import InvokeLineParser
from skyeye.utils import *


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
                copyCallerInfo = InvokeLineParser.matchMethodBlock(matcherCallerInfo,line,scan_strategy_list)
                if(copyCallerInfo):
                    SmaliParser.toStringScanInfo(copyCallerInfo)
                    # 情况扫描信息
                    matcherCallerInfo.target_class = None
                    matcherCallerInfo.target_method = None
                    matcherCallerInfo.target_ref_filed = None
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
        callerInfo.caller_class = className
        callerInfo.caller_method = methodDsec.strip()
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
        if not isEmpty(copyCallerInfo.target_method):
            resultLine ='行数={e} {a}:{b} 调用: {c}:{d}'.format(a=copyCallerInfo.caller_class,
                                b=copyCallerInfo.caller_method,
                                c=copyCallerInfo.target_class,
                                d=copyCallerInfo.target_method,
                                e=copyCallerInfo.invoke_num)
        else:
            resultLine ='行数={e} {a}:{b} 调用: {c}.{d}'.format(a=copyCallerInfo.caller_class,
                    b=copyCallerInfo.caller_method,
                    c=copyCallerInfo.target_class,
                    d=copyCallerInfo.target_ref_filed,
                    e=copyCallerInfo.invoke_num) 
        # print("😄😄😄扫描到了"+resultLine)
        
        
  
        