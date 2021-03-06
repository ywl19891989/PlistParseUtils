# coding=gbk
'''
Created on 2014年3月27日

@author: wenlongyang
'''
from xml.sax import ContentHandler, make_parser
import StringIO
import Image
import os
from module.data.Texture import Texture
from module.data.Frame import Frame

class XMLParser(ContentHandler):
    
    rootNode = None
    stack = []
    temp = ""
    curE = None
    
    KEY_NAME = "name"
    KEY_ATTRS = "attrs"
    KEY_CHILDS = "childs"
    KEY_VALUE = "value"
    
    def trimDoc(self, fileData):
        docTypeStart = fileData.find("<!DOCTYPE")
        docTypeEnd = fileData.find(">", docTypeStart)
        res = fileData[docTypeStart - 1: docTypeEnd + 1]
        fileData = fileData.replace(res, "")
        return fileData
    
    def parse(self, xmlFilePath):
        parser = make_parser()
        parser.setContentHandler(self)
        xmlFile = open(xmlFilePath)
        data = xmlFile.read().strip()
        
        data = self.trimDoc(data)
        
        data = StringIO.StringIO(data)
        self.rootNode = []
        self.stack = []
        parser.parse(data)
        return self.rootNode
    
    def startElement(self, name, attrs):
        self.temp = None
        newE = { self.KEY_NAME: name, self.KEY_ATTRS: attrs, self.KEY_CHILDS: None, self.KEY_VALUE: None}
        self.stack.append(newE)
        self.curE = newE
    
    def endElement(self, name):
        lastE = self.stack.pop()
        if len(self.stack) > 0:
            lastIndex = len(self.stack) - 1
            parent = self.stack[lastIndex]
            if parent[self.KEY_CHILDS] == None:
                parent[self.KEY_CHILDS] = []
            parent[self.KEY_CHILDS].append(lastE)
        else:
            self.rootNode.append(lastE)
        
    def characters(self, content):
        if self.temp == None:
            self.temp = ""
        self.temp += content
        self.curE[self.KEY_VALUE] = self.temp.strip()

class PlistParser:
    textures = []
    frames = []
    format = 0
    xmlParser = XMLParser()
    curFilePath = None
    
    KEY_FRAMES = "frames"
    KEY_METADATA = "metadata"
    KEY_META = "meta"
    KEY_FORMAT = "format"
    KEY_TEXTUREFILENAME = "textureFileName"
    
    def parse(self, filePath):
        self.format = 0
        self.curFilePath = filePath
        self.curFilePath = self.curFilePath.replace("\\", "/")
        rootNode = self.xmlParser.parse(filePath)
        texture, frameArr = self.handlePlistNode(rootNode)
        return texture, frameArr
        
    def getValueMap(self, node):
        res = {}
        childs = node[XMLParser.KEY_CHILDS]
        for i in range(0, len(childs), 2):
            keyName = childs[i][XMLParser.KEY_VALUE]
            keyValue = childs[i + 1]
            
            if keyValue[XMLParser.KEY_CHILDS] != None:
                keyValue = self.getValueMap(keyValue)
            elif len(keyValue[XMLParser.KEY_VALUE]) > 0:
                keyValue = str(keyValue[XMLParser.KEY_VALUE])
            elif len(keyValue[XMLParser.KEY_VALUE]) == 0:
                keyValue = str(keyValue[XMLParser.KEY_NAME])
            else:
                print "value error"
            res[str(keyName)] = keyValue
        return res
    
    def handlePlistNode(self, plistNode):
        valueDict = self.getValueMap(plistNode[0][XMLParser.KEY_CHILDS][0])
        
        splitPos = self.curFilePath.rfind("/")
        fileDir = self.curFilePath[0:splitPos + 1]
        fileName = self.curFilePath[splitPos + 1:]
        
        frames = valueDict[self.KEY_FRAMES]
        metaData = None
        if valueDict.has_key(self.KEY_METADATA):
            metaData = valueDict[self.KEY_METADATA]
        
        if valueDict.has_key(self.KEY_META):
            self.format = -1
            
        dotPos = fileName.rfind(".")
        textureFileName = fileName[0:dotPos] + ".png"
        if metaData != None:
            self.format = int(metaData[self.KEY_FORMAT])
            textureFileName = metaData[self.KEY_TEXTUREFILENAME]
        
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
        
        if self.format == -1:
            x = float(frameInfo["x"]);
            y = float(frameInfo["y"]);
            w = float(frameInfo["w"]);
            h = float(frameInfo["h"]);
            
            # init frame
            frame.init(x, y, w, h, 0, 0, w, h);
        elif self.format == 0:
            x = float(frameInfo["x"]);
            y = float(frameInfo["y"]);
            w = float(frameInfo["width"]);
            h = float(frameInfo["height"]);
            ox = float(frameInfo["offsetX"]);
            oy = float(frameInfo["offsetY"]);
            ow = int(frameInfo["originalWidth"]);
            oh = int(frameInfo["originalHeight"]);
            # check ow/oh
            if ow == 0 or oh == 0:
                print "originalWidth/Height not found on the SpriteFrame. AnchorPoint won't work as expected. Regenrate the .plist"
            
            # abs ow/oh
            ow = abs(ow);
            oh = abs(oh);
            
            # init frame
            frame.init(x, y, w, h, ox, oy, ow, oh);
        elif (self.format == 2 or self.format == 1):
            
            infos = self.trimStr(frameInfo["frame"])
            
            rotated = False;
            # rotation
            if self.format == 2:
                rotated = (frameInfo["rotated"] == "true");
            
            offset = self.trimStr(frameInfo["offset"])
            
            sourceSize = self.trimStr(frameInfo["sourceSize"]);
 
            # init frame
            frame.rotated = rotated
            frame.init(infos[0], infos[1], infos[2], infos[3], offset[0], offset[1], int(sourceSize[0]), int(sourceSize[1]))
        else:
            print "format unkown %s" % str(self.format)
            
        return frame
    
    def trimStr(self, instr):
        instr = instr.replace("{", "")
        instr = instr.replace("}", "")
        instr = instr.replace(" ", "")
        instr = instr.split(",")
        for index in range(0, len(instr)):
            instr[index] = float(instr[index])
        return instr
        
        
def testHandler():
    print "=============== SAX方式解析XML文档 ==================="
    xmlParser = XMLParser()
    rootNode = xmlParser.parse("test-Resources/res/plist/test.plist")
    print rootNode
