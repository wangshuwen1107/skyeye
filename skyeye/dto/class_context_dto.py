
# 类的继承关系
class ClassContext:
    class_name = ""
    parent = None

    def __init__(self, class_name=None, parent=None):
        self.class_name = class_name
        self.parent = parent
  