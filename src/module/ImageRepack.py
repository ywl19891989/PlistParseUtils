# coding=utf8
'''
Created on 2014-03-28

@author: wenlongyang
'''

import sys
import os
import Image
from FileUtils import *
from PlistParser import PlistParser
from ImageUtils import cropImg
import time 

EXCLUDE_FILES = {}

def printUsage():
    print "Usage: ImageRePack.py -i INPUT_DIR"
    print "Options:"
    print "  -i   INPUT_DIR    input dir, for example: ./src"
    print ""
    print "Sample: ./ImageRePack.py -i ./src"
    print ""
    
def getCurTime():
    curTime = time.strftime('%Y-%m-%d@%H%M%S',time.localtime(time.time()))
    return str(curTime)

def packDir(inputDir, outputPng, outputPlist):
    
    if os.path.exists(outputPng + ".png"):
        print "remove %s.png" % outputPng
        os.remove(outputPng + ".png")
    
    if os.path.exists(outputPlist + ".plist"):
        print "remove %s.plist" % outputPlist
        os.remove(outputPlist + ".plist")
    
    cmdStr = "TexturePacker --smart-update --format cocos2d \
--sheet %s.png \
--data %s.plist \
--quiet \
--opt RGBA8888 \
--algorithm MaxRects --maxrects-heuristics best \
%s/" % (outputPng, outputPlist, inputDir)
    os.popen(cmdStr).read()
    
def testCallLoaclExe():
    packDir("../../test-Resources/res2/plist/test", "../../test")
    
def initExclued():
    curPath = fixPath(str(os.getcwd())) + "/exclude.txt"
    print curPath
    if os.path.exists(curPath):
        excludeFile = open(curPath, "rt")
        lines = excludeFile.readlines()
        for line in lines:
            line = line.replace("\n", "")
            EXCLUDE_FILES[str(line)] = 1
        
def isExcludeFile(fileName):
    fileName = str(os.path.basename(fileName))
    return EXCLUDE_FILES.has_key(fileName)
    
def checkArgs(args):
    if len(args) < 2:
        printUsage()
        sys.exit()
        
    initExclued()
    srcDir = args[1]
    
    dstDir = os.environ["TMP"]
    dstDir = fixPath(dstDir)
    dstDir = dstDir + "/" + getCurTime()
    
    if os.path.exists(dstDir):
        os.removedirs(dstDir)
    os.makedirs(dstDir)
        
    fileArr = walkDir(srcDir)
    
    parser = PlistParser()
    
    plistImgs = []
    
    for plistPath in fileArr:
        plistPath = fixPath(plistPath)
        extName = os.path.splitext(plistPath)[1]
        if extName == ".plist" and not isExcludeFile(plistPath):
            outPath = fixPath(plistPath).replace(srcDir, dstDir)
            outPath = outPath[0:len(outPath) - 6]
            outLog = "split %s => %s" % (plistPath, outPath)
            outLog = outLog.replace(dstDir, "TEMPDIR")
            print outLog
            tex, frameArr = parser.parse(plistPath)
            if frameArr != None:
                plistImg = str(fixPath(tex.texDir + tex.texName))
                plistImgs.append(plistImg)
                pngPath = tex.texDir + tex.texName
                imgFile = Image.open(tex.texDir + tex.texName)
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                for frame in frameArr:
                    newImg = cropImg(imgFile, frame)
                    if not isImgExt(frame.name):
                        frame.name = frame.name + ".png"
                    print "save Img name %s" % outPath.replace(dstDir, "TEMPDIR") + "/" + frame.name
                    newImg.save(outPath + "/" + frame.name)
                packDir(outPath, outPath, outPath)
                outLog = "pack %s/* => %s.png" % (outPath, outPath)
                outLog = outLog.replace(dstDir, "TEMPDIR")
                print outLog
                removeDir(outPath)
                copy(outPath + ".png", pngPath)
                print "copy %s.png => %s" % (outPath.replace(dstDir, "TEMPDIR"), pngPath) 
                copy(outPath + ".plist", plistPath)
                print "copy %s.plist => %s" % (outPath.replace(dstDir, "TEMPDIR"), plistPath) 
                os.remove(outPath + ".png")
                os.remove(outPath + ".plist")
                
    print "plistImgs:"
    print plistImgs
            
    # remove temp dir        
    removeDir(dstDir)
            
if __name__ == '__main__':
    checkArgs(sys.argv[1:])
    #testCallLoaclExe()