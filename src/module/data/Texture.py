#coding=utf-8
'''
Created on 2014年9月2日

@author: wenlong
'''

class Texture:
    
    '''
    classdocs
    '''
    
    texDir, texName = None, None
    w, h = None, None
    
    texStr = {}
    
    def init(self, texDir, texName, w, h):
        self.texDir, self.texName = texDir, texName
        self.w, self.h = w, h
        
    def toStr(self):
        self.tDict = { "texDir": self.texDir, "texName": self.texName, "w": self.w, "h": self.h }
        self.texStr = "texDir %s texName %s w %.2f h %.2f" % ( self.texDir, self.texName, self.w, self.h)
        return str(self.texStr)
    
