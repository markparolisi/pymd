import unittest
from pymd import *

class TestPymd(unittest.TestCase):

    def setUp(self):
        self.pymd = Pymd(path = '/Users/mark/Dropbox/py-demo/pymd/sample')


    def testBasedir(self):
        expected = "/Users/mark/Dropbox/py-demo/pymd/sample"
        actual = self.pymd.baseDir
        self.assertEqual(expected, actual)

    def testBasedirArgs(self):
        stub = Pymd(path = '/Users/mark/fubar')
        expected = "/Users/mark/fubar"
        actual = stub.baseDir
        self.assertEqual(expected, actual)

    def testBasedirArgsPWD(self):
        stub = Pymd()
        expected = "/Users/mark/Dropbox/py-demo/pymd"
        actual = stub.baseDir
        self.assertEqual(expected, actual)

    def testMkdir(self):
        actual = self.pymd.mkDir(self.pymd.baseDir+"/export")
        self.assertTrue(actual)
        if(os.path.exists(self.pymd.baseDir+"/export") is True):
            shutil.rmtree(self.pymd.baseDir+"/export")

    def testFcopy(self):
        actual = self.pymd.fCopy('/Users/mark/Dropbox/py-demo/pymd/sample/css/style.css', 'css')
        self.assertTrue(actual)

    def testFcopy(self):
        actual = self.pymd.fCopy('/foo.bar', 'somedir')
        self.assertFalse(actual)

    def testMkfile(self):
        actual = self.pymd.mkFile('hello world', '/Users/mark/Dropbox/py-demo/pymd/helloworld.txt')
        self.assertTrue(actual)

    def testVerifyMdFile(self):
        expected = 'hello world'
        self.pymd.mkFile(expected, '/Users/mark/Dropbox/py-demo/pymd/helloworld.txt')
        actual = self.pymd.readFile('/Users/mark/Dropbox/py-demo/pymd/helloworld.txt')
        self.assertEqual(expected, actual)

    def testReadfile(self):
        expected = """# This is an H1 #

* list item 1
* list item 2
"""
        actual = self.pymd.readFile('/Users/mark/Dropbox/py-demo/pymd/sample/sample.md')
        message = "expected %s - returned %s actual" % (expected, actual)
        self.assertEqual(expected, actual, message)

    def testCovert(self):
        expected = "<h1>This is an H1</h1>\n"
        actual = self.pymd.convert("# This is an H1 #")
        self.assertEqual(expected, actual)

    def testMdReplace(self):
        expected = "<a href='file.html'>text</a>"
        actual = self.pymd.mdReplace("<a href='file.md'>text</a>")
        self.assertEqual(expected, actual)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()