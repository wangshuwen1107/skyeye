
class CallerInfo:
    #调用者的类名
    caller_class = ''
    #调用者的方法
    caller_method = ''
    #目标扫描类名
    target_class = ''
    #目标扫描方法
    target_method = ''
    #目标扫描的成员变量
    target_ref_filed = ''
    #执行的行数
    invoke_num = ''

    def __init__(self, caller_class="", caller_method="", target_class="",target_method="", invoke_num="",target_ref_filed = ""):
        self.caller_class = caller_class
        self.caller_method = caller_method
        self.target_class = target_class
        self.target_method = target_method
        self.invoke_num = invoke_num
        self.target_ref_filed = target_ref_filed
    
    def toResultJsonMap(self):
        jsoMap = {}
        jsoMap['caller_class'] = self.caller_class
        jsoMap['caller_method'] = self.caller_method
        jsoMap['invoke_num'] = self.invoke_num
        return jsoMap
    