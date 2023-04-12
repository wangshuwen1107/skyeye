

# 扫描配置
class ScanVO:
    class_name = ""
    method_name = ""
    filed_name = ""

    def __init__(self, class_name=None, method_name=None, filed_name=None):
        self.class_name = class_name
        self.method_name = method_name
        self.filed_name = filed_name
  

    @classmethod
    def from_json(cls, json_map=None):
        if json_map is not None:
            return ScanVO(class_name=json_map.get("className"),
                         method_name=json_map.get("methodName"),
                         filed_name=json_map.get("filedName"))
        return ScanVO()

