# coding=gbk
'''
Created on 2014年3月28日

@author: wenlongyang
'''

import sys
import os
import Image
from FileUtils import walkDir, copy
from PlistParser import PlistParser
from ImageUtils import cropImg

def printUsage():
    print "Usage: ImageCopy.py -src SRC_DIR -dst DST_DIR"
    print "Options:"
    print "  -src   SRC_DIR    input dir, for example: ./src"
    print "  -dst   DST_DIR    output dir, for example: ./dst"
    print ""
    print "Sample 1: ./ImageCopy.py -src ./src -dst ./dst"
    print "Sample 2: ./ImageCopy.py -src ./d1 -dst ./d2"
    print ""
    
def checkArgs(args):
    if len(args) < 4:
        printUsage()
        sys.exit()
    
    srcDir = args[1]
    dstDir = args[3]
        
    fileArr = walkDir(srcDir)
    
    pParser = PlistParser()
    
    plistImgs = []
    allImgs = []
    
    imgExts = [".png", ".jpg", ".bmp"]
    
    for fPath in fileArr:
        extName = os.path.splitext(fPath)[1]
        if extName == ".plist":
            outPath = fPath.replace(srcDir, dstDir)
            outPath = outPath[0:len(outPath) - 6]
            print "out: %s" % outPath
            tex, frameArr = pParser.parse(fPath)
            if frameArr != None:
                plistImg = tex.texDir + tex.texName
                plistImg = plistImg.replace("\\", "/")
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
    checkArgs(sys.argv[1:])