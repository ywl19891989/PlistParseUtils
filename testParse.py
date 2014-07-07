# coding=gbk
'''
Created on 2014年3月27日

@author: wenlongyang
'''

from PlistParser import PlistParser

handler = PlistParser()

fileDir = "res/plist/"
allPlist = [
"test.plist",
"test-0.99.4.plist",
"test-original.plist",
"test-spritepacker.plist",
"test-uikit.plist",
"test-zwoptex.plist"
]

for fileName in allPlist:
    filePath = fileDir + fileName
    print "filePath: %s {" % filePath
    texture, frameArr = handler.parse(filePath)
    print "    %s" % texture.tDict
    for f in frameArr:
        print "    %s" % f.fDict
    print "}"
    