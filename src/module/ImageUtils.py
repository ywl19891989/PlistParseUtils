# coding=gbk
'''
Created on 2014-3-27

@author: Hali
'''

import sys
import os
import Image
from PlistParser import Frame, Texture
from cgitb import text

def printUsage():
    print "Usage: ImageUtils.py [-s input=srcImgPath outSize=[(width,heigh)|(x,y,width,heigt)] outPath=outPath]"
    print "                     [-c input=srcImgPath srcRect=(x,y,w,h) outPath=outPath]"
    print "                     [-cs input=srcImgPath srcRect=(x,y,w,h) outPath=outPath outSize=(w,h)]"
    print "Options:"
    print "  -s    scale the image to input size"
    print "        input: srcImgPath the source image to scale"
    print "        outSize: size of image to scale [no space]"
    print "        outPath: path of Image to save"
    print ""
    print "  -c    crop the rect of image and save to outPath"
    print "        input: srcImgPath the source image to crop"
    print "        srcRect: rect of image to be crop [no space]"
    print "        outPath: path of croped Image to save"
    print ""
    print "  -cs    crop the rect of image and save to outPath"
    print "        input: srcImgPath the source image to crop"
    print "        srcRect: rect of image to be crop [no space]"
    print "        outPath: path of croped Image to save"
    print "        outSize: size of image crop to sace [no space]"
    print ""
    print "Scale Sample: ./ImageUtils.py -s input=./test.png outSize={20,20} outPath=./test-scale.png"
    print "Crop Sample: ./ImageUtils.py -c input=./test.png srcRect={0,0,20,20} outPath=./test-crop.png"
    print "Crop&Scale Sample: ./ImageUtils.py -cs input=./test.png outSize={10,10,20,20} outPath=./test-scale.png outSize=(100,100)"
    print ""
    
def scaleImg(img, box):
    if len(box) != 4:
        print "box arg len is Not enough!"
        sys.exit();
    
    if (box[2] == 0 or box[3] == 0):
        print "Error! outImg size(%d, %d) invalid!" % (box[2], box[3])
        sys.exit()
    img = img.resize((box[2], box[3]))
    newImg = Image.new("RGB", (box[2], box[3]), (255, 255, 255))
    newImg.putalpha(0)
    newImg.paste(img)
    return newImg
    
def cropImg(img, frame):
    x, y = int(frame.x), int(frame.y)
    w, h = int(frame.w), int(frame.h)
    ox, oy = int(frame.ox), int(frame.oy)
    ow, oh = int(frame.ow), int(frame.oh)
    
    px = int((ow - w)/2 + ox)
    py = int((oh - h)/2 - oy)

    rotation = 0
    if frame.rotated == True:
        print "rotated %s" % frame.rotated
        w, h = h, w
        rotation = 90
        
    box = (x, y, x + w, y + h)
    
    newImg = Image.new("RGB", (frame.ow, frame.oh), (255, 255, 255))
    newImg.putalpha(0)
    cropImg = img.crop(box)
    cropImg = cropImg.rotate(rotation)
    r, g, b, a = cropImg.split()
    newImg.paste( cropImg, (px, py), mask = a)
    return newImg
    
def checkArgs(args):
    
    if (len(args) != 4 and len(args) != 5):
        printUsage()
        sys.exit()
    
    argMode = args[0]
    
    if argMode == "-s":
        
        inputPath, outSize, outPath = args[1:]
        
        inputPath = inputPath.split("=")[1]
        
        outPath = outPath.split("=")[1]
        
        outSize = outSize.split("=")[1]
        outSize = outSize.replace("(", "")
        outSize = outSize.replace(")", "")
        sizeArg = outSize.split(",")
        if len(sizeArg) == 2:
            outSize = (0, 0, int(sizeArg[0]), int(sizeArg[1]))
        elif len(sizeArg) == 4:
            outSize = (int(sizeArg[0]), int(sizeArg[1]), int(sizeArg[2]), int(sizeArg[3]))
        
        if not os.path.exists(inputPath):
            print "input filePath(%s) not exist!" % inputPath
            sys.exit()
        
        inputImg = Image.open(inputPath)
        newImg = scaleImg(inputImg, outSize)
        dirName = os.path.dirname(outPath)
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        newImg.save(outPath)
        
    elif argMode == "-c":
        inputPath, srcRect, outPath = args[1:]
        
        inputPath = inputPath.split("=")[1]
        
        outPath = outPath.split("=")[1]
        
        srcRect = srcRect.split("=")[1]
        srcRect = srcRect.replace("(", "")
        srcRect = srcRect.replace(")", "")
        rectArg = srcRect.split(",")
        if not len(rectArg) == 4:
            print "in crop mode, src rect arg(%s) invalid!" % (args[2].split("=")[1])
            sys.exit()
        srcRect = (int(rectArg[0]), int(rectArg[1]), int(rectArg[2]), int(rectArg[3]))

        if not os.path.exists(inputPath):
            print "input filePath(%s) not exist!" % inputPath
            sys.exit()
        
        inputImg = Image.open(inputPath)
        frame = Frame()
        x, y, w, h = srcRect
        frame.init( x, y, w, h, 0, 0, w, h)
        newImg = cropImg(inputImg, frame)
        newImg.save(outPath)
    elif argMode == "-cs":
        inputPath, srcRect, outPath, outSize = args[1:]
        
        inputPath = inputPath.split("=")[1]
        
        outPath = outPath.split("=")[1]
        
        srcRect = srcRect.split("=")[1]
        srcRect = srcRect.replace("(", "")
        srcRect = srcRect.replace(")", "")
        rectArg = srcRect.split(",")
        if not len(rectArg) == 4:
            print "in crop mode, src rect arg(%s) invalid!" % (args[2].split("=")[1])
            sys.exit()
        srcRect = (int(rectArg[0]), int(rectArg[1]), int(rectArg[2]), int(rectArg[3]))

        outSize = outSize.split("=")[1]
        outSize = outSize.replace("(", "")
        outSize = outSize.replace(")", "")
        sizeArg = outSize.split(",")
        
        if not len(sizeArg) == 2:
            print "in crop mode, out size arg(%s) invalid!" % (args[2].split("=")[1])
            sys.exit()
            
        outSize = (int(sizeArg[0]), int(sizeArg[1]))
        
        if not os.path.exists(inputPath):
            print "input filePath(%s) not exist!" % inputPath
            sys.exit()
        
        inputImg = Image.open(inputPath)
        frame = Frame()
        x, y, w, h = srcRect
        ow, oh = outSize
        frame.init( x, y, w, h, 0, 0, w, h)
        newImg = cropImg(inputImg, frame)
        newImg = scaleImg(newImg, (0, 0, ow, oh))
        newImg.save(outPath)
    
if __name__ == '__main__':
    curDir = os.getcwd()
    checkArgs(sys.argv[1:])