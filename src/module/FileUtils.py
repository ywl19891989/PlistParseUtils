# coding=gbk
'''
Created on 2014-03-28

@author: wenlongyang
'''

import os
import module.Log as Log

IMG_EXT_DIC = {".png" : 1, ".jpg": 1}

def fixPath(filePath):
    filePath = filePath.replace("\\", "/")
    return filePath

def copy(srcPath, dstPath):
    srcFile = open(srcPath, "rb")
    dstDir = os.path.dirname(dstPath)
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    os.remove(dstPath)
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

def removeDir(dirPath):
    for root, dirs, files in os.walk(dirPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    if os.path.exists(dirPath):
        os.rmdir(dirPath)    
    
def isImgExt(filePath):
    extName = os.path.splitext(filePath)[1]
    return IMG_EXT_DIC.has_key(extName)

if __name__ == '__main__':
    pass