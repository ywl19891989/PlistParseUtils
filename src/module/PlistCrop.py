'''
Created on 2014-3-27

@author: Hali
'''

import sys
import os
from PlistParser import PlistParser
from module.ImageUtils import cropImg
from FileUtils import *
import Image

logInfo = 0
logWarning = 1
logError = 2
curLv = logInfo
#curLv = logWarning
#curLv = logError

def log(logLevel, outStr):
    if logLevel >= curLv:
        print outStr

def printUsage():
    print "Usage: PlistCrop.py -src SRC_DIR -dst DST_DIR"
    print "Options:"
    print "  -src   SRC_DIR    input dir, for example: ./src"
    print "  -dst   DST_DIR    output dir, for example: ./dst"
    print ""
    print "Sample 1: ./PlistCrop.py -src ./src -dst ./dst"
    print "Sample 2: ./PlistCrop.py -src ./d1 -dst ./d2"
    print ""
    
def walkDir(dirPath):
    log(logInfo, os.path.basename(dirPath) + ": {")
    files = os.listdir(dirPath)
    fileArr = []
    for childFile in files:
        fullPath = os.path.join(dirPath, childFile)
        if os.path.isdir(fullPath):
            fileChilds = walkDir(fullPath)
            for fileChild in fileChilds:
                fileArr.append(fileChild)
        else:
            log(logInfo, fullPath)
            fileArr.append(fullPath)
    log(logInfo, "}")
    return fileArr

def checkArgs(args):
    if len(args) < 4:
        printUsage()
        sys.exit()
        
    srcDir = args[1]
    dstDir = args[3]
    
    fileArr = walkDir(srcDir)
    
    pParser = PlistParser()
    
    for fPath in fileArr:
        if fPath[-6:] == ".plist":
            outPath = fPath.replace(srcDir, dstDir)
            outPath = outPath[0:len(outPath) - 6]
            print "out: %s" % outPath
            tex, frameArr = pParser.parse(fPath)
            imgFile = Image.open(tex.texDir + tex.texName)
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            for frame in frameArr:
                newImg = cropImg(imgFile, frame)
                if not isImgExt(frame.name):
                    frame.name = frame.name + ".png"
                print "name %s" % frame.name
                op = outPath + "\\" + frame.name
                print "outPath %s" % (op)
                newImg.save(op)

if __name__ == '__main__':
    checkArgs(sys.argv[1:])