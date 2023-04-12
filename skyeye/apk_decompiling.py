import os
import zipfile
import shutil
import subprocess
from skyeye.utils import *

def decompiling(apkPath:str,resultDir):
    if not os.path.exists(apkPath):
        print("❌apk文件不存在:"+apkPath)
        return
    if not zipfile.is_zipfile(apkPath):
        print("❌apk文件类型错误:"+apkPath)
        return   
    #将APK 改为zip 解压到resultDir目录
    realApkPath = os.path.join(os.getcwd(),apkPath)
    apkFile = zipfile.ZipFile(realApkPath,"r")
    #将APK的绝对路径去除.apk
    (_,apkPathWithoutExt) = os.path.split(apkPath)
    apkPathWithoutExt = apkPathWithoutExt.replace(".apk","")
    outputDirPath = os.path.join(os.getcwd(),apkPathWithoutExt)
    if resultDir:
       outputDirPath = os.path.join(os.getcwd(),resultDir,apkPathWithoutExt) 
    #clear历史文件夹
    delFiles(outputDirPath)
    print("🚀正在解压->"+outputDirPath)
    apkFile.extractall(outputDirPath)
    #获取dex文件
    for filePath in os.listdir(outputDirPath):
        if filePath.endswith(".dex"):
            dexFilePath = os.path.join(outputDirPath,filePath)
            #将dex->jar
            jarPath = dex2Jar(dexFilePath)
            #删除dex
            delFiles(dexFilePath)
            #解压jar
            unzipJar(jarPath,outputDirPath)
            #删除jar
            delFiles(jarPath)
    print("✅反编译目录->"+outputDirPath)
    openGUI(outputDirPath)
    
def openGUI(openDirOrFilePath):
    firstClassFilePath = ""
    if(isEmpty(openDirOrFilePath)):
        return
    if not os.path.exists(openDirOrFilePath):
        print("❌文件不存在") 
        return
    if os.path.isfile(openDirOrFilePath) and not openDirOrFilePath.endswith(".class"):
        print("❌文件不是.class") 
        return
    if os.path.isdir(openDirOrFilePath):
        walk = os.walk(openDirOrFilePath)
        for root,dir_list,file_list in walk:
            if root == openDirOrFilePath:
                continue
            for file_name in file_list:
                if file_name.endswith(".class") and  len(firstClassFilePath)==0:
                    firstClassFilePath = os.path.join(root,file_name)
    else:
        firstClassFilePath = openDirOrFilePath              
    current_file_dir = os.path.dirname(__file__)
    guiPath=  os.path.join(current_file_dir,'config/jd-gui-1.6.6.jar')
    command = None
    if(isEmpty(firstClassFilePath)):
        command ="java -jar "+guiPath
        print("✅正在打开JD-GUI") 
    else:
        print("✅正在打开JD-GUI firstClass->"+firstClassFilePath) 
        command ="java -jar "+guiPath+ " " +firstClassFilePath
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
def unzipJar(jarPath,outputDirPath):
    if not os.path.exists(jarPath) or not os.path.exists(outputDirPath):
        return
    jarFile = zipfile.ZipFile(jarPath,"r")
    jarFile.extractall(outputDirPath) 
          
def dex2Jar(dexPath):
    if not os.path.exists(dexPath):
        return ""
    (dexName,_) = os.path.splitext(dexPath)
    current_file_dir = os.path.dirname(__file__)
    dexDir = os.path.dirname(dexPath)
    jarPath = os.path.join(dexDir,dexName+".jar")
    dex2JarShPath=  os.path.join(current_file_dir,'config/dex-tools-2.1/d2j-dex2jar.sh')
    d2jInvokeShPath=  os.path.join(current_file_dir,'config/dex-tools-2.1/d2j_invoke.sh')
    command ="sudo chmod +x "+d2jInvokeShPath+"&& sh "+ dex2JarShPath+" "+dexPath+" -o "+jarPath+" --force"     
    commandResult = os.popen(command).readlines()      
    return jarPath
    
def delFiles(filePath):
    if os.path.exists(filePath):
       print("正在删除->"+filePath)
       if os.path.isdir(filePath):
           shutil.rmtree(filePath)
       else:
          os.remove(filePath)
