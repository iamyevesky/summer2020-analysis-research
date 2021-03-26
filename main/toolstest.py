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
import math

def assertDoNotRaise(function, params):
    try:
        function(params)
        return True
    except:
        return False

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
        self.assertEqual(tools.addDirectory(os.path.join(Path(os.path.dirname(__file__)), "new_folder"), "test_folder"), os.path.join(os.path.dirname(__file__), "new_folder", "test_folder"), 
                         "addDirectory() does not work when directory exists")
        os.rmdir("new_folder")
        self.assertFalse(os.path.exists("new_folder"))
    
    def test_addDirectory_pathNotExist(self):
        os.mkdir("new_folder")
        self.assertTrue(os.path.exists("new_folder"))
        self.assertEqual(tools.addDirectory(os.path.join(Path(os.path.dirname(__file__)), "new_folder"), "test_folder"), os.path.join(os.path.dirname(__file__), "new_folder", "test_folder"), 
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
        self.emptyFile = open("doesExist.txt", 'w')
        self.emptyFile.close()
        
        self.emptyFileToo = open("emptyFile.txt", 'w')
        self.emptyFileToo.close()
        
        self.commentFile = open("commentFile.txt", 'w')
        self.commentFile.write("#OUT_DIR = C:\\Users\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\data\n")
        self.commentFile.write("#BASE_DIR = C:\\Users\\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\sample\n")
        self.commentFile.write("#DATA_EMPTY = 135958\\Oscilloscope\\voltageDataScopeRun20210131135958(1)CollectionKind0.csv\n")
        self.commentFile.write("#DATA_ACTUAL = 140159\\Oscilloscope\n")
        self.commentFile.write("#DESCRIPTION = Empty Dirty Coil Form\n")
        self.commentFile.write("#M_G_FACTOR_FILE = MCoil\\20200317110751gfactors.csv\n")
        self.commentFile.write("#H_G_FACTOR_FILE = HCoil\\20200317110751gfactors.csv\n")
        self.commentFile.write("#CUTOFF_FREQ = 4000000\n")
        self.commentFile.write("#KNOWN_FREQ = 0\n")
        self.commentFile.write("#M_OVER_H_REAL_SUB = 0\n")
        self.commentFile.write("#M_OVER_H_IMAG_SUB = 0\n")
        self.commentFile.write("#M_OVER_H_CALIB = 0\n")
        self.commentFile.write("#pM_pH_DIFF_PHASE_ADJ = 0\n")
        self.commentFile.write("#M_OVER_H0_SUB = 0\n")
        self.commentFile.write("#H_PHASE_REAL_SUB = 0\n")
        self.commentFile.write("#H_PHASE_IMAG_SUB = 0\n")
        self.commentFile.write("#V_H_OFFSET = 30\n")
        self.commentFile.write("#NUM_PERIOD = 2\n")
        self.commentFile.write("#BEGIN_TIME = 0\n")
        self.commentFile.write("#POLARITY = 1.00\n")
        self.commentFile.write("#WITH_EMPTY = TRUE\n")
        self.commentFile.write("#NON_LINEAR_SUB = TRUE\n")
        self.commentFile.write("#TEMP_DIR = 140159\\Opsens\n")
        self.commentFile.write("#TIME_DIR = 140159\\Time\n")
        self.commentFile.write("#READ_TIME = TRUE\n")
        self.commentFile.write("#H_MIN = 20\n")
        self.commentFile.write("#H_MAX = 60\n")
        self.commentFile.write("#LEGEND = TEMPERATURE | m_max | osc_time | run_num\n")
        self.commentFile.write("#PLOT = H_INT_RECONSTRUCTED_REAL_LIST:M_INT_RECONSTRUCTED_REAL_LIST  #|\n")
        self.commentFile.write("#PLOT_LABEL = H (kA/m):M (kA/m) #| H (kA/m):M (kA/m)\n")
        self.commentFile.write("#PROPERTY_PLOT = TEMPERATURE:HC | INTEGRAL:HC | temperature:osc_time\n")
        self.commentFile.write("#PROPERTY_PLOT_LABEL = Temperature(degC):Hc(T) | integral:Hc(T) | Temperature(degC):Time(sec)\n")        
        self.commentFile.close()
        
        self.configFile = open("correctConfigFile.txt", 'w')
        self.configFile.write("OUT_DIR = C:\\Users\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\data\n")
        self.configFile.write("BASE_DIR = C:\\Users\\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\sample\n")
        self.configFile.write("DATA_EMPTY = 135958\\Oscilloscope\\voltageDataScopeRun20210131135958(1)CollectionKind0.csv\n")
        self.configFile.write("DATA_ACTUAL = 140159\\Oscilloscope\n")
        self.configFile.write("DESCRIPTION = Empty Dirty Coil Form\n")
        self.configFile.write("M_G_FACTOR_FILE = MCoil\\20200317110751gfactors.csv\n")
        self.configFile.write("H_G_FACTOR_FILE = HCoil\\20200317110751gfactors.csv\n")
        self.configFile.write("CUTOFF_FREQ = 4000000\n")
        self.configFile.write("KNOWN_FREQ = 0\n")
        self.configFile.write("M_OVER_H_REAL_SUB = 0\n")
        self.configFile.write("M_OVER_H_IMAG_SUB = 0\n")
        self.configFile.write("M_OVER_H_CALIB = 0\n")
        self.configFile.write("PM_PH_DIFF_PHASE_ADJ = 0\n")
        self.configFile.write("M_OVER_H0_SUB = 0\n")
        self.configFile.write("H_PHASE_REAL_SUB = 0\n")
        self.configFile.write("H_PHASE_IMAG_SUB = 0\n")
        self.configFile.write("V_H_OFFSET = 30\n")
        self.configFile.write("NUM_PERIOD = 2\n")
        self.configFile.write("BEGIN_TIME = 0\n")
        self.configFile.write("POLARITY = 1.00\n")
        self.configFile.write("WITH_EMPTY = TRUE\n")
        self.configFile.write("NON_LINEAR_SUB = TRUE\n")
        self.configFile.write("TEMP_DIR = 140159\\Opsens\n")
        self.configFile.write("TIME_DIR = 140159\\Time\n")
        self.configFile.write("READ_TIME = TRUE\n")
        self.configFile.write("H_MIN = 20\n")
        self.configFile.write("H_MAX = 60\n")
        self.configFile.write("LEGEND = TEMPERATURE | m_max | osc_time | run_num\n")
        self.configFile.write("PLOT = H_INT_RECONSTRUCTED_REAL_LIST:M_INT_RECONSTRUCTED_REAL_LIST \n")
        self.configFile.write("PLOT_LABEL = H (kA/m):M (kA/m)\n")
        self.configFile.write("PROPERTY_PLOT = TEMPERATURE:HC | INTEGRAL:HC | temperature:osc_time\n")
        self.configFile.write("PROPERTY_PLOT_LABEL = Temperature(degC):Hc(T) | integral:Hc(T) | Temperature(degC):Time(sec)\n")
        self.configFile.close()
        
        self.lastOUTDIRwrong = open("lastOUT_DIRFolderWrongConfigFile.txt", 'w')
        self.lastOUTDIRwrong.write("OUT_DIR = C:\\Users\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\datr\n")
        self.lastOUTDIRwrong.write("BASE_DIR = C:\\Users\\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\sample\n")
        self.lastOUTDIRwrong.write("DATA_EMPTY = 135958\\Oscilloscope\\voltageDataScopeRun20210131135958(1)CollectionKind0.csv\n")
        self.lastOUTDIRwrong.write("DATA_ACTUAL = 140159\\Oscilloscope\n")
        self.lastOUTDIRwrong.write("DESCRIPTION = Empty Dirty Coil Form\n")
        self.lastOUTDIRwrong.write("M_G_FACTOR_FILE = MCoil\\20200317110751gfactors.csv\n")
        self.lastOUTDIRwrong.write("H_G_FACTOR_FILE = HCoil\\20200317110751gfactors.csv\n")
        self.lastOUTDIRwrong.write("CUTOFF_FREQ = 4000000\n")
        self.lastOUTDIRwrong.write("KNOWN_FREQ = 0\n")
        self.lastOUTDIRwrong.write("M_OVER_H_REAL_SUB = 0\n")
        self.lastOUTDIRwrong.write("M_OVER_H_IMAG_SUB = 0\n")
        self.lastOUTDIRwrong.write("M_OVER_H_CALIB = 0\n")
        self.lastOUTDIRwrong.write("PM_PH_DIFF_PHASE_ADJ = 0\n")
        self.lastOUTDIRwrong.write("M_OVER_H0_SUB = 0\n")
        self.lastOUTDIRwrong.write("H_PHASE_REAL_SUB = 0\n")
        self.lastOUTDIRwrong.write("H_PHASE_IMAG_SUB = 0\n")
        self.lastOUTDIRwrong.write("V_H_OFFSET = 30\n")
        self.lastOUTDIRwrong.write("NUM_PERIOD = 2\n")
        self.lastOUTDIRwrong.write("BEGIN_TIME = 0\n")
        self.lastOUTDIRwrong.write("POLARITY = 1.00\n")
        self.lastOUTDIRwrong.write("WITH_EMPTY = TRUE\n")
        self.lastOUTDIRwrong.write("NON_LINEAR_SUB = TRUE\n")
        self.lastOUTDIRwrong.write("TEMP_DIR = 140159\\Opsens\n")
        self.lastOUTDIRwrong.write("TIME_DIR = 140159\\Time\n")
        self.lastOUTDIRwrong.write("READ_TIME = TRUE\n")
        self.lastOUTDIRwrong.write("H_MIN = 20\n")
        self.lastOUTDIRwrong.write("H_MAX = 60\n")
        self.lastOUTDIRwrong.write("LEGEND = TEMPERATURE | m_max | osc_time | run_num\n")
        self.lastOUTDIRwrong.write("PLOT = H_INT_RECONSTRUCTED_REAL_LIST:M_INT_RECONSTRUCTED_REAL_LIST \n")
        self.lastOUTDIRwrong.write("PLOT_LABEL = H (kA/m):M (kA/m)\n")
        self.lastOUTDIRwrong.write("PROPERTY_PLOT = TEMPERATURE:HC | INTEGRAL:HC | temperature:osc_time\n")
        self.lastOUTDIRwrong.write("PROPERTY_PLOT_LABEL = Temperature(degC):Hc(T) | integral:Hc(T) | Temperature(degC):Time(sec)\n")
        self.lastOUTDIRwrong.close()
        
        self.outdirWrong = open("OUT_DIRWrongConfigFile.txt", 'w')
        self.outdirWrong.write("OUT_DIR = C:\\Users\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2021\\data\n")
        self.outdirWrong.write("BASE_DIR = C:\\Users\\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\sample\n")
        self.outdirWrong.write("DATA_EMPTY = 135958\\Oscilloscope\\voltageDataScopeRun20210131135958(1)CollectionKind0.csv\n")
        self.outdirWrong.write("DATA_ACTUAL = 140159\\Oscilloscope\n")
        self.outdirWrong.write("DESCRIPTION = Empty Dirty Coil Form\n")
        self.outdirWrong.write("M_G_FACTOR_FILE = MCoil\\20200317110751gfactors.csv\n")
        self.outdirWrong.write("H_G_FACTOR_FILE = HCoil\\20200317110751gfactors.csv\n")
        self.outdirWrong.write("CUTOFF_FREQ = 4000000\n")
        self.outdirWrong.write("KNOWN_FREQ = 0\n")
        self.outdirWrong.write("M_OVER_H_REAL_SUB = 0\n")
        self.outdirWrong.write("M_OVER_H_IMAG_SUB = 0\n")
        self.outdirWrong.write("M_OVER_H_CALIB = 0\n")
        self.outdirWrong.write("PM_PH_DIFF_PHASE_ADJ = 0\n")
        self.outdirWrong.write("M_OVER_H0_SUB = 0\n")
        self.outdirWrong.write("H_PHASE_REAL_SUB = 0\n")
        self.outdirWrong.write("H_PHASE_IMAG_SUB = 0\n")
        self.outdirWrong.write("V_H_OFFSET = 30\n")
        self.outdirWrong.write("NUM_PERIOD = 2\n")
        self.outdirWrong.write("BEGIN_TIME = 0\n")
        self.outdirWrong.write("POLARITY = 1.00\n")
        self.outdirWrong.write("WITH_EMPTY = TRUE\n")
        self.outdirWrong.write("NON_LINEAR_SUB = TRUE\n")
        self.outdirWrong.write("TEMP_DIR = 140159\\Opsens\n")
        self.outdirWrong.write("TIME_DIR = 140159\\Time\n")
        self.outdirWrong.write("READ_TIME = TRUE\n")
        self.outdirWrong.write("H_MIN = 20\n")
        self.outdirWrong.write("H_MAX = 60\n")
        self.outdirWrong.write("LEGEND = TEMPERATURE | m_max | osc_time | run_num\n")
        self.outdirWrong.write("PLOT = H_INT_RECONSTRUCTED_REAL_LIST:M_INT_RECONSTRUCTED_REAL_LIST \n")
        self.outdirWrong.write("PLOT_LABEL = H (kA/m):M (kA/m)\n")
        self.outdirWrong.write("PROPERTY_PLOT = TEMPERATURE:HC | INTEGRAL:HC | temperature:osc_time\n")
        self.outdirWrong.write("PROPERTY_PLOT_LABEL = Temperature(degC):Hc(T) | integral:Hc(T) | Temperature(degC):Time(sec)\n")
        self.outdirWrong.close()
        
        self.configFileError = open("errorConfigFile.txt", 'w')
        self.configFileError.close()
        
        
    def tearDown(self):
        os.remove("doesExist.txt")
        os.remove("commentFile.txt")
        os.remove("correctConfigFile.txt")
        os.remove("errorConfigFile.txt")
        os.remove("emptyFile.txt")
        os.remove("lastOUT_DIRFolderWrongConfigFile.txt")
        os.remove("OUT_DIRWrongConfigFile.txt")
        
        deleteDir = os.path.abspath(Path("C:\\Users\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\datr"))
        if os.path.isdir(deleteDir):
            os.rmdir(deleteDir)
            
            
    
    def test_configFileExist(self):
        with self.assertRaises(tools.ReaderError) as error:
            tools.Reader("doesNotExist.txt")
            
        with self.assertRaises(tools.ReaderError) as notError:
            tools.Reader("doesExist.txt")
        
        self.assertEqual(error.exception.message, "Configuration file does not exist or wrongly specified")
        self.assertEqual(error.exception.expression, "doesNotExist.txt")
        
        self.assertNotEqual(notError.exception.message, "Configuration file does not exist or wrongly specified")
        self.assertNotEqual(notError.exception.expression, "doesExist.txt")
    
    def test_correctDelimiter(self):
        with self.assertRaises(tools.ReaderError) as error:
            tools.Reader("doesExist.txt", "|")
            
        with self.assertRaises(tools.ReaderError) as notError:
            tools.Reader("doesExist.txt", "+")
         
        self.assertEqual(error.exception.message, "This symbol cannot serve as a delimiter for the Reader object")
        self.assertEqual(error.exception.expression, "|")
        
        self.assertNotEqual(notError.exception.message, "This symbol cannot serve as a delimiter for the Reader object")
        self.assertNotEqual(notError.exception.expression, "+")
        
    def test_commentingWorks(self):
        with self.assertRaises(tools.ReaderError) as error:
            tools.Reader("emptyFile.txt")
        
        with self.assertRaises(tools.ReaderError) as sameError:
            tools.Reader("commentFile.txt")
        
        # Empty file is gives the same error as a commented legit file
        self.assertEqual(error.exception.message, sameError.exception.message)
        self.assertEqual(error.exception.expression, sameError.exception.expression)
    
    def test_parameterDeclaration(self):
        self.configFile = open(self.configFile.name, 'a')
        self.configFile.write("\n")
        self.configFile.write("\n")
        self.configFile.close()
        
        # Empty strings appended at the end are ignored and do not raise any errors
        self.assertTrue(assertDoNotRaise(lambda x : tools.Reader(x), "correctConfigFile.txt"))
        
        self.configFile = open(self.configFile.name, 'a')
        self.configFile.write("\n")
        self.configFile.write("ABBBA\n")
        self.configFile.close()
        with self.assertRaises(tools.ReaderError) as error:
            tools.Reader("correctConfigFile.txt")
        
        self.assertEqual(error.exception.message, "Line could not be read from file")
        self.assertEqual(error.exception.expression, "ABBBA")
    
    def test_parameterExistence(self):
        # All parameters are declared for this file
        self.assertTrue(assertDoNotRaise(lambda x : tools.Reader(x), "correctConfigFile.txt"))
        
        self.configFile = open(self.configFile.name, 'a')
        self.configFile.write("\n")
        self.configFile.write("ABBBA =  ABBBA\n")
        self.configFile.close()
        with self.assertRaises(tools.ReaderError) as error:
            tools.Reader("correctConfigFile.txt")
        
        self.assertEqual(error.exception.message, "Property is not poorly defined or not necessary")
        self.assertEqual(error.exception.expression, "ABBBA")

    def test_creationOfLastDirectoryOfPropertyOUT_DIR(self):
        self.reader = tools.Reader("lastOUT_DIRFolderWrongConfigFile.txt")
        self.assertTrue(os.path.isdir(self.reader.get("OUT_DIR")))
        
        with self.assertRaises(tools.ReaderError) as error:
            tools.Reader("OUT_DIRWrongConfigFile.txt")
        
        self.assertEqual(error.exception.message, "OUT_DIR does not exist.")
        
        
class ReaderClassMethodTestClass(unittest.TestCase):
    
    def setUp(self):
        self.configFile = open("correctConfigFile.txt", 'w')
        self.configFile.write("OUT_DIR = C:\\Users\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\data\n")
        self.configFile.write("BASE_DIR = C:\\Users\\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\sample\n")
        self.configFile.write("DATA_EMPTY = 135958\\Oscilloscope\\voltageDataScopeRun20210131135958(1)CollectionKind0.csv\n")
        self.configFile.write("DATA_ACTUAL = 140159\\Oscilloscope\n")
        self.configFile.write("DESCRIPTION = Empty Dirty Coil Form\n")
        self.configFile.write("M_G_FACTOR_FILE = MCoil\\20200317110751gfactors.csv\n")
        self.configFile.write("H_G_FACTOR_FILE = HCoil\\20200317110751gfactors.csv\n")
        self.configFile.write("CUTOFF_FREQ = 4000000\n")
        self.configFile.write("KNOWN_FREQ = 0\n")
        self.configFile.write("M_OVER_H_REAL_SUB = 0\n")
        self.configFile.write("M_OVER_H_IMAG_SUB = 0\n")
        self.configFile.write("M_OVER_H_CALIB = 0\n")
        self.configFile.write("PM_PH_DIFF_PHASE_ADJ = 0\n")
        self.configFile.write("M_OVER_H0_SUB = 0\n")
        self.configFile.write("H_PHASE_REAL_SUB = 0\n")
        self.configFile.write("H_PHASE_IMAG_SUB = 0\n")
        self.configFile.write("V_H_OFFSET = 30\n")
        self.configFile.write("NUM_PERIOD = 2\n")
        self.configFile.write("BEGIN_TIME = 0\n")
        self.configFile.write("POLARITY = 1.00\n")
        self.configFile.write("WITH_EMPTY = TRUE\n")
        self.configFile.write("NON_LINEAR_SUB = TRUE\n")
        self.configFile.write("TEMP_DIR = 140159\\Opsens\n")
        self.configFile.write("TIME_DIR = 140159\\Time\n")
        self.configFile.write("READ_TIME = TRUE\n")
        self.configFile.write("H_MIN = 20\n")
        self.configFile.write("H_MAX = 60\n")
        self.configFile.write("LEGEND = TEMPERATURE | m_max | osc_time | run_num\n")
        self.configFile.write("PLOT = H_INT_RECONSTRUCTED_REAL_LIST:M_INT_RECONSTRUCTED_REAL_LIST \n")
        self.configFile.write("PLOT_LABEL = H (kA/m):M (kA/m)\n")
        self.configFile.write("PROPERTY_PLOT = TEMPERATURE:HC | INTEGRAL:HC | temperature:osc_time\n")
        self.configFile.write("PROPERTY_PLOT_LABEL = Temperature(degC):Hc(T) | integral:Hc(T) | Temperature(degC):Time(sec)\n")
        self.configFile.close()
        
        self.configFile = open("correctAnotherConfigFile.txt", 'w')
        self.configFile.write("OUT_DIR = C:\\Users\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\data\n")
        self.configFile.write("BASE_DIR = C:\\Users\\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\sample\n")
        self.configFile.write("DATA_EMPTY = 135958\\Oscilloscope\\voltageDataScopeRun20210131135958(1)CollectionKind0.csv\n")
        self.configFile.write("DATA_ACTUAL = 140159\\Oscilloscope\n")
        self.configFile.write("DESCRIPTION = Empty Dirty Coil Form\n")
        self.configFile.write("M_G_FACTOR_FILE = MCoil\\20200317110751gfactors.csv\n")
        self.configFile.write("H_G_FACTOR_FILE = HCoil\\20200317110751gfactors.csv\n")
        self.configFile.write("CUTOFF_FREQ = 4000000\n")
        self.configFile.write("KNOWN_FREQ = 0\n")
        self.configFile.write("M_OVER_H_REAL_SUB = 0\n")
        self.configFile.write("M_OVER_H_IMAG_SUB = 0\n")
        self.configFile.write("M_OVER_H_CALIB = 0\n")
        self.configFile.write("PM_PH_DIFF_PHASE_ADJ = 0\n")
        self.configFile.write("M_OVER_H0_SUB = 0\n")
        self.configFile.write("H_PHASE_REAL_SUB = 0\n")
        self.configFile.write("H_PHASE_IMAG_SUB = 0\n")
        self.configFile.write("V_H_OFFSET = 30\n")
        self.configFile.write("NUM_PERIOD = 2\n")
        self.configFile.write("BEGIN_TIME = 0\n")
        self.configFile.write("POLARITY = 1.00\n")
        self.configFile.write("WITH_EMPTY = TRUE\n")
        self.configFile.write("NON_LINEAR_SUB = TRUE\n")
        self.configFile.write("TEMP_DIR = 140159\\Opsens\n")
        self.configFile.write("TIME_DIR = 140159\\Time\n")
        self.configFile.write("READ_TIME = FALSE\n")
        self.configFile.write("H_MIN = 20\n")
        self.configFile.write("H_MAX = 60\n")
        self.configFile.write("LEGEND = TEMPERATURE | m_max | osc_time | run_num\n")
        self.configFile.write("PLOT = H_INT_RECONSTRUCTED_REAL_LIST:M_INT_RECONSTRUCTED_REAL_LIST \n")
        self.configFile.write("PLOT_LABEL = H (kA/m):M (kA/m)\n")
        self.configFile.write("PROPERTY_PLOT = TEMPERATURE:HC | INTEGRAL:HC | temperature:osc_time\n")
        self.configFile.write("PROPERTY_PLOT_LABEL = Temperature(degC):Hc(T) | integral:Hc(T) | Temperature(degC):Time(sec)\n")
        self.configFile.close()
        
        self.reader = tools.Reader("correctConfigFile.txt")
        self.anotherReader = tools.Reader("correctAnotherConfigFile.txt")
        
        self.readerOutput = open('expectedOutput.txt', 'w')
        self.readerOutput.write("OUT_DIR = C:\\Users\\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\data\n")
        self.readerOutput.write("BASE_DIR = C:\\Users\\yeves\\OneDrive - lafayette.edu\\School Documents\\Competition, Research Documents\\SummerResearch2020\\sample\n")
        self.readerOutput.write("M_G_FACTOR_FILE = MCoil\\20200317110751gfactors.csv\n")
        self.readerOutput.write("H_G_FACTOR_FILE = HCoil\\20200317110751gfactors.csv\n")
        self.readerOutput.write("DATA_EMPTY = 135958\\Oscilloscope\\voltageDataScopeRun20210131135958(1)CollectionKind0.csv\n")
        self.readerOutput.write("DATA_ACTUAL = 140159\\Oscilloscope\n")
        self.readerOutput.write("DESCRIPTION = Empty Dirty Coil Form\n")
        self.readerOutput.write("CUTOFF_FREQ = 4000000\n")
        self.readerOutput.write("KNOWN_FREQ = 0\n")
        self.readerOutput.write("M_OVER_H_REAL_SUB = 0\n")
        self.readerOutput.write("M_OVER_H_IMAG_SUB = 0\n")
        self.readerOutput.write("V_H_OFFSET = 30\n")
        self.readerOutput.write("M_OVER_H_CALIB = 0\n")
        self.readerOutput.write("PM_PH_DIFF_PHASE_ADJ = 0\n")
        self.readerOutput.write("M_OVER_H0_SUB = 0\n")
        self.readerOutput.write("NUM_PERIOD = 2\n")
        self.readerOutput.write("NON_LINEAR_SUB = True\n")
        self.readerOutput.write("H_PHASE_REAL_SUB = 0\n")
        self.readerOutput.write("H_PHASE_IMAG_SUB = 0\n")
        self.readerOutput.write("BEGIN_TIME = 0\n")
        self.readerOutput.write("WITH_EMPTY = True\n")
        self.readerOutput.write("TEMP_DIR = 140159\\Opsens\n")
        self.readerOutput.write("H_MIN = 20\n")
        self.readerOutput.write("POLARITY = 1.00\n")
        self.readerOutput.write("H_MAX = 60\n")
        self.readerOutput.write("LEGEND = TEMPERATURE | m_max | osc_time | run_num\n")
        self.readerOutput.write("PLOT = H_INT_RECONSTRUCTED_REAL_LIST:M_INT_RECONSTRUCTED_REAL_LIST\n")
        self.readerOutput.write("PLOT_LABEL = H (kA/m):M (kA/m)\n")
        self.readerOutput.write("PROPERTY_PLOT = TEMPERATURE:HC | INTEGRAL:HC | temperature:osc_time\n")
        self.readerOutput.write("PROPERTY_PLOT_LABEL = Temperature(degC):Hc(T) | integral:Hc(T) | Temperature(degC):Time(sec)\n")
        self.readerOutput.write("TIME_DIR = 140159\Time\n")
        self.readerOutput.write("READ_TIME = True\n")
        self.readerOutput.close()
        
    def tearDown(self):
        os.remove("correctConfigFile.txt")
        os.remove("correctAnotherConfigFile.txt")
        os.remove('expectedOutput.txt')
        self.readerOutput.close()
        filePath = os.path.join(self.reader.get("OUT_DIR"), self.reader.get("DATE"), self.reader.get("TIME"))
        removeFilePath = os.path.join(self.reader.get("OUT_DIR"), self.reader.get("DATE"))
        if os.path.exists(filePath):
            for file in os.listdir(filePath):
                os.remove(os.path.join(filePath, file))
        
            os.rmdir(filePath)
            
            # The date file path might contain data already before testing hence undesirable to removed directory
            try:
                os.rmdir(removeFilePath)
            except OSError:
                pass
            
    
    def test_get(self):
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.get("DOES NOT EXIST")
        self.assertEqual(error.exception.message, "Property does not exist in configuration file")
        self.assertEqual(error.exception.expression, "DOES NOT EXIST")
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.get("PLOT", tools.Reader.asFloat)
        self.assertEqual(error.exception.message, "Property is not a float value")
        self.assertEqual(error.exception.expression, "PLOT")
        
        
        self.assertTrue(assertDoNotRaise(self.reader.get, "WITH_EMPTY"))
        prevValue = self.reader.get("WITH_EMPTY")
        self.reader._data["WITH_EMPTY"] = ""
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.get("WITH_EMPTY")
        self.assertEqual(error.exception.message, "Property does not exist in configuration file")
        self.assertEqual(error.exception.expression, "WITH_EMPTY")
        self.reader._data["WITH_EMPTY"] = prevValue
        
        
    def test_getRunTemp(self):
        self.assertTrue(assertDoNotRaise(self.reader.getRunTemp, "20210131140159(1)CollectionKind1"))
        self.assertTrue(assertDoNotRaise(self.reader.getRunTemp, "20210131140159(18)CollectionKind1"))
        self.assertFalse(assertDoNotRaise(self.reader.getRunTemp, "20210131140159(21)CollectionKind1"))
        self.assertFalse(assertDoNotRaise(self.reader.getRunTemp, "20210131140159(100)CollectionKind1"))
        
        expectedValues = [25.26, 25.28, 25.28, 25.32, 25.36, 25.41, 25.45, 25.52, 25.51, 25.55, 25.58, 25.61, 25.65, 25.68, 25.76, 25.84, 25.86, 25.88, 25.95, 25.99]
        for i in range(len(expectedValues)):
            self.assertAlmostEqual(self.reader.getRunTemp("20210131140159("+str(i + 1)+")CollectionKind1"), expectedValues[i])
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getRunTemp("2021013114015(1)CollectionKind1")
        self.assertEqual(error.exception.message, "Voltage file name is not in the right format. Expected: 'voltageDataScopeRun'+ '(<RUN_NUM>)' + <DATE> + <TIME> + 'CollectionKind' + <KIND_NUM> + '.csv' where 'CollectionKind' + <KIND_NUM> is optional for backwards compatibility")
        self.assertEqual(error.exception.expression, "2021013114015(1)CollectionKind1")
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getRunTemp("20210131140158(1)CollectionKind1")
        self.assertEqual(error.exception.message, "Temp-V-Run Series data of this date-time value not added to TEMP_DIR.")
        self.assertEqual(error.exception.expression, "20210131140158")
        
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getRunTemp("20210131140159(1)CollectionKind5")
        self.assertEqual(error.exception.message, "Temp-V-Run Series data of dateTime 20210131140159 does not have this value of 'CollectionKind' added to TEMP_DIR.")
        self.assertEqual(error.exception.expression, 5)
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getRunTemp("20210131140159CollectionKind1")
        self.assertEqual(error.exception.message, "Voltage file name is not in the right format. Expected: 'voltageDataScopeRun'+ '(<RUN_NUM>)' + <DATE> + <TIME> + 'CollectionKind' + <KIND_NUM> + '.csv' where 'CollectionKind' + <KIND_NUM> is optional for backwards compatibility")
        self.assertEqual(error.exception.expression, "20210131140159CollectionKind1")
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getRunTemp("20210131140159(21)CollectionKind1")
        self.assertEqual(error.exception.message, "Temp-V-Run Series data of this date-time value does not contain temperature value for Run 21")
        self.assertEqual(error.exception.expression, "20210131140159")
        
    def test_getTime(self):
        self.assertTrue(assertDoNotRaise(lambda x: self.reader.getTime(x[0], x[1]), ("20210131140159(1)CollectionKind1", 'program')))
        self.assertTrue(assertDoNotRaise(lambda x: self.reader.getTime(x[0], x[1]), ("20210131140159(18)CollectionKind1", 'program')))
        self.assertTrue(assertDoNotRaise(lambda x: self.reader.getTime(x[0], x[1]), ("20210131140159(21)CollectionKind1", 'program')))
        self.assertTrue(assertDoNotRaise(lambda x: self.reader.getTime(x[0], x[1]), ("20210131140159(21)CollectionKind1", 'opsens')))
        self.assertFalse(assertDoNotRaise(lambda x: self.reader.getTime(x[0], x[1]), ("20210131140159(21)CollectionKind1", 'oscilloscope')))
        self.assertFalse(assertDoNotRaise(lambda x: self.reader.getTime(x[0], x[1]), ("20210131140159(100)CollectionKind1", 'oscilloscope')))
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getTime("2021013114015(1)CollectionKind1", 'program')
        self.assertEqual(error.exception.message, "Voltage file name is not in the right format. Expected: 'voltageDataScopeRun'+ '(<RUN_NUM>)' + <DATE> + <TIME> + 'CollectionKind' + <KIND_NUM> + '.csv' where 'CollectionKind' + <KIND_NUM> is optional for backwards compatibility")
        self.assertEqual(error.exception.expression, "2021013114015(1)CollectionKind1")
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getTime("20210131140158(1)CollectionKind1", 'program')
        self.assertEqual(error.exception.message, "Time data of this date-time value not added to TIME_DIR.")
        self.assertEqual(error.exception.expression, "20210131140158")
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getTime("20210131140159(1)CollectionKind5", 'program')
        self.assertEqual(error.exception.message, "Time-V-Run Series data of dateTime 20210131140159 does not have this value of 'CollectionKind' added to TEMP_DIR.")
        self.assertEqual(error.exception.expression, 5)
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getTime("20210131140159CollectionKind1", 'oscilloscope')
        self.assertEqual(error.exception.message, "Voltage file name is not in the right format. Expected: 'voltageDataScopeRun'+ '(<RUN_NUM>)' + <DATE> + <TIME> + 'CollectionKind' + <KIND_NUM> + '.csv' where 'CollectionKind' + <KIND_NUM> is optional for backwards compatibility")
        self.assertEqual(error.exception.expression, "20210131140159CollectionKind1")
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getTime("20210131140159(21)CollectionKind1", 'oscilloscope')
        self.assertEqual(error.exception.message, "Time data of this date-time value does not contain start time value for Run 21")
        self.assertEqual(error.exception.expression, "20210131140159")
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getTime("20210131140159(21)CollectionKind1", 'NOT_EXPECTED')
        self.assertEqual(error.exception.message, "Reader.getTime() `kind` option is not an expected value.")
        self.assertEqual(error.exception.expression, 'NOT_EXPECTED')
        
        self.assertTrue(math.isnan(self.anotherReader.getTime("20210131140159(21)CollectionKind1", 'program')))
        
        expectedValues = [0.2028684, 0.2028682, 0.9512336, 0.9512334, 1.6772168, 1.6772166, 2.3519779, 2.3519777, 3.0287938, 3.0287936, 3.6954844, 3.6954842, 4.3722015, 4.3722013, 5.050884, 5.0508838, 5.7237166, 5.7237164, 6.4074793, 6.4074791, 7.090481, 7.0904808, 7.7653434, 7.7653432, 8.4423567, 8.4423565, 9.1210733, 9.1210731, 9.7983369, 9.7983367, 10.474582, 10.4745818, 11.1543001, 11.1542999, 11.8365654, 11.8365652, 12.5089323, 12.5089321, 13.1803286, 13.1803284]
        for i in range(0, 40, 2):
            key = "20210131140159("+str(i//2 + 1)+")CollectionKind1"
            self.assertAlmostEqual(self.reader.getTime(key, "oscilloscope", relative=False), expectedValues[i])
            self.assertAlmostEqual(self.reader.getTime(key, "oscilloscope", relative=True), expectedValues[i + 1]) 
            
    def test_getTempSeriesDf(self):
        self.assertTrue(assertDoNotRaise(self.reader.getTempSeriesDf, "20210131140159(1)CollectionKind1"))
        self.assertFalse(assertDoNotRaise(self.reader.getTempSeriesDf, "20210131140158(1)CollectionKind1"))
        self.assertFalse(assertDoNotRaise(self.reader.getTempSeriesDf, "2021013114015(1)CollectionKind1"))
        self.assertFalse(assertDoNotRaise(self.reader.getTempSeriesDf, "20210131140159(1)"))
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getTempSeriesDf("2021013114015(1)CollectionKind1")
        self.assertEqual(error.exception.message, "Voltage file name is not in the right format. Expected: 'voltageDataScopeRun'+ '(<RUN_NUM>)' + <DATE> + <TIME> + 'CollectionKind' + <KIND_NUM> + '.csv' where 'CollectionKind' + <KIND_NUM> is optional for backwards compatibility")
        self.assertEqual(error.exception.expression, "2021013114015(1)CollectionKind1")
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getTempSeriesDf("20210131140158(1)CollectionKind1")
        self.assertEqual(error.exception.message, "Temp-V-Run Series data of this date-time value not added to TEMP_DIR.")
        self.assertEqual(error.exception.expression, "20210131140158")
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getTempSeriesDf("20210131140159(1)")
        self.assertEqual(error.exception.message, "Temp-V-Run Series data of dateTime 20210131140159 does not have this value of 'CollectionKind' added to TEMP_DIR.")
        self.assertEqual(error.exception.expression, -1)
        
    def test_getRumNum(self):
        self.assertTrue(assertDoNotRaise(self.reader.getRunNum, "20210131140159(1)CollectionKind1"))
        self.assertFalse(assertDoNotRaise(self.reader.getRunNum, "20210131140159CollectionKind1"))
        
        self.assertEqual(self.reader.getRunNum("20210131140159(1)CollectionKind1"), 1)
        
        with self.assertRaises(tools.ReaderError) as error:
            self.reader.getRunNum("20210131140159CollectionKind1")
        self.assertEqual(error.exception.message, "Voltage file name is not in the right format. Expected: 'voltageDataScopeRun'+ '(<RUN_NUM>)' + <DATE> + <TIME> + 'CollectionKind' + <KIND_NUM> + '.csv' where 'CollectionKind' + <KIND_NUM> is optional for backwards compatibility")
        self.assertEqual(error.exception.expression, "20210131140159CollectionKind1")
    
    def test_writeConfigFile(self):
        self.reader.writeConfigFile()
        
        filePath = os.path.join(self.reader.get("OUT_DIR"), self.reader.get("DATE"), self.reader.get("TIME"))
        if os.path.exists(filePath):
            listDir = os.listdir(filePath)
            file = listDir[0]
            
            self.readerOutput = open('expectedOutput.txt')
            otherLineList = []
            for line in self.readerOutput:
                otherLineList.append(line)
            self.readerOutput.close()
            
            
            for index, line in enumerate(open(os.path.join(filePath, file))):
                self.assertEqual(line, otherLineList[index])
        
        else:
            print("Files were not written")
            self.assertTrue(False)
        
    
    
        
if __name__ == '__main__':
    unittest.main()