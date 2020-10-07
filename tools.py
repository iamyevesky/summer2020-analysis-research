# -*- coding: utf-8 -*-
"""Tools Package

This script contains helper classes and exceptions which provide an interface
to interact with the voltage and temperature analysis program 
using a text file as input and produce csv files and plot images as outputs
based on specifications in the input text file.

This script requires that `pandas`, `numpy`, and `mathplotlib` are installed
within the Python environment. 

This program is written with Python version 3.7.3 with Spyder IDE.

This file is imported as a module and contains the following classes:
    * ReaderError - Exception for Reader class
    * WriterError - Exception for Writer class
    * Writer - Writes output data for analysis program
    * Reader - Reads input data for analysis program

It provides the following functions:
    * getBool - Returns bool value True if string input is an affirmative word
    * addDirectory - Joins two string filepaths into one
    
"""

import os
import datetime
import pandas as pd
import numpy as np
import re
from typing import Any, Dict, Tuple, List
import math
import matplotlib.pyplot as plt

class ReaderError(Exception):
    """
    A class that serves as an Exception for the Reader class.
    
    Attributes
    ----------
    expression : str
        Variable or value for which an error or exception is associated with.
    message : str
        Error or exception message associated with expression.
    """
    
    def __init__(self, expression: str, message: str):
        """
        Args:
            expression: Variable or value for which an error or exception is associated with.
            message: Error or exception message associated with expression.
        """
        self.expression = expression
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.expression} -> {self.message}'
    
    
class WriterError(Exception):
    """
    A class that serves as an Exception for the Writer class.
    
    Attributes
    ----------
    expression : str
        Variable or value for which an error or exception is associated with.
    message : str
        Error or exception message associated with expression.
    """
    
    def __init__(self, expression: str, message: str):
        """
        
        Parameters
        ----------
        expression : str
             Variable or value for which an error or exception is associated with.
        message : str
            Error or exception message associated with expression.
        
        Returns
        -------
        None.
        """
        self.expression = expression
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.expression} -> {self.message}'


class Writer(object):
    """
    Writes output data in .csv files and plot images in .pdf and .jpg files
    
    Output files are written to this directory:
        OUT_DIR/DATE(YYYYMMDD)/TIME(HHMMSS)
    where OUT_DIR is value obtained from Reader object passed during
    initialization of object. DATE and TIME are date and time values
    at which analysis program run.
    
    Analyzed voltage data of each voltage run is stored in:
        OUT_DIR/DATE(YYYYMMDD)/TIME(HHMMSS)/MHAnalyzed
    with naming system: 
        voltageDataScopeRun + DATE + TIME + (RUN_NUMBER) + _ + TYPE + DESCRIPTION + _ + Analyzed + .csv
    where DATE and TIME are the date and time values associated with the
    original raw voltage dataset,
    RUN_NUMBER is the run number associated with the raw original voltage dataset,
    TYPE is the kind of voltage dataset the original raw voltage (EMPTY or ACTUAL recording)
    and DESCRIPTION is value obtained from Reader object passed during intialization.
    
    Analyzed empty field voltage datasets
    (Voltage data collected when coil was filled with no nanoparticles)
    are stored as:
        EMPTY + _ + DESCRIPTION + _ + Analyzed + .csv
        
    Graph plot output of Writer object is stored in:
        OUT_DIR/DATE(YYYYMMDD)/TIME(HHMMSS)/MHPlots
    with naming system:
        COMBINED_+ X + _v_ + Y + _ + DESCRIPTION + .csv
    where X and Y are plotting parameters obtained from dictionary object containing
    pandas.DataFrame and dictionary object of property values of each analyzed voltage dataset.
    X and Y could both be either property parameters or series parameters of each analyzed voltage dataset.
    Its possible values are explained in the docstring of the `main` module.
    DESCRIPTION is value obtained from Reader object passed during intialization.
    
    Attributes
    ----------
    None.
    
    """
    
    def __init__(self, reader: 'Reader', dictionary: Dict[str, Tuple[pd.DataFrame, dict]]) -> 'Writer':
        """
        Parameters
        ----------
        reader : 'Reader'
            Reader object associated with analysis program.
        dictionary : Dict[str, Tuple[pd.DataFrame, dict]]
            Dictionary obecjt containing outputs of fundmagphase function of `analysis` module.

        Returns
        -------
        None.

        """
        
        self._dict = dictionary
        self._reader = reader
        
    def writeData(self) -> None:
        """Writes analyzed data into specified file directory.

        Returns
        -------
        None.

        """
        path = addDirectory(addDirectory(addDirectory(self._reader.get("OUT_DIR"), self._reader.get("DATE")), self._reader.get("TIME")), "MHAnalyzed")
        for key in self._dict:
            self._dict[key][0].to_csv(addDirectory(path, key + '_'+ self._reader.get("DESCRIPTION") + '_Analyzed' + ".csv"), index=False)
    
    def writePlots(self) -> None:
        """Writes plots of analyzed data into specified file directory.

        Returns
        -------
        None.

        """
        anyKey = [*self._dict][0]
        
        plotList = self._reader.get("PLOT").split("||")
        plotLabel = self._reader.get("PLOT_LABEL").split("||")
        for i in range(len(plotList)):
            item = plotList[i].strip()
            string = plotLabel[i].strip()
            x, y = item.split(":")
            xlabel, ylabel = string.split(":")
            xlabel = xlabel.strip()
            ylabel = ylabel.strip()
            x = x.strip()
            y = y.strip()
            self._plotFunc(self._reader.get("LEGEND"), x, y, xlabel, ylabel, anyKey, i)
            
        propertyPlotList = self._reader.get("PROPERTY_PLOT").split("||")
        propertyPlotLabel = self._reader.get("PROPERTY_PLOT_LABEL").split("||")
        for i in range(len(propertyPlotList)):
            item = propertyPlotList[i].strip()
            string = propertyPlotLabel[i].strip()
            x, y = item.split(":")
            xlabel, ylabel = string.split(":")
            xlabel = xlabel.strip()
            ylabel = ylabel.strip()
            x = x.strip()
            y = y.strip()
            valueListX = []
            valueListY = []
            for key in self._dict:
                try:
                    valueListX.append(self._dict.get(key)[1][x])
                except:
                    raise WriterError(x, "X-parameter not defined properly for PROPERTY_PLOT parameter in configuration file for plot kind: "+x+':'+y)
                try:
                    valueListY.append(self._dict.get(key)[1][y])
                except:
                    raise WriterError(x, "Y-parameter not defined properly for PROPERTY_PLOT parameter in configuration file for plot kind: "+x+':'+y)
            self._plotPropFunc(valueListX, valueListY, x, y, xlabel, ylabel)
            
    
    def _roundNum(self, value, sigfig: int) -> float:
        """Rounds any numeric value to specified significant figure

        Parameters
        ----------
        value
            Any numeric value.
        sigfig : int
            Number of significant figures value is rounded to.

        Returns
        -------
        float
            Round number of input value to specified significant figures.
        """
        if abs(value) == 0 or abs(value) == math.inf:
            return value
        return round(value, -int(math.floor(math.log10(abs(value)))) + sigfig - 1)
    
    def _plotPropFunc(self, xlist: List[float], ylist: List[float], x: str, y: str, xlabel: str, ylabel: str):
        """Plots graph of property parameters of each analyzed voltage run dataset

        Parameters
        ----------
        xlist : List[float]
            List of x-parameter datapoints.
        ylist : List[float]
            List of y-parameter datapoints.
        x : str
            Name of x-parameter.
        y : str
            Name of y-parameter.
        xlabel : str
            Label of x-parameter on graph.
        ylabel : str
            Label of y-parameter on graph

        Returns
        -------
        None.

        """
        path = addDirectory(addDirectory(addDirectory(self._reader.get("OUT_DIR"), self._reader.get("DATE")), self._reader.get("TIME")), "MHPlots")
        plt.figure()
        plt.plot(xlist, ylist, 'ro')
        plt.title(self._reader.get("DESCRIPTION") + " PLOT: " + x + "_v_" + y)
        plt.grid(True)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        pdfPath = addDirectory(path, "COMBINED" + '_' + x + "_v_" + y + '_' + self._reader.get("DESCRIPTION") + ".pdf")
        jpgPath = addDirectory(path, "COMBINED" + '_' + x + "_v_" + y + '_' + self._reader.get("DESCRIPTION") + ".jpg")
        plt.savefig(pdfPath, bbox_inches='tight')
        plt.savefig(jpgPath, bbox_inches='tight')
        
    def _plotFunc(self, legend: str, x: str, y: str, xlabel: str, ylabel: str, anyKey: str, index: int):
        """Plots graph of series parameters of each analyzed voltage run dataset.

        Parameters
        ----------
        legend : str
            Property parameter of each voltage dataset which serves as graph's legend
        x : str
            Name of x-parameter.
        y : str
            Name of y-parameter.
        xlabel : str
            Label of x-parameter on graph.
        ylabel : str
            Label of y-parameter on graph.
        anyKey : str
            Key value used to access analysis output of voltage run for error checking
        index : int
            Used as an index for differentiating the many plots created

        Raises
        ------
        WriterError
            Raised when:
                * Legend parameter LEGEND not defined properly.
                * X or Y parameters not defined properly for a specific plot kind.

        Returns
        -------
        None.

        """
        path = addDirectory(addDirectory(addDirectory(self._reader.get("OUT_DIR"), self._reader.get("DATE")), self._reader.get("TIME")), "MHPlots")
        
        plt.figure(index)
        ax = plt.axes()
        numOfColors = 0
        dataDict = {}
        
        if legend not in self._dict.get(anyKey)[1]:
            raise WriterError(legend, "Legend parameter LEGEND not defined properly in configuration file")
        elif x not in self._dict.get(anyKey)[0]:
            raise WriterError(x, "X-parameter not defined properly for PLOT parameter in configuration file for plot kind: "+x+':'+y)
        elif y not in self._dict.get(anyKey)[0]:
            raise WriterError(y, "Y-parameter not defined properly for PLOT parameter in configuration filefor plot kind: "+x+':'+y)
        
        for key in self._dict:
            if self._dict.get(key)[1]["H_MAX"] >= self._reader.get("H_MIN", Reader.asFloat) and self._dict.get(key)[1]["H_MAX"] <= self._reader.get("H_MAX", Reader.asFloat):
                numOfColors += 1
                if dataDict.get(self._roundNum(self._dict.get(key)[1][legend], 2)) is None:
                    dataDict[self._roundNum(self._dict.get(key)[1][legend], 2)] = []
                data = [self._dict.get(key)[0][x].to_numpy(), self._dict.get(key)[0][y].to_numpy()]
                dataDict.get(self._roundNum(self._dict.get(key)[1][legend], 2)).append(data)
        
        labelList = sorted(list(dataDict.keys()))
        ax.set_prop_cycle(color = [plt.cm.rainbow(i) for i in np.linspace(0, 1, numOfColors)])
        for key in labelList:
            dataList = dataDict.get(key)
            for data in dataList:
                plt.plot(data[0], data[1], label=key)
        
        plt.title(self._reader.get("DESCRIPTION") + " LEGEND: "+legend)
        plt.grid(True)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        handles, labels = ax.get_legend_handles_labels()
        ax = plt.figure(0).gca()
        for i, p in enumerate(ax.get_lines()):
            if p.get_label() in labels[:i]:
                idx = labels.index(p.get_label())
                p.set_c(ax.get_lines()[idx].get_c())
                p.set_label('_' + p.get_label())
        pdfPath = addDirectory(path, "COMBINED" + '_' + x + "_v_" + y + '_' + self._reader.get("DESCRIPTION") + ".pdf")
        jpgPath = addDirectory(path, "COMBINED" + '_' + x + "_v_" + y + '_' + self._reader.get("DESCRIPTION") + ".jpg")
        plt.legend(bbox_to_anchor=(0., 1.50, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.savefig(pdfPath, bbox_inches='tight')
        plt.savefig(jpgPath, bbox_inches='tight')
        
        
class Reader(object):
    """
    Reads the configuration text file sent as input from Main class in `main` module.
    
    Any line in file defined as:
        PROPERTY DELIMITER VALUE
    is accepted. E.g. DATA_ACTUAL = Opsens/path
    where this case DELIMITER is "=".
    
    Comment lines (any line begining with "#") and empty lines are ignored
    
    Any other line throws an error.
    
    Properties specified in configuration file are read into the program and necessary computation
    such as csv file reading and data manipulation for easy access of data for
    other components of the program is done.
    
    Input property data is written into file of directory:
        OUT_DIR/DATE(YYYYMMDD)/TIME(HHMMSS)
    with naming system: 
        DATE + TIME + DESCRIPTION + .txt
    where DATE and TIME are the date and time values at which analysis is done,
    DESCRIPTION and OUT_DIR are values obtained from the configuration file.
    
    Attributes
    ----------
    None.
    """
    
    asFloat = True
    """
    bool: Serves as a boolean parameter for code legibility. 
    """
    
    def __init__(self, fileDir: str, delimiter:str = "="):
        """
        Parameters
        ----------
        fileDir : str
            File directory of input configuration file
        delimiter : str, optional
            Delimiter of properties in configuration file. The default is "=".

        Raises
        ------
        ReaderError
            Raised when:
                * Any property not needed by program is defined.
                * Any non-empty line which is not a comment is defined without a delimiter.
                * When a directory defined as a property in the configuration file does not exist.
                * If the expected kind of dataset read from a csv file is wrong.

        Returns
        -------
        None.

        """
        self._data = {"OUT_DIR":"", "BASE_DIR":"", "M_G_FACTOR_FILE":"", "H_G_FACTOR_FILE":"", "DATA_EMPTY":"", "DATA_ACTUAL":"", 
                     "DESCRIPTION":"", "CUTOFF_FREQ":"", "KNOWN_FREQ":"", "M_OVER_H_REAL_SUB":"", "M_OVER_H_IMAG_SUB":"", 
                     "M_OVER_H_CALIB":"", "pM_pH_DIFF_PHASE_ADJ":"", "M_OVER_H0_SUB":"", "NUM_PERIOD":"", 
                     "BEGIN_TIME":"", "WITH_EMPTY":"", "TEMP_DIR":"", "H_MIN":"", "H_MAX":"", "LEGEND":"",
                     "PLOT":"", "PLOT_LABEL":"", "PROPERTY_PLOT":"", "PROPERTY_PLOT_LABEL": "", "TIME_DIR": ""}
        currentDate = datetime.datetime.now()
        date = str(currentDate.strftime("%Y%m%d"))
        time = str(currentDate.strftime('%H%M%S'))
        self._data["DATE"] = date
        self._data["TIME"] = time
        file = open(fileDir, 'r')
        for line in file:
            line = line.strip()
            try:
                key, value = line.split(delimiter)
                key = key.strip()
                value = value.strip()
                if key in self._data:
                    self._data[key] = value
                else:
                    raise ReaderError(key, "Property is not poorly defined or not necessary")
                    file.close()
            except ValueError:
                if len(line) == 0 or line.startswith('#'):
                    continue
                elif len(line) > 0:
                    raise ReaderError(line, "Line could not be read from file")
                else:
                   raise ReaderError(line, "Unknown unexpected error") 
                
                
        file.close()
        
        if not os.path.isdir(self.get("OUT_DIR")):
            raise ReaderError(self.get("OUT_DIR"), "OUT_DIR does not exist.")
        elif not os.path.isdir(self.get("BASE_DIR")):
            raise ReaderError(self.get("BASE_DIR"), "BASE_DIR does not exist.")
            
        infoFile = open(addDirectory(addDirectory(addDirectory(self.get("OUT_DIR"), self.get("DATE")), self.get("TIME")), self.get("DATE") + self.get("TIME") +self.get("DESCRIPTION") + ".txt"), 'w')
        infoFile.write('Inputs\n');
        infoFile.write('*************************\n');
        infoFile.write('\n');
        for key in self._data:
            infoFile.write(key + " = "+self._data.get(key)+'\n')
        infoFile.close()
        
        try:
            self._data["H_G_FACTOR_DATAFRAME"] = pd.read_csv(os.path.join(self.get("BASE_DIR"), self.get("H_G_FACTOR_FILE")))
        except:
            raise ReaderError(self.get("H_G_FACTOR_FILE"),
                              "H_G_FACTOR_FILE not defined properly or does not exist. File read from directory: " + os.path.join(self.get("BASE_DIR"), self.get("H_G_FACTOR_FILE")))

        try:
            self._data["M_G_FACTOR_DATAFRAME"] = pd.read_csv(os.path.join(self.get("BASE_DIR"), self.get("M_G_FACTOR_FILE")))
        except:
            raise ReaderError(self.get("M_G_FACTOR_FILE"),
                              "M_G_FACTOR_FILE not defined properly or does not exist. File read from directory: " + os.path.join(self.get("BASE_DIR"), self.get("M_G_FACTOR_FILE")))
            
        self._data["DICT_DATAFRAME_ACTUAL"] = {}
        self._data["DICT_DATAFRAME_TEMPERATURE"] = {"TEMP_V_RUN":{}, "TEMP_V_TIME":{}}
        self._data["WITH_EMPTY"] = getBool(self.get("WITH_EMPTY"))
        if (self._data["WITH_EMPTY"]):
            try:
               df = pd.read_csv(os.path.join(self.get("BASE_DIR"), self.get("DATA_EMPTY")))
            except:
                raise ReaderError(self.get("DATA_EMPTY"),
                                  "DATA_EMPTY file not defined properly or does not exist. File read from directory: " + os.path.join(self.get("BASE_DIR"), self.get("DATA_EMPTY")))
            
            if "Voltage(CH1)" in df.columns:
                self._data["DATAFRAME_EMPTY"] = df
            else:
                raise ReaderError(self.get("DATA_EMPTY"), "DATA_EMPTY file is not of expected voltage dataset kind")
       
        path = os.path.join(self.get("BASE_DIR"), self.get("DATA_ACTUAL"))
        
        readTempData = False
        
        if not os.path.exists(path):
            raise ReaderError(path, "Combined BASE_DIR + DATA_ACTUAL path does not exist.")
        
        for file in os.listdir(path):
            if ".csv" in file:
                readTempData = True
                df = pd.read_csv(os.path.join(path, file))
                if not "Voltage(CH1)" in df.columns:
                    raise ReaderError(file, "Voltage dataset of such filename in DATA_ACTUAL is not of expected voltage dataset kind")
                else:
                    self._data["DICT_DATAFRAME_ACTUAL"][file.rstrip(".csv")] = df
                
        if not readTempData:
            raise ReaderError(self.get("DATA_ACTUAL"), "DATA_ACTUAL path contains no expected voltage data files")
        
        
        tempPath = os.path.join(self.get("BASE_DIR"), self.get("TEMP_DIR"))
        
        if not os.path.exists(tempPath):
            raise ReaderError(tempPath, "Combined BASE_DIR + TEMP_DIR path does not exist.")
        
        for file in os.listdir(tempPath):
            if ".csv" in file:
                df = pd.read_csv(os.path.join(tempPath, file))
                regex = re.compile(r'\d{14}')
                
                try:
                    dateTime = regex.findall(file)[0]
                except:
                    raise ReaderError(file, "Temperature file of such filename in TEMP_DIR is not an expected csv dataset.")
                    
                if "Oscilloscope Run" in df.columns and "Temp" in df.columns:
                    self._data["DICT_DATAFRAME_TEMPERATURE"]["TEMP_V_RUN"][dateTime] = df
                elif "Time" in df.columns and "Temp" in df.columns:
                    self._data["DICT_DATAFRAME_TEMPERATURE"]["TEMP_V_TIME"][dateTime] = df
                else:
                    raise ReaderError(file, "Temperature file of such filename in TEMP_DIR is not an expected csv dataset.")
        
        # self._data["DICT_DATAFRAME_TIME"] = {}
        # timePath = os.path.join(self.get("BASE_DIR"), self.get("TIME_DIR"))
        
        # if not os.path.exists(timePath):
        #     raise ReaderError(timePath, "Combined BASE_DIR + TIME_DIR path does not exist.")
        
        # for file in os.listdir(timePath):
        #     if ".csv" in file:
        #         df = pd.read_csv(os.path.join(timePath, file))
        #         regex = re.compile(r'\d{14}')
                
        #         try:
        #             dateTime = regex.findall(file)[0]
        #         except:
        #             raise ReaderError(file, "Time file of such filename in TIME_DIR is not an expected csv dataset.")
                    
        #         if "Oscilloscope Run" in df.columns and "Time" in df.columns:
        #             self._data["DICT_DATAFRAME_TIME"][dateTime] = df
        #         else:
        #             raise ReaderError(file, "Time file of such filename in TIME_DIR is not an expected csv dataset.")
    
    def get(self, prop: str, kind: bool=False) -> Any:
        """
        Returns a property stored within the Reader object.

        Parameters
        ----------
        prop : str
            Property to be returned.
        kind : bool, optional
            Returns property as a string when True. The default is False.

        Raises
        ------
        ReaderError
            Raised when:
                * Property does not exist.
                * When output cannot be converted to string.

        Returns
        -------
        Any
            Property's value.

        """
        value = None
        try:
            value = self._data.get(prop)
        except KeyError:
            raise ReaderError(prop, "Property does not exist in configuration file")
            
        if isinstance(value, str) and len(value) == 0:
            raise ReaderError(prop, "Property does not exist in configuration file")
        if kind:
            try:
                return float(value)
            except ValueError:
                raise ReaderError(prop, "Property is not a float value")
        else:
            return value
    
    def getRunTemp(self, filename: str) -> float:
        """
        Returns the a voltage run dataset's temperature.

        Parameters
        ----------
        filename : str
            Filename of voltage run dataset.

        Raises
        ------
        ReaderError
            Raised when:
                * When Temp-V-Run Series data of voltage run is not added to TEMP_DIR.

        Returns
        -------
        float
            Temperature during voltage run during data collection.
        """
        regex = re.compile(r'\d{14}')
        dateTime = regex.findall(filename)[0]
        tempDf = None
        if dateTime in self._data["DICT_DATAFRAME_TEMPERATURE"]["TEMP_V_RUN"]:
            tempDf = self._data["DICT_DATAFRAME_TEMPERATURE"]["TEMP_V_RUN"].get(dateTime)
        else:
            raise ReaderError(dateTime, "Temp-V-Run Series data of this date-time value not added to TEMP_DIR.")
            
        regex = re.compile(r'\W\d+\W')
        value = int(regex.findall(filename)[0].strip('()'))
        try:
            return tempDf["Temp"][value - 1]
        except KeyError:
            raise ReaderError(dateTime, "Temp-V-Run Series data of this date-time value does not contain temperature value for Run "+str(value))
        
    def getTempSeriesDf(self, filename: str) -> pd.DataFrame:
        """
        Returns the Temp-V-Time Series data of a voltage run.

        Parameters
        ----------
        filename : str
            Filename of voltage run.

        Raises
        ------
        ReaderError
            Raised when:
                * When Temp-V-Time Series data of voltage run is not added to TEMP_DIR.

        Returns
        -------
        pd.DataFrame
            Temp-V-Time Series dataset of voltage run.

        """
        regex = re.compile(r'\d{14}')
        dateTime = regex.findall(filename)[0]
        if dateTime in self._data["DICT_DATAFRAME_TEMPERATURE"]["TEMP_V_TIME"]:
            return self._data["DICT_DATAFRAME_TEMPERATURE"]["TEMP_V_TIME"].get(dateTime)
        else:
            raise ReaderError(dateTime, "Temp-V-Run Series data of this date-time value not added to TEMP_DIR.")

        
def addDirectory(iPath: str, newPath: str) -> str:
    """
    Creates initial path and joins two directories into one. 
    
    Method Example
    --------------
    >>> addDirectory("C:\\Documents", "DocumentPath")
    
    "C:\\Documents\\DocumentPath"

    Parameters
    ----------
    iPath : str
        Initial path or directory. This is created if it does not exist
    newPath : str
        Path to be joined to initial path.

    Returns
    -------
    str
        Full string of joined file-paths.
    """
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    return iPath+'\\'+newPath
    
def getBool(boolStr: str) -> bool:
    """
    Returns True if string input is an affirmative word.

    Parameters
    ----------
    boolStr : str
        Input string.

    Returns
    -------
    bool
        Returns True if string input is an affirmative word.

    """
    return boolStr.lower() in ["true", "y", "yes"]