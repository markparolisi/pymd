import sys
import os
import markdown2
import re
import shutil

class Pymd:

    def __init__(self, args = []):
        if len(args) > 1:
            self.baseDir = args[1]
        else:
            self.baseDir = os.getcwd()

    def readFile(self, fpath):
        fh = open(fpath, 'r')
        content = fh.read()
        fh.close()
        return content

    def convert(self, fcontents):
        return markdown2.markdown(fcontents)

    def mkDir(self, dirPath):
        if os.path.exists(dirPath) is False :
            os.makedirs(dirPath)
        return os.path.exists(dirPath)

    def mkFile(self, fcontents, path):
        fh = open(path, 'w')
        fh.write(fcontents)
        fh.close()
        return os.path.exists(path)

    def fCopy(self, path, dirs):
        if os.path.exists(path) is False:
            return False

        if os.path.exists(self.baseDir+"/export") is False:
            self.mkDir(self.baseDir+"/export")

        name = os.path.basename(path)
        shutil.copy2(path, self.baseDir+"/export/"+dirs+name )
        return os.path.exists(self.baseDir+"/export/"+dirs+name)

    def mdReplace(self, fcontents):
        return re.sub(r'href=(.*)\.md', "href=\g<1>.html", fcontents, flags=re.IGNORECASE)

    def traverse(self):
        for root, dirs, files in os.walk(self.baseDir):
            relPath = root.split(self.baseDir)[1]+"/"
            print relPath
            for file in files:
                self.mkDir(self.baseDir+"/export/"+relPath)
                if file.endswith(".md"):
                    newFileName = file.replace('.md', ".html")
                    self.mkFile(self.convert(self.readFile(root+"/"+file)), self.baseDir+"/export/"+relPath+newFileName)
                else:
                    self.fCopy(root+"/"+file, relPath)

        print "YAY!!!! All Done."
        return True

if __name__ == '__main__':
    args = sys.argv
    Pymd.main(args)