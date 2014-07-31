# coding=gbk
'''
Created on 2014-03-28

@author: wenlongyang
'''

import os
import Log

def copy(srcPath, dstPath):
    srcFile = open(srcPath, "rb")
    dstDir = os.path.dirname(dstPath)
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    dstFile = open(dstPath, "wb")
    temp = srcFile.read()
    srcFile.close()
    
    dstFile.write(temp)
    dstFile.close()

def walkDir(dirPath):
    Log.log(Log.logInfo, os.path.basename(dirPath) + ": {")
    files = os.listdir(dirPath)
    fileArr = []
    for childFile in files:
        fullPath = os.path.join(dirPath, childFile)
        if os.path.isdir(fullPath):
            fileChilds = walkDir(fullPath)
            for fileChild in fileChilds:
                fileArr.append(fileChild)
        else:
            Log.log(Log.logInfo, fullPath)
            fileArr.append(fullPath)
    Log.log(Log.logInfo, "}")
    return fileArr

if __name__ == '__main__':
    pass