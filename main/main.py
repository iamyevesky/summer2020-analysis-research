# -*- coding: utf-8 -*-
"""Main Package

This script contains Main class which connects the helper classes, Reader and
Writer from the `tools` package and the fundmagphase function from `analysis`
package to run the analysis program.

This script requires that `tools` and `analysis` packages
are installed within the Python environment. 

This program is written with Python version 3.7.3 with Spyder IDE and
can be run on its own on the command line.

This file can be imported as a module and contains the following class:
    * Main - Central class which runs the analysis program.

"""


import PySimpleGUI as sg
import analysis
from tools import Writer, Reader, ReaderError

class Main(object):
    """
    A class that utilizes the helper objects and functions from `tools` and 
    `analysis` packages and provides the program logic to run the analysis
    program.
    
    This class accepts a string parameter during initialization
    which is the directory of the .txt configuration file from which 
    the program's needed parameters and configuration are read from.
    
    The configuration file's parameters for analysis are listed below:
        * OUT_DIR:
            Directory where analyzed files are written to.
        * BASE_DIR:
            Relative directory where other file directory parameters
            are read from.
        * DATA_EMPTY:
            File-path of the voltage run dataset considered as the empty field
            voltage reading. Ought to be a .csv file.
        * DATA_ACTUAL:
            File-path containing all voltage run dataset to be analyzed i.e
            non-empty field voltage reading.
        * DESCRIPTION:
            Description of analysis to be done.
            E.g: Analyze-GdSi-heated
        * M_G_FACTOR_FILE:
            File-path of M-Coil G-Factor dataset file. Ought to be a .csv file.
        * H_G_FACTOR_FILE:
            File-path of H-Coil G-Factor dataset file. Ought to be a .csv file.
        * CUTOFF_FREQ:
            Numeric parameter needed for analysis function.
        * KNOWN_FREQ:
            Numeric parameter needed for analysis function.
        * M_OVER_H_REAL_SUB:
            Numeric parameter needed for analysis function.
            Parameter is sent as a parameter to the analysis function
            fundmagphase along with each non-empty voltage reading dataset
            when WITH_EMPTY parameter is FALSE and sent as a parameter
            along with empty voltage reading dataset to the fundmagphase
            function when WITH_EMPTY is TRUE.
        * M_OVER_H_IMAG_SUB:
            Numeric parameter needed for analysis function.
            Parameter is sent as a parameter to the analysis function
            fundmagphase along with each non-empty voltage reading dataset
            when WITH_EMPTY parameter is FALSE and sent as a parameter
            along with empty voltage reading dataset to the fundmagphase
            function when WITH_EMPTY is TRUE.
        * M_OVER_H_CALIB:
            Numeric parameter needed for analysis function.
            Parameter is sent as a parameter to the analysis function
            fundmagphase along with each non-empty voltage reading dataset
            when WITH_EMPTY parameter is FALSE and sent as a parameter
            along with empty voltage reading dataset to the fundmagphase
            function when WITH_EMPTY is TRUE.
        * PM_PH_DIFF_PHASE_ADJ:
            Numeric parameter needed for analysis function.
            Parameter is sent as a parameter to the analysis function
            fundmagphase along with each non-empty voltage reading dataset
            when WITH_EMPTY parameter is FALSE and sent as a parameter
            along with empty voltage reading dataset to the fundmagphase
            function when WITH_EMPTY is TRUE.
        * M_OVER_H0_SUB:
            Numeric parameter needed for analysis function.
            Parameter is sent as a parameter to the analysis function
            fundmagphase along with each non-empty voltage reading dataset
            when WITH_EMPTY parameter is FALSE and sent as a parameter
            along with empty voltage reading dataset to the fundmagphase
            function when WITH_EMPTY is TRUE.
        * H_PHASE_REAL_SUB:
            Numeric parameter needed for analysis function.
            Parameter is sent as a parameter to the analysis function
            fundmagphase along with each non-empty voltage reading dataset
            when WITH_EMPTY parameter is FALSE and sent as a parameter
            along with empty voltage reading dataset to the fundmagphase
            function when WITH_EMPTY is TRUE.
        * H_PHASE_IMAG_SUB:
            Numeric parameter needed for analysis function.
            Parameter is sent as a parameter to the analysis function
            fundmagphase along with each non-empty voltage reading dataset
            when WITH_EMPTY parameter is FALSE and sent as a parameter
            along with empty voltage reading dataset to the fundmagphase
            function when WITH_EMPTY is TRUE.
        * NON_LINEAR_SUB:
            Boolean variable that states if a linear or non-lienar subtraction
            is performed on non-empty datasets
        * V_H_OFFSET:
            The degree of freedom from the maximum voltage maximum of the empty
            dataset to pass for a non-linear subtraction.
        * NUM_PERIOD:
            Numeric parameter needed for analysis function.
        * BEGIN_TIME:
            Numeric parameter needed for analysis function.
        * WITH_EMPTY:
            Parameter which states if an empty field voltage recording should
            be considered during analysis or not. Value is either TRUE or FALSE.
        * POLARITY:
            Parameter which controls the polarity of the voltage data read 
            into the program
        * TEMP_DIR:
            File-path containing all temperature datasets of non-empty field
            voltage datasets to be analyzed.
        * TIME_DIR:
            File-path containing all temperature datasets of non-empty field
            voltage datasets to be analyzed.
        * READ_TIME:
            Parameter which states if time data recording should
            be considered during analysis or not. Value is either TRUE or FALSE.
    
    The configuration file's parameters for plotting are listed below:
        * H_MIN:
            Minimum value of H_MAX property of analyzed voltage datasets to be
            plotted. Numeric value expected.
        * H_MAX:
            Maximum value of H_MAX property of analyzed voltage datasets to be
            plotted. Numeric value expected.
        * LEGEND:
            Plot's legend. Accepted values are:
                * "M_OVER_H_REAL"
                * "M_OVER_H_IMAG"
                * "M_OVER_H_G"
                * "pM_MINUS_pH_G"
                * "M_OVER_H0"
                * "OSC_TIME"
                * "TEMPERATURE"
                * "H_MAX"
                * "M_MAX"
                * "HC"
                * "DMDH"
                * "DMDH_OVER_M_MAX"
                * "INTEGRAL"
                * "RUN_NUM"
            These accepted values are considered property values of each
            analyzed voltage dataset.
        * PLOT:
            Series to plot on combined graph.
            Accepted PLOT values are of nature:
                X:Y || X:Y || .... || X:Y
            where X and Y are plotting parameters. Accepted X and Y values are:
                * "TIME"
                * V_H
                * V_M
                * "H_RECONSTRUCTED_REAL_LIST"
                * "M_RECONSTRUCTED_REAL_LIST"
                * "H_INT_RECONSTRUCTED_REAL_LIST"
                * "M_INT_RECONSTRUCTED_REAL_LIST"
                * "FREQ_LIST"
                * "M_SPECTRUM_REAL"
                * "M_SPECTRUM_IMAG"
                
        * PLOT_LABEL:
            Labels of series to be plotted on combined graph.
            Accepted PLOT_LABEL values are of nature:
                X-LABEL:Y-LABEL || X-LABEL:Y-LABEL || .... || X-LABEL:Y-LABEL
            X-LABEL and Y-LABEL could be any value.
            
            Note:
                Length of PLOT_LABEL and PLOT must be the same. An error
                would be thrown if it is not the case.
                E.g. "PLOT = V_M:V_H || TIME:V_H"
                     "PLOT_LABEL = A:B"
                Since label for "TIME:V_H" is not defined, an error would be
                thrown.
                
        * PROPERTY_PLOT:
            Property values of all analyzed voltage datasets to be plotted.
            This plot is not restricted by H_MAX and H_MIN parameters.
            Accepted PROPERTY_PLOT values are of nature:
                X:Y || X:Y || .... || X:Y
            where X and Y are plotting parameters. Accepted X and Y values are:
                * "M_OVER_H_REAL"
                * "M_OVER_H_IMAG"
                * "M_OVER_H_G"
                * "pM_MINUS_pH_G"
                * "M_OVER_H0"
                * "OSC_TIME"
                * "TEMPERATURE"
                * "H_MAX"
                * "M_MAX"
                * "HC"
                * "DMDH"
                * "DMDH_OVER_M_MAX"
                * "INTEGRAL"
                * "RUN_NUM"
                
        * PROPERTY_PLOT_LABEL:
            Labels of property values to be plotted on combined graph.
            Accepted PROPERTY_PLOT_LABEL values are of nature:
                X-LABEL:Y-LABEL || X-LABEL:Y-LABEL || .... || X-LABEL:Y-LABEL
            X-LABEL and Y-LABEL could be any value.
            
            Note:
                Length of PROPERTY_PLOT_LABEL and PROPERTY_PLOT must be the same.
                An error would be thrown if it is not the case.
    
    Every line in the configuration file should be of nature:
        PARAMETER DELIMITER VALUE
        E.g. :TEMP_DIR = Opsens\
    where default delimiter is "=".
    
    The configuration file can contain empty line spaces and comments.
    Comment lines begin with the symbol "#".
    E.g. A user can add these lines to the config file and it would be ignored:
        # This is the second run of the day
        
        # Error popped up with TEMP_DIR parameter
    
    Attributes
    ----------
    reader : Reader
        Reader object that extracts parameters from configuration file.
    dict : Dict[str, Tuple[pd.DataFrame, Dict[str, float]]]
        Dictionary object that stores the analysis output data for each
        analyzed voltage dataset output from fundmagphase function in `analysis`. 
    writer: Writer
        Writer object that writes output data and plot data.
    
    """
    
    def __init__(self, configDir: str):
        """

        Parameters
        ----------
        configDir : str
            File path of configuration text file.

        Returns
        -------
        None.

        """
        print("Starting Main program")
        print("Reading config file for program inputs")
        self.reader = Reader(configDir)
        self.reader.writeConfigFile()
        print("Data successfully read from .txt configuration file")
        self.dict = {}
        
    def run(self) -> None:
        """
        Runs the analysis program.

        Returns
        -------
        None.

        """
        if self.reader.get("WITH_EMPTY"):
            self._withEmpty()
        else:
            self._withoutEmpty()
        self.writer = Writer(self.reader, self.dict)
        print("Writing data into OUT_DIR")
        self.writer.writeData()
        print("Running plot code")
        self.writer.writePlots()
        print("Program sucessfully completed")
        
    def _withoutEmpty(self) -> None:
        """
        Runs analysis program without an empty field voltage dataset.

        Returns
        -------
        None.

        """
        print("Running analysis without empty data")
        for key in self.reader.get("DICT_DATAFRAME_ACTUAL"):
            if not key.startswith("voltageDataScopeRun"):
                return
            self.dict[key + "_ACTUAL_LINEAR"] = analysis.fundmagphase(
                self.reader.get("DICT_DATAFRAME_ACTUAL").get(key),
                self.reader.get("M_G_FACTOR_DATAFRAME"),
                self.reader.get("H_G_FACTOR_DATAFRAME"),
                self.reader.get("CUTOFF_FREQ", Reader.asFloat),
                self.reader.get("KNOWN_FREQ", Reader.asFloat),
                self.reader.get("M_OVER_H_REAL_SUB", Reader.asFloat),
                self.reader.get("M_OVER_H_IMAG_SUB", Reader.asFloat),
                self.reader.get("M_OVER_H_CALIB", Reader.asFloat),
                self.reader.get("PM_PH_DIFF_PHASE_ADJ", Reader.asFloat),
                self.reader.get("M_OVER_H0_SUB", Reader.asFloat),
                self.reader.get("H_PHASE_REAL_SUB", Reader.asFloat),
                self.reader.get("H_PHASE_IMAG_SUB", Reader.asFloat),
                self.reader.get("NUM_PERIOD", Reader.asFloat),
                self.reader.get("BEGIN_TIME", Reader.asFloat),
                self.reader.get("POLARITY", Reader.asFloat),
                runNum = self.reader.getRunNum(key),
                temperature=self.reader.getRunTemp(key),
                time=self.reader.getTime(key, "oscilloscope")
            )
        print("Analysis of actual data completed")
        
    def _withEmpty(self) -> None:
        """
        Runs analysis program with empty field voltage dataset.

        Returns
        -------
        None.

        """
        print("Running analysis with empty data")
        self.dict["EMPTY"] = analysis.fundmagphase(
            self.reader.get("DATAFRAME_EMPTY"),
            self.reader.get("M_G_FACTOR_DATAFRAME"),
            self.reader.get("H_G_FACTOR_DATAFRAME"),
            self.reader.get("CUTOFF_FREQ", Reader.asFloat),
            self.reader.get("KNOWN_FREQ", Reader.asFloat),
            self.reader.get("M_OVER_H_REAL_SUB", Reader.asFloat),
            self.reader.get("M_OVER_H_IMAG_SUB", Reader.asFloat),
            self.reader.get("M_OVER_H_CALIB", Reader.asFloat),
            self.reader.get("PM_PH_DIFF_PHASE_ADJ", Reader.asFloat),
            self.reader.get("M_OVER_H0_SUB", Reader.asFloat),
            self.reader.get("H_PHASE_REAL_SUB", Reader.asFloat),
            self.reader.get("H_PHASE_IMAG_SUB", Reader.asFloat),
            self.reader.get("NUM_PERIOD", Reader.asFloat),
            self.reader.get("BEGIN_TIME", Reader.asFloat),
            self.reader.get("POLARITY", Reader.asFloat)
        )
        print("Analysis of empty data completed")
        print("Running analysis of actual data")
        linearSignifier = "LINEAR"
        for key in self.reader.get("DICT_DATAFRAME_ACTUAL"):
            if not key.startswith("voltageDataScopeRun"):
                return
            nonLinearSub = self.reader.get("NON_LINEAR_SUB")
            vHMax = 0
            if nonLinearSub:
                vHMax = self.reader.get("DICT_DATAFRAME_ACTUAL").get(key).iloc[:,1].max()
                if vHMax <= self.dict.get("EMPTY")[1]["V_H_MAX"] + self.reader.get("V_H_OFFSET", Reader.asFloat) and vHMax >= self.dict.get("EMPTY")[1]["V_H_MAX"] - self.reader.get("V_H_OFFSET", Reader.asFloat):
                    linearSignifier = "NON_LINEAR"
                else:
                    nonLinearSub = False
                
            
            self.dict[key + "_ACTUAL_" + linearSignifier] = analysis.fundmagphase(
                self.reader.get("DICT_DATAFRAME_ACTUAL").get(key),
                self.reader.get("M_G_FACTOR_DATAFRAME"),
                self.reader.get("H_G_FACTOR_DATAFRAME"),
                self.reader.get("CUTOFF_FREQ", Reader.asFloat),
                self.reader.get("KNOWN_FREQ", Reader.asFloat),
                self.dict.get("EMPTY")[1]["M_OVER_H_REAL"],
                self.dict.get("EMPTY")[1]["M_OVER_H_IMAG"],
                self.reader.get("M_OVER_H_CALIB", Reader.asFloat),
                self.reader.get("PM_PH_DIFF_PHASE_ADJ", Reader.asFloat),
                self.reader.get("M_OVER_H0_SUB", Reader.asFloat),
                self.dict.get("EMPTY")[1]["H_PHASE_REAL"],
                self.dict.get("EMPTY")[1]["H_PHASE_IMAG"],
                self.reader.get("NUM_PERIOD", Reader.asFloat),
                self.reader.get("BEGIN_TIME", Reader.asFloat),
                self.reader.get("POLARITY", Reader.asFloat),
                temperature=self.reader.getRunTemp(key),
                runNum = self.reader.getRunNum(key),
                time=self.reader.getTime(key, "oscilloscope"),
                isNonLinearSub = nonLinearSub,
                Mspecrealforsub = self.dict.get("EMPTY")[0]["M_SPECTRUM_REAL"],
                Mspecimagforsub = self.dict.get("EMPTY")[0]["M_SPECTRUM_IMAG"]
            )
        
        print("Analysis of actual data completed")    
        
if __name__ == "__main__":
    event, values = sg.Window('Configuration File Selection',
                  [[sg.Text('Select Cogfiguration File: ', size=(25, 1)), 
                    sg.InputText(key='-FILE-'), 
                    sg.FileBrowse()],
                  [sg.B('Run Program')]]).read(close=True)
    
    path = values['-FILE-']
    if path is None:
        raise ReaderError("Configuration File", "No file was selected in pop-up windows")
    elif len(path) == 0:
        raise ReaderError("Configuration File", "No file was selected in pop-up windows")
    else:
        Main(path).run()
