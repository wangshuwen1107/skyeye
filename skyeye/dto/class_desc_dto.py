
class CallerInfo:
    class_name = ''
    method_name = ''
    invoke_class = ''
    invoke_func = ''
    invoke_num = ''
    
    def __init__(self, class_name="", method_name="", invoke_class="",invoke_func="",invoke_num=""):
        self.class_name = class_name
        self.method_name = method_name
        self.invoke_class = invoke_class
        self.invoke_func = invoke_func
        self.invoke_num = invoke_num
    
    def toResultJsonMap(self):
        jsoMap = {}
        jsoMap['class_name'] = self.class_name
        jsoMap['method_name'] = self.method_name
        jsoMap['invoke_num'] = self.invoke_num
        return jsoMap
    