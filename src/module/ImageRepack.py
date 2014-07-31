# coding=gbk
'''
Created on 2014��3��28��

@author: wenlongyang
'''

import sys
import os
import Image
from FileUtils import walkDir, copy
from PlistParser import PlistParser
from ImageUtils import cropImg
import time 

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

def fixPath(filePath):
    filePath = filePath.replace("\\", "/")
    return filePath

def packDir(inputDir, outputFileName):
    cmdStr = "TexturePacker --format cocos2d \
--data %s.plist \
--verbose \
--sheet %s.png \
--opt RGBA8888 \
--algorithm MaxRects --maxrects-heuristics best \
%s/" % (outputFileName, outputFileName, inputDir)
    print cmdStr
    res = os.popen(cmdStr).read()
    print res
    os.system(cmdStr)
    
def testCallLoaclExe():
    packDir("../../test-Resources/res2/plist/test", "../../test")
    packDir("../../test-Resources/Images-out/item_effect/effectfirebird_RETINA", "../../test")
    
def checkArgs(args):
    if len(args) < 2:
        printUsage()
        sys.exit()
        
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
    allImgs = []
    
    imgExts = [".png", ".jpg", ".bmp"]
    
    for fPath in fileArr:
        extName = os.path.splitext(fPath)[1]
        if extName == ".plist":
            outPath = fPath.replace(srcDir, dstDir)
            outPath = outPath[0:len(outPath) - 6]
            print "out: %s" % outPath
            tex, frameArr = parser.parse(fPath)
            if frameArr != None:
                plistImg = tex.texDir + tex.texName
                plistImg = fixPath(plistImg)
                plistImgs.append(plistImg)
                imgFile = Image.open(tex.texDir + tex.texName)
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                for frame in frameArr:
                    newImg = cropImg(imgFile, frame)
                    if frame.name[-4:] != ".png":
                        frame.name = frame.name + ".png"
                    print "name %s" % frame.name
                    op = outPath + "\\" + frame.name
                    print "outPath %s" % (op)
                    newImg.save(op)
        elif extName in imgExts:
            fPath = fPath.replace("\\", "/")
            allImgs.append(fPath)
    
    print "plistImgs:"
    print plistImgs
    
    for imgF in allImgs:
        if not imgF in plistImgs:
            ss = srcDir.replace("\\", "/")
            dd = dstDir.replace("\\", "/")
            outPath = imgF.replace(ss, dd)
            print "copy %s => %s" % (imgF, outPath)
            copy(imgF, outPath)
            
if __name__ == '__main__':
    #checkArgs(sys.argv[1:])
    testCallLoaclExe()