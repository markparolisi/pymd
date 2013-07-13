import unittest
from pymd import *

class TestPymd(unittest.TestCase):

    def setUp(self):
        self.path = os.getcwd()
        self.pymd = Pymd(path = self.path+'/sample')

    def testBasedir(self):
        expected = self.path+"/sample"
        actual = self.pymd.baseDir
        self.assertEqual(expected, actual)

    def testBasedirArgs(self):
        stub = Pymd(path = '/Users/mark/fubar')
        expected = "/Users/mark/fubar"
        actual = stub.baseDir
        self.assertEqual(expected, actual)

    def testBasedirArgsPWD(self):
        stub = Pymd()
        expected = self.path
        actual = stub.baseDir
        self.assertEqual(expected, actual)

    def testMkdir(self):
        actual = self.pymd.mkDir(self.pymd.baseDir+"/export")
        self.assertTrue(actual)
        if(os.path.exists(self.pymd.baseDir+"/export") is True):
            shutil.rmtree(self.pymd.baseDir+"/export")

    def testFcopy(self):
        actual = self.pymd.fCopy(self.path+'/doc/css/style.css', 'css')
        self.assertTrue(actual)

    def testFcopy(self):
        actual = self.pymd.fCopy('/foo.bar', 'somedir')
        self.assertFalse(actual)

    def testMkfile(self):
        actual = self.pymd.mkFile('hello world', self.path+'/helloworld.txt')
        self.assertTrue(actual)
        os.remove(self.path+'/helloworld.txt')

    def testVerifyMdFile(self):
        expected = 'hello world'
        self.pymd.mkFile(expected, self.path+'/helloworld.txt')
        actual = self.pymd.readFile(self.path+'/helloworld.txt')
        self.assertEqual(expected, actual)
        os.remove(self.path+'/helloworld.txt')

    def testReadfile(self):
        expected = '<link rel="stylesheet" href="css/style.css" />\n'
        actual = self.pymd.readFile(self.path+'/sample/header.md')
        message = "expected %s - returned %s " % (expected, actual)
        self.assertEqual(expected, actual, message)

    def testCovert(self):
        expected = "<h1>This is an H1</h1>\n"
        actual = self.pymd.convert("# This is an H1 #")
        self.assertEqual(expected, actual)

    def testMdReplace(self):
        expected = "<a href='file.html'>text</a>"
        actual = self.pymd.mdReplace("<a href='file.md'>text</a>")
        self.assertEqual(expected, actual)

    def testZip(self):
        self.pymd.zip(self.path+'/sample/', self.path+'/export-archive.zip')
        actual = os.path.exists(self.path+'/export-archive.zip')
        self.assertTrue(actual)
        os.remove(self.path+'/export-archive.zip')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()