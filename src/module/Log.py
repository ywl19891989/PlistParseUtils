# coding=gbk
'''
Created on 2014��3��28��

@author: wenlongyang
'''

logInfo = 0
logWarning = 1
logError = 2
curLv = logInfo
#curLv = logWarning
#curLv = logError

def log(logLevel, outStr):
    if logLevel >= curLv:
        print outStr

if __name__ == '__main__':
    pass