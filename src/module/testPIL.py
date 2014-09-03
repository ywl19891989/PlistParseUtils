#coding=utf-8
'''
Created on 2014年9月3日

@author: wenlong
'''
import Image
import os
from ImageUtils import cropImg
from FileUtils import *

def main():
    print "main"
    img = Image.open("../../test-Resources/atlas/atlas2.png").convert("RGBA")
    print "img mode %s" % img.mode
    img.show()
    # name text_gameover x 0.00 y 1926.00 w 288.00 h 72.00
    
    text_gameover = img.crop((0, 512, 238, 512 + 126));
    text_gameover.show()

    newImg = Image.new("RGBA", text_gameover.size, (255, 255, 255, 255))
    newImg.show()
    
    for i in range(text_gameover.size[0]):
        for j in range(text_gameover.size[1]):
            p = text_gameover.getpixel((i, j))
            print p
    
    print "text_gameover mode %s" % text_gameover.mode
    text_gameover.save("../../test/t.png")
    
if __name__ == '__main__':
    main()