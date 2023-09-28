# coding=UTF-8
import os
from skyeye.dto import *
from skyeye.utils import *

class ClassContextCenter:
    
    class_context_map = {}

    @classmethod
    def shared(cls):
        if not hasattr(ClassContextCenter, "_instance"):
            ClassContextCenter._instance = ClassContextCenter()
        return ClassContextCenter._instance

    def __init__(self):
        pass


    def getClassContext(self,className='')->ClassContext:
        classContext = self.class_context_map.get(className)
        if(classContext):
            # print("命中缓存:"+className)
            return classContext
        else:
            classContextHead = self.scanSuperClass(className)
            self.class_context_map[className] = classContextHead
            return classContextHead
    
    
    def scanSuperClass(self,className='')->ClassContext:
        classSmaliPath = os.path.join(os.getcwd(),'out/smali/'+className.replace(".","/")+".smali")
        
        headClassContext = ClassContext()
        headClassContext.class_name = className
        
        if(not  os.path.exists(classSmaliPath)):
            return headClassContext
    
        smaliFile = open(classSmaliPath)
        lines = smaliFile.readlines()
        for line in lines:
         if(line.startswith('.super')):
            superClassName = line[line.index('L')+1:line.index(";")].replace("/",".")
            if not isEmpty(superClassName):
               headClassContext.parent = self.scanSuperClass(superClassName)
            smaliFile.close()
            break
        return headClassContext