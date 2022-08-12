
class CallerInfo:
    class_name = ''
    method_name = ''
    invoke_class = ''
    invoke_func = ''
    
    def __init__(self, class_name="", method_name="", invoke_class="",invoke_func=""):
        self.class_name = class_name
        self.method_name = method_name
        self.invoke_class = invoke_class
        self.invoke_func = invoke_func
    
    def toResultJsonMap(self):
        jsoMap = {}
        jsoMap['class_name'] = self.class_name
        jsoMap['method_name'] = self.method_name
        return jsoMap
    