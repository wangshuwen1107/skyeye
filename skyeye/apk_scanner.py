# coding=UTF-8
import os
import sys
from turtle import st
import zipfile
import time
import shutil
from skyeye.config_center import ConfigCenter
from skyeye.result_wirter import ResultWirter
from skyeye.smali_parser import SmaliParser

def startScan(apkPath,configYamlPath,resultDir):
    # 初始化配置
    ConfigCenter.initialize(configYamlPath)
    # 获取扫描规则 
    if(len(ConfigCenter.scan_config)==0):
        print("请配置扫描策略")
        return
    ResultWirter.initialize()
    # 清除之前可能遗留的临时文件
    delAllTempFiles()
    dexList = getDexFileList(apkPath)
    toSmail(dexList)
    if  not scanSmalis(ConfigCenter.scan_config) :
        delAllTempFiles()
        return
    resultJsonFilePath = ResultWirter.shared().wirte(resultDir)
    print("✅ 扫描结果: "+resultJsonFilePath)
    delAllTempFiles()

    
def scanSmalis(scan_strategy_list):
    print("🚀 开始扫描,过程大概持续2分钟...")
    startTime = int(time.time())
    outputSmaliDirPath = os.path.join(os.getcwd(),'out/smali')
    if not os.path.isdir(outputSmaliDirPath):
        print("目标smali文件夹="+outputSmaliDirPath+"为空，结束扫描❌")
        return False
    walk = os.walk(outputSmaliDirPath)
    for path,dir_list,file_list in walk:
        for file_name in file_list:
            SmaliParser.scanSingleSmali(os.path.join(path,file_name),scan_strategy_list)
    scanTime = int(time.time()) - startTime
    print("✅ 扫描耗时"+str(scanTime)+"s")
    return True
           
#  将dex转换成smail           
def toSmail(dexList):
    startTime = int(time.time())
    print("🚀 换成smali,过程大概持续2分钟...")
    current_file_dir = os.path.dirname(__file__)
    outputSmaliDirPath = os.path.join(os.getcwd(),'out/smali')
    if os.path.isdir(outputSmaliDirPath) == True:
       shutil.rmtree(outputSmaliDirPath)
    for dexPath in dexList:
        baksmilJarPath=  os.path.join(current_file_dir,'config/baksmali-2.5.2.jar')
        # baksmilJarPath= os.path.abspath('/config/baksmali-2.5.2.jar')
        command = "java -jar "+ baksmilJarPath+" d "+dexPath+" -o "+outputSmaliDirPath
        toSmailResult = os.popen(command).readlines()
        # print("换成smali----toSmailResult="+str(toSmailResult))
    toSmailTime = int(time.time()) - startTime
    print("✅ 换成smali成功 耗时"+str(toSmailTime)+"s")

# 提取APK中的dex文件
def getDexFileList(apkPath):
    realApkPath = os.path.join(os.getcwd(),apkPath)
    outputDexDirPath = os.path.join(os.getcwd(),"out/dex")
    apkFile = zipfile.ZipFile(realApkPath,"r")
    dexFileList = []
    
    if os.path.exists(outputDexDirPath):
       shutil.rmtree(outputDexDirPath)
    if os.path.isdir(outputDexDirPath) == False:
       os.makedirs(outputDexDirPath)

    for tempFile in apkFile.namelist():
        if tempFile.endswith(".dex"):
            dexFilePath = os.path.join(outputDexDirPath,tempFile)
            dexfile = open(dexFilePath,'wb+')
            dexfile.write(apkFile.read(tempFile))
            dexFileList.append(dexFilePath)
            dexfile.close()
        
    return dexFileList

def delAllTempFiles():
    startTime = int(time.time())
    outputDirPath = os.path.join(os.getcwd(),"out")
    if os.path.exists(outputDirPath):
       print("🚀 删除临时文件夹"+outputDirPath+" ...")
       shutil.rmtree(outputDirPath)
       delDirTimes = int(time.time()) - startTime
       print("✅ 删除临时文件夹"+str(delDirTimes)+"s")
  
