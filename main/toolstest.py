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
        
        self.configFileError = open("errorConfigFile.txt", 'w')
        self.configFileError.close()
        
    def tearDown(self):
        os.remove("doesExist.txt")
        os.remove("commentFile.txt")
        os.remove("correctConfigFile.txt")
        os.remove("errorConfigFile.txt")
        os.remove("emptyFile.txt")
    
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
        
        self.reader = tools.Reader("correctConfigFile.txt")
    
    def tearDown(self):
        os.remove("correctConfigFile.txt")
    
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
        
        self.assertEqual(self.reader.getRunTemp("20210131140159(1)CollectionKind1"), 25.26)
        self.assertEqual(self.reader.getRunTemp("20210131140159(18)CollectionKind1"), 25.88)
        self.assertEqual(self.reader.getRunTemp("20210131140159(20)CollectionKind1"), 25.99)
        
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