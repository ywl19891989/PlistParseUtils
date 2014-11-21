#coding=utf-8
'''
Created on 2014年11月18日

@author: wenlong
'''
import filecmp
import zipfile
import os

def dirCmp(a, b, bOnlyArr, diffArr, funnyArr):
    x = filecmp.dircmp(a, b)
    for f in x.right_only:
        bOnlyArr.append(b + "/" + f)
    for f in x.diff_files:
        diffArr.append(b + "/" + f)
    for f in x.funny_files:
        funnyArr.append(b + "/" + f)
    for subDir in x.subdirs:
        dirCmp(a + "/" + subDir, b + "/" + subDir, bOnlyArr, diffArr, funnyArr)

def testDirCmp():
    bOnlyArr = []
    diffArr = []
    funnyArr = []
    dirCmp("filecmp/res-a", "filecmp/res-b", bOnlyArr, diffArr, funnyArr)
    print "right-only files: %s" % (str(bOnlyArr))
    print "diff files: %s" % (str(diffArr))
    print "funny files: %s" % (str(funnyArr))

def removeDir(dirPath):
    for root, dirs, files in os.walk(dirPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    if os.path.exists(dirPath):
        os.rmdir(dirPath)  

def copy(srcPath, dstPath):
    if not os.path.exists(srcPath):
        return
    srcFile = open(srcPath, "rb")
    dstDir = os.path.dirname(dstPath)
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    if os.path.isfile(dstPath) and os.path.exists(dstPath):
        os.remove(dstPath)
    dstFile = open(dstPath, "wb")
    temp = srcFile.read()
    srcFile.close()
    
    dstFile.write(temp)
    dstFile.close()  

def cleanAndMakeDir(dirPath):
    removeDir(dirPath)
    os.makedirs(dirPath)

def UnZipFile(zipFilePath, extractPath):
    zipFile = zipfile.ZipFile(zipFilePath)
    cleanAndMakeDir(extractPath)
    for f in zipFile.namelist():
        zipFile.extract(f, extractPath)
        
def makeZipDif(newZip, oldZip, outPath):
    print "makeZipDif(%s, %s, %s)" % (newZip, oldZip, outPath)
    suffix = newZip[-3:]
    resFolder = ""
    if suffix == "apk":
        resFolder = "assets/"
    elif suffix == "ipa":
        resFolder = "Payload/HGAME.app/"
    
    oldUnZipPath = "package/temp/old/"
    UnZipFile(oldZip, oldUnZipPath)
    newZipPath = "package/temp/new/"
    UnZipFile(newZip, newZipPath)
    bOnlyArr = []
    diffArr = []
    funnyArr = []
    dirCmp(oldUnZipPath + resFolder + "res", newZipPath + resFolder + "res", bOnlyArr, diffArr, funnyArr)
    dirCmp(oldUnZipPath + resFolder + "asset", newZipPath + resFolder + "asset", bOnlyArr, diffArr, funnyArr)
    print "right-only files: %s" % (str(bOnlyArr))
    print "diff files: %s" % (str(diffArr))
    print "funny files: %s" % (str(funnyArr))    
    updateZipFilePath = "package/temp/update.zip"
    updateZipFile = zipfile.ZipFile(updateZipFilePath, 'w' ,zipfile.ZIP_DEFLATED)
    for onlyF in bOnlyArr:
        zipName = onlyF[len(newZipPath + resFolder):]
        updateZipFile.write(onlyF, zipName)
        print "update.zip add %s" % zipName
    for diffF in diffArr:
        zipName = diffF[len(newZipPath + resFolder):]
        updateZipFile.write(diffF, zipName)
        print "update.zip add %s" % zipName
    updateZipFile.close()
    
    removeDir(oldUnZipPath)
    removeDir(newZipPath)

    copy(updateZipFilePath, outPath)
    os.remove(updateZipFilePath)

def testUnZip():
    
    updateFolder = "../../test-Resources/package/update/"
    platformArr = [ "android", "iOS" ]
    platformPrefixArr = { "android": "ap", "iOS": "ip" }
    
    for platformName in platformArr:
        packagePath = updateFolder + platformName + "/"
        apkFileArr = open(packagePath + "package.txt").readlines()
        lastFile = None
        for apkFileName in apkFileArr:
            apkFileName = str(apkFileName).strip()
            updateFileName = apkFileName[:len(apkFileName) - 3]
            updateFileName = updateFileName + "data"
            updateFileName = updateFileName.replace("hgame.", platformPrefixArr[platformName])
            if not lastFile == None:
                makeZipDif(packagePath + apkFileName, packagePath + lastFile, packagePath + updateFileName)
            lastFile = apkFileName
    

if __name__ == '__main__':
    testUnZip()
    