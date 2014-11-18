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

def testUnZip():
    lastApkPath = "package/android/last.apk"
    lastApkUnZipPath = "package/android/last"
    UnZipFile(lastApkPath, lastApkUnZipPath)
    newApkPath = "package/android/new.apk"
    newApkUnZipPath = "package/android/new"
    UnZipFile(newApkPath, newApkUnZipPath)
    
    bOnlyArr = []
    diffArr = []
    funnyArr = []
    dirCmp(lastApkUnZipPath + "/assets", newApkUnZipPath + "/assets", bOnlyArr, diffArr, funnyArr)
    print "right-only files: %s" % (str(bOnlyArr))
    print "diff files: %s" % (str(diffArr))
    print "funny files: %s" % (str(funnyArr))
    
    updateApkZipPath = "package/android/update.zip"
    updateApkZipFile = zipfile.ZipFile(updateApkZipPath, 'w' ,zipfile.ZIP_DEFLATED)
    for onlyF in bOnlyArr:
        zipName = onlyF[len(newApkUnZipPath + "/assets/"):]
        updateApkZipFile.write(onlyF, zipName)
        print "android update.zip add %s" % zipName
    for diffF in diffArr:
        zipName = diffF[len(newApkUnZipPath + "/assets/"):]
        updateApkZipFile.write(diffF, zipName)
        print "android update.zip add %s" % zipName
    updateApkZipFile.close()
    
    removeDir(lastApkUnZipPath)
    removeDir(newApkUnZipPath)
    
    lastIPAPath = "package/iOS/last.ipa"
    lastIPAUnZipPath = "package/iOS/last/"
    UnZipFile(lastIPAPath, lastIPAUnZipPath)
    newIPAPath = "package/iOS/new.ipa"
    newIPAUnZipPath = "package/iOS/new/"
    UnZipFile(newIPAPath, newIPAUnZipPath)
    bOnlyArr = []
    diffArr = []
    funnyArr = []
    dirCmp(lastIPAUnZipPath + "/Payload/HGAME.app/res", newIPAUnZipPath + "/Payload/HGAME.app/res", bOnlyArr, diffArr, funnyArr)
    dirCmp(lastIPAUnZipPath + "/Payload/HGAME.app/asset", newIPAUnZipPath + "/Payload/HGAME.app/asset", bOnlyArr, diffArr, funnyArr)
    print "right-only files: %s" % (str(bOnlyArr))
    print "diff files: %s" % (str(diffArr))
    print "funny files: %s" % (str(funnyArr))     
    updateIPAZipPath = "package/iOS/update.zip"
    updateIPAZipFile = zipfile.ZipFile(updateIPAZipPath, 'w' ,zipfile.ZIP_DEFLATED)
    for onlyF in bOnlyArr:
        zipName = onlyF[len(newIPAUnZipPath + "/Payload/HGAME.app/"):]
        updateIPAZipFile.write(onlyF, zipName)
        print "iOS update.zip add %s" % zipName
    for diffF in diffArr:
        zipName = diffF[len(newIPAUnZipPath + "/Payload/HGAME.app/"):]
        updateIPAZipFile.write(diffF, zipName)
        print "iOS update.zip add %s" % zipName
    updateIPAZipFile.close()
     
    removeDir(lastIPAUnZipPath)
    removeDir(newIPAUnZipPath)

if __name__ == '__main__':
#     testDirCmp()
    testUnZip()
    