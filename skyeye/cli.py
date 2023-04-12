# coding=UTF-8
import argparse
from skyeye.apk_scanner import startScan
from skyeye.apk_decompiling import decompiling
from skyeye.apk_decompiling import openGUI
from skyeye.config import VERSION
from skyeye.version_check import checkVersions

def version():
    return "version:"+VERSION


def scan(args):
    inputApkPath = args.input
    configYamlPath = args.config
    outputResultDirPath = args.output
    startScan(inputApkPath,configYamlPath,outputResultDirPath)

def dec(args):
    inputApkPath = args.input
    outputDir = args.output
    decompiling(inputApkPath,outputDir)
    

def openJDGUI(args):
    openGUI(args.input)

def run():
    parser = argparse.ArgumentParser(prog="skyeye")

    parser.add_argument("-v","--version", help=u"查看版本号",action="store_true")
    
    subparsers = parser.add_subparsers(title='客户端工具')
    
    scan_parser = subparsers.add_parser('scan',help="扫描APK中指定类方法引用")
    scan_parser.add_argument("-i","--input", type=str, help="输入扫描的APK路径",metavar="")
    scan_parser.add_argument("-c","--config", type=str, help="扫描配置yaml文件路径",metavar="")
    scan_parser.add_argument("-o","--output", type=str,nargs='?', help="输出结果的文件夹路径",metavar="")
    scan_parser.set_defaults(func=scan)
    
    decompiling_parser = subparsers.add_parser('dec',help="反编译APK")
    decompiling_parser.add_argument("-i","--input", type=str, help="目标APK路径",metavar="")
    decompiling_parser.add_argument("-o","--output", type=str,nargs='?', help="输出结果的文件夹路径",metavar="")
    decompiling_parser.set_defaults(func=dec)
    
    class_gui_parser = subparsers.add_parser('jd',help="打开JD-GUI工具")
    class_gui_parser.add_argument("-i","--input", type=str, help="目标class文件路径 或者 class文件夹路径",metavar="")
    class_gui_parser.set_defaults(func=openJDGUI)
    
    args = parser.parse_args()
    # print("args="+str(args))

    if hasattr(args, "func"):
        args.func(args)
        return
    if args.version:
        checkVersions()
        print(version())
        return
    parser.print_help()
       
       
       
if __name__ == '__main__':
    run()