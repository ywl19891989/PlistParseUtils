#coding=utf-8
'''
Created on 2014年9月2日

@author: wenlong
'''

class Frame(object):
    
    '''
    classdocs
    '''
    
    tex = None
    name = None
    x, y = None, None
    w, h = None, None
    offset_x, offset_y = None, None
    original_w, original_h = None, None
    rotated = False
    
    frameStr = None
    
    def init(self, x, y, w, h, ox, oy, ow, oh):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.ox, self.oy = ox, oy
        self.ow, self.oh = int(ow), int(oh)
    
    def toStr(self):
        self.frameStr = "name %s x %.2f y %.2f w %.2f h %.2f ox %.2f oy %.2f ow %.2f oh %.2f" % ( self.name, self.x, self.y, self.w, self.h, self.ox, self.oy, self.ow, self.oh )
        return str(self.frameStr)

        