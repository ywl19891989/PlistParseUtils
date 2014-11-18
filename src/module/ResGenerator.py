#coding=utf-8
'''
Created on 2014年11月18日

@author: wenlong
'''

from module import FileUtils as FileUtils 
from module.PlistParser import PlistParser

def test(a):
    resPath = "../../test-Resources/Images/"
    allFiles = FileUtils.walkDir(resPath)
    resPathLen = len(resPath)
    for f in allFiles:
        realPath = f[resPathLen:].replace("\\", "/") 
        print realPath
        if realPath[-6:] == ".plist":
            plistParser = PlistParser()
            texture, frameArr = plistParser.parse(f)
            if not texture == None and not frameArr == None:
                print texture.toStr()
                for frame in frameArr:
                    print frame.toStr()

if __name__ == '__main__':
    test()