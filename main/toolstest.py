# -*- coding: utf-8 -*-
"""Tools Test Package

This script contains test classes which provide performs unit tests
for the classes and exceptions listed in the tools package in the `main` folder.

This script requires that `pandas`, `numpy`, and `matplotlib` are installed
within the Python environment. 

This program is written with Python version 3.7.3 with Spyder IDE.
"""
import os
from pathlib import Path
import unittest
import tools


class ReaderErrorTestClass(unittest.TestCase):
    def setUp(self):
        self.readerError = tools.ReaderError("Expression", "Message")
    
    def test_init(self):
        self.assertEqual(self.readerError.expression, "Expression", "Expression was not added")
        self.assertEqual(self.readerError.message, "Message", "Message was not added")
    def test_toString(self):    
        self.assertEqual(str(self.readerError), "Expression -> Message", "toString() function does not work")
    

class WriterErrorTestClass(unittest.TestCase):
    def setUp(self):
        self.writerError = tools.WriterError("Expression", "Message")
    
    def test_init(self):
        self.assertEqual(self.writerError.expression, "Expression", "Expression was not added")
        self.assertEqual(self.writerError.message, "Message", "Message was not added")
        
    def test_toString(self): 
        self.assertEqual(str(self.writerError), "Expression -> Message", "toString() function does not work")
       
        
class ToolsGlobalFunctionTest(unittest.TestCase):
    def test_addDirectory_pathExist(self):
        self.assertFalse(os.path.exists("new_folder"))
        os.mkdir("new_folder")
        self.assertEqual(tools.addDirectory(os.path.join(Path(os.path.dirname(__file__)), "new_folder"), "test_folder"), os.path.join(Path(os.path.dirname(__file__)), "new_folder") + "\\test_folder", 
                         "addDirectory() does not work when directory exists")
        os.rmdir("new_folder")
        self.assertFalse(os.path.exists("new_folder"))
    
    def test_addDirectory_pathNotExist(self):
        os.mkdir("new_folder")
        self.assertTrue(os.path.exists("new_folder"))
        self.assertEqual(tools.addDirectory(os.path.join(Path(os.path.dirname(__file__)), "new_folder"), "test_folder"), os.path.join(Path(os.path.dirname(__file__)), "new_folder") + "\\test_folder", 
                         "addDirectory() does not work when directory does not exists")
        os.rmdir("new_folder")
        self.assertFalse(os.path.exists("new_folder"))
    
    def test_getBool(self):
        self.assertTrue(tools.getBool("YES"))
        self.assertTrue(tools.getBool("Y"))
        self.assertTrue(tools.getBool("yEs"))
        self.assertTrue(tools.getBool("True"))
        self.assertTrue(tools.getBool("trUE"))
        
        self.assertFalse(tools.getBool("No"))
        self.assertFalse(tools.getBool("Yeah"))
        self.assertFalse(tools.getBool("Okay"))
    
    def test_substringInList(self):
        self.assertFalse(tools.substringInList("", []))
        self.assertTrue(tools.substringInList("", [""]))
        self.assertTrue(tools.substringInList("", ["Abc", "Def"]))
        
        self.assertFalse(tools.substringInList("ab", ["Abc", "Def"]))
        self.assertTrue(tools.substringInList("Ab", ["Abc", "Def"]))
        self.assertTrue(tools.substringInList("ef", ["Abc", "Def"]))
        
        self.assertFalse(tools.substringInList("efg", ["Abc", "Def"]))


class ReaderClassInitTestClass(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_configFileExist(self):
        pass
        
    def test_commentingWorks(self):
        pass
    
    def test_parameterDeclaration(self):
        pass
    
    def test_syntaxCorrectness(self):
        pass
    
    def test_infoFileOutput(self):
        pass
    
    def test_parameterExistence(self):
        pass


class ReaderClassMethodTestClass(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_get(self):
        pass
    
    def test_getRunTemp(self):
        pass
    
    def test_getTime(self):
        pass
    
    def test_getTempTimeSeriesDf(self):
        pass
    
    def test_getRumNum(self):
        pass


class WriterClassMethodTestClass(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_writeData(self):
        pass
    
    def test_roundNum(self):
        pass
    
    def test_writePlots(self):
        pass
        
        
    
    
        
if __name__ == '__main__':
    unittest.main()