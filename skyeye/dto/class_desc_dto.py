
class CallerInfo:
    #调用者的类名
    class_name = ''
    #调用者的方法
    method_name = ''
    #目标扫描类名
    invoke_class = ''
    #目标扫描方法
    invoke_func = ''
    #目标扫描的成员变量
    ref_filed = ''
    #执行的行数
    invoke_num = ''

    
    def __init__(self, class_name="", method_name="", invoke_class="",invoke_func="", invoke_num="",ref_filed = ""):
        self.class_name = class_name
        self.method_name = method_name
        self.invoke_class = invoke_class
        self.invoke_func = invoke_func
        self.ref_filed = ref_filed
        self.invoke_num = invoke_num
    
    def toResultJsonMap(self):
        jsoMap = {}
        jsoMap['class_name'] = self.class_name
        jsoMap['method_name'] = self.method_name
        jsoMap['invoke_num'] = self.invoke_num
        return jsoMap
    