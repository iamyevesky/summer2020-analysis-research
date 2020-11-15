# -*- coding: utf-8 -*-
"""Analysis Package

This script contains functions which provide means to perform analysis on voltage
data.

This script requires that `pandas`, `numpy`, `scipy`and 
`mathplotlib` are installed within the Python environment. 

This program is written with Python version 3.7.3 with Spyder IDE.

This file is imported as a module and contains the following functions:
    * fundmagphase - Main function which analyzes voltage data 
    
"""

import os
import numpy as np
import math
import scipy
from scipy.interpolate import interp1d
import pandas as pd
from typing import Dict, List, Tuple, Callable

pi = math.pi

def fundmagphase(ambrelldata: pd.DataFrame, Mgdata: pd.DataFrame, Hgdata: pd.DataFrame, high_cutoff_freq: int,
                 known_freq: int, MoverHrealforsub: float, MoverHimagforsub: float, MoverHforcalib: float,
                 pMminuspHforphaseadj: float, MoverH0forsubtraction: float, Mspecrealforsub: List[float],
                 Mspecimagforsub: List[float], Hphaserealforsub: float, Hphaseimagforsub: float, 
                 est_num_periods: int, begintime: int, temperature: float=np.nan, isNonLinearSub: bool = False) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    

    Parameters
    ----------
    ambrelldata : pd.DataFrame
        Raw voltage run time-series dataset to be analyzed 
    Mgdata : pd.DataFrame
        M-Coil G-Factor dataset used in analysis
    Hgdata : pd.DataFrame
        H-Coil G-Factor dataset used in analysis
    high_cutoff_freq : int
        High cutoff frequency specified in configuration data
    known_freq : int
        Known frequency specified in configuration data
    MoverHrealforsub : float
        Empty field reading value subtituted from analysed datasets of 
        non-empty field voltage readings. 
    MoverHimagforsub : float
        Empty field reading value subtituted from analysed datasets of 
        non-empty field voltage readings.
    MoverHforcalib : float
        Empty field reading value subtituted from analysed datasets of 
        non-empty field voltage readings.
        Currently not implemented at the behest of Dr. Boekelheide.
    pMminuspHforphaseadj : float
        Empty field reading value subtituted from analysed datasets of 
        non-empty field voltage readings.
        Currently not implemented at the behest of Dr. Boekelheide.
    MoverH0forsubtraction : float
        Empty field reading value subtituted from analysed datasets of 
        non-empty field voltage readings.
        Currently not implemented at the behest of Dr. Boekelheide.
    Mspecrealforsub: List[float]
    
    Mspecimagforsub: List[float]
    
    Hphaserealforsub: float
    
    Hphaseimagforsub: float
    
    est_num_periods : int
        
    begintime : int
        
    temperature : float, optional
        Temperature recorded during collection of voltage run time-series dataset. The default is np.nan.
    isNonLinearSub: bool, optional
        Instructs if fundmagphase should perform a linear or non-linear subtraction of background noise
    Returns
    -------
    logger : pd.DataFrame
        Analyzed voltage run dataframe.
    hashMap : dict
        Dictionary of analyzed dataset properties.

    """
    

    """
    Calib factors from Jackson 2018-2019
    # in units of kA/m per V-s
    #M_CALIB_FACTOR = -9.551e6
    #H_CALIB_FACTOR = -1.88e7
    """
    
    """
    Calib factors from Zoe August 2019
    in units of kA/m per V-s
    """
    M_CALIB_FACTOR = -9.551e6
    H_CALIB_FACTOR = -2.26e7
    POLARITY = -1
    pi = math.pi
    times = ambrelldata.iloc[:,0].values.tolist()
    H = ambrelldata.iloc[:,1].values.tolist()
    M = (np.array(ambrelldata.iloc[:,2].values.tolist())*POLARITY).tolist()
    
    total_points = len(M)
    timestep = times[1]-times[0]
    startdatpoint = int(begintime/timestep)+1
    bigHspectrum = np.fft.fft(H)
    bigfreq = np.fft.fftfreq(total_points, d=timestep) 
    fundindex = np.argmax(np.abs(bigHspectrum[1:(int(total_points/2))]))+1
    guess_freq = bigfreq[fundindex]
    
    """
    Best results when exact frequency is used. The most accurate frequency
    can be found using the opt_freq routine. However, it can take some time.
    If the frequency is known from previous runs or because it is manufactured
    test data, it should be entered in as one of the parameters of
    fundmagphase. If the frequency is unknown and the user wants to run
    opt_freq, input 'known_freq' as 0.
    """
    
    if known_freq == 0:
        frequency = opt_freq(H, total_points, timestep, guess_freq)
    else:
        frequency = known_freq
        
    period = 1/int(frequency)
    tsteps_in_period = period//timestep
    lower = startdatpoint
    adj_total_points = int(est_num_periods * tsteps_in_period)
    new_upper = lower + adj_total_points
    times = times[lower:new_upper]
    M = M[lower:new_upper]
    H = H[lower:new_upper]

    """
    FFT to create spectrum of truncated data
    """ 
    Mspectrum = np.fft.fft(M)
    Hspectrum = np.fft.fft(H)
    freq = np.fft.fftfreq(adj_total_points, d=timestep)        

    """
    Determine the frequency (again... should be redundant)
    """
    halfpoints = int(adj_total_points/2)
    fundindex = np.argmax(np.abs(Hspectrum[1:halfpoints]))+1
    frequency = abs(freq[fundindex])
    period = 1/frequency
    tsteps_in_period = int(period/timestep)
    est_num_periods = fundindex

    """
    Determine some basic info about the fundamental frequency (phase and mag)
    """
    pH = np.angle(Hspectrum[est_num_periods])
    pM = np.angle(Mspectrum[est_num_periods])
    pMminuspH = pi_mod(pM - pH)
    Hmag = np.abs(Hspectrum[est_num_periods])
    Mmag = np.abs(Mspectrum[est_num_periods])
    MoverH = Mmag/Hmag
    MoverHreal = MoverH*np.cos(pMminuspH)
    MoverHimag = MoverH*np.sin(pMminuspH)    
    Hphasereal = np.cos(pH)
    Hphaseimag = np.sin(pH)
    MoverH0 = np.real(Mspectrum[0]/Hspectrum[0])
    if (pMminuspH > pi/2) or (pMminuspH < -pi/2):
        pMminuspH -= pi
        MoverH = -MoverH

    """
    Substraction of empty spectrum
    """
    for i in [est_num_periods, (len(Mspectrum)-est_num_periods)]:
        phase_sign = np.sign(freq[i])
        transfer_func_Hphase = complex(Hphasereal, -phase_sign*Hphaseimag)
        Mspectrum[i] = Mspectrum[i]*transfer_func_Hphase
        Mspectrum[i] -= Hmag*complex(MoverHrealforsub, phase_sign*MoverHimagforsub)
        Mspectrum[i] = Mspectrum[i]/transfer_func_Hphase

    """
    G-Factor correction
    """
    g_interp_real, g_interp_imag = calculate_g(Mgdata, high_cutoff_freq)
    Hg_interp_real, Hg_interp_imag = calculate_g(Hgdata, high_cutoff_freq)
    Mspectrum_gcorr = [0.0+0.0j]*len(Mspectrum)
    Hspectrum_gcorr = [0.0+0.0j]*len(Hspectrum) #changed Mspectrum into Hspectrum
    
    for i in range(len(Mspectrum)):
        if (i>0) and (np.abs(freq[i]) < high_cutoff_freq) and odd_harmonic_M(len(freq), i, est_num_periods) == 1:
            Mspectrum_gcorr[i] = Mspectrum[i]
            phase_sign_2 = np.sign(freq[i])
            """"
            Subtraction of background spectrum. If nonLinearSub is False,
            that means to only subtract the fundamental.
            """
            if isNonLinearSub:
                transfer_func_Hphase = complex(Hphasereal, -phase_sign*Hphaseimag)
                transfer_func_Hphase_sub = complex(Hphaserealforsub, -phase_sign*Hphaseimagforsub)
                Mspectrum_gcorr[i] = Mspectrum_gcorr[i]*transfer_func_Hphase
                term_to_subtract =  complex(Mspecrealforsub[i], Mspecimagforsub[i])*transfer_func_Hphase_sub
                Mspectrum_gcorr[i] -= term_to_subtract
                Mspectrum_gcorr[i] = Mspectrum_gcorr[i]/transfer_func_Hphase
            
            transfer_func_g = complex(g_interp_real(abs(freq[i])), phase_sign_2*g_interp_imag(abs(freq[i])))
            Mspectrum_gcorr[i] = Mspectrum_gcorr[i]*transfer_func_g
            
        if i == est_num_periods or i == (len(Mspectrum) - est_num_periods):
            Hspectrum_gcorr[i] = Hspectrum[i]            
            phase_sign_2 = np.sign(freq[i])
            transfer_func_Hg = complex(Hg_interp_real(abs(freq[i])), phase_sign_2*Hg_interp_imag(abs(freq[i])))
            Hspectrum_gcorr[i] = Hspectrum_gcorr[i]*transfer_func_Hg
 
    """
    Reconstruction of signal
    """
    Mreconstructed = np.fft.ifft(Mspectrum_gcorr)
    Hreconstructed = np.fft.ifft(Hspectrum_gcorr)
    pHg = np.angle(Hspectrum_gcorr[est_num_periods])
    pMg = np.angle(Mspectrum_gcorr[est_num_periods])
    pMminuspHg = pi_mod(pMg - pHg)
    Hmagg = np.abs(Hspectrum_gcorr[est_num_periods])
    Mmagg = np.abs(Mspectrum_gcorr[est_num_periods])
    MoverHg = Mmagg/Hmagg
    if (pMminuspHg > pi/2) or (pMminuspHg < -pi/2):
        pMminuspHg -= pi
        MoverHg = -MoverHg
    
    """
    Integration of signal
    """    
    Mspectrum_int = [0.0+0.0j]*len(Mspectrum_gcorr)
    Hspectrum_int = [0.0+0.0j]*len(Mspectrum_gcorr)
    
    for i in range(len(Mspectrum_gcorr)):
        if i > 0:
            Mspectrum_int[i] = (-1.0j)*Mspectrum_gcorr[i]/(2*pi*(freq[i]))
            Hspectrum_int[i] = (-1.0j)*Hspectrum_gcorr[i]/(2*pi*(freq[i]))

    """
    Reconstruction of integrated signal
    """
    Mintreconstructed = np.fft.ifft(Mspectrum_int)
    Hintreconstructed = np.fft.ifft(Hspectrum_int)

    """
    Try integrating another way to check
    """
    Mintreconstructed2 = [0.0]*len(Mreconstructed)
    Hintreconstructed2 = [0.0]*len(Mreconstructed)
    for i in range(len(Mreconstructed)-1):
        Mintreconstructed2[i+1] = Mintreconstructed2[i]+Mreconstructed[i]*timestep
        Hintreconstructed2[i+1] = Hintreconstructed2[i]+Hreconstructed[i]*timestep
    Mintreconstructed2[0] = Mintreconstructed2[1]-(Mintreconstructed2[2]-Mintreconstructed2[1])
    Hintreconstructed2[0] = Hintreconstructed2[1]-(Hintreconstructed2[2]-Hintreconstructed2[1])
    cM = np.mean(Mintreconstructed2)
    cH = np.mean(Hintreconstructed2)
    for i in range(len(Mreconstructed)):
        Mintreconstructed2[i] -= cM
        Hintreconstructed2[i] -= cH

    """
    M and H calibration
    """
    for i in range(len(Mintreconstructed)):
        Mintreconstructed[i] = M_CALIB_FACTOR*Mintreconstructed[i]
        Mintreconstructed2[i] = M_CALIB_FACTOR*Mintreconstructed2[i]
        Hintreconstructed[i] = H_CALIB_FACTOR*Hintreconstructed[i]
        Hintreconstructed2[i] = H_CALIB_FACTOR*Hintreconstructed2[i]
    
    
    Mreconstructedreal = np.real(Mreconstructed)
    Hreconstructedreal = np.real(Hreconstructed)
    Mreconstructedreallist = Mreconstructedreal.tolist()
    Hreconstructedreallist = Hreconstructedreal.tolist()
    Mintreconstructedreal = np.real(Mintreconstructed)
    Hintreconstructedreal = np.real(Hintreconstructed)
    Mintreconstructedreallist = Mintreconstructedreal.tolist()
    Hintreconstructedreallist = Hintreconstructedreal.tolist()
    Mspectrumreal = (np.real(Mspectrum)).tolist()
    Mspectrumimag = (np.imag(Mspectrum)).tolist()
    freqlist = freq.tolist()
    
    """ THIS IS A PLACEHOLDER - SHOULD GET osc_time FROM osctimefile.txt """
    osc_time = 0.0
    
    Hmax = np.amax(Hintreconstructedreallist)
    Mmax = np.amax(Mintreconstructedreallist)
    
    integral = 0.0
    
    for j in range(len(Hintreconstructedreallist)-1):
        if Mintreconstructedreallist[j+1] > 0 and Mintreconstructedreallist[j] < 0:
            Hc1 = Hintreconstructedreallist[j] - (Hintreconstructedreallist[j+1] - Hintreconstructedreallist[j])*Mintreconstructedreallist[j]/(Mintreconstructedreallist[j+1]-Mintreconstructedreallist[j])
            dMdH1 = (Mintreconstructedreallist[j+1]-Mintreconstructedreallist[j-1])/(Hintreconstructedreallist[j+1]-Hintreconstructedreallist[j-1])
        if Mintreconstructedreallist[j+1] < 0 and Mintreconstructedreallist[j] > 0:
            Hc2 = Hintreconstructedreallist[j] - (Hintreconstructedreallist[j+1] - Hintreconstructedreallist[j])*Mintreconstructedreallist[j]/(Mintreconstructedreallist[j+1]-Mintreconstructedreallist[j])
            dMdH2 = (Mintreconstructedreallist[j+1]-Mintreconstructedreallist[j-1])/(Hintreconstructedreallist[j+1]-Hintreconstructedreallist[j-1])
        integral += ((Mintreconstructedreallist[j+1]+Mintreconstructedreallist[j])/2)*(Hintreconstructedreallist[j]-Hintreconstructedreallist[j+1])
    integral = integral/est_num_periods
    Hc = (Hc1-Hc2)/2
    dMdH = (dMdH1+dMdH2)/2
    dMdH_over_Mmax = dMdH/Mmax
    
    # Note to code maintainer:
    #     Remember to update docstring comment of main module (main.py) when a new
    #     property parameter is added to labelSeries and valueSeries
        
    labelSeries = ["M_OVER_H_REAL", "M_OVER_H_IMAG", "M_OVER_H_G", "pM_MINUS_pH_G", "M_OVER_H0", "H_PHASE_REAL", "H_PHASE_IMAG", "OSC_TIME", "TEMPERATURE", "H_MAX", "M_MAX", "HC", "DMDH", "DMDH_OVER_M_MAX", "INTEGRAL"]
    valueSeries = [MoverHreal, MoverHimag, MoverHg, pMminuspHg, MoverH0, Hphasereal, Hphaseimag, osc_time, temperature, Hmax, Mmax, Hc, dMdH, dMdH_over_Mmax, integral]
    hashMap = {}
    
    for i in range(len(labelSeries)):
        hashMap[labelSeries[i]] = valueSeries[i]
        
    for i in range(len(labelSeries), len(freqlist)): #pandas.DataFrame does not accept lists of different lengths.
        labelSeries.append("")
        valueSeries.append(0.00)
    
    
    logger = pd.DataFrame()
    logger["TIME"] = times
    logger["V_H"] = H
    logger["V_M"] = M
    logger["H_RECONSTRUCTED_REAL_LIST"] = Hreconstructedreallist
    logger["M_RECONSTRUCTED_REAL_LIST"] = Mreconstructedreallist
    logger["H_INT_RECONSTRUCTED_REAL_LIST"] = Hintreconstructedreallist
    logger["M_INT_RECONSTRUCTED_REAL_LIST"] = Mintreconstructedreallist
    logger["FREQ_LIST"] = freqlist
    logger["M_SPECTRUM_REAL"] = Mspectrumreal
    logger["M_SPECTRUM_IMAG"]  = Mspectrumimag
    logger["STAT_LIST_LABEL"] = labelSeries
    logger["STAT_LIST_VALUE"] = valueSeries
    return logger, hashMap


def opt_freq(H: List[float], total_points: int, timestep: float, guess_freq: int) -> int:
    """
    Frequency from fft of whole dataset is not exactly correct.
    Best results when fft is performed on a dataset with an integer number of periods
    This routine tests the fft results of truncated versions of the dataset to find the optimal frequency
    This procedure can take some time. The fft algorithm takes a variable amount of time depending on the
    number of data points in the set. It is fastest (~1 second) when the number of data points is divisible by 2
    and other small divisors. It is slowest when the number of data points is prime (~1 hour).
    Thus I have implemented an algorithm to zero in on the optimal frequency by first
    testing those truncated data sets with numbers of points divisble by powers of 2,
    and then zeroing in from there.
    """
    best_fom = 1
    frequency = 0
    guess_period = 1/guess_freq
    guess_tsteps_in_period = guess_period//timestep
    powersof2 = [1024, 256, 64, 16, 4]
    last_i =  total_points - guess_tsteps_in_period//2
    jrange =  powersof2[0] * math.floor(guess_tsteps_in_period//(2 * powersof2[0]))
    for j in range(len(powersof2)):
        freqsforfom = []
        fom = []
        ilist = []
        fundindexlist = []
        if j > 0:
            jrange = powersof2[j-1]
        center_i =  int(powersof2[j]*math.floor(last_i/powersof2[j]))
        lower_lim = max(center_i - jrange, int(3*guess_tsteps_in_period/4))
        upper_lim = min(center_i + jrange, total_points)
        for i in range(lower_lim, upper_lim, powersof2[j]):
            testH = H[0:(i)]
            testHspectrum = np.fft.fft(testH)
            freqspectrum = np.fft.fftfreq((i), d=timestep)
            fundindex = np.argmax(np.abs(testHspectrum[1:(int(total_points/2))]))+1
            guess_freq = abs(freqspectrum[fundindex])
            offpeak = np.abs(testHspectrum[fundindex+1])
            onpeak = np.abs(testHspectrum[fundindex])
            fomi = offpeak/onpeak
            fom.append(fomi)
            freqsforfom.append(guess_freq)
            ilist.append(i)
            fundindexlist.append(fundindex)
            if fomi < best_fom:
                best_fom = fomi
                frequency = guess_freq
                best_i = i
                last_i = best_i
    return frequency
   
    
def calculate_g(gdata: pd.DataFrame, high_cutoff_freq: int) -> Tuple[Callable[[List[float]], List[float]]]:
    avgfreqlist = gdata.iloc[:,0].values.tolist()
    greallist = gdata.iloc[:,3].values.tolist()
    gimaglist = gdata.iloc[:,4].values.tolist()
    high_cutoff_freq = np.amin([high_cutoff_freq, avgfreqlist[-1]])
    g_interp_real = interp1d(avgfreqlist, greallist, kind='linear', assume_sorted = False)
    g_interp_imag = interp1d(avgfreqlist, gimaglist, kind='linear', assume_sorted = False)
    return(g_interp_real, g_interp_imag)

def pi_mod(pavg: float) -> float:
    while (pavg < 0 or pavg > 2*pi):
        if pavg < 0:
            pavg += 2*pi
        if pavg > 2*pi:
            pavg -= 2*pi
    return pavg

def odd_harmonic_M(length: int, i: int, est_num_periods: int) -> Tuple[int]:
    oddnums = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39]
    if (i % est_num_periods == 0) and ((round(i/est_num_periods) in oddnums and i < length/2) or (round((length - i)/est_num_periods) in oddnums and i > length/2)):
            return(1)
    else:
        return(0)

def addDirectory(iPath: str, newPath: str) -> str:
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    return iPath+'\\'+newPath


"""Code below do not serve any known function in main function: fundmagphase()"""
def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c

def fit_sin(tt, yy):
    #Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset"
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(np.abs(Fyy[1:]))+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = 1.41*np.std(yy)
    guess_w = 2.*np.pi*guess_freq
    guess_offset = np.mean(yy)
    ind1 = int(len(yy)/4)
    ind2 = int(len(yy)/8)
    arccosarg = (yy[ind1] - yy[0])/((tt[ind1] - tt[0])*guess_amp*guess_w)
    if arccosarg > 1:
        arccosarg = 1
    if arccosarg < -1:
        arccosarg = -1
    guess_phase = np.arccos(arccosarg)-pi_mod(guess_w*tt[ind2])
    guess = np.array([guess_amp, guess_w, guess_phase, guess_offset])
    try:
        popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess, maxfev = 200000)
    except:
        popt = [guess_amp, guess_w, guess_phase, guess_offset]
    A, w, p, c = popt
    return [A, w, p, c]

def pi_mod_array(phasearray):
    for k in range(len(phasearray)):
        phasearray[k] = pi_mod(phasearray[k])
    topcount = 0
    midcount = 0
    bottomcount = 0
    for k in range(len(phasearray)):
        if phasearray[k] < pi/2:
            bottomcount += 1
        elif phasearray[k] > 3*pi/2:
            topcount += 1
        else:
            midcount += 1
    if ((bottomcount + topcount) > midcount):
        mult = np.sign(bottomcount - topcount)
        if mult ==0: mult = 1
        cutoff = pi
        for k in range(len(phasearray)):
            if mult*phasearray[k] > mult*float(cutoff):
                phasearray[k] = phasearray[k] - mult*2*pi
    return phasearray

def writefunc(k):
    if k % 10 == 0:
        return 1
    else:
        return 0

def fftdata(selectarray):
    arraylist = selectarray
    Mspectrumselect = np.fft.fft(arraylist)
    realMspectrumselect = np.real(Mspectrumselect)
    imagMspectrumselect = np.imag(Mspectrumselect)
    
    realMspectrumlist = realMspectrumselect.tolist()
    imagMspectrumlist = imagMspectrumselect.tolist()
    return([realMspectrumlist, imagMspectrumlist])