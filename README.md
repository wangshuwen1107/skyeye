## APK扫描工具
skyeye是一款基于python3实现的扫描APK中代码引用的CLI工具

### 安装
#### python3环境安装
    brew install python3

#### skyeye安装
    pip3 install skyeye

#### pythonCli环境配置
-  zsh
在.zshrc中增加以下配置 export PATH="/Users/{yourHostName}/Library/Python/3.8/bin:$PATH"
- bash
在.bash_profile中增加以下配置 export PATH="/Users/{yourHostName}/Library/Python/3.8/bin:$PATH"


### 使用
#### 扫描APK中代码引用

1. 创建yaml文件,格式如下

```yaml
 - className: "com.xx.xx.yourClassName1"
   methodName: "yourMethodName1"
 - className: "com.xx.xx.yourClassName2"
   methodName: "yourMethodName2"
```
如果methodName不填写,会扫描className所有方法的外部的引用情况，目前仅支持：
- 扫描特定类的所有方法外部的引用
- 扫描特定类的特定方法的外部引用

2. 扫描

```bash
    skyeye scan
      -i , --input       输入扫描的APK路径
      -c , --config      扫描配置yaml文件路径
      -o , --output      输出结果的文件夹路径 【可选，默认运行文件夹路径】
```

3. 输出结果，格式如下
```json
{
    "com.test.Class:testMethod(Landroid.content.Context;)Ljava.lang.String;": [
        {
            "class_name": "com.test.CallerClassName",
            "method_name": "private final CallerFuncName()V"
        }   
    ]
}
```

#### 查看当前版本
```bash
skyeye -v 
输出版本同时，检查更新
```

### changeLog
####  3.0.1
- 增加PyYaml的依赖
####  3.0.0
- 扫描特定类的所有方法外部的引用
- 扫描特定类的特定方法的外部引用
