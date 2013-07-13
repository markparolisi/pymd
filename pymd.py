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


__version__ = '1.0'
__author__ = "Mark Parolisi, John Ciacia, Michael Pretty"


# Leaving these outside and capitalizing to act as psuedo constants
DS          = "/"
EXPORT_DIR  = "export-html"

class Pymd:

    # @constructor
    def __init__(self, path = None):
        if path is not None:
            self.baseDir = path
        else:
            self.baseDir = os.getcwd()
        self.header = None

    # Find and read contents of a file
    # @param fPath {String} Absolute path to file
    # @return {String | Bool}  Content of of the file or False if file doesn't exist
    def readFile(self, fPath):
        if os.path.exists(fPath) is False :
            return False
        fh = open(fPath, 'r')
        content = fh.read()
        fh.close()
        return content

    # Convert markdown content to HTML using the markdown2 module
    # @param fContents {String} Text to covert
    # @return {String} The HTML version of the content
    def convert(self, fContents):
        return markdown2.markdown(fContents)

    # Create a new directory
    # @param dirPath {String} Absolute path to directory
    # @return {Bool} If the new path exists
    def mkDir(self, dirPath):
        if os.path.exists(dirPath) is False :
            try:
                os.makedirs(dirPath)
            except:
                print "Could not create export directory - ", dirPath
                return False
        return os.path.exists(dirPath)

    # Write a new file
    # @param fCotents {String} contents to write
    # @param {String} Path to write to
    # @return {Bool}
    def mkFile(self, fContents, path):
        if os.path.exists(os.path.dirname(path)) is False:
            self.mkDir(os.path.dirname(path))
        fh = open(path, 'w')
        try:
            fh.write(fContents.encode('utf-8'))
        except:
            print "Could not write file - ", path
            return False
        fh.close()
        return os.path.exists(path)

    # Copy a file to the export directory
    # @param path
    # @param dirs
    # @return {Bool}
    def fCopy(self, path, dirs):

        if os.path.exists(path) is False:
            return False

        # Create the export directory if it does not yet exist
        if os.path.exists(self.baseDir+DS+EXPORT_DIR) is False:
            self.mkDir(self.baseDir+DS+EXPORT_DIR)

        # Create subdirectory if needed
        if os.path.exists(self.baseDir+DS+EXPORT_DIR+dirs) is False :
            self.mkDir(self.baseDir+DS+EXPORT_DIR+dirs)

        name = os.path.basename(path)

        shutil.copy2(path, self.baseDir+DS+EXPORT_DIR+dirs+name )
        return os.path.exists(self.baseDir+DS+EXPORT_DIR+dirs+name)

    # Scan the contents of the document and replace links ending with .md to .html
    # @param fContents {String} Text to scan
    # @return {String} filtered text
    def mdReplace(self, fContents):
        return re.sub(r'href=(.*)\.md', "href=\g<1>.html", fContents, flags=re.IGNORECASE)

    # If the user passes the -z argument, compress the new export directory
    # @param path {String}
    # @param archiveName {String}
    # @return {Bool} True if new paths exists or False if the file could not be written
    def zip(self, path, archiveName):
        assert os.path.isdir(path)
        with closing(ZipFile(archiveName, "w", ZIP_DEFLATED)) as z:
            for root, dirs, files in os.walk(path):
               for fn in files:
                    absfn = os.path.join(root, fn)
                    zfn = absfn[len(path)+len(os.sep):]
                    try:
                        z.write(absfn, zfn)
                        return os.path.exists(path)
                    except:
                        print "Could not write archive file"
                        return False

    # Append new html files with a global header
    # @param headerContents {String} The file contents of the header file
    # @return {Bool} False if file could not be written
    def addHeader(self, headerContents):
        if self.header is None:
            return False
        for root, dirs, files in os.walk(self.baseDir+DS+EXPORT_DIR):
            for file in files:
                if file.endswith('.html'):
                    f = open(root+DS+file,'r')
                    fContent = f.read()
                    f.close()
                    f = open(root+DS+file, 'w')
                    try:
                        f.write(headerContents + fContent)
                    except:
                        print "Could not write header file"
                        return False
                    f.close()

    # Walk over directory and run the app
    def traverse(self):
        for root, dirs, files in os.walk(self.baseDir):
            relPath = root.split(self.baseDir)[1]+DS
            for file in files:
                if ".git" in root:
                    continue
                print "Processing "+ root
                self.mkDir(self.baseDir+EXPORT_DIR+relPath)
                if file.endswith(".md"):
                    if os.path.basename(file) == 'header.md':
                        self.header = self.mdReplace(self.convert(self.readFile(root+DS+file)))
                    else:
                        newFileName = file.replace('.md', ".html")
                        self.mkFile(self.mdReplace(self.convert(self.readFile(root+DS+file))), self.baseDir+DS+EXPORT_DIR+relPath+newFileName)
                else:
                    self.fCopy(root+DS+file, relPath)
        self.addHeader(self.header)
        print "YAY!!!! All Done."

# The CL functionality
# @param argv Command line arguments
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