# coding=gbk
'''
Created on 2014年3月27日

@author: wenlongyang
'''
import Image
import os
from data.Texture import Texture
from data.Frame import Frame
from ImageUtils import cropImg
from FileUtils import *

class AtlasParser:
    textures = []
    frames = []
    curFilePath = None
    
    def parse(self, filePath):
        self.curFilePath = filePath
        self.curFilePath = self.curFilePath.replace("\\", "/")
        texture, frameArr = self.handleAtlasFile()
        return texture, frameArr
        
    def handleAtlasFile(self):
        
        atlasFileData = open(self.curFilePath)
        dataLines = atlasFileData.readlines()
        
        frames = {}
        for dataLine in dataLines:
            dataLine = str(dataLine)
            frameInfos = dataLine.split(" ")
            frames[str(frameInfos[0])] = frameInfos[1:]
        
        splitPos = self.curFilePath.rfind("/")
        fileDir = self.curFilePath[0:splitPos + 1]
        
        fileName = self.curFilePath[splitPos + 1:]
        dotPos = fileName.rfind(".")
        textureFileName = fileName[0:dotPos] + ".png"
        
        texture = Texture()
        texture.texDir = fileDir
        texture.texName = textureFileName
        
        texPath = str(texture.texDir + texture.texName)
        if not os.path.exists(texPath):
            print "texture %s not exist!" % texPath
            return texPath, None
        texFile = Image.open(texPath)
        texSize = texFile.size
        w, h = texSize[0], texSize[0]
        texture.init(fileDir, textureFileName, w, h)
        
        frameArr = []
        
        for key in frames:
            frame = Frame()
            frame.name = str(key)
            frame.tex = texture
            self.decodeFrame(frame, frames[key])
            frameArr.append(frame)
            
        return texture, frameArr
    
    def decodeFrame(self, frame, frameInfo):
        
        if len(frameInfo) == 6:
            # ow 288 oh 512 x 0.0 y 0.0 w 0.28125 h 0.5
            ow = int(frameInfo[0]);
            oh = int(frameInfo[1]);
            x = float(frameInfo[2]) * frame.tex.w;
            y = float(frameInfo[3]) * frame.tex.h;
            w = float(frameInfo[4]) * frame.tex.w;
            h = float(frameInfo[5]) * frame.tex.h;
            
            if x > int(x) + 0.5:
                x = int(x) + 1
                
            if y > int(y) + 0.5:
                y = int(y) + 1
            
            # check ow/oh
            if ow == 0 or oh == 0:
                print "originalWidth/Height not found on the SpriteFrame. AnchorPoint won't work as expected. Regenrate the .plist"
            
            # abs ow/oh
            ow = abs(ow);
            oh = abs(oh);
            
            # init frame
            frame.init(x, y, w, h, 0, 0, ow, oh);
        else:
            print "format unkown %s" % str(self.format)
            
        return frame
    
        
def testHandler():
    
    atlasParser = AtlasParser()
    inPath = "../../test-Resources/atlas"
    outPath = "../../test-Resources/atlas-out"
    
    for root, _, files in os.walk(inPath): 
        for fileName in files:
            if fileName.endswith(".txt"):
                atlasPath = root + "/" + fileName
                outAtlasPath = atlasPath[0:len(atlasPath) - 4]
                outAtlasPath = outAtlasPath.replace(inPath, outPath)
                tex, frameArr = atlasParser.parse(atlasPath)
                imgFile = Image.open(tex.texDir + tex.texName).convert("RGBA")
                if not os.path.exists(outAtlasPath):
                    os.makedirs(outAtlasPath)
                for frame in frameArr:
                    newImg = cropImg(imgFile, frame)
                    if not isImgExt(frame.name):
                        frame.name = frame.name + ".png"
                    op = outAtlasPath + "/" + frame.name
                    newImg.save(op)


if __name__ == '__main__':
    testHandler()