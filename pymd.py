#!/usr/bin/env python

from __future__ import with_statement
import getopt
import sys
import os
import markdown2
import re
import shutil
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED


__version__ = '0.1'
__author__ = "Mark Parolisi, John Ciacia, Michael Pretty"


#leaving these outside and capitalizing to act as psuedo constants
DS = "/"
EXPORT_DIR = "export"

class Pymd:

    def __init__(self, path = None):
        if path is not None:
            self.baseDir = path
        else:
            self.baseDir = os.getcwd()
        self.header = None

    def readFile(self, fPath):
        fh = open(fPath, 'r')
        content = fh.read()
        fh.close()
        return content

    def convert(self, fContents):
        return markdown2.markdown(fContents)

    def mkDir(self, dirPath):
        if os.path.exists(dirPath) is False :
            os.makedirs(dirPath)
        return os.path.exists(dirPath)

    def mkFile(self, fContents, path):
        fh = open(path, 'w')
        try:
            fh.write(fContents.encode('utf-8'))
        except:
            print "Could not write file"
        fh.close()
        return os.path.exists(path)

    def fCopy(self, path, dirs):
        if os.path.exists(path) is False:
            return False

        if os.path.exists(self.baseDir+DS+EXPORT_DIR) is False:
            self.mkDir(self.baseDir+DS+EXPORT_DIR)

        name = os.path.basename(path)
        shutil.copy2(path, self.baseDir+DS+EXPORT_DIR+DS+dirs+name )
        return os.path.exists(self.baseDir+DS+EXPORT_DIR+DS+dirs+name)

    def mdReplace(self, fContents):
        return re.sub(r'href=(.*)\.md', "href=\g<1>.html", fContents, flags=re.IGNORECASE)

    def zip(self, path, archiveName):
        assert os.path.isdir(path)
        with closing(ZipFile(archiveName, "w", ZIP_DEFLATED)) as z:
            for root, dirs, files in os.walk(path):
               for fn in files:
                    absfn = os.path.join(root, fn)
                    zfn = absfn[len(path)+len(os.sep):]
                    try:
                        z.write(absfn, zfn)
                    except:
                        print "Could not write archive file"

    def addHeader(self, headerContents):
        if self.header is None:
            return False
        for root, dirs, files in os.walk(self.baseDir+DS+EXPORT_DIR):
            for file in files:
                if file.endswith('.html'):
                    f = open(root+DS+file,'r')
                    fContent = f.read()
                    f.close()
                    f =  open(root+DS+file, 'w')
                    try:
                        f.write(headerContents + fContent)
                    except:
                        print "Could not write header file"
                    f.close()

    def traverse(self):
        for root, dirs, files in os.walk(self.baseDir):
            relPath = root.split(self.baseDir)[1]+DS
            for file in files:
                print "Processing "+ root
                self.mkDir(self.baseDir+DS+EXPORT_DIR+DS+relPath)
                if file.endswith(".md"):
                    if os.path.basename(file) == 'header.md':
                        self.header = self.mdReplace(self.convert(self.readFile(root+DS+file)))
                    else:
                        newFileName = file.replace('.md', ".html")
                        self.mkFile(self.mdReplace(self.convert(self.readFile(root+DS+file))), self.baseDir+DS+EXPORT_DIR+DS+relPath+newFileName)
                else:
                    self.fCopy(root+DS+file, relPath)
        self.addHeader(self.header)
        print "YAY!!!! All Done."


def main(argv):

    usage = """
        -h --help                 Prints this help text
        -z --zip                  Zip archive the export directory
        -p --path (dirpath)       Path of directory to process. Uses PWD if absent
    """
    path = os.getcwd()
    zip = None
    try:
        opt, args = getopt.getopt(argv, "hzp:", ["help", "zip", "path="])
    except getopt.GetoptError, err:
        print str(err)
        print usage
        sys.exit(2)
    for o, a in opt:
        if o in ("-h", "--help"):
            print usage
            sys.exit()
        elif o in ("-p", "--path"):
            path = a
        elif o in ("-z", "--zip"):
            zip = True
        else:
            assert False, "unhandled option"

    p = Pymd(path = path)
    p.traverse()
    if zip is True:
        p.zip(p.baseDir+DS+EXPORT_DIR, p.baseDir+DS+EXPORT_DIR+'-archive.zip')

if __name__ == "__main__":
    main(sys.argv[1:])